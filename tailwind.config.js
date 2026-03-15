/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#1e3a8a", // Deep blue
                secondary: "#eab308", // Golden yellow (representing law/justice)
                dark: "#0f172a",
                darkHighlight: "#1e293b",
                light: "#f8fafc",
            }
        },
    },
    plugins: [],
}
