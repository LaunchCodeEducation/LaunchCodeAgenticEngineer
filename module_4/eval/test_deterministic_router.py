import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from route_task_deterministic import route_for_path, route_files


def test_tests_path_routes_to_tester():
    assert route_for_path("tests/test_example.py") == "tester"


def test_docs_path_routes_to_project_manager():
    assert route_for_path("docs/usage.md") == "project-manager"


def test_workflow_path_routes_to_orchestrator():
    assert route_for_path(".github/workflows/ci.yml") == "orchestrator"


def test_unmatched_path_defaults_to_implementer():
    assert route_for_path("src/app.py") == "implementer"


def test_route_files_groups_by_role():
    result = route_files(["src/app.py", "tests/test_app.py", "docs/readme.md"])
    assert result["implementer"] == ["src/app.py"]
    assert result["tester"] == ["tests/test_app.py"]
    assert result["project-manager"] == ["docs/readme.md"]
