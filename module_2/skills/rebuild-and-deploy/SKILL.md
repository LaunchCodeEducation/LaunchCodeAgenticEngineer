Rebuild the Docker image and push it to DockerHub.

Before doing anything, ask the user for:
- The DockerHub username/repository (default: `us-central1-docker.pkg.dev/hire-human/hire-human-ai/agentic_engineer_2`)
- A version tag to apply alongside `latest` (e.g. `2.1`). If the user says "skip" or "none", only tag as `latest`.

Show the user the exact commands that will be run and ask for confirmation before proceeding.

Steps:
1. Confirm the working directory contains a `Dockerfile`. If not, ask the user to navigate to the correct directory (e.g. `module_2/`).
2. Run the build, tagging as both `latest` and the version tag if provided:
   ```
   docker build -t <repo>:latest -t <repo>:<version> .
   ```
   If no version tag, just:
   ```
   docker build -t <repo>:latest .
   ```
3. If the build fails, stop and report the error. Do not attempt to push.
4. Push each tag separately:
   ```
   docker push <repo>:latest
   docker push <repo>:<version>   # if a version tag was provided
   ```
5. If any push fails, report the error and remind the user to run `docker login` if they are not authenticated.
6. On success, confirm the image is live and print the full image reference (e.g. `us-central1-docker.pkg.dev/hire-human/hire-human-ai/agentic_engineer_2:2.1`).
