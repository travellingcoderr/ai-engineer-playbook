# Use an official Node.js runtime as a parent image
FROM node:20-alpine AS build

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json ./

# Install dependencies
RUN npm install

# Accept build arguments
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Copy the actual code
COPY . .

# Build the application
RUN npm run build

# Use a lightweight server to serve the build
FROM node:20-alpine AS serve
WORKDIR /app
COPY --from=build /app/dist ./dist
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["serve", "-s", "dist", "-l", "3000"]
