"""Generate the animated terminal SVGs for the GitHub profile README."""

import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"

THEMES = {
    "dark": {
        "bg": "#1C1917",
        "chrome": "#292524",
        "fg": "#F7F5F0",
        "dim": "#A8A29E",
        "accent": "#C17A5C",
        "grid": "#44403C",
        "border": "#3A3532",
    },
    "light": {
        "bg": "#F7F5F0",
        "chrome": "#EFEBE2",
        "fg": "#1C1917",
        "dim": "#78716C",
        "accent": "#B0694B",
        "grid": "#D6D3D1",
        "border": "#E2DDD3",
    },
}

WIDTH = 860
PAD_X = 28
FONT_SIZE = 14
CHAR_W = 8.43
LINE_H = 22
TOP = 64
TYPE_SPEED = 0.045
PROMPT = "lucas@rio ~ $ "

SCRIPT = [
    ("cmd", "whoami"),
    ("out", [("fg", "Lucas Rolim"), ("dim", "  ·  data & AI leader  ·  entrepreneur  ·  Rio de Janeiro, BR")]),
    ("out", [("dim", "Engineer by training, operator by habit. I turn data into decisions and AI into P&L.")]),
    ("gap",),
    ("cmd", "cat career.log"),
    ("out", [("accent", "now     "), ("fg", "leading AI agent builds"), ("dim", " at one of LatAm's largest tech companies")]),
    ("out", [("accent", "now     "), ("fg", "founder, 21xlabs"), ("dim", " · my AI consultancy for established companies")]),
    ("out", [("accent", "before  "), ("fg", "Director of Data & AI"), ("dim", " at high-growth startups")]),
    ("out", [("accent", "edu     "), ("fg", "M.Sc. UFRJ"), ("dim", "  ·  Stanford (business & innovation)  ·  Berkeley (data strategy)")]),
    ("gap",),
    ("cmd", "ls ~/expertise"),
    ("out", [("fg", "data-strategy/   data-platforms/   analytics/      machine-learning/")]),
    ("out", [("fg", "ai-agents/       llm-evals/        data-teams/     product-and-business/")]),
    ("gap",),
    ("cmd", "cat consulting.md"),
    ("out", [("accent", "> "), ("dim", "I advise founders and execs on where data and AI actually pay off,")]),
    ("out", [("accent", "> "), ("dim", "price each bet in ROI before any code, then build it with their team.")]),
    ("out", [("accent", "> "), ("dim", "No ROI, no project. Open source, no lock-in. They own what we ship.")]),
    ("gap",),
    ("cmd", "plot --compounding"),
    ("plot",),
    ("cmd", "echo $CONTACT"),
    ("out", [("accent", "linkedin.com/in/lucasrolim"), ("dim", "   ·   "), ("accent", "21xlabs.com")]),
    ("cursor",),
]


def tspans(parts, colors):
    """Render colored segments of a line as SVG tspans."""
    return "".join(
        f'<tspan fill="{colors[c]}">{escape(t)}</tspan>' for c, t in parts
    )


def reveal(t):
    """Return a SMIL element that makes its parent visible at time t."""
    return f'<set attributeName="opacity" to="1" begin="{t:.2f}s" fill="freeze"/>'


def plot_svg(y0, t, c):
    """Draw the y = 2^x thesis chart and return (svg, height, end_time)."""
    h = 166
    x0 = PAD_X + 24
    w = 360
    base = y0 + h - 30
    top = y0 + 6
    pts = []
    for i in range(121):
        u = i / 120
        v = (2 ** (u * 6) - 1) / (2 ** 6 - 1)
        pts.append(f"{x0 + u * w:.1f},{base - v * (base - top):.1f}")
    lin = f"{x0},{base} {x0 + w},{base - (base - top) * 0.32:.1f}"
    length = 640
    draw = 1.6
    lx = x0 + w + 40
    svg = f"""
  <g opacity="0">{reveal(t)}
    <line x1="{x0}" y1="{top - 4}" x2="{x0}" y2="{base}" stroke="{c['grid']}" stroke-width="1"/>
    <line x1="{x0}" y1="{base}" x2="{x0 + w + 8}" y2="{base}" stroke="{c['grid']}" stroke-width="1"/>
    <polyline points="{lin}" fill="none" stroke="{c['dim']}" stroke-width="1.4" stroke-dasharray="3 5"/>
    <polyline points="{' '.join(pts)}" fill="none" stroke="{c['accent']}" stroke-width="2.6" stroke-linecap="round"
      stroke-dasharray="{length}" stroke-dashoffset="{length}">
      <animate attributeName="stroke-dashoffset" from="{length}" to="0" begin="{t + 0.2:.2f}s" dur="{draw}s" fill="freeze"
        calcMode="spline" keySplines="0.4 0 0.2 1" keyTimes="0;1"/>
    </polyline>
    <text x="{x0 + w - 4}" y="{base + 20}" fill="{c['dim']}" text-anchor="end">effort →</text>
    <text x="{x0 - 10}" y="{top + 4}" fill="{c['dim']}" text-anchor="end">↑</text>
  </g>
  <g opacity="0">{reveal(t + draw + 0.1)}
    <text x="{lx}" y="{y0 + 30}"><tspan fill="{c['accent']}">━━ </tspan><tspan fill="{c['fg']}">y = 2^x</tspan><tspan fill="{c['dim']}">   data × business context</tspan></text>
    <text x="{lx}" y="{y0 + 54}"><tspan fill="{c['dim']}">┄┄ </tspan><tspan fill="{c['fg']}">y = x  </tspan><tspan fill="{c['dim']}">   tech without context</tspan></text>
    <text x="{lx}" y="{y0 + 92}" fill="{c['dim']}">engineering compounds when</text>
    <text x="{lx}" y="{y0 + 116}" fill="{c['dim']}">it starts from the outcome.</text>
  </g>"""
    return svg, h, t + draw + 0.5


def build(theme):
    """Assemble the full terminal SVG for one theme."""
    c = THEMES[theme]
    body = []
    y = TOP
    t = 0.6
    for step in SCRIPT:
        kind = step[0]
        if kind == "gap":
            y += LINE_H * 0.55
        elif kind == "cmd":
            cmd = step[1]
            start_x = PAD_X + len(PROMPT) * CHAR_W
            vals = ";".join(f"{i * CHAR_W:.1f}" for i in range(len(cmd) + 1))
            dur = TYPE_SPEED * (len(cmd) + 1)
            cid = f"c{len(body)}"
            body.append(f"""
  <clipPath id="{cid}"><rect x="{start_x}" y="{y - 16}" width="0" height="{LINE_H}">
    <animate attributeName="width" values="{vals}" calcMode="discrete" begin="{t + 0.25:.2f}s" dur="{dur:.2f}s" fill="freeze"/>
  </rect></clipPath>
  <g opacity="0">{reveal(t)}
    <text x="{PAD_X}" y="{y}"><tspan fill="{c['accent']}">lucas@rio</tspan><tspan fill="{c['dim']}"> ~ $ </tspan></text>
    <text x="{start_x}" y="{y}" fill="{c['fg']}" clip-path="url(#{cid})" font-weight="600">{escape(cmd)}</text>
  </g>""")
            t += 0.25 + dur + 0.35
            y += LINE_H
        elif kind == "out":
            body.append(
                f'\n  <g opacity="0">{reveal(t)}<text x="{PAD_X}" y="{y}">{tspans(step[1], c)}</text></g>'
            )
            t += 0.09
            y += LINE_H
        elif kind == "plot":
            svg, h, t = plot_svg(y - 10, t + 0.1, c)
            body.append(svg)
            y += h
        elif kind == "cursor":
            t += 0.3
            body.append(f"""
  <g opacity="0">{reveal(t)}
    <text x="{PAD_X}" y="{y}"><tspan fill="{c['accent']}">lucas@rio</tspan><tspan fill="{c['dim']}"> ~ $ </tspan></text>
    <rect x="{PAD_X + len(PROMPT) * CHAR_W:.1f}" y="{y - 14}" width="9" height="18" fill="{c['accent']}">
      <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/>
    </rect>
  </g>""")
            y += LINE_H
    height = int(y + 10)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" role="img" aria-label="Lucas Rolim — data and AI engineer, data and AI leader and entrepreneur">
  <style>
    text {{ font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', Menlo, Consolas, 'Liberation Mono', monospace; font-size: {FONT_SIZE}px; white-space: pre; }}
  </style>
  <rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" fill="{c['bg']}" stroke="{c['border']}"/>
  <path d="M0.5 12.5 a12 12 0 0 1 12 -12 h{WIDTH - 25} a12 12 0 0 1 12 12 v24 h-{WIDTH - 1} z" fill="{c['chrome']}"/>
  <circle cx="24" cy="18" r="6" fill="#E0645A"/>
  <circle cx="44" cy="18" r="6" fill="#E5B045"/>
  <circle cx="64" cy="18" r="6" fill="#5FB566"/>
  <text x="{WIDTH / 2}" y="23" fill="{c['dim']}" text-anchor="middle" style="font-size:12px">lucas@rio — zsh</text>
{''.join(body)}
</svg>
"""


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name in THEMES:
        (OUT / f"terminal-{name}.svg").write_text(build(name))
        print("wrote", OUT / f"terminal-{name}.svg")
