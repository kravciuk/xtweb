import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0', // Bind to 0.0.0.0 for Docker compatibility
    port: 3000, // Match the port in Dockerfile and docker-compose.yml
    strictPort: true, // Avoid fallback to another port
    watch: {
      usePolling: true, // Ensure hot reload works inside Docker
    },
  },  
})
