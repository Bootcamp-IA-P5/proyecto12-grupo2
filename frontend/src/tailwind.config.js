/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        kumo: {
          cyan: '#00e5ff',     // El color eléctrico del ojo
          dark: '#050a14',     // Fondo muy oscuro
          panel: '#0f172a',    // Para los paneles/tarjetas
          accent: '#2563eb',   // Azul secundario
        },
        fontFamily: {
          sans: ['Inter', 'sans-serif'], // Fuente moderna
        }
      },
    },
  },
  plugins: [],
}