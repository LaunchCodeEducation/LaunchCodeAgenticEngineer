# LaunchCodeDocker

Docker development environment for LaunchCode's **Agentic Programming** course. Provides a consistent, pre-configured Python environment with AI/ML libraries, Anthropic Claude integration, and the Claude Code CLI.

## Quick Start from GitHub

Clone the repo and build locally:

```bash
git clone https://github.com/heatonresearch/LaunchCodeDocker.git
cd LaunchCodeDocker
docker build -t agentic_engineer_1_1 .
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace agentic_engineer_1_1
```

Or skip the build entirely and pull the pre-built image from DockerHub:

```bash
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace heatonresearch/agentic_engineer_1_1:latest
```

## Build

```bash
docker build -t agentic_engineer_1_1 .
```

To force a complete rebuild from scratch (ignoring all cached layers):

```bash
docker build --no-cache -t agentic_engineer_1_1 .
```

## Run

### With a local workspace (recommended)

Mount your local project folder into the container so your files live on your machine, not inside Docker:

```bash
docker run -it --rm -p 8501:8501 -p 8502:8502 -v /path/to/your/workspace:/workspace agentic_engineer_1_1
```

Replace `/path/to/your/workspace` with the actual path on your machine. To use the current directory, you can use `./` (works on macOS, Linux, and modern Windows):

```bash
docker run -it --rm -p 8501:8501 -p 8502:8502 -v ./:/workspace agentic_engineer_1_1
```

Or with `$PWD` on macOS/Linux:

```bash
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace agentic_engineer_1_1
```

On Windows (Command Prompt):

```cmd
docker run -it --rm -p 8501:8501 -v "%cd%":/workspace agentic_engineer_1_1
```

On Windows (PowerShell):

```powershell
docker run -it --rm -p 8501:8501 -v "${PWD}:/workspace" agentic_engineer_1_1
```

Files you create or edit inside `/workspace` in the container will be saved to your local folder and persist after the container exits.

### Without a local workspace

```bash
docker run -it --rm -p 8501:8501 agentic_engineer_1_1
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

## Publishing to DockerHub

Build and tag the image for DockerHub, then push:

```bash
docker build -t heatonresearch/agentic_engineer_1_1:latest .
docker login
docker push heatonresearch/agentic_engineer_1_1:latest
```

To tag a specific version alongside `latest`:

```bash
docker build -t heatonresearch/agentic_engineer_1_1:latest -t heatonresearch/agentic_engineer_1_1:1.0 .
docker push heatonresearch/agentic_engineer_1_1:latest
docker push heatonresearch/agentic_engineer_1_1:1.0
```

Students can then pull and run the image directly without building it locally:

```bash
docker run -it --rm -p 8501:8501 -v "$PWD":/workspace heatonresearch/agentic_engineer_1_1:latest
```

## Running Streamlit apps

From inside the container:

```bash
streamlit run app.py
```

Then open [http://localhost:8501](http://localhost:8501) in your browser.
