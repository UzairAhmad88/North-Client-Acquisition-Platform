/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "var(--background)",
        foreground: "var(--foreground)",
        // 1. Forest Green — Primary Identity (15-20%)
        forest: {
          50: '#f2f9f6',
          100: '#e1f3ec',
          200: '#c2e6d8',
          300: '#94d2bb',
          400: '#5fb695',
          500: '#2a9a71',
          600: '#173f35',
          700: '#0f4c3a',
          800: '#0b382b',
          900: '#07251c',
          950: '#03140e',
        },
        // 2. Soft Light Purple — AI & Intelligence (5-8%)
        softpurple: {
          50: '#faf5ff',
          100: '#f3e8ff',
          200: '#e9d5ff',
          300: '#d8b4fe',
          400: '#c084fc',
          500: '#a855f7',
          600: '#9333ea',
          700: '#7e22ce',
          800: '#6b21a8',
          900: '#581c87',
          950: '#3b0764',
        },
        // 3. Warm Ivory & White — Foundation (65-75%)
        warmivory: {
          50: '#ffffff',
          100: '#fdfcf9',
          200: '#faf9f6',
          300: '#f5f3ee',
          400: '#eae6dd',
          500: '#dcd6c9',
        },
        // 4. Warm Brown — Knowledge & Human Warmth (2-5%)
        warmbrown: {
          50: '#fdf8f3',
          100: '#f7ede2',
          200: '#e6ccb2',
          300: '#ddb892',
          400: '#b07d62',
          500: '#92400e',
          600: '#78350f',
          700: '#582c12',
          800: '#43200e',
          900: '#2d1408',
        },
        // 5. Muted Antique Gold — Value Accent (1-3%)
        antiquegold: {
          50: '#fefdf8',
          100: '#fef9c3',
          200: '#fef3c7',
          300: '#fde68a',
          400: '#f59e0b',
          500: '#d97706',
          600: '#c59b27',
          700: '#b45309',
          800: '#92400e',
          900: '#78350f',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'Consolas', 'monospace'],
      },
      boxShadow: {
        'soft-sm': '0 1px 3px 0 rgba(15, 23, 42, 0.04), 0 1px 2px -1px rgba(15, 23, 42, 0.04)',
        'soft-md': '0 4px 12px -2px rgba(15, 23, 42, 0.06), 0 2px 4px -2px rgba(15, 23, 42, 0.04)',
        'soft-lg': '0 10px 25px -3px rgba(15, 23, 42, 0.08), 0 4px 6px -4px rgba(15, 23, 42, 0.04)',
        'gold-glow': '0 4px 14px -2px rgba(197, 155, 39, 0.25)',
        'forest-glow': '0 4px 20px -2px rgba(15, 76, 58, 0.25)',
      }
    },
  },
  plugins: [],
};
