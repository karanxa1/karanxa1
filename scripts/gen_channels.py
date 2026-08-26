#!/usr/bin/env python3
"""Generate the channels signal-rail SVGs (light + dark).

One rail, one node per channel, and a pulse of light that sweeps left->right
lighting each channel as it passes — the "one platform, every channel" motif,
cohesive with the hero signature's traveling pulse. Animation is pure CSS
keyframes (GitHub strips SMIL) and respects prefers-reduced-motion.

Edit CHANNELS, then run:  python3 scripts/gen_channels.py
"""
from pathlib import Path

CHANNELS = ["WHATSAPP", "INSTAGRAM", "FACEBOOK", "VOICE", "EMAIL", "WEB CHAT"]

W, H = 880, 104
MARGIN = 40           # side margin for the first/last node column
RAIL_Y = 46
T = 4.4               # animation cycle seconds
TRAVEL_FRAC = 0.70    # fraction of the cycle the pulse spends travelling

THEMES = {
    "light": {"ink": "#16181d", "mute": "#5b6472", "rail": "#d3d8df", "ring": "#c7ccd4"},
    "dark":  {"ink": "#e8eaed", "mute": "#949cab", "rail": "#2b2f38", "ring": "#363b45"},
}


def node_centers(n):
    col = (W - 2 * MARGIN) / n
    return [MARGIN + col * (i + 0.5) for i in range(n)]


def build(theme: str) -> str:
    c = THEMES[theme]
    cx = node_centers(len(CHANNELS))
    first, last = cx[0], cx[-1]
    span = last - first

    nodes = []
    for i, (x, label) in enumerate(zip(cx, CHANNELS)):
        f = 0 if len(cx) == 1 else i / (len(cx) - 1)
        delay = round(TRAVEL_FRAC * f * T, 3)
        nodes.append(f'''  <g transform="translate({x:.2f},{RAIL_Y})">
    <circle class="ring" r="6"/>
    <circle class="dot" r="3" style="animation-delay:{delay}s"/>
  </g>
  <text class="lbl" x="{x:.2f}" y="{RAIL_Y + 32}" text-anchor="middle">{label}</text>''')

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Channels: {", ".join(CHANNELS)}">
  <title>Channels</title>
  <defs>
    <linearGradient id="trail" gradientUnits="userSpaceOnUse" x1="-22" y1="0" x2="0" y2="0">
      <stop offset="0" stop-color="{c['ink']}" stop-opacity="0"/>
      <stop offset="1" stop-color="{c['ink']}" stop-opacity="1"/>
    </linearGradient>
  </defs>
  <style>
    text {{ font-family: ui-monospace, "SF Mono", "JetBrains Mono", Menlo, monospace; }}
    .lbl  {{ font-size: 10.5px; letter-spacing: 0.18em; fill: {c['mute']}; }}
    .ring {{ fill: none; stroke: {c['ring']}; stroke-width: 1.5; }}
    .dot  {{
      fill: {c['ink']}; opacity: 0.5;
      transform-box: fill-box; transform-origin: center;
      animation: pulse {T}s ease-in-out infinite;
    }}
    .sweep {{ animation: sweep {T}s cubic-bezier(0.5, 0, 0.5, 1) infinite; }}
    .sweep-dot   {{ fill: {c['ink']}; }}
    .sweep-trail {{ stroke: url(#trail); stroke-width: 3; stroke-linecap: round; }}
    @keyframes sweep {{
      0%   {{ transform: translateX(0px); opacity: 0; }}
      5%   {{ opacity: 1; }}
      {int(TRAVEL_FRAC*100)}%  {{ transform: translateX({span:.2f}px); opacity: 1; }}
      {int(TRAVEL_FRAC*100)+6}%  {{ transform: translateX({span:.2f}px); opacity: 0; }}
      100% {{ transform: translateX({span:.2f}px); opacity: 0; }}
    }}
    @keyframes pulse {{
      0%   {{ transform: scale(0.7); opacity: 0.5; }}
      4%   {{ transform: scale(1.75); opacity: 1; }}
      11%  {{ transform: scale(0.7); opacity: 0.5; }}
      100% {{ transform: scale(0.7); opacity: 0.5; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .dot {{ animation: none; opacity: 0.8; }}
      .sweep {{ display: none; }}
    }}
  </style>

  <line class="rail" x1="{MARGIN}" y1="{RAIL_Y}" x2="{W - MARGIN}" y2="{RAIL_Y}" stroke="{c['rail']}" stroke-width="1.5"/>

{chr(10).join(nodes)}

  <g transform="translate({first:.2f},{RAIL_Y})">
    <g class="sweep">
      <line class="sweep-trail" x1="-22" y1="0" x2="0" y2="0"/>
      <circle class="sweep-dot" r="4"/>
    </g>
  </g>
</svg>
'''


def main():
    out = Path(__file__).resolve().parent.parent / "assets"
    for theme in THEMES:
        (out / f"channels-{theme}.svg").write_text(build(theme))
        print(f"wrote assets/channels-{theme}.svg")


if __name__ == "__main__":
    main()
