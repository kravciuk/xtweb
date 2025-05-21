# Use Node.js 20
FROM node:20

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json package-lock.json ./

# Install dependencies and ensure Vite is installed globally
#RUN npm ci --no-audit && npm install -g vite
RUN rm -f node_modules && \
    npm install --no-audit --prefer-offline

# Copy the rest of the frontend files
COPY . .

# Expose the frontend port
EXPOSE 3000

# Start the development server
CMD ["npx", "vite", "--host"]
# CMD ["/bin/bash"]
