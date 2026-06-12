FROM node:20-alpine

# Install build dependencies if needed (e.g. libc6-compat)
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Install dependencies first for better caching
COPY package.json package-lock.json ./
RUN npm ci

# Copy the rest of the application
COPY . .

# Disable telemetry during build
ENV NEXT_TELEMETRY_DISABLED=1

# Build the Next.js app
RUN npm run build

# Expose port
EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# Run the app
CMD ["npm", "start"]
