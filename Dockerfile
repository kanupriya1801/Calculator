FROM jenkins/inbound-agent:latest

USER root

# Install Python and pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Create working directory
RUN mkdir -p /app && chown jenkins:jenkins /app

USER jenkins
WORKDIR /app

# Optional: copy your Python app if building directly
# COPY . /app
