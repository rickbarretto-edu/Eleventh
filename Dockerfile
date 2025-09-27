FROM denoland/deno:latest

WORKDIR /app

# Copy only what's needed
COPY ./src ./src
COPY ./README.md ./README.md

# Cache deps
RUN deno cache src/decks/server.ts

EXPOSE 8000

CMD ["run", "--allow-net", "--allow-env", "src/decks/server.ts"]
