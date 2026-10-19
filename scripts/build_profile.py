"""Generate a compact console-inspired profile and its plain-text alternative.

Install scripts/requirements.txt, then run python3 scripts/build_profile.py.
Font outlines, original artwork and embedded assets render without remote services.
"""

from base64 import b64encode
from functools import lru_cache
from html import escape
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

from profile_content import CONTACTS, PROJECTS, SITE, TOOLS

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
@keyframes insert { from { transform: translateY(-24px); } to { transform: translateY(0); } }
@keyframes boot { 0%,30% { opacity: .12; } 100% { opacity: 1; } }
@keyframes status { 50% { opacity: .4; } }
@media (prefers-reduced-motion: reduce) {
  .insert,.display,.status { animation: none !important; }
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
    content += rect(102, 9, 66, 33, CREAM, 2) + d.text("PLAY", 112, 31, 18, BG) + '</g>'
    content += rect(14, 35, 248, 363, "#090a08", 25)
    content += rect(9, 29, 248, 363, "#aaa89e", 25)
    content += '<path d="M24 24h208q18 0 18 18v290q0 50-48 50H24q-20 0-20-20V44q0-20 20-20Z" fill="url(#shell)" stroke="#f1eee5" stroke-width="2"/>'
    content += rect(19, 49, 215, 202, "#61695e", 13)
    content += rect(29, 62, 195, 175, LCD_INK, 5)
    content += rect(33, 67, 187, 165, LCD, 2)
    screen = d.text("PLAYER 01", 43, 84, 11, LCD_INK)
    screen += person(42, 94, 1.7)
    screen += d.text("JOSÉ LUIS", 90, 111, 20, LCD_INK) + d.text("CABALLERO.", 90, 133, 20, LCD_INK)
    screen += rect(43, 155, 166, 20, LCD_INK)
    screen += d.text("Projects", 54, 170, 16, LCD) + d.text("03", 199, 170, 15, LCD, align="right")
    screen += d.text("About me", 54, 193, 16, LCD_INK) + d.text("Contact", 54, 215, 16, LCD_INK)
    content += '<g class="display">' + screen + '</g>'
    content += rect(33, 67, 187, 165, "url(#lcd-grid)")
    content += d.text("PORTFOLIO", 23, 275, 19, "#454b68")
    content += d.text("PRESS START", 24, 290, 8, "#6b6c66", "arcade")
    content += '<circle cx="24" cy="37" r="3" fill="#b25543" class="status"/>'
    content += '<circle cx="64" cy="327" r="31" fill="#c7c7bc"/>'
    content += '<path d="M55 300h18v18h18v18H73v18H55v-18H37v-18h18Z" fill="#25262a"/>'
    content += '<circle cx="176" cy="333" r="19" fill="#b8b6ab"/><circle cx="210" cy="310" r="19" fill="#b8b6ab"/>'
    content += '<circle cx="176" cy="330" r="16" fill="#803753"/><circle cx="210" cy="307" r="16" fill="#803753"/>'
    content += d.text("B", 176, 358, 13, "#454b68", align="center") + d.text("A", 218, 334, 13, "#454b68", align="center")
    content += '<path d="m93 361 18-7m9 7 18-7" stroke="#878e7c" stroke-width="7" stroke-linecap="round"/>'
    content += '<path d="m198 352 13 16m-5-23 13 16m-5-23 13 16" stroke="#9ca28f" stroke-width="4" stroke-linecap="round"/>'
    return content



def hero(mobile=False):
    d = Drawing()
    w, h = (480, 430) if mobile else (840, 330)
    c = d.text("HI, I'M", 28, 42, 15, MUTED, "arcade")
    c += d.text("JOSÉ LUIS", 28, 89, 32 if mobile else 36, INK, "arcade")
    c += d.text("CABALLERO.", 28, 133, 32 if mobile else 36, GREEN, "arcade")
    if mobile:
        c += d.text("Front-end &", 28, 185, 26, INK)
        c += d.text("mobile developer.", 28, 215, 26, INK)
        c += d.text("Building at Wdtech.", 28, 259, 22, MUTED)
        c += d.text("Based in Cádiz.", 28, 287, 22, MUTED)
        c += group(console(d), 295, 156, .57)
        c += action(d, "Play my portfolio", 28, 345, 247)
    else:
        c += d.text("Front-end & mobile developer. Based in Cádiz.", 28, 179, 24, INK, max_width=540)
        c += d.text("At Wdtech. Making the web a little more playful.", 28, 213, 21, MUTED, max_width=550)
        c += action(d, "Play my portfolio", 28, 253, 260)
        # No rule or text sits behind the cartridge's complete animation path.
        c += '<g transform="translate(603 30) rotate(-4 89 140) scale(.69)">' + console(d) + '</g>'
    d.save("header" + ("-mobile" if mobile else ""), w, h,
           "José Luis Caballero. Front-end and mobile developer in Cádiz. Building at Wdtech. Play my interactive portfolio.", c)


def project_panel(project, mobile=False):
    """Compact cartridge artwork alongside its readable project label."""
    d = Drawing()
    w, h = (480, 180) if mobile else (840, 158)
    x, y, cw, ch = 28, 8, 132, 137
    c = rect(x+5, y+5, cw, ch, "#080a07", 8)
    c += f'<path d="M{x+16} {y}H{x+cw-16}v9h16v{ch-9}H{x}V{y+9}h16Z" fill="#343b2f" stroke="#67735a"/>'
    for dy in (17, 22, 27):
        c += rect(x+14, y+dy, cw-28, 2, "#57614c")
    c += rect(x+10, y+35, cw-20, 76, "#13170f", 3)
    c += image(ROOT / "assets/projects" / project["image"], x+14, y+39, cw-28, 62, "xMidYMid slice")
    c += rect(x+14, y+101, cw-28, 5, project["accent"])
    c += rect(x+37, y+120, cw-74, 17, "#10140d", 2)
    for pin_x in range(x+42, x+cw-38, 8):
        c += rect(pin_x, y+122, 3, 15, "#b7a268")
    tx = 184
    text_width = w-tx-28
    c += d.text(project["title"], tx, 47, 28 if mobile else 31, INK, max_width=text_width)
    c += d.paragraph(project["summary"], tx, 79, text_width, 22 if mobile else 24, 27, MUTED)
    if mobile:
        c += d.text(project["medium"], tx, 143, 21, project["accent"])
    else:
        c += d.text(project["stack"], tx, 118, 21, project["accent"], max_width=text_width)
    d.save(project["id"] + ("-mobile" if mobile else ""), w, h,
           project["title"] + ". " + project["summary"] + " " + project["stack"] + ". Open project.", c)


def toolkit(mobile=False):
    d = Drawing()
    w, h = (480, 198) if mobile else (840, 143)
    c = rect(28, 8, w-56, 1, LINE)
    c += d.text("TOOLS I REACH FOR", 28, 40, 14, MUTED, "arcade")
    columns = 3 if mobile else 6
    column = (w-56)/columns
    for index, (asset, label) in enumerate(TOOLS):
        x = 28+(index%columns)*column+column/2
        y = 58+(index//columns)*70
        c += image(ROOT / "assets/tech" / f"{asset}.svg", x-15, y, 30, 30)
        c += d.text(label, x, y+52, 20, INK, align="center", max_width=column-8)
    d.save("toolkit" + ("-mobile" if mobile else ""), w, h,
           "Tools I reach for: " + ", ".join(label for _, label in TOOLS) + ".", c)


def headings(mobile=False):
    w = 480 if mobile else 840
    suffix = "-mobile" if mobile else ""
    d = Drawing()
    c = rect(28, 7, w-56, 1, LINE) + d.text("A FEW THINGS I'VE BUILT", 28, 42, 17, INK, "arcade", max_width=w-56)
    d.save("work"+suffix, w, 58, "A few things I've built. Select a cartridge to open the project.", c)
    d = Drawing()
    c = rect(28, 8, w-56, 1, LINE)
    c += d.text("Offline: boxing, padel & family.", 28, 40, 19 if mobile else 22, MUTED, max_width=w-56)
    d.save("personal"+suffix, w, 60, "Away from the keyboard: boxing, padel and family.", c)
    d = Drawing()
    c = d.text("Plain-text version", 28, 33, 18, MUTED)
    d.save("footer"+suffix, w, 54, "Read this profile as plain text.", c)


def contact_button(key, label):
    d = Drawing()
    w, h = 280, 66
    c = rect(8, 5, w-16, 52, GREEN if key == "email" else RAISED, 5, f'stroke="{LINE}"')
    c += d.text(label, w/2, 39, 26, BG if key == "email" else INK, align="center")
    # Same composition scales well to the smallest supported layout.
    for suffix in ("", "-mobile"):
        d.save("contact-"+key+suffix, w, h, label, c)


def picture(name, alt, url=None, width="100%"):
    content = f'''<picture>
    <source media="(max-width: 600px)" srcset="./assets/profile/{name}-mobile.svg" />
    <img src="./assets/profile/{name}.svg" width="{width}" align="top" alt="{escape(alt, quote=True)}" />
  </picture>'''
    return f'<a href="{url}">\n  {content}\n</a>' if url else content


def write_readme():
    blocks = [picture("header", "José Luis Caballero. Front-end and mobile developer in Cádiz. Building at Wdtech. Open my interactive portfolio.", SITE),
              picture("work", "A few things I've built. Select a cartridge to open the project.")]
    for p in PROJECTS:
        blocks.append(picture(p["id"], p["title"] + ". " + p["summary"] + " " + p["stack"] + ". Open project.", p["url"]))
    blocks += [picture("toolkit", "Tools I reach for: " + ", ".join(label for _, label in TOOLS) + "."),
               picture("personal", "Away from the keyboard: boxing, padel and family.")]
    # One shared line avoids Markdown paragraph gaps between the three links.
    blocks.append("\n".join(picture("contact-"+key, label, url, "32%") for key, label, url in CONTACTS))
    blocks.append(picture("footer", "Read this profile as plain text.", "./PROFILE.md"))
    (ROOT / "README.md").write_text("<!-- Generated by scripts/build_profile.py. Edit copy in scripts/profile_content.py. -->\n\n" + "\n\n".join(blocks) + "\n")
    text = "# José Luis Caballero\n\nFront-end & mobile developer in Cádiz, Spain. At Wdtech. Making the web a little more playful.\n\n"
    text += f"[Play my interactive portfolio]({SITE})\n\n## A few things I've built\n\n"
    text += "\n\n".join(f"- [{p['title']}]({p['url']}) — {p['summary']} {p['stack']}." for p in PROJECTS)
    text += "\n\n**Tools I reach for:** " + ", ".join(label for _, label in TOOLS) + ".\n\n"
    text += "Away from the keyboard: boxing, padel and family.\n\n"
    text += " / ".join(f"[{label}]({url})" for _, label, url in CONTACTS) + "\n"
    (ROOT / "PROFILE.md").write_text(text)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for mobile in (False, True):
        hero(mobile)
        headings(mobile)
        for project in PROJECTS:
            project_panel(project, mobile)
        toolkit(mobile)
    for key, label, _ in CONTACTS:
        contact_button(key, label)
    write_readme()
    print("Built the compact profile, mobile layouts and plain-text version.")
