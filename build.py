#!/usr/bin/env python3
# 実行: python3 build.py → index.html を作り直す（型は akiba-anime-day-kids のユリア式）
# 地図は eatmap（akiba-where-to-eat）と同一方式: SVGスケッチ地図＋pinzoom.js（_tools/pinzoom.js は eatmap engine のコピー）
import json, os, math, random, re
URL = "https://yukitchy.github.io/tokyo-museums-for-robert/"
here = os.path.dirname(os.path.abspath(__file__))
C = json.load(open(os.path.join(here, "img/credits.json")))

# img, tag, name, hours chip, reserve?, maps query, official URL (hours source)
S = [
 ("THE STORY OF TOKYO", [
  ("edo-tokyo.jpg", "History", "Edo-Tokyo Museum", "9:30–17:30 · Closed Mon", False, "Edo-Tokyo Museum Ryogoku", "https://www.edo-tokyo-museum.or.jp/en/information/hours/"),
  ("tnm.jpg", "Art & History", "Tokyo National Museum", "9:30–17:00 · Closed Mon", False, "Tokyo National Museum", "https://www.tnm.jp/modules/r_free_page/index.php?id=113&amp;lang=en"),
  ("hokusai.jpg", "Ukiyo-e Art", "Sumida Hokusai Museum", "9:30–17:30 · Closed Mon", False, "Sumida Hokusai Museum", "https://hokusai-museum.jp/modules/Page/pages/view/1111?lang=en"),
  ("tatemonoen.jpg", "Architecture", "Edo-Tokyo Open Air Architectural Museum", "9:30–17:30 · Closed Mon", False, "Edo-Tokyo Open Air Architectural Museum", "https://www.tatemonoen.jp/english/raien/holiday.php"),
 ]),
 ("MANGA & ANIME PILGRIMAGE", [
  ("ghibli.jpg", "Anime", "Ghibli Museum, Mitaka", "10:00–18:00 · Closed Tue", True, "Ghibli Museum Mitaka", "https://www.ghibli-museum.jp/en/tickets/"),
  ("tokiwaso.jpg", "Manga", "Tokiwa-so Manga Museum", "10:00–18:00 · Closed Mon", False, "Tokiwa-so Manga Museum", "https://tokiwasomm.jp/guide/"),
  ("suginami.jpg", "Anime", "Suginami Animation Museum", "10:00–18:00 · Closed Mon", False, "Suginami Animation Museum", "https://www.sam.or.jp/guide"),
  ("fujiko.jpg", "Manga", "Fujiko F. Fujio Museum", "10:00–18:00 · Closed Tue", True, "Fujiko F. Fujio Museum Kawasaki", "https://fujiko-museum.com/english.html"),
 ]),
 ("SCIENCE, TRAINS & ONE OF A KIND", [
  ("kiseichu.jpg", "One of a Kind", "Meguro Parasitological Museum", "10:00–17:00 · Closed Mon, Tue", False, "Meguro Parasitological Museum", "https://www.kiseichu.org/e-top"),
  ("kahaku.jpg", "Science", "National Museum of Nature and Science", "9:00–17:00 · Closed Mon", False, "National Museum of Nature and Science Ueno", "https://www.kahaku.go.jp/english/riyou/nyukan-annai/index.html"),
  ("railway.jpg", "Trains", "The Railway Museum", "10:00–17:00 · Closed Tue", False, "The Railway Museum Omiya", "https://www.railway-museum.jp/information/"),
 ]),
]
HERO = ["edo-tokyo.jpg", "tnm.jpg", "ghibli.jpg"]
POINTS = [
 ("For", "Robert: 10 days in Tokyo built around the Ave Mujica shows (May 29–30, K-Arena Yokohama). These are the museums from our lesson, plus a few more worth the trip."),
 ("When", "Most museums in Tokyo close on Mondays. The Monday right after the shows (May 31) is a closed day almost everywhere — keep it for shopping or a day trip instead."),
 ("Tickets", "Two on this list are reservation-only and sell out: the Ghibli Museum and the Fujiko F. Fujio Museum. Tickets go on sale about a month ahead — set a reminder. Everywhere else, you can just walk in."),
 ("Note", "Hours below were checked in November 2026. Please double-check the official site before you go."),
]
OG = os.environ.get("OG", "3")
# map pins: lat, lng, card shift (l/r/""), card below the point (for the Ueno/Ryogoku 2x2 cluster)
LL = {"edo-tokyo.jpg": (35.6965, 139.7957, "l", 1), "tnm.jpg": (35.7189, 139.7766, "l", 0),
      "hokusai.jpg": (35.6967, 139.8008, "r", 1), "tatemonoen.jpg": (35.7155, 139.5124, "l", 0),
      "ghibli.jpg": (35.6962, 139.5704, "l", 0), "tokiwaso.jpg": (35.7262, 139.6855, "", 0),
      "suginami.jpg": (35.7125, 139.6148, "", 0), "fujiko.jpg": (35.6098, 139.5625, "", 0),
      "kiseichu.jpg": (35.6315, 139.7068, "", 0), "kahaku.jpg": (35.7164, 139.7763, "r", 0),
      "railway.jpg": (35.9214, 139.6178, "", 0)}
# pin labels on the sketch map (short names, eatmap .lbl style)
SHORT = {"edo-tokyo.jpg": "Edo-Tokyo Museum", "tnm.jpg": "Tokyo National Museum", "hokusai.jpg": "Hokusai Museum",
         "tatemonoen.jpg": "Open Air Museum", "ghibli.jpg": "Ghibli Museum", "tokiwaso.jpg": "Tokiwa-so",
         "suginami.jpg": "Suginami Animation", "fujiko.jpg": "Fujiko F. Fujio Museum",
         "kiseichu.jpg": "Parasitological Museum", "kahaku.jpg": "Nature & Science", "railway.jpg": "Railway Museum"}

# ---- sketch map data (eatmap mapbg 方式: 緯度経度ポリラインをそのまま描く) ----
YAMANOTE = [(35.6812,139.7671),(35.6751,139.7633),(35.6662,139.7583),(35.6554,139.7568),(35.6457,139.7476),(35.6285,139.7388),(35.6197,139.7286),(35.6260,139.7236),(35.6339,139.7158),(35.6467,139.7101),(35.6580,139.7016),(35.6702,139.7027),(35.6831,139.7020),(35.6896,139.7006),(35.7013,139.7003),(35.7137,139.7037),(35.7212,139.7066),(35.7289,139.7114),(35.7318,139.7282),(35.7335,139.7394),(35.7365,139.7469),(35.7380,139.7609),(35.7321,139.7667),(35.7278,139.7708),(35.7208,139.7781),(35.7141,139.7774),(35.7074,139.7745),(35.6984,139.7731),(35.6918,139.7709)]
CHUO = [(35.6812,139.7671),(35.6918,139.7709),(35.6997,139.7650),(35.6859,139.7301),(35.6896,139.7006),(35.7056,139.6658),(35.7053,139.6496),(35.7046,139.6354),(35.7041,139.6199),(35.7033,139.5996),(35.7032,139.5799),(35.7027,139.5607),(35.7023,139.5450),(35.7017,139.5242),(35.7012,139.5036),(35.7005,139.4700)]
SOBU = [(35.6812,139.7671),(35.6886,139.7744),(35.6943,139.7827),(35.6961,139.7927),(35.6966,139.8138),(35.6966,139.8400)]
TOHOKU = [(35.9063,139.6239),(35.8936,139.6334),(35.8587,139.6572),(35.8186,139.6845),(35.7786,139.7210),(35.7528,139.7380),(35.7380,139.7609),(35.7321,139.7667),(35.7278,139.7708),(35.7141,139.7774),(35.7074,139.7745),(35.6984,139.7731),(35.6918,139.7709),(35.6812,139.7671),(35.6751,139.7633),(35.6662,139.7583),(35.6554,139.7568),(35.6457,139.7476),(35.6285,139.7388),(35.5885,139.7279),(35.5623,139.7160),(35.5319,139.6968),(35.5050,139.6880)]
SAIKYO = [(35.9063,139.6239),(35.8455,139.6479),(35.8019,139.6910),(35.7786,139.7210),(35.7449,139.7191),(35.7289,139.7114)]
ODAKYU = [(35.6896,139.7006),(35.6686,139.6795),(35.6613,139.6669),(35.6408,139.5997),(35.6214,139.5703),(35.6175,139.5646),(35.6100,139.5500)]
# station labels: name, lat, lng, anchor, dx, dy
STLBL = [("OMIYA",35.9063,139.6239,'start',26,5),("UENO",35.7141,139.7774,'start',26,5),
         ("TOKYO",35.6812,139.7671,'start',26,5),("RYOGOKU",35.6961,139.7927,'middle',0,27),
         ("IKEBUKURO",35.7289,139.7114,'end',-26,5),("SHINJUKU",35.6896,139.7006,'end',-26,5),
         ("MEGURO",35.6339,139.7158,'start',26,5),("MITAKA",35.7027,139.5607,'middle',0,-16),
         ("KOGANEI",35.7012,139.5036,'middle',0,27)]

K2 = '#121212'; GY = '#E9E8E4'
def _blds(seed=5, pad=14):
    XS = [0,70,205,340,470,560,600]; YS = [0,70,200,330,470,600,680]
    r = random.Random(seed); out = []
    for i in range(6):
        for j in range(6):
            x0,y0,x1,y1 = XS[i]+pad, YS[j]+pad, XS[i+1]-pad, YS[j+1]-pad
            if x1-x0 < 20 or y1-y0 < 20: continue
            nx = 3 if x1-x0 > 150 else 2 if x1-x0 > 70 else 1; ny = 2 if y1-y0 > 70 else 1
            w = (x1-x0)/nx; h = (y1-y0)/ny
            for a in range(nx):
                for b in range(ny):
                    if r.random() < .1: continue
                    g = 3 + r.random()*2
                    out.append((x0+a*w+g, y0+b*h+g, w-2*g, h-2*g, r.random()))
    return out
def _path(pl): return 'M' + ' L'.join(f'{x} {y}' for x, y in pl)
def _halo(t, x, y, anchor='middle', size=13):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="900" fill="{K2}" stroke="{GY}" stroke-width="4" stroke-linejoin="round" paint-order="stroke">{t}</text>'
def _line(f, pts, close=False):
    d = _path([f(a, b) for a, b in pts]) + ('Z' if close else '')
    return (f'<path d="{d}" fill="none" stroke="{K2}" stroke-width="18" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="#fff" stroke-width="10" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{K2}" stroke-width="2.5" stroke-dasharray="12 12" stroke-linejoin="round"/>')
def _gline(f, pts):
    return f'<path d="{_path([f(a, b) for a, b in pts])}" fill="none" stroke="#8C8B86" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
def project(pts):
    la0 = sum(a for a, _ in pts)/len(pts); k = math.cos(math.radians(la0))*111320
    xy = lambda a, b: (b*k, -a*111320)
    P = [xy(a, b) for a, b in pts]; xs = [p[0] for p in P]; ys = [p[1] for p in P]
    sc = min((600-120)/(max(xs)-min(xs)), (680-140)/(max(ys)-min(ys)))
    ox = 300-(max(xs)+min(xs))/2*sc; oy = 340-(max(ys)+min(ys))/2*sc
    return (lambda a, b: (round(xy(a, b)[0]*sc+ox), round(xy(a, b)[1]*sc+oy))), sc
def tokyo_bg(f, sc):
    s = f'<rect x="-420" y="-420" width="1440" height="1520" fill="{GY}"/>'
    g = ''.join(f'<line x1="{x}" y1="0" x2="{x}" y2="680" stroke="#fff" stroke-width="14"/>' for x in range(70, 620, 135))
    g += ''.join(f'<line x1="0" y1="{y}" x2="600" y2="{y}" stroke="#fff" stroke-width="14"/>' for y in range(70, 700, 130))
    s += g
    for x, y, w, h, r in _blds():
        s += f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{"#D9D8D3" if r < .5 else "#CFCEC9"}"/>'
    s += _gline(f, ODAKYU)
    s += _line(f, TOHOKU); s += _line(f, SAIKYO); s += _line(f, SOBU); s += _line(f, CHUO); s += _line(f, YAMANOTE, True)
    L = ''
    for name, a, b, anchor, dx, dy in STLBL:
        x, y = f(a, b)
        s += f'<rect class="stbar" x="{x-22}" y="{y-8}" width="44" height="16" rx="2" fill="{K2}" transform="rotate(0 {x} {y})"/><circle class="stdot" cx="{x}" cy="{y}" r="6" fill="{GY}"/>'
        L += _halo(name, x+dx, y+dy, anchor, 13)
    s += f'<g class="bgl">{L}</g>'
    s += f'<g transform="translate(40 56)"><circle r="19" fill="none" stroke="{K2}" stroke-width="2"/><path d="M0 -15 L6 4 L0 0 L-6 4Z" fill="{K2}"/><text y="-23" text-anchor="middle" font-size="12" font-weight="900" fill="{K2}">N</text></g>'
    L2 = 5000*sc
    s += f'<g transform="translate(24 652)"><path d="M0 0H{L2:.0f}M0 -5V5M{L2:.0f} -5V5M{L2/2:.0f} -3V3" stroke="{K2}" stroke-width="2.5" fill="none"/><text x="{L2/2:.0f}" y="-9" text-anchor="middle" font-size="11" font-weight="800" fill="{K2}">5 km</text></g>'
    return s

esc = lambda s: s.replace("&", "&amp;")
clock = '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 4.5V8l2.5 1.8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'

def tile(m, n):
    img, tag, name, hrs, res, q, _ = m
    href = "https://www.google.com/maps/search/?api=1&amp;query=" + q.replace(" ", "+")
    h, d = hrs.split(" · ")
    chips = ('<span class="chip r">Reservation only</span>' if res else "") + f'<span class="chip">{clock}<span>{h} ·</span><span>{d}</span></span>'
    return (f'<div class="tw" id="m{n}"><a class="num" href="#map" data-n="{n}" aria-label="Show {n} on the map">{n}</a><a class="tile" href="{href}" target="_blank" rel="noopener" aria-label="{esc(name)} on Google Maps">'
            f'<span class="ph"><img src="img/{img}" alt="" loading="lazy"><span class="tt">{esc(tag)}</span></span>'
            f'<span class="tn">{esc(name)}</span><span class="chips">{chips}</span></a></div>')

_n = iter(range(1, 99))
secs = "".join(f'<section><h2 class="bar">{esc(t)}</h2><div class="wall">' + "".join(tile(m, next(_n)) for m in ms) + "</div></section>" for t, ms in S)
points = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in POINTS)
hero = "".join(f'<img src="img/{f}" alt="">' for f in HERO)
allm = [m for _, ms in S for m in ms]
names = {m[0]: m[2] for m in allm}
cred = "; ".join(f'{names[f]}: <a href="{c["url"]}">{c["author"]}</a> ({c["license"]})' for f, c in C.items() if f in names)
offi = " · ".join(f'<a href="{m[6]}">{esc(m[2])}</a>' for m in allm)
PHJ = json.dumps({i: f"img/{m[0]}" for i, m in enumerate(allm, 1)})
PINZOOM = open(os.path.join(here, "_tools/pinzoom.js")).read()

def svgmap():
    mp = [(LL[m[0]][0], LL[m[0]][1]) for m in allm]
    f, sc = project(mp + [(a, b) for _, a, b, _, _, _ in STLBL])
    pin = [list(f(a, b)) for a, b in mp]
    for _ in range(60):  # 近すぎるピンを少し離す（スケッチ地図なので見やすさ優先・eatmap と同じ）
        for i in range(len(pin)):
            for j in range(i):
                dx, dy = pin[i][0]-pin[j][0], pin[i][1]-pin[j][1]; d = math.hypot(dx, dy) or .1
                if d < 38: mv = (38-d)/2; pin[i][0] += dx/d*mv; pin[i][1] += dy/d*mv; pin[j][0] -= dx/d*mv; pin[j][1] -= dy/d*mv
    o = f'<svg id="map" viewBox="0 0 600 680" role="img" aria-label="Sketch map of the {len(pin)} museums">{tokyo_bg(f, sc)}'
    for i, (m, (x, y)) in enumerate(zip(allm, pin), 1):
        x, y = round(x), round(y); nm = SHORT[m[0]]
        w = round(len(nm)*8.4+20); lx = min(max(x-w//2, 4), 596-w); ly = y-42 if y > 50 else y+14
        o += f'<a class="pin" href="#m{i}" data-n="{i}"><circle cx="{x}" cy="{y}" r="16" fill="#121212" stroke="#fff" stroke-width="3"/><text x="{x}" y="{y+6}" text-anchor="middle" font-size="16" font-weight="900" fill="#fff">{i}</text><g class="lbl"><rect x="{lx}" y="{ly}" width="{w}" height="28" fill="#121212"/><text x="{lx+w//2}" y="{ly+19}" text-anchor="middle" font-size="14" font-weight="800" fill="#fff">{esc(nm)}</text></g></a>'
    # 地名ラベル(.bgl)はピンに隠れないよう SVG の最後尾へ（eatmap と同じ）
    i = o.index('<g class="bgl">'); d = 0; end = None
    for mm in re.finditer(r'<g(?:\s[^>]*)?>|</g>', o[i:]):
        if mm.group(0) == '</g>':
            d -= 1
            if d == 0: end = i+mm.end(); break
        else: d += 1
    assert end, 'bgl group not closed'
    bglg = o[i:end]; o = o[:i]+o[end:]
    return o+bglg+'</svg>'
MAPSVG = svgmap()
desc = "Eleven museums in and around Tokyo for 10 days around the Ave Mujica shows, late May 2027."

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>Tokyo Museums for Robert</title><meta name="robots" content="noindex,nofollow"><meta name="description" content="{desc}">
<link rel="canonical" href="{URL}"><meta property="og:type" content="website"><meta property="og:url" content="{URL}">
<meta property="og:title" content="Tokyo Museums for Robert"><meta property="og:description" content="{desc}">
<meta property="og:image" content="{URL}ogp/og-{OG}.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{URL}ogp/og-{OG}.png">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 64 64%22%3E%3Crect width=%2264%22 height=%2264%22 fill=%22%23121212%22/%3E%3Crect x=%2214%22 y=%2214%22 width=%2236%22 height=%2236%22 fill=%22%23D9342B%22/%3E%3C/svg%3E">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap" rel="stylesheet">
<style>
:root{{--bg:#F1EFEA;--ink:#121212;--red:#D9342B;--mu:#5D5A54}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 Archivo,sans-serif;overflow-x:hidden}}
a{{color:inherit}}
.col{{max-width:760px;margin:0 auto;padding:0 max(16px,env(safe-area-inset-left,0px))}}
h1,h2{{font-family:Archivo,sans-serif;font-stretch:62%;font-weight:900;text-transform:uppercase;letter-spacing:-.01em;white-space:nowrap}}
.top{{display:flex;justify-content:space-between;font-weight:800;font-size:13px;letter-spacing:.14em;padding:18px 0 8px;border-bottom:4px solid var(--ink)}}
h1{{margin:14px 0 4px;font-size:min(8.2vw,62px);line-height:.95}}
.sub{{margin:0 0 16px;font-weight:700;font-size:15px;color:var(--mu)}}
.hero{{display:grid;grid-template-columns:3fr 2fr;grid-template-rows:1fr 1fr;gap:3px;height:min(78vw,440px)}}
.hero img{{display:block;width:100%;height:100%;object-fit:cover;min-width:0;min-height:0}}.hero img:first-child{{grid-row:1/3}}
.hb{{display:flex;justify-content:space-between;gap:12px;background:var(--ink);color:#fff;padding:13px 16px;font-weight:800;font-size:13px;letter-spacing:.08em;white-space:nowrap;text-transform:uppercase}}.hb b{{color:#FF7A6E}}
.pts{{margin:26px 0 0;border-top:4px solid var(--ink)}}
.pts div{{display:grid;grid-template-columns:76px 1fr;gap:12px;padding:12px 0;border-bottom:1px solid #c9c5bc}}
.pts dt{{font:900 18px/1.25 Archivo,sans-serif;font-stretch:62%;text-transform:uppercase;letter-spacing:.04em;color:var(--red)}}
.pts dd{{margin:0;font-size:15px}}
.bar{{margin:38px 0 10px;font-size:min(7.2vw,32px);line-height:1;padding-bottom:8px;border-bottom:4px solid var(--ink)}}
.wall{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px 10px}}
.tile{{display:flex;flex-direction:column;gap:6px;text-decoration:none;min-width:0}}
.tile .ph{{position:relative;display:block;aspect-ratio:4/3;overflow:hidden;background:#222}}
.tile img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transition:transform .3s}}.tile:hover img{{transform:scale(1.03)}}
.tt{{position:absolute;left:0;top:0;background:var(--red);color:#fff;font:900 12px/1 Archivo,sans-serif;letter-spacing:.08em;text-transform:uppercase;padding:6px 8px}}
.tn{{font-weight:800;font-size:16px;line-height:1.2}}
.chips{{margin-top:auto;display:flex;flex-wrap:wrap;gap:4px}}
.chip{{display:inline-flex;align-items:center;gap:5px;background:var(--ink);color:#fff;font:800 12px/1 Archivo,sans-serif;font-stretch:80%;letter-spacing:.02em;line-height:1.25;padding:5px 7px;max-width:100%;flex-wrap:wrap;column-gap:4px}}.chip span{{white-space:nowrap}}.chip svg{{flex:none;color:#FF7A6E}}
.chip.r{{background:var(--red)}}
.tw{{position:relative;display:flex;flex-direction:column;min-width:0}}.tw .tile{{flex:1}}
.num{{position:absolute;z-index:2;right:0;top:0;min-width:28px;height:28px;display:grid;place-items:center;background:var(--ink);color:#fff;font:900 15px/1 Archivo,sans-serif;text-decoration:none}}
#map{{display:block;width:100%;height:auto;background:#E9E8E4;border:4px solid var(--ink)}}
#map text{{font-family:Archivo,sans-serif;pointer-events:none}}
.pin{{cursor:pointer}}.pin .lbl{{display:none}}.pin:hover .lbl,.pin.on .lbl{{display:block}}
.mapnote{{margin:8px 0 0;font-size:13px;color:var(--mu);font-weight:700}}
.flash .ph{{outline:4px solid var(--red);outline-offset:2px}}
.foot{{margin-top:44px;padding:20px 0 44px;border-top:4px solid var(--ink);font-size:13px;color:var(--mu)}}.foot p{{margin:0 0 10px}}.foot b{{color:var(--ink)}}
@media(max-width:699px){{.tw:last-child:nth-child(odd){{grid-column:1/-1}}.tw:last-child:nth-child(odd) .ph{{aspect-ratio:2.4/1}}}}
@media(min-width:700px){{.wall{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
</style></head><body>
<div class="col"><div class="top"><span>GUEST GUIDE</span><span>LATE MAY 2027</span></div>
<h1>Tokyo Museums for Robert</h1>
<p class="sub">10 days in Tokyo around the Ave Mujica shows — late May 2027</p>
<div class="hero">{hero}</div>
<div class="hb"><span>{len(allm)} museums</span><a href="#map"><b>Tap for the map</b></a></div>
<dl class="pts">{points}</dl>
<section><h2 class="bar">THE MAP</h2>{MAPSVG}
<p class="mapnote">Numbers match the list below. Tap a pin to see the name, tap again to jump to the place.</p></section>
{secs}
<div class="foot"><p><b>Hours checked November 2026 — see official sites for the latest.</b></p>
<p>Official sites: {offi}</p>
<p>Photos from Wikimedia Commons. {cred}.</p></div></div>
<script>
window.__PH={PHJ};
{PINZOOM}
var onPin=null;
document.querySelectorAll('#map .pin').forEach(function(a){{a.addEventListener('click',function(ev){{ev.preventDefault();if(onPin!==a){{if(onPin)onPin.classList.remove('on');onPin=a;a.classList.add('on');return}}var c=document.getElementById('m'+a.dataset.n);if(c){{c.scrollIntoView({{behavior:'smooth',block:'center'}});c.classList.remove('flash');void c.offsetWidth;c.classList.add('flash')}}if(onPin){{onPin.classList.remove('on');onPin=null}}}})}});
document.getElementById('map').addEventListener('click',function(ev){{if(!ev.target.closest('.pin')&&onPin){{onPin.classList.remove('on');onPin=null}}}});
document.addEventListener("click",function(e){{
  var a=e.target.closest(".num");
  if(a){{e.preventDefault();document.getElementById("map").scrollIntoView({{behavior:"smooth",block:"center"}});var rb=document.querySelector('.mz [data-z="reset"]');if(rb&&!rb.hidden)rb.click();document.querySelectorAll('#map .pin.on').forEach(function(p){{p.classList.remove('on')}});var pin=document.querySelector('#map .pin[data-n="'+a.dataset.n+'"]');if(pin){{pin.classList.add('on');onPin=pin}}return}}
}});
</script>
</body></html>'''
open(os.path.join(here, "index.html"), "w").write(html)
print("built", len(html))
