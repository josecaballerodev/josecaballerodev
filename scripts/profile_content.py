"""Public profile copy. Keep dates, roles and links aligned with joseluisdev.es."""

SITE = "https://www.joseluisdev.es/en"
CV = SITE + "/cv"
PROJECTS = [
    {
        "id": "paulitaadiaz", "number": "01", "title": "Paulitaadiaz",
        "kind": "A room you can explore", "accent": "#c9a6f7",
        "lines": ["Paula's streaming room, in 3D.", "Her dog Ecco, seasonal decorations", "and a live community cork board."],
        "role": "Design & development", "stack": "Next.js · Three.js · Redis",
        "url": SITE + "/project/paulitaadiaz", "image": "paulitaadiaz.webp",
    },
    {
        "id": "helementa", "number": "02", "title": "Helementa",
        "kind": "IoT, made understandable", "accent": "#ff9a65",
        "lines": ["Devices, real-time data and alerts.", "Interfaces that make sensor data", "easier to understand and act on."],
        "role": "Front-end at Wdtech", "stack": "React · Next.js · TypeScript",
        "url": SITE + "/project/helementa", "image": "helementa.webp",
    },
    {
        "id": "helementa-app", "number": "03", "title": "Helementa App",
        "kind": "The same world, in your pocket", "accent": "#79c9be",
        "lines": ["IoT monitoring for iOS and Android.", "Device maps, notifications and", "remote control, wherever you are."],
        "role": "Mobile development at Wdtech", "stack": "React Native · Expo · TypeScript",
        "url": SITE + "/project/helementa-mobile", "image": "helementa-app.webp",
    },
    {
        "id": "wdtech", "number": "05", "title": "Wdtech",
        "kind": "Technology with a visual story", "accent": "#ed837b",
        "lines": ["A website for an IoT company.", "3D, motion and real use cases", "to explain connected environments."],
        "role": "Front-end development", "stack": "Next.js · Three.js · GSAP",
        "url": SITE + "/project/wdtech", "image": "wdtech.webp",
    },
]
MORE_PROJECTS = [
    ("04", "Nexum", "Safety technology", "#ff9a65", SITE + "/project/nexum"),
    ("06", "Santipatico", "PC tuning & bookings", "#f5c747", SITE + "/project/santipatico"),
    ("07", "Enasun", "Solar energy", "#e7c97f", SITE + "/project/enasun"),
    ("08", "AbyssRP", "Web & game server", "#97afff", SITE + "/project/abyss-rp"),
]
JOBS = [
    ("Apr 2025 — now", "Wdtech", "Mobile & front-end developer", "IoT interfaces, apps and corporate websites."),
    ("Jan — Apr 2025", "Freelance", "Front-end & UX/UI designer", "Landing pages and administration dashboards."),
    ("Mar 2023 — Jan 2025", "AbyssRP Network", "Web & server developer", "A roleplay community, built with web tools and Lua."),
    ("Jan 2022 — Mar 2023", "ALTEN España", "Front-end developer", "Web applications with React and JavaScript."),
]
TOOLS = [
    ("typescript", "TypeScript"), ("react", "React / Native"),
    ("nextjs", "Next.js"), ("expo-dark", "Expo"),
    ("threejs-dark", "Three.js"), ("gsap", "GSAP"),
    ("motion-dark", "Motion"), ("tailwindcss", "Tailwind CSS"), ("figma", "Figma"),
]
CONTACTS = [
    ("email", "Email", "Let's talk", "mailto:joseluiscaballerodev@gmail.com"),
    ("linkedin", "LinkedIn", "Work & experience", "https://www.linkedin.com/in/joseluiscaballerodev"),
    ("telegram", "Telegram", "Say hello", "https://t.me/joseluiscaballerow"),
    ("cv", "Full CV", "The complete picture", CV),
]
