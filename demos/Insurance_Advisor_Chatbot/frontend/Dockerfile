# Stage 1: Build the React app
FROM node:20-slim AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Stage 2: Serve the app
FROM node:20-slim
WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist

# Cloud Run provides the PORT environment variable
CMD ["sh", "-c", "serve -s dist -l $PORT"]
