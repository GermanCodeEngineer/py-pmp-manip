FROM node:20-slim

# Create non-root user
RUN useradd -m runner
USER runner

WORKDIR /app

# Copy extractor script into container
COPY ../extractor.js /app/extractor.js

# Entrypoint: run JS extractor
ENTRYPOINT ["node", "extractor.js"]
