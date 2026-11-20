#!/usr/bin/env python3
# 実行: python3 build.py → index.html を作り直す（型は akiba-anime-day-kids のユリア式）
import json, os
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
OG = os.environ.get("OG", "1")

esc = lambda s: s.replace("&", "&amp;")
clock = '<svg viewBox="0 0 16 16" width="12" height="12" aria-hidden="true"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 4.5V8l2.5 1.8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>'

def tile(m):
    img, tag, name, hrs, res, q, _ = m
    href = "https://www.google.com/maps/search/?api=1&amp;query=" + q.replace(" ", "+")
    h, d = hrs.split(" · ")
    chips = ('<span class="chip r">Reservation only</span>' if res else "") + f'<span class="chip">{clock}<span>{h} ·</span><span>{d}</span></span>'
    return (f'<a class="tile" href="{href}" target="_blank" rel="noopener" aria-label="{esc(name)} on Google Maps">'
            f'<span class="ph"><img src="img/{img}" alt="" loading="lazy"><span class="tt">{esc(tag)}</span></span>'
            f'<span class="tn">{esc(name)}</span><span class="chips">{chips}</span></a>')

secs = "".join(f'<section><h2 class="bar">{esc(t)}</h2><div class="wall">' + "".join(tile(m) for m in ms) + "</div></section>" for t, ms in S)
points = "".join(f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in POINTS)
hero = "".join(f'<img src="img/{f}" alt="">' for f in HERO)
allm = [m for _, ms in S for m in ms]
names = {m[0]: m[2] for m in allm}
cred = "; ".join(f'{names[f]}: <a href="{c["url"]}">{c["author"]}</a> ({c["license"]})' for f, c in C.items() if f in names)
offi = " · ".join(f'<a href="{m[6]}">{esc(m[2])}</a>' for m in allm)
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
.foot{{margin-top:44px;padding:20px 0 44px;border-top:4px solid var(--ink);font-size:13px;color:var(--mu)}}.foot p{{margin:0 0 10px}}.foot b{{color:var(--ink)}}
@media(max-width:699px){{.tile:last-child:nth-child(odd){{grid-column:1/-1}}.tile:last-child:nth-child(odd) .ph{{aspect-ratio:2.4/1}}}}
@media(min-width:700px){{.wall{{grid-template-columns:repeat(3,minmax(0,1fr))}}}}
</style></head><body>
<div class="col"><div class="top"><span>GUEST GUIDE</span><span>LATE MAY 2027</span></div>
<h1>Tokyo Museums for Robert</h1>
<p class="sub">10 days in Tokyo around the Ave Mujica shows — late May 2027</p>
<div class="hero">{hero}</div>
<div class="hb"><span>{len(allm)} museums</span><b>Tap for the map</b></div>
<dl class="pts">{points}</dl>
{secs}
<div class="foot"><p><b>Hours checked November 2026 — see official sites for the latest.</b></p>
<p>Official sites: {offi}</p>
<p>Photos from Wikimedia Commons. {cred}.</p></div></div>
</body></html>'''
open(os.path.join(here, "index.html"), "w").write(html)
print("built", len(html))
