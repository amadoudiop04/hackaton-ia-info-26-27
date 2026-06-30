import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Frontend servi sur http://localhost:5173 (origine autorisée par le CORS backend)
export default defineConfig({
  plugins: [react()],
  server: { port: 5173 },
});
