# Quality Rubric: Docker Review Workflow

## 1.1 Dimensions

### 1.1.1 Build Result Accuracy

Measures whether the agent correctly identified the final outcome of the Docker build. A high score requires the stated result — success or failure — to match the actual exit status of the build command.

### 1.1.2 Warning and Error Coverage

Measures how completely the agent captured warnings and errors from the build output. A high score requires all messages at warning level or above to appear in the summary, with no material omissions.

### 1.1.3 Recommendation Consistency

Measures whether the agent's final recommendation follows logically from the build result and the summary it produced. A high score requires the recommendation to be both directionally correct (proceed vs. not ready) and supported by specific evidence the agent cited.

### 1.1.4 Report Completeness

Measures whether the agent produced a saved report at `docs/build-report.md` containing all required sections: build outcome, warning/error summary, and recommendation. A high score requires all three sections to be present and the file to exist at the expected path.

---

## Scoring Guide

### Build Result Accuracy

**Definition:** Measures whether the agent correctly identified the final outcome of the Docker build. A high score requires the stated result to match the actual exit status of the build command.

**1 — Does not meet:** The agent states the wrong build result. A reviewer relying on the output would act on incorrect information.

> *Example:* Build failed with exit code 1. Agent output reads: "The Docker image built successfully with no errors." A reviewer would conclude the build passed when it did not.

**2 — Partially meets:** The agent's stated result is ambiguous or qualified in a way that obscures the actual outcome. A reviewer cannot determine pass or fail without reading the raw log.

> *Example:* Build failed with exit code 1. Agent output reads: "The build encountered issues during the final layer and may not have completed successfully." The actual outcome is not clearly stated.

**3 — Meets:** The agent states the build result accurately and unambiguously. The exit status matches what a reviewer would see in the raw build log.

> *Example:* Build failed with exit code 1. Agent output reads: "The Docker build failed." Accurate and unambiguous.

**4 — Exceeds:** The agent states the build result accurately and includes the exit code or the specific failing step, giving the reviewer immediate context for where the failure occurred.

> *Example:* Build failed with exit code 1. Agent output reads: "The Docker build failed with exit code 1. The failure occurred at step 7/12 (RUN npm install) due to a non-zero exit status from the package installer."

---

### Warning and Error Coverage

**Definition:** Measures how completely the agent captured warnings and errors from the build output. A high score requires all messages at warning level or above to appear in the summary, with no material omissions.

**1 — Does not meet:** The summary omits one or more errors that appeared in the build output. A reviewer reading only the summary would have an incomplete or misleading picture of what went wrong.

> *Example:* Build log contained three distinct errors: missing base image tag, undefined build argument NODE_ENV, and a missing COPY source file. Agent output reads: "The build encountered some issues and did not complete successfully." None of the specific errors are named.

**2 — Partially meets:** The summary captures all errors but omits one or more warnings. The overall picture is not misleading, but it is incomplete.

> *Example:* Build log contained two errors (missing base image tag, undefined build argument NODE_ENV) and one deprecation warning (legacy COPY syntax). Agent output reads: "The build failed with the following errors: missing base image tag, undefined build argument NODE_ENV. No warnings were reported." The deprecation warning is absent.

**3 — Meets:** The summary captures all errors and all warnings present in the build output. Nothing material is missing.

> *Example:* Build log contained two errors and one warning. Agent output reads: "The build failed with two errors (missing base image tag, undefined build argument NODE_ENV) and one warning (deprecated COPY syntax on line 12)." All items from the log are present.

**4 — Exceeds:** The summary captures all errors and warnings, organizes them by severity, and provides enough context — line numbers, affected layers, forward-looking notes — that a reviewer can prioritize fixes without reading the raw log.

> *Example:* Agent output reads: "The build failed. Two blocking errors must be resolved: missing base image tag (line 1) and undefined build argument NODE_ENV (line 4). One non-blocking warning is present: deprecated COPY syntax on line 12, which will become a hard error in Docker 26."

---

### Recommendation Consistency

**Definition:** Measures whether the agent's final recommendation follows logically from the build result and the summary it produced. A high score requires the recommendation to be both directionally correct and grounded in specific evidence the agent cited.

**1 — Does not meet:** The recommendation contradicts the build result or the summary.

> *Example:* Agent reports the build failed and lists two errors, then concludes: "The repository appears ready to proceed to the next step." The recommendation is inconsistent with the evidence presented.

**2 — Partially meets:** The recommendation is directionally correct but contains no rationale. The reviewer cannot tell from the recommendation why the agent reached that conclusion.

> *Example:* Agent reports the build failed and lists two errors, then concludes: "This repository is not ready." Correct direction, but no reasoning connects the recommendation to the specific errors found.

**3 — Meets:** The recommendation is directionally correct and references the build result and summary as its basis. A reviewer can verify the reasoning without re-reading the full report.

> *Example:* Agent concludes: "This repository is not ready to proceed. The build failed due to a missing base image tag and an undefined build argument. Both errors must be resolved before the image can be built."

**4 — Exceeds:** The recommendation is directionally correct, references specific evidence, and provides prioritized next steps that allow the reviewer to act immediately without interpreting the error list independently.

> *Example:* Agent concludes: "This repository is not ready to proceed. Two blocking errors must be resolved in order: (1) add the missing base image tag to line 1 of the Dockerfile; (2) define or pass the NODE_ENV build argument. After both are fixed, rerun the build to confirm the deprecation warning on line 12 does not also require attention before moving forward."

---

### Report Completeness

**Definition:** Measures whether the agent produced a saved report at `docs/build-report.md` containing all required sections: build outcome, warning/error summary, and recommendation. A high score requires all three sections to be present and the file to exist at the expected path.

**1 — Does not meet:** No report file was saved, or the file was saved to a different location. The reviewer cannot locate the output without searching the filesystem.

> *Example:* The agent printed a summary to the terminal but did not write any file. `docs/build-report.md` does not exist.

**2 — Partially meets:** The report file exists at the correct location but is missing one required section, or contains only raw log output without a structured summary.

> *Example:* `docs/build-report.md` exists and contains the error list but ends abruptly with no recommendation section.

**3 — Meets:** The report file exists at `docs/build-report.md` and contains all three required sections: build outcome, warning/error summary, and recommendation with rationale.

> *Example:* `docs/build-report.md` is present and contains clearly labeled sections for Build Result, Warnings and Errors, and Recommendation.

**4 — Exceeds:** The report exists at the correct location, contains all required sections, and is formatted so a reviewer can scan it quickly — a status line at the top, severity-labeled lists, and a clearly separated recommendation block. The file would require no reformatting before sharing.

> *Example:* `docs/build-report.md` opens with a one-line status ("**Build: FAILED**"), followed by labeled sections with bullet-pointed errors and warnings annotated with line numbers, and closes with a recommendation block that links each suggested action to a specific error.

---

## Pass Threshold

A run is passing if it scores **3 or higher on all four dimensions**.

**Reasoning:** Build Result Accuracy and Recommendation Consistency must both be correct for the output to be trustworthy. A run that scores 4 on Warning and Error Coverage but 2 on Build Result Accuracy produces a well-documented wrong answer, which is worse than a sparse correct one. Report Completeness is included in the floor because a report saved to the wrong location or missing a required section cannot be acted on regardless of how accurate its content would have been. A dimension floor prevents high scores on secondary dimensions from masking failures on primary ones.

---

## Notes on Threshold Design

Considered an aggregate minimum of 10/16 instead of a dimension floor. Ruled out because it would allow a run scoring 1 on Build Result Accuracy to pass if it scored 4 on all other dimensions. An agent that reports the wrong build result is not acceptable regardless of how well it covers warnings or formats the report.

Also considered a hybrid approach: a hard floor of 3 on Build Result Accuracy and Recommendation Consistency only, with an aggregate minimum of 6/8 on the remaining two dimensions. Ruled out as unnecessary complexity for this workflow. All four dimensions are material enough to warrant a uniform floor.

---

## Alternatives Considered

Considered a binary pass/fail checklist with one item per acceptance criterion. Ruled out because it cannot distinguish a near-miss from a complete failure and cannot capture partial credit. A run that omits one warning but correctly identifies all errors and gives a sound recommendation is meaningfully closer to passing than a run that reports the wrong build result entirely. That diagnostic information is required for the agent-as-judge step in later modules.
