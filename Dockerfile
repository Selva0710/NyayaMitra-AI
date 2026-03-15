# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package config and install dependencies
COPY package.json ./
# Since we manually created package.json without a lockfile, we just run install
RUN npm install

# Copy source code and build
COPY . .
RUN npm run build

# Production stage using Nginx
FROM nginx:alpine

# Copy built assets
COPY --from=builder /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
