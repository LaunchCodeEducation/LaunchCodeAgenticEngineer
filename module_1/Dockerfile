FROM python:3.12-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y \
    curl \
    git \
    bash \
    ca-certificates \
    nano \
    procps \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Claude Code
RUN npm install -g @anthropic-ai/claude-code

# Install OpenCode
RUN npm install -g opencode-ai

# Install ngrok
RUN curl -sSL https://ngrok-agent.s3.amazonaws.com/ngrok.asc \
    | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null \
    && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" \
    | tee /etc/apt/sources.list.d/ngrok.list \
    && apt-get update && apt-get install -y ngrok \
    && rm -rf /var/lib/apt/lists/*

# Claude Code configuration: default settings + status line
RUN mkdir -p /root/.claude
COPY settings.json /root/.claude/settings.json
COPY statusline.sh /root/.claude/statusline.sh
RUN chmod +x /root/.claude/statusline.sh

# Copy entrypoint script
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Student shell quality-of-life improvements
RUN echo 'export PS1="ai-course:\\w# "' >> /root/.bashrc && \
    echo 'alias ll="ls -alF"' >> /root/.bashrc && \
    echo 'alias la="ls -A"' >> /root/.bashrc && \
    echo 'alias l="ls -CF"' >> /root/.bashrc && \
    echo 'alias python="python3"' >> /root/.bashrc && \
    echo 'alias pip="pip3"' >> /root/.bashrc

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["/bin/bash"]
