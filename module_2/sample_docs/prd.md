# PRD: Docker Review Workflow

This workflow reviews a repository's Docker setup by running the documented build command, reporting the outcome, and recommending whether the repo is ready to proceed.

---

## Trigger

A developer invokes `claude "Review this repo's Docker setup..."` from the repo root. The workflow is initiated manually; there is no automated hook. The repository folder must be present and accessible in the working directory when the agent is invoked.

---

## Decision Events

- If no Dockerfile or documented build command can be located, the agent reports that the setup is undocumented and recommends against proceeding. It does not attempt to infer or construct a build command.
- If the Docker build succeeds (exit code 0), the agent summarizes any warnings present in the build output and recommends proceeding.
- If the Docker build fails (non-zero exit code), the agent reports all error output and recommends against proceeding. It does not attempt to fix errors, modify the Dockerfile, or retry the build.
- If warnings are present alongside a successful build, the agent includes those warnings in the summary and acknowledges them in the recommendation rationale.

---

## Actions

1. Read the repository's documentation (README, Makefile, or equivalent) to identify the documented Docker build command.
2. Run the documented Docker build command inside the sandbox.
3. Capture the complete output from the build process (stdout and stderr).
4. Evaluate the build result: success (exit code 0) or failure (non-zero exit code).
5. Identify all warnings and errors present in the captured output.
6. Produce a written summary of the build outcome, including all warnings and errors found.
7. Write a final recommendation (ready to proceed or not ready) with a brief rationale tied to the build result and summary.
8. Save the report to `docs/build-report.md`.

---

## Acceptance Criteria

- The agent correctly identifies whether the Docker image built successfully or failed.
- The summary includes all warnings and errors present in the build output; it does not omit any.
- The recommendation is consistent with the build result: a successful build receives a "ready to proceed" recommendation; a failed build receives a "not ready" recommendation.
- The agent did not push, publish, deploy, or modify any files outside of `docs/build-report.md`.
- The report is saved to `docs/build-report.md`.

---

## Assumptions

- Docker is installed and available in the sandbox environment.
- The repository contains documentation that identifies the correct build command.
- The working directory is the repository root when the agent is invoked.

## Risks

- If the repository has no documented build command, the agent may fail to locate it. This case is handled by the first decision event.
- Build times may vary significantly depending on base image size and network conditions.

## Open Questions

- Should the agent identify which specific layer caused a failure, or only report the final error message?
- Is there a maximum acceptable build time after which a run should be recorded as a timeout?
