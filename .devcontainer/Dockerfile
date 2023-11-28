# Image for a NYU Lab development environment
FROM rofrano/pipeline-selenium:latest

# Become a regular user for development
ARG USERNAME=vscode
USER $USERNAME

# Install user mode tools
COPY .devcontainer/scripts/install-tools.sh /tmp/
RUN cd /tmp && bash ./install-tools.sh

# Set up the Python development environment
WORKDIR /app
COPY requirements.txt .
RUN sudo pip install -U pip wheel && \
    sudo pip install -r requirements.txt
