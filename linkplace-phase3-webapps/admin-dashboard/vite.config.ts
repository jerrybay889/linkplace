import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    allowedHosts: [
      '0f9b6925-41eb-4a3a-a7dd-72939d75ff21-00-o6yhlr32ewwy.sisko.replit.dev',
      // 기존 허용 도메인 추가
    ]
  }
});
