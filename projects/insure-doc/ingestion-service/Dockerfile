# Use standard Node.js base image
FROM node:20-slim

# Set workdir to the project root
WORKDIR /app

# 1. Install all dependencies at the root
COPY package*.json ./
RUN npm cache clean --force && npm install --legacy-peer-deps && npm dedupe

# 2. Copy the entire project structure
COPY . .

# Expose the Ingestion port
EXPOSE 3001

# Run the ingestion script from the root
CMD ["npm", "run", "dev:ingestion"]
