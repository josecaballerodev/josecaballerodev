"""Generate JL / POCKET's GitHub edition and its plain-text alternative.

Install scripts/requirements.txt, then run python3 scripts/build_profile.py.
Font outlines, original artwork and embedded assets render without remote services.
"""

from base64 import b64encode
from functools import lru_cache
from html import escape
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

from profile_content import CONTACTS, CV, JOBS, MORE_PROJECTS, PROJECTS, SITE, TOOLS

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile"
BG, RAISED, LINE = "#11120f", "#1b1d18", "#34392e"
INK, MUTED, GREEN = "#eeeee4", "#bec2b5", "#a9cc7f"
LCD, LCD_INK = "#b4c67f", "#293e20"
CREAM, WINE = "#e5e1d7", "#803753"

FONTS = {
    "pixel": TTFont(ROOT / "assets/fonts/PixelifySans.ttf"),
    "arcade": TTFont(ROOT / "assets/fonts/Silkscreen-Regular.ttf"),
}
GLYPH_SETS = {name: font.getGlyphSet() for name, font in FONTS.items()}

STYLE = """
.insert { animation: insert 1.4s cubic-bezier(.2,.75,.25,1) both; }
.display { animation: boot 1.8s ease-out both; }
.status { animation: status 1s ease-in-out 3; }
.underline { transform-origin: left; animation: extend 1.2s ease-out both; }
@keyframes insert { from { transform: translateY(-24px); } to { transform: translateY(0); } }
@keyframes boot { 0%,30% { opacity: .12; } 100% { opacity: 1; } }
@keyframes status { 50% { opacity: .4; } }
@keyframes extend { from { transform: scaleX(.15); } to { transform: scaleX(1); } }
@media (prefers-reduced-motion: reduce) {
  .insert,.display,.status,.underline { animation: none !important; }
}
"""


def rect(x, y, w, h, fill, rx=0, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {extra}/>'


def group(content, x=0, y=0, scale=1, extra=""):
    return f'<g transform="translate({x} {y}) scale({scale})" {extra}>{content}</g>'


@lru_cache(maxsize=None)
def image_data(path):
    mime = {".png": "image/png", ".webp": "image/webp", ".svg": "image/svg+xml"}[path.suffix]
    return "data:" + mime + ";base64," + b64encode(path.read_bytes()).decode()


def image(path, x, y, w, h, fit="xMidYMid meet", extra=""):
    return f'<image x="{x}" y="{y}" width="{w}" height="{h}" preserveAspectRatio="{fit}" href="{image_data(path)}" {extra}/>'


@lru_cache(maxsize=None)
def glyph_path(font_name, glyph_name):
    pen = SVGPathPen(GLYPH_SETS[font_name])
    GLYPH_SETS[font_name][glyph_name].draw(pen)
    return pen.getCommands()


def measure(value, size, font_name="pixel"):
    font = FONTS[font_name]
    cmap = font.getBestCmap()
    return sum(font["hmtx"][cmap[ord(char)]][0] for char in value) * size / font["head"].unitsPerEm


class Drawing:
    """Each image includes only the glyphs it actually uses, once per SVG."""

    def __init__(self):
        self.glyphs = set()

    def text(self, value, x, y, size=24, color=INK, font="pixel", align="left", max_width=None):
        width = measure(value, size, font)
        if max_width is not None and width > max_width + .1:
            raise ValueError(f"Text exceeds its {max_width}px column: {value!r} ({width:.1f}px)")
        if align == "right":
            x -= width
        elif align == "center":
            x -= width / 2
        face = FONTS[font]
        scale = size / face["head"].unitsPerEm
        cursor, uses = 0, []
        for char in value:
            glyph_name = face.getBestCmap()[ord(char)]
            self.glyphs.add((font, glyph_name))
            uses.append(f'<use href="#{font}-{glyph_name}" x="{cursor}"/>')
            cursor += face["hmtx"][glyph_name][0]
        return f'<g fill="{color}" transform="translate({x:g} {y:g}) scale({scale:g} {-scale:g})">{"".join(uses)}</g>'

    def paragraph(self, value, x, y, width, size=24, leading=32, color=MUTED):
        lines, current = [], ""
        for word in value.split():
            proposed = f"{current} {word}".strip()
            if measure(proposed, size) > width and current:
                lines.append(current)
                current = word
            else:
                current = proposed
        if current:
            lines.append(current)
        return "".join(self.text(line, x, y + i * leading, size, color, max_width=width)
                       for i, line in enumerate(lines))

    def save(self, name, width, height, title, content):
        definitions = "".join(f'<path id="{font}-{glyph}" d="{glyph_path(font, glyph)}"/>'
                              for font, glyph in sorted(self.glyphs))
        document = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<defs>{definitions}
<linearGradient id="shell" x2=".7" y2="1"><stop stop-color="#f1eee5"/><stop offset="1" stop-color="#d4d0c6"/></linearGradient>
<pattern id="lcd-grid" width="3" height="3" patternUnits="userSpaceOnUse"><rect width=".5" height="3" fill="#293e20" opacity=".1"/><rect width="3" height=".5" fill="#293e20" opacity=".1"/></pattern>
</defs><style>{STYLE}</style>
{rect(0, 0, width, height, BG)}{content}
</svg>
'''
        (OUT / f"{name}.svg").write_text(document)


# Reused from the original PixelPerson in the portfolio's console, unchanged.
PERSON = [
    "........................", "........11111...........", "......111111111.........",
    ".....11121111111........", ".....112211111111.......", ".....111111111111.......",
    ".....113333331111.......", "....1333333333311.......", "....1331333133331.......",
    "....1331333133331.......", ".....33333333333........", "......333133333.........",
    "......333311333.........", ".......3333333..........", "........33333...........",
    "......122332211.........", ".....12222222211........", "....1222222222211.......",
    "....1222222222211.......", "....3322222222233.......", "....3322222222233.......",
    "....3312222222133.......", ".....31222222213........", "......111111111.........",
    "......112221211.........", "......1122.1211.........", "......1122.1211.........",
    "......1122.1211.........", "......1111.1111.........", ".....11111.11111........",
    "........................", "........................",
]


def person(x, y, scale=1, color=LCD_INK):
    paths = []
    for row, line in enumerate(PERSON):
        for col, shade in enumerate(line):
            if shade != ".":
                opacity = {"1": 1, "2": .72, "3": .35}[shade]
                paths.append(rect(col, row, 1, 1, color, extra=f'opacity="{opacity}"'))
    return group("".join(paths), x, y, scale, 'shape-rendering="crispEdges"')


def action(d, label, x, y, width, fill=GREEN):
    content = rect(x, y, width, 48, fill, 6)
    content += f'<circle cx="{x+25}" cy="{y+24}" r="12" fill="{BG}"/>'
    content += d.text("A", x+25, y+30, 20, fill, align="center")
    content += d.text(label, x+48, y+31, 22, BG, max_width=width-60)
    return content


def console(d):
    content = '<g class="insert">' + rect(90, 1, 90, 58, "#292d28", 5)
    content += rect(102, 9, 66, 33, CREAM, 2) + d.text("JL-26", 111, 31, 18, BG) + '</g>'
    content += rect(14, 35, 248, 363, "#090a08", 25)
    content += rect(9, 29, 248, 363, "#aaa89e", 25)
    content += '<path d="M24 24h208q18 0 18 18v290q0 50-48 50H24q-20 0-20-20V44q0-20 20-20Z" fill="url(#shell)" stroke="#f1eee5" stroke-width="2"/>'
    content += rect(19, 49, 215, 202, "#61695e", 13)
    content += rect(29, 62, 195, 175, LCD_INK, 5)
    content += rect(33, 67, 187, 165, LCD, 2)
    screen = d.text("PLAYER 01", 43, 84, 11, LCD_INK) + d.text("JL / POCKET", 210, 84, 11, LCD_INK, align="right")
    screen += person(42, 94, 1.7)
    screen += d.text("JOSÉ LUIS", 90, 111, 20, LCD_INK) + d.text("CABALLERO.", 90, 133, 20, LCD_INK)
    screen += rect(43, 155, 166, 20, LCD_INK)
    screen += d.text("Projects", 54, 170, 16, LCD) + d.text("02", 199, 170, 15, LCD, align="right")
    screen += d.text("About me", 54, 193, 16, LCD_INK) + d.text("Contact", 54, 215, 16, LCD_INK)
    content += '<g class="display">' + screen + '</g>'
    content += rect(33, 67, 187, 165, "url(#lcd-grid)")
    content += d.text("JL / POCKET", 23, 275, 19, "#454b68")
    content += d.text("DESIGNED TO BE EXPLORED", 24, 290, 8, "#6b6c66", "arcade")
    content += '<circle cx="24" cy="37" r="3" fill="#b25543" class="status"/>'
    content += '<circle cx="64" cy="327" r="31" fill="#c7c7bc"/>'
    content += '<path d="M55 300h18v18h18v18H73v18H55v-18H37v-18h18Z" fill="#25262a"/>'
    content += '<circle cx="176" cy="333" r="19" fill="#b8b6ab"/><circle cx="210" cy="310" r="19" fill="#b8b6ab"/>'
    content += '<circle cx="176" cy="330" r="16" fill="#803753"/><circle cx="210" cy="307" r="16" fill="#803753"/>'
    content += d.text("B", 176, 358, 13, "#454b68", align="center") + d.text("A", 218, 334, 13, "#454b68", align="center")
    content += '<path d="m93 361 18-7m9 7 18-7" stroke="#878e7c" stroke-width="7" stroke-linecap="round"/>'
    content += '<path d="m198 352 13 16m-5-23 13 16m-5-23 13 16" stroke="#9ca28f" stroke-width="4" stroke-linecap="round"/>'
    return content


def section_heading(d, number, label, w, subtitle=None):
    s = rect(28, 15, w-56, 1, LINE)
    s += d.text(number, 28, 58, 17, GREEN, "arcade")
    s += d.text(label, 77, 60, 30, INK)
    if subtitle:
        s += d.text(subtitle, 28, 99, 22, MUTED, max_width=w-56)
    return s


def hero(mobile=False):
    d = Drawing()
    w, h = (480, 772) if mobile else (840, 476)
    c = d.text("JL / POCKET", 28, 38, 21, INK, "arcade")
    c += d.text("GITHUB EDITION", w-28, 37, 11, MUTED, "arcade", "right")
    c += rect(28, 55, w-56, 1, LINE)
    c += d.text("HELLO, I'M", 28, 105, 17, MUTED, "arcade")
    c += d.text("JOSÉ LUIS", 28, 151, 35, INK, "arcade")
    c += d.text("CABALLERO.", 28, 194, 35, GREEN, "arcade")
    c += d.text("Front-end & mobile developer.", 28, 239, 25, INK)
    c += d.text("Web designer. Based in Cádiz.", 28, 269, 23, MUTED)
    if mobile:
        c += action(d, "Open my interactive portfolio", 28, 293, 424)
        c += group(console(d), 111, 353, .96)
        c += d.text("joseluisdev.es", 28, 750, 21, MUTED)
    else:
        c += d.paragraph("I build websites and apps. With a little something you weren't expecting.", 28, 320, 400, 25, 32, MUTED)
        c += action(d, "Open my portfolio", 28, 397, 296)
        c += '<g transform="translate(527 48) rotate(-4 128 200)">' + console(d) + '</g>'
    d.save("header" + ("-mobile" if mobile else ""), w, h,
           "José Luis Caballero. Front-end and mobile developer, web designer in Cádiz. Open the interactive JL / POCKET portfolio.", c)


def cartridge(d, project):
    c = rect(9, 7, 221, 239, "#090a08", 12)
    c += '<path d="M22 0h176v13h19v216H0V13h22Z" fill="#30332f" stroke="#62685c" stroke-width="1"/>'
    for y in [19, 24, 29]:
        c += rect(31, y, 155, 2, "#555b50")
    c += rect(17, 40, 185, 152, "#10110e", 5) + rect(22, 45, 175, 142, "#f6f5f1", 2)
    c += rect(22, 45, 12, 142, project["accent"])
    c += image(ROOT / "assets/projects" / project["image"], 39, 50, 153, 89, "xMidYMid slice")
    c += d.text(project["title"], 39, 160, 19, BG, max_width=157)
    c += d.text("Nº " + project["number"], 39, 179, 12, "#4a5144")
    c += d.text("JL-26", 188, 179, 12, "#4a5144", align="right")
    c += rect(53, 210, 111, 20, "#161b11")
    for x in range(60, 163, 10):
        c += rect(x, 213, 5, 17, "#c7a75e")
    return c


def project_panel(project, mobile=False):
    d = Drawing()
    w, h = (480, 548) if mobile else (840, 300)
    x = 28 if mobile else 310
    c = rect(28, h-1, w-56, 1, LINE)
    c += d.text(project["number"] + " / " + project["role"], x, 32, 19, project["accent"], max_width=w-x-28)
    c += d.text(project["title"], x, 75, 37, INK, max_width=w-x-28)
    for index, line in enumerate(project["lines"]):
        c += d.text(line, x, 114 + index*30, 23 if mobile else 24, MUTED, max_width=w-x-28)
    c += d.text(project["stack"], x, 210, 21, project["accent"], max_width=w-x-28)
    c += group(cartridge(d, project), 131 if mobile else 38, 243 if mobile else 29, .95)
    c += d.text("Open the case study", x, h-26, 24, INK)
    c += rect(x, h-17, 196, 1, project["accent"])
    d.save(project["id"] + ("-mobile" if mobile else ""), w, h,
           project["title"] + ". " + " ".join(project["lines"]) + " " + project["role"] + ". " + project["stack"], c)


def mini_cartridge(number, title, kind, accent, mobile=False):
    d = Drawing()
    w, h = (320, 142) if mobile else (420, 132)
    c = rect(14, 10, w-28, h-20, RAISED, 8, f'stroke="{LINE}"')
    c += rect(28, 31, 5, h-62, accent, 2)
    c += d.text(title, 49, 61, 31 if mobile else 32, INK, max_width=w-70)
    c += d.text(kind, 49, 94, 23 if mobile else 24, MUTED, max_width=w-70)
    d.save("more-" + number + ("-mobile" if mobile else ""), w, h, title + ": " + kind + ". Open case study.", c)


def experience(mobile=False):
    d = Drawing()
    w, h = (480, 820) if mobile else (840, 596)
    c = section_heading(d, "02", "Experience", w)
    for index, (date, company, role, summary) in enumerate(JOBS):
        y = 101 + index*(157 if mobile else 102)
        x = 51 if mobile else 265
        c += f'<circle cx="35" cy="{y+10}" r="4" fill="{GREEN if index == 0 else "#5e6952"}"/>'
        if index < len(JOBS)-1:
            c += rect(34.5, y+22, 1, 130 if mobile else 77, LINE)
        c += d.text(date, 51, y+17, 20, GREEN if index == 0 else MUTED)
        c += d.text(company, x, y+(51 if mobile else 17), 29, INK)
        c += d.text(role, x, y+(81 if mobile else 48), 23, MUTED, max_width=w-x-28)
        c += d.paragraph(summary, x, y+(111 if mobile else 77), w-x-28, 21, 26, MUTED)
    c += rect(28, h-70, w-56, 1, LINE)
    c += d.text("Full experience & education in my CV", 28, h-30, 23, GREEN, max_width=w-56)
    d.save("experience" + ("-mobile" if mobile else ""), w, h,
           "Experience. " + " ".join(f"{company}, {date}, {role}. {summary}" for date, company, role, summary in JOBS), c)


def toolkit(mobile=False):
    d = Drawing()
    w, h = (480, 450) if mobile else (840, 380)
    c = section_heading(d, "03", "My toolkit", w)
    column = (w-56)/3
    for index, (asset, label) in enumerate(TOOLS):
        x, y = 28+(index%3)*column, 93+(index//3)*(98 if mobile else 75)
        if mobile:
            c += image(ROOT / "assets/tech" / f"{asset}.svg", x+column/2-18, y, 36, 36)
            lines = {"React / Native": ["React", "/ Native"], "Tailwind CSS": ["Tailwind", "CSS"]}.get(label, [label])
            for line_index, line in enumerate(lines):
                c += d.text(line, x+column/2, y+61+line_index*22, 21, INK, align="center", max_width=column-6)
        else:
            c += image(ROOT / "assets/tech" / f"{asset}.svg", x+4, y, 35, 35)
            c += d.text(label, x+53, y+26, 25, INK, max_width=column-59)
    c += rect(28, h-59, w-56, 1, LINE)
    c += d.text("Web · Mobile · 3D · Motion", 28, h-25, 24, MUTED)
    d.save("toolkit" + ("-mobile" if mobile else ""), w, h,
           "My toolkit: TypeScript, React, React Native, Next.js, Expo, Three.js, GSAP, Motion, Tailwind CSS and Figma.", c)


def about(mobile=False):
    d = Drawing()
    w, h = (480, 590) if mobile else (840, 366)
    c = section_heading(d, "04", "Behind the controls", w)
    c += d.paragraph("I started programming because I like creating and designing. I like seeing people surprised by something I've made.",
                     28, 111, w-56 if mobile else 492, 26, 33, INK)
    c += d.text("When I close the laptop:", 28, 295 if mobile else 241, 24, MUTED)
    c += d.text("Boxing. Padel. Family.", 28, 330 if mobile else 278, 27, GREEN)
    c += image(ROOT / "assets/jose-luis-pixel.png", 272 if mobile else 570, 365 if mobile else 83, 180 if mobile else 235, 180 if mobile else 235)
    if mobile:
        c += person(35, 389, 3.6, GREEN)
        c += d.text("Cádiz, Spain", 28, 566, 24, MUTED)
    else:
        c += d.text("Cádiz, Spain", 28, 333, 21, MUTED)
    d.save("about" + ("-mobile" if mobile else ""), w, h,
           "I started programming because I like creating and designing. I like seeing people surprised by something I've made. Outside work: boxing, padel and time with my family. Cádiz, Spain.", c)


def contact_heading(mobile=False):
    d = Drawing()
    w, h = (480, 204) if mobile else (840, 177)
    c = section_heading(d, "05", "Let's talk", w)
    c += d.paragraph("Have a project or a job opportunity in mind? Tell me what you're working on.", 28, 108, w-56, 26, 33, MUTED)
    d.save("contact" + ("-mobile" if mobile else ""), w, h,
           "Have a project or a job opportunity in mind? Tell me what you're working on.", c)


def contact_button(key, label, subtitle, mobile=False):
    d = Drawing()
    w, h = (320, 136) if mobile else (420, 122)
    primary = key == "email"
    c = rect(14, 8, w-28, h-16, GREEN if primary else RAISED, 9, f'stroke="{GREEN if primary else LINE}"')
    c += d.text(label, 33, 56, 32, BG if primary else INK)
    c += d.text(subtitle, 33, 94, 23, "#293e20" if primary else MUTED, max_width=w-50)
    d.save("contact-" + key + ("-mobile" if mobile else ""), w, h, label + ": " + subtitle, c)


def headings(mobile=False):
    w = 480 if mobile else 840
    suffix = "-mobile" if mobile else ""
    d = Drawing()
    d.save("work"+suffix, w, 132, "Choose a cartridge. Selected projects.",
           section_heading(d, "01", "Choose a cartridge", w) + d.text("Design, development & a bit of play.", 28, 101, 24, MUTED, max_width=w-56))
    d = Drawing()
    d.save("more"+suffix, w, 64, "More from the collection", d.text("More from the collection", 28, 43, 24, MUTED))
    d = Drawing()
    d.save("footer"+suffix, w, 90, "JL / POCKET. Plain-text profile.",
           rect(28, 22, w-56, 1, LINE) + d.text("JL / POCKET", 28, 63, 15, GREEN, "arcade") +
           d.text("Plain-text profile", w-28, 63, 21, MUTED, align="right"))


def picture(name, alt, url=None, width="100%"):
    content = f'''<picture>
    <source media="(max-width: 600px)" srcset="./assets/profile/{name}-mobile.svg" />
    <img src="./assets/profile/{name}.svg" width="{width}" align="top" alt="{escape(alt, quote=True)}" />
  </picture>'''
    return f'<a href="{url}">\n  {content}\n</a>' if url else content


def write_readme():
    blocks = [picture("header", "José Luis Caballero. Front-end and mobile developer, web designer in Cádiz. Open the interactive JL / POCKET portfolio.", SITE),
              picture("work", "Choose a cartridge. Selected projects.")]
    for p in PROJECTS:
        blocks.append(picture(p["id"], p["title"] + ". " + " ".join(p["lines"]) + " " + p["role"] + ". " + p["stack"] + ". Open case study.", p["url"]))
    blocks.append(picture("more", "More from the collection"))
    for number, title, kind, _, url in MORE_PROJECTS:
        blocks.append(picture("more-"+number, title + ": " + kind + ". Open case study.", url, "49%"))
    blocks += [picture("experience", "Experience. " + " ".join(f"{company}, {date}: {role}. {summary}" for date, company, role, summary in JOBS) + " Open the full CV.", CV),
               picture("toolkit", "TypeScript, React, React Native, Next.js, Expo, Three.js, GSAP, Motion, Tailwind CSS and Figma."),
               picture("about", "I started programming because I like creating and designing. I like seeing people surprised by something I've made. Outside work: boxing, padel and time with my family. Cádiz, Spain."),
               picture("contact", "Have a project or a job opportunity in mind? Tell me what you're working on.")]
    for key, label, subtitle, url in CONTACTS:
        blocks.append(picture("contact-"+key, label + ": " + (url.removeprefix("mailto:") if key == "email" else subtitle), url, "49%"))
    blocks.append(picture("footer", "JL / POCKET. Read the plain-text version of this profile.", "./PROFILE.md"))
    (ROOT / "README.md").write_text("<!-- Generated by scripts/build_profile.py. Edit copy in scripts/profile_content.py. -->\n\n" + "\n\n".join(blocks) + "\n")
    text = "# José Luis Caballero\n\nFront-end & mobile developer and web designer, based in Cádiz, Spain.\n\n"
    text += f"[Interactive portfolio]({SITE}) · [Full CV]({CV})\n\n## Projects\n\n"
    text += "\n\n".join(f"### [{p['title']}]({p['url']})\n\n{' '.join(p['lines'])}\n\n{p['role']} · {p['stack']}" for p in PROJECTS)
    text += "\n\nMore projects: " + " · ".join(f"[{title}]({url})" for _, title, _, _, url in MORE_PROJECTS)
    text += "\n\n## Experience\n\n" + "\n\n".join(f"**{company}** · {date}\n\n{role}. {summary}" for date, company, role, summary in JOBS)
    text += "\n\n## Toolkit\n\nTypeScript, React, React Native, Next.js, Expo, Three.js, GSAP, Motion, Tailwind CSS and Figma.\n\n"
    text += "## Behind the controls\n\nI started programming because I like creating and designing. I like seeing people surprised by something I've made. Outside work, I enjoy boxing, padel and time with my family.\n\n## Contact\n\n"
    text += " · ".join(f"[{label}]({url})" for _, label, _, url in CONTACTS) + "\n"
    (ROOT / "PROFILE.md").write_text(text)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for mobile in (False, True):
        hero(mobile)
        headings(mobile)
        for project in PROJECTS:
            project_panel(project, mobile)
        for number, title, kind, accent, _ in MORE_PROJECTS:
            mini_cartridge(number, title, kind, accent, mobile)
        experience(mobile)
        toolkit(mobile)
        about(mobile)
        contact_heading(mobile)
        for key, label, subtitle, _ in CONTACTS:
            contact_button(key, label, subtitle, mobile)
    write_readme()
    print("Built the complete JL / POCKET profile, mobile compositions and plain-text version.")
