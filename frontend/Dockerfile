FROM node:20-alpine

WORKDIR /app

COPY package.json .
# COPY package-lock.json .

# Install dependencies with platform-specific settings
RUN npm install --platform=linux --arch=x64

COPY . .

EXPOSE 5173

# Add host flag to allow external connections
CMD [ "npm", "run", "dev", "--", "--host" ]
