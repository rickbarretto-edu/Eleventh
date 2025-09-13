FROM mcr.microsoft.com/devcontainers/rust:1-1-bullseye

# Install dependencies
RUN apt-get update && \ 
    apt-get install -y curl unzip && \ 
    rm -rf /var/lib/apt/lists/*

# Set Deno
RUN curl -fsSL https://deno.land/install.sh | sh
ENV DENO_INSTALL="/root/.deno"
ENV PATH="$DENO_INSTALL/bin:$PATH"

RUN apt-get update && \
    apt-get install -y docker-compose-plugin && \
    rm -rf /var/lib/apt/lists/*
