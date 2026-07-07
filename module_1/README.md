# LaunchCodeAgenticEngineer

Docker development environment for LaunchCode's **Agentic Programming** course. Provides a consistent, pre-configured Python environment with AI/ML libraries, Anthropic Claude integration, and the Claude Code CLI.

## Quick Start from GitHub

Clone the repo and build locally:

```bash
git clone https://github.com/LaunchCodeEducation/LaunchCodeAgenticEngineer.git
cd LaunchCodeAgenticEngineer
docker build -t agentic_engineer_1 .
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace agentic_engineer_1
```

Or skip the build entirely and pull the pre-built image from DockerHub:

```bash
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace us-central1-docker.pkg.dev/hire-human/hire-human-ai/agentic_engineer_1:latest
```

## Build

```bash
docker build -t agentic_engineer_1 .
```

To force a complete rebuild from scratch (ignoring all cached layers):

```bash
docker build --no-cache -t agentic_engineer_1 .
```

## Run

### With a local workspace (recommended)

Mount your local project folder into the container so your files live on your machine, not inside Docker:

```bash
docker run -it --rm -p 8501:8501 -p 8502:8502 -v /path/to/your/workspace:/workspace agentic_engineer_1
```

Replace `/path/to/your/workspace` with the actual path on your machine. To use the current directory, you can use `./` (works on macOS, Linux, and modern Windows):

```bash
docker run -it --rm -p 8501:8501 -p 8502:8502 -v ./:/workspace agentic_engineer_1
```

Or with `$PWD` on macOS/Linux:

```bash
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace agentic_engineer_1
```

On Windows (Command Prompt):

```cmd
docker run -it --rm -p 8501:8501 -v "%cd%":/workspace agentic_engineer_1
```

On Windows (PowerShell):

```powershell
docker run -it --rm -p 8501:8501 -v "${PWD}:/workspace" agentic_engineer_1
```

Files you create or edit inside `/workspace` in the container will be saved to your local folder and persist after the container exits.

### Without a local workspace

```bash
docker run -it --rm -p 8501:8501 agentic_engineer_1
```

Note: any files created inside the container will be lost when it exits.

## Gmail API Credentials

To use the Gmail API, you need a `credentials.json` file downloaded from the [Google Cloud Console](https://console.cloud.google.com/).

Place `credentials.json` in your workspace directory (the folder you mount as `/workspace`). Inside the container it will be accessible at `/workspace/credentials.json`.

Your code should reference it as:

```python
from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
```

> **Keep `credentials.json` private.** Add it to `.gitignore` so it is never committed to source control:
>
> ```
> credentials.json
> token.json
> ```

On first run, Google will prompt you to authorize access. The resulting `token.json` will be saved in your workspace and reused on subsequent runs.

## Images

Images are built and published automatically by a GitHub Action whenever the main repository (not forks) changes — you don't need to build or push manually.

Students can pull and run the published image directly without building it locally:

```bash
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace us-central1-docker.pkg.dev/hire-human/hire-human-ai/agentic_engineer_1:latest
```
