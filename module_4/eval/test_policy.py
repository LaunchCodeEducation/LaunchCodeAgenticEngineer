"""Verify that the governance policy document and its enforcement artifacts agree.

Run from the repository root: pytest eval/test_policy.py -v
"""

import json
import re
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
POLICY = REPO / "docs" / "governance-policy.md"
STORAGE_ALLOW = REPO / "mcp-servers" / "storage" / "allow-list.json"
RETRIEVAL_ALLOW = REPO / "mcp-servers" / "retrieval" / "allow-list.json"
RUN_AGENT = REPO / "scripts" / "run-agent.sh"
SKILLS_DIR = REPO / ".skills"


def _subsection(chunk: str, title: str) -> str:
    match = re.search(
        r"###\s+" + re.escape(title) + r"\s*\n(.*?)(?=\n###\s|\Z)",
        chunk,
        re.S,
    )
    return match.group(1) if match else ""


def parse_policy() -> dict:
    text = POLICY.read_text(encoding="utf-8")
    roles = {}
    for chunk in re.split(r"^##\s+Role:\s*", text, flags=re.M)[1:]:
        name = chunk.splitlines()[0].strip()
        entry = {
            "storage_ops": set(),
            "retrieve_granted": False,
            "retrieve_ceiling": None,
            "skills_permitted": set(),
            "workspace": None,
            "memory": None,
        }

        mcp = _subsection(chunk, "MCP server and operation access")
        for op, server, granted in re.findall(
            r"^\|\s*([a-z_]+)\s*\|\s*([a-z]+)\s*\|\s*(YES|NO)\s*\|",
            mcp,
            re.M,
        ):
            if granted == "YES" and server == "storage":
                entry["storage_ops"].add(op)
            if granted == "YES" and server == "retrieval" and op == "retrieve":
                entry["retrieve_granted"] = True

        skills = _subsection(chunk, "Skill activation scope")
        for skill, granted in re.findall(
            r"^\|\s*([a-z0-9-]+)\s*\|\s*(YES|NO)\s*\|",
            skills,
            re.M,
        ):
            if granted == "YES":
                entry["skills_permitted"].add(skill)

        ceiling = re.search(r"\*\*Maximum level:\*\*\s*([a-z]+)", chunk)
        if ceiling:
            entry["retrieve_ceiling"] = ceiling.group(1)

        container = re.search(
            r"\*\*Container permissions:\*\*\s*workspace\s+(read-only|read-write),\s*memory\s+(mounted|omitted)",
            chunk,
        )
        if container:
            entry["workspace"] = {"read-only": "ro", "read-write": "rw"}[container.group(1)]
            entry["memory"] = {"mounted": True, "omitted": False}[container.group(2)]

        roles[name] = entry
    return roles


def parse_run_agent() -> dict:
    text = RUN_AGENT.read_text(encoding="utf-8")
    modes = {}
    for pattern, body in re.findall(r"^\s*([a-z|_-]+)\)\s*\n(.*?);;", text, re.S | re.M):
        mode = re.search(r'WORKSPACE_MODE="(\w+)"', body)
        memory = re.search(r"MOUNT_MEMORY=(\d+)", body)
        if not mode or not memory:
            continue
        for role in pattern.split("|"):
            modes[role.strip()] = {
                "workspace": mode.group(1),
                "memory": memory.group(1) == "1",
            }
    return modes


def parse_skill(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    permitted = re.search(r"\*\*Permitted roles:\*\*\s*(.+)", text)
    if not permitted:
        return set()
    return {role.strip() for role in permitted.group(1).split(",") if role.strip() and role.strip() != "none"}


POLICY_ROLES = parse_policy()
STORAGE_ALLOW_DATA = json.loads(STORAGE_ALLOW.read_text(encoding="utf-8"))
RETRIEVAL_ALLOW_DATA = json.loads(RETRIEVAL_ALLOW.read_text(encoding="utf-8"))["retrieve"]
RUN_AGENT_MODES = parse_run_agent()
SKILL_FILES = sorted(SKILLS_DIR.glob("*.md"))
ROLE_NAMES = sorted(POLICY_ROLES.keys())


def test_policy_document_parsed():
    assert ROLE_NAMES, "No role entries were parsed from governance-policy.md."


@pytest.mark.parametrize("role", ROLE_NAMES)
def test_storage_allowlist_matches_policy(role):
    policy_ops = POLICY_ROLES[role]["storage_ops"]
    allow_ops = {op for op, roles in STORAGE_ALLOW_DATA.items() if role in roles}
    assert allow_ops == policy_ops, (
        f"{role}: storage allow-list grants {sorted(allow_ops)}, "
        f"policy grants {sorted(policy_ops)}"
    )


@pytest.mark.parametrize("role", ROLE_NAMES)
def test_retrieval_grant_matches_policy(role):
    rule = RETRIEVAL_ALLOW_DATA.get(role)
    granted = bool(rule and rule.get("granted"))
    assert granted == POLICY_ROLES[role]["retrieve_granted"], f"{role}: retrieve grant disagrees with policy"
    if granted:
        assert rule["classification_ceiling"] == POLICY_ROLES[role]["retrieve_ceiling"], (
            f"{role}: classification ceiling disagrees with policy"
        )


@pytest.mark.parametrize("skill_path", SKILL_FILES, ids=lambda p: p.stem)
def test_skill_scope_matches_policy(skill_path):
    skill = skill_path.stem
    permitted_in_file = parse_skill(skill_path)
    permitted_in_policy = {
        role for role, data in POLICY_ROLES.items() if skill in data["skills_permitted"]
    }
    assert permitted_in_file == permitted_in_policy, (
        f"{skill}: skill file permits {sorted(permitted_in_file)}, "
        f"policy permits {sorted(permitted_in_policy)}"
    )


@pytest.mark.parametrize("role", ROLE_NAMES)
def test_container_permissions_match_policy(role):
    policy_mode = {
        "workspace": POLICY_ROLES[role]["workspace"],
        "memory": POLICY_ROLES[role]["memory"],
    }
    assert policy_mode["workspace"] is not None, f"{role}: policy has no Container permissions line"
    assert RUN_AGENT_MODES.get(role) == policy_mode, (
        f"{role}: run-agent.sh uses {RUN_AGENT_MODES.get(role)}, "
        f"policy says {policy_mode}"
    )


def test_allowlist_files_present_in_repo():
    assert STORAGE_ALLOW.exists(), "storage allow-list.json is missing"
    assert RETRIEVAL_ALLOW.exists(), "retrieval allow-list.json is missing"


@pytest.mark.parametrize("role", ROLE_NAMES)
def test_no_storage_overgrant(role):
    policy_ops = POLICY_ROLES[role]["storage_ops"]
    allow_ops = {op for op, roles in STORAGE_ALLOW_DATA.items() if role in roles}
    overgranted = allow_ops - policy_ops
    assert not overgranted, f"{role}: allow-list grants {sorted(overgranted)} not permitted by policy"
