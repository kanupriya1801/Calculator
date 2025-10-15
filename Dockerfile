FROM jenkins/inbound-agent:latest
USER root

# Install Python and pip (for your Python app)
RUN apt-get update && \
    apt-get install -y python3 python3-pip curl gnupg && \
    apt-get clean

# Install Helm
RUN curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# Create working directory
RUN mkdir -p /app && chown jenkins:jenkins /app

USER jenkins
WORKDIR /app
