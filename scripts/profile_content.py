"""Short public profile copy and links, aligned with joseluisdev.es."""

SITE = "https://www.joseluisdev.es/en"
PROJECTS = [
    {
        "id": "paulitaadiaz", "title": "Paulitaadiaz", "accent": "#c9a6f7", "medium": "3D & community",
        "summary": "A streaming room you can explore in 3D.",
        "stack": "Next.js · Three.js · Redis",
        "url": SITE + "/project/paulitaadiaz", "image": "paulitaadiaz.webp",
    },
    {
        "id": "helementa-app", "title": "Helementa App", "accent": "#79c9be", "medium": "iOS & Android",
        "summary": "IoT monitoring, on iOS and Android.",
        "stack": "React Native · Expo · TypeScript",
        "url": SITE + "/project/helementa-mobile", "image": "helementa-app.webp",
    },
    {
        "id": "wdtech", "title": "Wdtech", "accent": "#ed837b", "medium": "Web & motion",
        "summary": "A website for the connected world.",
        "stack": "Next.js · Three.js · GSAP",
        "url": SITE + "/project/wdtech", "image": "wdtech.webp",
    },
]
TOOLS = [
    ("typescript", "TypeScript"), ("react", "React"), ("nextjs", "Next.js"),
    ("expo-dark", "Expo"), ("threejs-dark", "Three.js"), ("figma", "Figma"),
]
CONTACTS = [
    ("email", "Say hello", "mailto:joseluiscaballerodev@gmail.com"),
    ("linkedin", "LinkedIn", "https://www.linkedin.com/in/joseluiscaballerodev"),
    ("portfolio", "Portfolio", SITE),
]
