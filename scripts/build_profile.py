"""Build the profile's original SVG illustrations with Python's standard library.

Run from any directory: python3 scripts/build_profile.py
The portrait is embedded unchanged so GitHub can render each SVG as an image.
"""

from base64 import b64encode
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "profile"
OUT.mkdir(exist_ok=True)

INK = "#f1eee5"
MUTED = "#b5b8b1"
GREEN = "#b7d6a1"
PEACH = "#e6b18b"
BLUE = "#91b8ce"
BG = "#121615"

# A small original 5 × 7 alphabet; paths keep the lettering independent of fonts.
GLYPHS = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [
    "01110/10001/10001/11111/10001/10001/10001",
    "11110/10001/10001/11110/10001/10001/11110",
    "01111/10000/10000/10000/10000/10000/01111",
    "11110/10001/10001/10001/10001/10001/11110",
    "11111/10000/10000/11110/10000/10000/11111",
    "11111/10000/10000/11110/10000/10000/10000",
    "01111/10000/10000/10111/10001/10001/01111",
    "10001/10001/10001/11111/10001/10001/10001",
    "11111/00100/00100/00100/00100/00100/11111",
    "00111/00010/00010/00010/10010/10010/01100",
    "10001/10010/10100/11000/10100/10010/10001",
    "10000/10000/10000/10000/10000/10000/11111",
    "10001/11011/10101/10101/10001/10001/10001",
    "10001/11001/11001/10101/10011/10011/10001",
    "01110/10001/10001/10001/10001/10001/01110",
    "11110/10001/10001/11110/10000/10000/10000",
    "01110/10001/10001/10001/10101/10010/01101",
    "11110/10001/10001/11110/10100/10010/10001",
    "01111/10000/10000/01110/00001/00001/11110",
    "11111/00100/00100/00100/00100/00100/00100",
    "10001/10001/10001/10001/10001/10001/01110",
    "10001/10001/10001/10001/10001/01010/00100",
    "10001/10001/10001/10101/10101/11011/10001",
    "10001/10001/01010/00100/01010/10001/10001",
    "10001/10001/01010/00100/00100/00100/00100",
    "11111/00001/00010/00100/01000/10000/11111",
]))


def pixel(text, x, y, size=3, color=INK):
    paths = []
    for index, char in enumerate(text.upper()):
        glyph = GLYPHS.get("E" if char == "É" else char, "")
        cells = [(col, row) for row, line in enumerate(glyph.split("/"))
                 for col, bit in enumerate(line) if bit == "1"]
        if char == "É":
            cells += [(3, -2), (2, -1)]
        for col, row in cells:
            paths.append(f"M{x + (index * 6 + col) * size:g} {y + row * size:g}h{size:g}v{size:g}h{-size:g}z")
    return f'<path fill="{color}" shape-rendering="crispEdges" d="{"".join(paths)}"/>'


def rect(x, y, w, h, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" {extra}/>'


def text(value, x, y, size=19, color=MUTED, extra=""):
    return f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{color}" {extra}>{escape(value)}</text>'


def group(content, x=0, y=0, scale=1, extra=""):
    return f'<g transform="translate({x} {y}) scale({scale})" {extra}>{content}</g>'


STYLE = """
.enter { animation: enter .75s cubic-bezier(.2,.7,.3,1) both; }
.second { animation-delay: .13s; }
.third { animation-delay: .26s; }
.cartridge { animation: insert 1.8s cubic-bezier(.2,.7,.3,1) both; }
.screen { animation: power 2s ease-out both; }
.heart { animation: heart 1.7s ease-in-out 2; transform-box: fill-box; transform-origin: center; }
.chart { stroke-dasharray: 350; stroke-dashoffset: 0; animation: chart 2.4s ease-out both; }
.lamp { animation: light 2.2s ease-out both; }
@keyframes enter { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: none; } }
@keyframes insert { from { transform: translateY(-22px); } to { transform: translateY(0); } }
@keyframes power { 0%,30% { opacity: .25; } 100% { opacity: 1; } }
@keyframes heart { 0%,60%,100% { transform: scale(1); } 75% { transform: scale(1.12); } }
@keyframes chart { from { stroke-dashoffset: 350; } to { stroke-dashoffset: 0; } }
@keyframes light { from { opacity: .2; } to { opacity: 1; } }
@media (prefers-reduced-motion: reduce) {
  .enter,.cartridge,.screen,.heart,.chart,.lamp { animation: none !important; }
}
"""


def svg(name, w, h, title, content):
    document = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>{STYLE}</style>
{rect(0, 0, w, h, BG)}
{content}
</svg>
'''
    (OUT / f"{name}.svg").write_text(document)


def heart(x, y, color=PEACH, scale=1):
    return group(f'<g class="heart"><path fill="{color}" d="M0 4h4V0h8v4h4V0h8v4h4v8h-4v4h-4v4h-4v4h-4v-4H8v-4H4v-4H0z"/></g>', x, y, scale)


def portrait(x, y, size):
    data = b64encode((ROOT / "assets" / "jose-luis-pixel.png").read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{size}" height="{size}" xlink:href="data:image/png;base64,{data}"/>'


def header(compact=False):
    w, h = (480, 458) if compact else (840, 322)
    content = rect(28, 28, 8, 8, GREEN) + text("JOSÉ LUIS / CÁDIZ, ES", 48, 37, 13, MUTED, 'letter-spacing="1.5"')
    content += '<g class="enter">' + pixel("JOSÉ LUIS", 28, 83, 5.5) + '</g>'
    content += '<g class="enter second">' + pixel("CABALLERO", 28, 137, 5.5, GREEN) + '</g>'
    content += text("Front-end & mobile developer.", 28, 216, 22, INK)
    content += text("Web designer. Curious by nature.", 28, 247, 20)
    if compact:
        content += portrait(282, 265, 160)
        content += heart(35, 307, PEACH, .65)
        content += text("I like making", 28, 362, 20, INK)
        content += text("things you remember.", 28, 390, 20, INK)
    else:
        content += rect(548, 42, 240, 240, "#1c2420")
        content += portrait(559, 44, 224)
        content += heart(747, 39, PEACH, .8)
        content += text("I like making things you remember.", 28, 291, 17, PEACH)
    content += rect(28, h-12, w-56, 1, "#333d34")
    svg("header-mobile" if compact else "header", w, h,
        "José Luis Caballero. Front-end and mobile developer, web designer. Cádiz, Spain.", content)


def console():
    cartridge = rect(69, 2, 64, 49, "#70816c") + rect(78, 9, 46, 25, GREEN) + pixel("JL", 86, 15, 1.8, BG)
    body = rect(41, 29, 122, 170, "#313b33") + rect(33, 22, 122, 170, "#e3dfcc")
    body += rect(44, 36, 99, 80, "#667362") + rect(53, 45, 81, 62, "#b7c787")
    display = pixel("PLAY", 63, 57, 2, "#344b31") + rect(62, 84, 62, 4, "#6d8452")
    display += rect(62, 93, 44, 3, "#6d8452")
    body += '<g class="screen">' + display + '</g>'
    body += rect(51, 139, 39, 13, "#303b32") + rect(64, 126, 13, 39, "#303b32")
    body += rect(115, 137, 15, 15, "#a55c63") + rect(133, 124, 15, 15, "#a55c63")
    body += rect(85, 174, 15, 4, "#7f8775") + rect(107, 174, 15, 4, "#7f8775")
    for y in range(166, 182, 5):
        body += rect(131, y, 15, 2, "#a6ae9a")
    return '<g class="cartridge">' + cartridge + '</g>' + body


def room():
    # An original cutaway studio illustration, not a screenshot of the project.
    art = '<path d="M15 50 112 9 222 56 126 99Z" fill="#6c5962"/>'
    art += '<path d="M15 50 126 99v110L15 160Z" fill="#3f343c"/><path d="m126 99 96-43v111l-96 42Z" fill="#51424b"/>'
    art += '<path d="m15 160 111-49 96 56-96 42Z" fill="#a17c78"/>'
    art += rect(41, 89, 55, 43, "#242c30") + rect(47, 95, 43, 30, "#c08caf", 'class="lamp"')
    art += rect(55, 101, 27, 3, "#ecd5e4") + rect(55, 109, 16, 3, "#967fae")
    art += '<path d="m29 137 68-13 52 25-74 16Z" fill="#d0b0a2"/>'
    art += rect(41, 148, 5, 22, "#3f343c") + rect(124, 155, 5, 25, "#3f343c")
    art += rect(152, 100, 34, 28, "#b2937a") + rect(159, 104, 8, 10, "#eee6cb") + rect(173, 109, 8, 10, "#d0a5b3")
    art += rect(80, 145, 26, 33, "#64526e") + rect(89, 174, 8, 15, "#323436")
    art += rect(180, 148, 19, 24, "#cbb49e") + rect(174, 139, 10, 13, "#819c73") + rect(187, 131, 10, 23, "#98b188")
    art += heart(195, 25, "#d4a4bb", .8)
    return art


def devices():
    art = rect(8, 24, 177, 120, "#718e9b") + rect(14, 30, 165, 108, "#202c32")
    art += rect(24, 43, 39, 5, BLUE) + rect(24, 57, 139, 1, "#40515a")
    for x, height in [(28, 24), (47, 38), (66, 29), (85, 48)]:
        art += rect(x, 119-height, 10, height, "#425a65")
    art += '<path class="chart" d="M25 110 45 98 66 101 87 78 110 83 130 68 164 72" fill="none" stroke="#b7d6a1" stroke-width="3"/>'
    art += rect(83, 144, 25, 16, "#718e9b") + rect(59, 160, 73, 5, "#8a9c9e")
    art += rect(147, 81, 68, 119, "#a9bec8") + rect(153, 87, 56, 107, "#233239")
    art += rect(174, 90, 14, 3, "#a9bec8") + rect(161, 106, 39, 5, INK)
    for y in [125, 145, 165]:
        art += rect(161, y, 7, 7, GREEN) + rect(175, y+1, 25, 4, "#6e8c9b")
    return art


PROJECTS = [
    dict(slug="portfolio", title="MY PORTFOLIO", color=GREEN,
         desktop=["A small console with a lot to explore.", "Project cartridges, pixel art & minigames."],
         mobile=["A small console with a lot to explore.", "Cartridges, pixel art & minigames."],
         stack="Next.js / TypeScript / Three.js", cta="Play the portfolio", art=console),
    dict(slug="paulitaadiaz", title="PAULITAADIAZ", color="#d4a4bb",
         desktop=["A streamer's corner of the internet, in 3D.", "Her room, her dog & a community cork board."],
         mobile=["A streamer's room, brought to life in 3D.", "Her dog & a community cork board."],
         stack="Next.js / Three.js / Redis", cta="Step inside the room", art=room),
    dict(slug="helementa", title="HELEMENTA", color=BLUE,
         desktop=["Connected devices. Clear interfaces.", "IoT monitoring on the web and on mobile."],
         mobile=["Connected devices. Clear interfaces.", "IoT monitoring on web & mobile."],
         stack="Work at Wdtech / React / React Native", cta="Explore the case study", art=devices),
]


def project_card(project, compact=False):
    w, h = (480, 356) if compact else (840, 244)
    content = rect(0, 0, 3, h, project["color"])
    content += pixel(project["title"], 28, 29, 3, project["color"])
    for i, line in enumerate(project["mobile" if compact else "desktop"]):
        content += text(line, 28, 84+i*28, 21 if compact else 20, INK if i == 0 else MUTED)
    content += text(project["stack"], 28, 149, 17)
    content += text(project["cta"], 28, h-34, 20, project["color"])
    x, y, scale = (257, 170, .78) if compact else (584, 22, .96)
    content += group(project["art"](), x, y, scale)
    svg(project["slug"] + ("-mobile" if compact else ""), w, h,
        project["title"] + ". " + " ".join(project["desktop"]), content)


if __name__ == "__main__":
    for compact in (False, True):
        header(compact)
        for project in PROJECTS:
            project_card(project, compact)
    print("Built 8 self-contained SVGs in assets/profile/.")
