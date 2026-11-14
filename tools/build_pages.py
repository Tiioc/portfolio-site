"""Builds the portfolio's main pages (homepage, both project pages, the demo shell)
from one template, so the icons, nav and footer stay the same everywhere.
Run: python3 tools/build_pages.py
"""
ROOT = "/home/user/finances/site/"

ICONS = {
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "user": '<circle cx="12" cy="8" r="4"/><path d="M4 21v-1a6 6 0 0 1 6-6h4a6 6 0 0 1 6 6v1"/>',
    "users": '<circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><circle cx="17" cy="8" r="3"/><path d="M17 14a5 5 0 0 1 5 5"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "tag": '<path d="M20.59 13.41 13.42 20.58a2 2 0 0 1-2.83 0L2 12V2h10l8.59 8.59a2 2 0 0 1 0 2.82z"/><circle cx="7" cy="7" r="1.5"/>',
    "card": '<rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/><path d="M6 15h4"/>',
    "alert": '<path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    "check": '<path d="M20 6 9 17l-5-5"/>',
    "list": '<path d="M9 6h11M9 12h11M9 18h11"/><path d="m3 6 1 1 2-2M3 12l1 1 2-2M3 18l1 1 2-2"/>',
    "id": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M15 9h3M15 13h3M6 16h6"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
    "sheet": '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "play": '<path d="M7 4v16l13-8z"/>',
    "code": '<path d="m16 18 6-6-6-6M8 6l-6 6 6 6"/>',
    "up": '<path d="M7 17 17 7M8 7h9v9"/>',
    "school": '<path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2 9 2 12 0v-5"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v2"/>',
    "eye": '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    "pen": '<path d="M12 20h9"/><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4z"/>',
    "home": '<path d="M3 11 12 3l9 8"/><path d="M5 10v10h14V10"/>',
    "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20a15 15 0 0 1 0-20z"/>',
    "phone": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M11 18h2"/>',
    "scissors": '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.1 15.9M14.5 14.5 20 20M8.1 8.1 12 12"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
    for k, v in ICONS.items()) + "</svg>"
ic = lambda name, cls="": f'<svg class="icon {cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'

SITE = "https://tylerbunn.netlify.app/"
WORDS_BEFORE = 1349  # the first InboxOwner page: 1,002 words showing + 347 in its collapsed section
def page(path, title, desc, body, depth, current=None, script="", og="general", absolute=False, theme="home"):
    up = "/" if absolute else "../" * depth
    built = "<p>Built in plain HTML and CSS with Claude Code, which I directed and fact-checked.</p>" if theme in ("home", "site") else ""
    url = SITE + path.replace("index.html", "")
    cur = ' aria-current="page"'
    nav = "".join(f'<a href="{up}#{k}"{cur if k == current else ""}>{v}</a>'
                  for k, v in [("projects", "Projects"), ("experience", "Experience"), ("contact", "Contact")])
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="Tyler Bunn">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}og/{og}.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="627">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&amp;family=JetBrains+Mono:wght@400;500;700&amp;display=swap">
<link rel="stylesheet" href="{up}style.css">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Crect width='32' height='32' rx='8' fill='%237c3aed'/%3E%3Ctext x='16' y='21' font-family='Arial' font-weight='700' font-size='14' fill='white' text-anchor='middle'%3ETB%3C/text%3E%3C/svg%3E">
{script}</head>
<body class="t-{theme}">
{SPRITE}
<div class="page">
<nav class="site" aria-label="Site"><a class="brand" href="{up}">Tyler Bunn</a><span class="nav-links">{nav}</span></nav>
{body}
<footer>
{built}
<p><a href="mailto:itstylerbunn@gmail.com">itstylerbunn@gmail.com</a> · <a href="https://www.linkedin.com/in/tdbunn">linkedin.com/in/tdbunn</a></p>
</footer>
</div>
</body>
</html>
"""
    open(ROOT + path, "w").write(html)

def flow(items, small=False):
    """Problem -> Tool -> Result picture."""
    cells = []
    for i, (icon, label, tone) in enumerate(items):
        cells.append(f'<div class="flow-step {tone}"><span class="flow-icon">{ic(icon)}</span><span class="flow-label">{label}</span></div>')
        if i < len(items) - 1:
            cells.append(f'<span class="flow-arrow" aria-hidden="true">{ic("arrow")}</span>')
    kind = ["Problem", "Tool", "Result"]
    aria = ". ".join(f"{kind[i]}: {lab}" for i, (_, lab, _) in enumerate(items))
    return f'<div class="flow{" small" if small else ""}" role="img" aria-label="{aria}">{"".join(cells)}</div>'

def steps(items):
    return '<ol class="how">' + "".join(
        f'<li class="{tone}"><span class="how-icon">{ic(icon)}</span><div><strong>{t}</strong><span>{d}</span></div></li>'
        for icon, t, d, tone in items) + "</ol>"

def gfx(kind):
    """One small decorative banner per project page, so the pages don't all look alike."""
    if kind == "radar":   # InboxOwner: a radar finding waiting emails
        body = ('<g class="g-rings"><circle cx="226" cy="60" r="18"/><circle cx="226" cy="60" r="36"/><circle cx="226" cy="60" r="54"/>'
                '<path d="M172 60h108M226 6v108"/></g>'
                '<g class="g-sweep"><path d="M226 60 L226 6 A54 54 0 0 1 272.8 33 Z"/></g>'
                '<circle class="g-blip late" cx="248" cy="38" r="4.5"/><circle class="g-blip late b2" cx="200" cy="82" r="4.5"/><circle class="g-blip ok" cx="240" cy="78" r="4.5"/>'
                '<g class="g-mail"><rect x="20" y="50" width="26" height="18" rx="3"/><path d="m20 53 13 9 13-9"/><rect x="74" y="50" width="26" height="18" rx="3"/><path d="m74 53 13 9 13-9"/>'
                '<path class="g-dash" d="M108 59h52"/></g>')
    elif kind == "twins":  # Member Billing: same name, different IDs
        def person(x, tag):
            return (f'<g class="g-person"><circle cx="{x}" cy="34" r="12"/><path d="M{x-20} 74a20 20 0 0 1 40 0"/></g>'
                    f'<rect class="g-tag" x="{x-27}" y="84" width="54" height="20" rx="5"/><text class="g-id" x="{x}" y="98" text-anchor="middle">{tag}</text>')
        body = (person(176, "M-1012") + person(256, "M-1031") + '<text class="g-neq" x="216" y="52" text-anchor="middle">≠</text>'
                '<g class="g-grid">' + "".join(f'<circle cx="{24 + c * 18}" cy="{36 + r * 18}" r="4"/>' for r in range(3) for c in range(5)) + '</g>')
    else:                  # This site: a page going online
        body = ('<g class="g-win"><rect x="22" y="22" width="110" height="78" rx="8"/><path d="M22 40h110"/></g>'
                '<g class="g-windots"><circle cx="34" cy="31" r="2.5"/><circle cx="43" cy="31" r="2.5"/><circle cx="52" cy="31" r="2.5"/></g>'
                '<g class="g-long"><rect x="34" y="52" width="60" height="6" rx="3"/><rect x="34" y="66" width="84" height="6" rx="3"/><rect x="34" y="80" width="46" height="6" rx="3"/></g>'
                '<path class="g-arrow" d="M148 60h34m-10-9 10 9-10 9"/>'
                '<g class="g-globe"><circle cx="238" cy="60" r="34"/><path d="M204 60h68M238 26c-18 18-18 50 0 68M238 26c18 18 18 50 0 68"/></g>'
                '<circle class="g-live" cx="262" cy="36" r="6"/>')
    return f'<svg class="gfx gfx-{kind}" viewBox="0 0 300 120" aria-hidden="true" focusable="false">{body}</svg>'

def orbit():
    """Decorative hero graphic: three tilted orbits with slow-moving dots. Pure SVG + CSS."""
    rings = "".join(
        f'<g class="orbit-spin s{i}"><circle r="{r}" fill="none" class="ring"/><circle cx="{r}" r="{d}" class="sat {tone}"/></g>'
        for i, (r, d, tone) in enumerate([(70, 6, "c1"), (115, 8, "c2"), (165, 6, "c3")]))
    return ('<svg class="orbit" viewBox="-190 -190 380 380" aria-hidden="true" focusable="false">'
            '<defs><radialGradient id="core" cx="35%" cy="35%"><stop offset="0" stop-color="#7fe7f5"/><stop offset="1" stop-color="#6d7cff"/></radialGradient></defs>'
            f'<g transform="rotate(-24) scale(1 .42)">{rings}</g>'
            '<circle r="20" fill="url(#core)" class="core"/><circle r="34" fill="none" class="halo"/></svg>')

def process():
    """How both projects were made: four steps on one line."""
    items = [("eye", "Spot it", "A real problem from work"), ("pen", "Write the rules", "What counts as a mistake"),
             ("code", "Direct the build", "Claude Code writes the code"), ("check", "Test it", "On new cases, then fix")]
    cells = "".join(f'<li><span class="p-dot">{ic(icon)}</span><strong>{t}</strong><span>{d}</span></li>' for icon, t, d in items)
    return f'<ol class="process">{cells}</ol>'

def nextlink(href, label):
    return f'<a class="next" href="{href}"><span>Next project</span><strong>{label}</strong>{ic("arrow")}</a>'

# ---------------------------------------------------------------------------- homepage
home = f"""
<div class="mc">
<aside class="mc-side">
  {orbit()}
  <img class="avatar" src="me.jpg" width="72" height="72" alt="Tyler Bunn">
  <h1>Tyler Bunn</h1>
  <p class="role">I'm a Project Management student at Boise State. I worked a club front desk, then became a Membership Advisor. I want an operations, coordinator or front office role in Seattle.</p>
  <p class="status"><span class="live-dot" aria-hidden="true"></span>Available now</p>
  <p class="actions top-cta"><a class="btn" href="mailto:itstylerbunn@gmail.com">{ic("mail")}Email me</a></p>
  <nav class="mc-nav" aria-label="Sections">
    <a href="#projects"><i></i>Projects</a>
    <a href="#experience"><i></i>Experience</a>
    <a href="#work"><i></i>How I work</a>
    <a href="#contact"><i></i>Contact</a>
  </nav>
</aside>

<main class="mc-main">
<section id="projects" class="mc-sec">
  <h2 class="mc-label"><span>01</span>Projects</h2>
  <p class="intro">These are small projects I built by combining my personal experience, what I've learned in my classes, and real problems I ran into at work.</p>
  <a class="mrow teal" href="inboxowner/">
    <div><h3>InboxOwner {ic("arrow")}</h3><p>Every department's email came to my front desk. This tool gives each email an owner.</p></div>
    <div class="read"><b>87%</b><span>right on emails it sorted by itself</span></div>
  </a>
  <a class="mrow violet" href="member-billing/">
    <div><h3>Member Billing Tracker {ic("arrow")}</h3><p>Two members shared a name and I charged the wrong one. This sheet looks members up by ID.</p></div>
    <div class="read"><b>15 of 15</b><span>planted mistakes caught</span></div>
  </a>
  <a class="mrow amber minor" href="this-site/">
    <div><h3>This site {ic("arrow")}</h3><p>My portfolio. I planned it, directed the build and put it online.</p></div>
  </a>
  <p class="chart-note made">Both tools were tested on made-up data.</p>
</section>

<section id="experience" class="mc-sec">
  <h2 class="mc-label"><span>02</span>Experience and school</h2>
  <ul class="timeline plain">
    <li><div><strong>Outback Steakhouse</strong><span class="when">Dec 2025 – Jun 2026 · Santa Clarita, CA</span><span>Busser, promoted to food runner within six months.</span></div></li>
    <li><div><strong>The Paseo Club</strong><span class="when">Dec 2024 – Oct 2025 · Santa Clarita, CA</span><span>Front Desk, then Membership Advisor. Email routing, billing fixes and refunds in HubSpot.</span></div></li>
    <li><div><strong>Cooksey's Lifeguard &amp; Swim Academy</strong><span class="when">Mar 2023 – Mar 2024 · Santa Clarita, CA</span><span>Lifeguard and swim instructor. Often the only staff member on duty.</span></div></li>
    <li><div><strong>Boise State University</strong><span class="when">Expected Spring 2028</span><span>B.S. in Project Management.</span></div></li>
  </ul>
</section>

<section id="work" class="mc-sec">
  <h2 class="mc-label"><span>03</span>How I work</h2>
  <p>I learn how things work before I suggest changes.</p>
  {process()}
</section>

<section id="contact" class="mc-sec">
  <h2 class="mc-label"><span>04</span>Contact</h2>
  <p>I'm in Mukilteo and can be in Seattle for an interview on short notice.</p>
  <p class="actions"><a class="btn primary" href="mailto:itstylerbunn@gmail.com">{ic("mail")}Email me</a><a class="btn" href="https://www.linkedin.com/in/tdbunn">{ic("link")}LinkedIn</a></p>
</section>
</main>
</div>
<script>
(function () {{
  var links = document.querySelectorAll('.mc-nav a');
  if (!('IntersectionObserver' in window)) return;
  var io = new IntersectionObserver(function (es) {{
    es.forEach(function (e) {{ if (e.isIntersecting) links.forEach(function (a) {{ a.classList.toggle('on', a.getAttribute('href') === '#' + e.target.id); }}); }});
  }}, {{ rootMargin: '-30% 0px -60% 0px' }});
  document.querySelectorAll('.mc-sec').forEach(function (x) {{ io.observe(x); }});
}})();
</script>
"""

# ---------------------------------------------------------------------------- InboxOwner
def chart_waits():
    rows = [("Cancellation emails", 18.7, "pink"), ("Trial questions", 1.2, "teal")]
    bars = "".join(f'<div class="hbar {tone}"><span class="hbar-label">{lab}</span><span class="hbar-track"><span class="hbar-area"><span class="hbar-fill" style="width:{v / 18.7 * 100:.1f}%"></span></span><span class="hbar-value">{v} hrs</span></span></div>' for lab, v, tone in rows)
    return f'''<figure class="chart" aria-label="Typical wait for a first reply: cancellation emails 18.7 hours, trial questions 1.2 hours.">
  <figcaption>Wait for a first reply</figcaption>{bars}
  <p class="chart-note">Counts only hours the gym was open.</p></figure>'''

inbox = f"""
<header class="page-head teal">
  {gfx("radar")}
  <span class="pc-icon big">{ic("inbox")}</span>
  <h1>InboxOwner</h1>
  <p class="pc-tags">Tested on made-up data</p>
</header>

<section class="block"><h2><span class="num">1</span>The problem</h2>
<p>At The Paseo Club, every department's email came to the front desk. Nobody could tell who had answered what.</p></section>

<section class="block"><h2><span class="num">2</span>What I made</h2>
<p>A tool that gives every email an owner and shows who is still waiting. I set the rules and tested it. Claude Code wrote the code.</p>
<p class="actions"><a class="btn primary" href="demo/#owners">{ic("play")}Try the demo</a><a class="btn" href="code/">{ic("code")}See the code</a></p>
<p class="aside">A version for real Gmail exists, but no real team has used it yet.</p>
<figure class="peek teal" role="img" aria-label="A peek at the demo: three late emails, each with one owner.">
  <figcaption>A peek at the demo</figcaption>
  <div class="peek-row"><div><strong>Free trial?</strong><span>Mateo Fischer · Trial inquiries</span></div><span class="pill late">Late by 81 hrs</span><span class="own">Jordan</span></div>
  <div class="peek-row"><div><strong>Cancel membership</strong><span>Casey Haddad · Cancellations</span></div><span class="pill late">Late by 79 hrs</span><span class="own">Maya</span></div>
  <div class="peek-row"><div><strong>Hold request</strong><span>Avery Moreno · Membership freezes</span></div><span class="pill late">Late by 64 hrs</span><span class="own">Jordan</span></div>
  <p class="chart-note">Owners are the ones the demo suggests.</p>
</figure></section>

<section class="block"><h2><span class="num">3</span>How it works</h2>
{steps([("tag", "Sorts new mail", "Guesses the topic or asks a person.", "amber"),
        ("user", "Gives it an owner", "One person's name on each email.", "violet"),
        ("clock", "Times the wait", "How long each email waits.", "teal")])}</section>

<section class="block"><h2><span class="num">4</span>What it found</h2>
{chart_waits()}
<p>Cancellation emails waited far longer than trial questions. So the tool gives each one an owner and a deadline.</p></section>

<section class="block"><h2><span class="num">5</span>How I tested it</h2>
<p>My first rules only fit old emails. One even matched "lease" inside "please." So I tested on 96 new emails it had never seen. It got 87% right of the ones it sorted by itself.</p></section>

{nextlink("../member-billing/", "Member Billing Tracker")}

<details>
<summary>The fine print</summary>
<ul>
  <li>A made-up gym with four staff and 548 emails from 90 days.</li>
</ul>
</details>
"""
page("inboxowner/index.html", "InboxOwner, by Tyler Bunn", "A simple tool that shows who owns each email in a shared inbox. Tested on made-up data.", inbox, 1, og="inboxowner", theme="inbox")

# ---------------------------------------------------------------------------- Member Billing
def chart_billing():
    def row(label, cells, value, tone=""):
        dots = "".join(f'<span class="d {c}"></span>' for c in cells)
        return f'<div class="dots-row {tone}"><span class="dots-label">{label}</span><span class="dots">{dots}</span><span class="dots-value">{value}</span></div>'
    return f'''<figure class="chart" aria-label="15 mistakes I put in on purpose. Looking members up by ID: 15 caught, 0 mistakes. Looking them up by name: 2 wrong and 2 false alarms.">
  <figcaption>15 mistakes I put in on purpose</figcaption>
  {row("My sheet, by member ID", ["ok"] * 15, "15 caught")}
  {row("If it looked people up by name", ["ok"] * 13 + ["bad"] * 2 + ["bad extra"] * 2, "2 wrong, 2 false alarms", "worse")}
  <p class="legend"><span><i class="d ok"></i>Caught right</span><span><i class="d bad"></i>Wrong</span><span><i class="d bad extra"></i>False alarm</span></p>
  <p class="chart-note">A real Google Sheet you can open.</p></figure>'''

billing = f"""
<header class="page-head violet">
  {gfx("twins")}
  <span class="pc-icon big">{ic("card")}</span>
  <h1>Member Billing Tracker</h1>
  <p class="pc-tags">Tested on made-up data</p>
</header>

<section class="block"><h2><span class="num">1</span>The problem</h2>
<p>At The Paseo Club, I handled dues, refunds and failed payments. I once charged the wrong member because two members had the same name.</p></section>

<section class="block"><h2><span class="num">2</span>What I made</h2>
<p>A Google Sheet that catches billing mistakes and lists what to fix. I set the rules and tested it. Claude Code wrote the formulas and script.</p>
<p class="actions"><a class="btn primary" href="https://docs.google.com/spreadsheets/d/1F_MrU0XxCY8uG9Ryjuv_wpOlGj6v7UtjT_gvkpw3xWQ/edit">{ic("sheet")}Open the sheet</a><a class="btn" href="code/">{ic("code")}See the code</a></p>
<figure class="peek violet" role="img" aria-label="A peek at the fix list: four rows, each starting with what to do.">
  <figcaption>A peek at the fix list</figcaption>
  <div class="peek-row"><span class="act a-call">Call</span><div><strong>Mia Shaw <i>M-1013</i></strong><span>Member disputed this charge</span></div><span class="amt">$189</span></div>
  <div class="peek-row"><span class="act a-retry">Retry card</span><div><strong>Sam Jensen <i>M-1019</i></strong><span>Card declined, not retried</span></div><span class="amt">$95</span></div>
  <div class="peek-row"><span class="act a-refund">Refund</span><div><strong>Felix Reyes <i>M-1006</i></strong><span>Charged twice this month</span></div><span class="amt">$189</span></div>
  <div class="peek-row"><span class="act a-refund">Send refund</span><div><strong>Chris Morgan <i>M-1031</i></strong><span>Refund approved, never sent</span></div><span class="amt">$95</span></div>
  <p class="chart-note">4 of the 15 rows.</p>
</figure></section>

<section class="block"><h2><span class="num">3</span>How it works</h2>
{steps([("id", "Uses member IDs", "So two members with the same name stay separate.", "violet"),
        ("alert", "Catches mistakes", "Declined cards, double charges, unsent refunds.", "pink"),
        ("list", "Makes a fix list", "Who to call, refund or retry.", "teal")])}</section>

<section class="block"><h2><span class="num">4</span>What the test showed</h2>
{chart_billing()}
<p>Looking up by name got 2 wrong and raised 2 false alarms. I planted these mistakes, so this is an easy test. A wrong price would still get through.</p></section>

{nextlink("../this-site/", "This site")}

<details>
<summary>The fine print</summary>
<ul>
  <li>A made-up club with 36 members and 113 payments. I planted 15 mistakes.</li>
  <li>A short script can email the fix list at 8am. I haven't run it inside the sheet yet.</li>
</ul>
</details>
"""
page("member-billing/index.html", "Member Billing Tracker, by Tyler Bunn", "A Google Sheet that catches billing mistakes at a members' club and makes a fix list. Tested on made-up data.", billing, 1, og="member-billing", theme="billing")

# ---------------------------------------------------------------------------- demo shell
demo = f"""
<header class="page-head teal">
  <span class="pc-icon big">{ic("play")}</span>
  <h1>InboxOwner demo</h1>
</header>
<p>A made-up gym's shared inbox with four staff: Maya, Jordan, Priya and Sam. <a href="../">Back to the project</a></p>
<noscript><p><strong>This demo needs JavaScript to run.</strong> The project page works without it.</p></noscript>
<div class="tabs" id="demo-tabs" role="tablist">
  <button role="tab" data-tab="waits" aria-selected="true">Wait times</button>
  <button role="tab" data-tab="owners" aria-selected="false">Who owns what</button>
  <button role="tab" data-tab="sorting" aria-selected="false">Sorting</button>
</div>
<div id="p-waits" role="tabpanel"></div>
<div id="p-owners" role="tabpanel" hidden></div>
<div id="p-sorting" role="tabpanel" hidden></div>
"""
page("inboxowner/demo/index.html", "InboxOwner demo", "Live demo of InboxOwner on a made-up gym inbox.", demo, 2, og="inboxowner", theme="inbox",
     script='<script src="demo.js" defer></script>\n')

# ---------------------------------------------------------------------------- Order-to-Cash (retired; reached only from old links)
o2c = f"""
<section class="retired">
<header class="page-head blue">
  <span class="pc-icon big">{ic("sheet")}</span>
  <h1>Order-to-Cash Tracker (2026)</h1>
</header>
<p class="lead">I've since reworked this project into the Member Billing Tracker, which fits my front desk experience better.</p>
<p class="actions"><a class="btn primary" href="../member-billing/">{ic("card")}See the Member Billing Tracker</a></p>
<p class="small-link"><a href="original/">View the original version</a></p>
</section>
"""
page("order-to-cash/index.html", "Order-to-Cash Tracker, by Tyler Bunn", "An earlier project, since reworked into the Member Billing Tracker.", o2c, 1, theme="o2c")

# ---------------------------------------------------------------------------- This site (the third project)
import re as _re, html as _html
def count_words(path):
    src = open(ROOT + path).read()
    src = _re.sub(r"<(head|nav|footer|svg|script)[^>]*>.*?</\1>", " ", src, flags=_re.S)
    return len(_html.unescape(_re.sub(r"<[^>]+>", " ", src)).split())
NOW = count_words("inboxowner/index.html")

def readout():
    rows = [("Projects", "3"), ("Live demo", "1"), ("Shared sheet", "1"), ("Checks on the demo", "29")]
    body = "".join(f'<div class="hbar-row-plain"><span class="hbar-label">{k}</span><span class="hbar-value">{v}</span></div>' for k, v in rows)
    return f'''<figure class="chart readout" aria-label="What is online: 3 projects, 1 live demo, 1 shared sheet, 29 checks on the demo.">
{body}</figure>'''

thissite = f"""
<header class="page-head amber">
  {gfx("lines")}
  <span class="pc-icon big">{ic("globe")}</span>
  <h1>This site</h1>
  <p class="pc-tags">You're looking at it</p>
</header>

<section class="block"><h2><span class="num">1</span>The problem</h2>
<p>A resume can't show a working demo. I needed one place to show my projects.</p></section>

<section class="block"><h2><span class="num">2</span>What I made</h2>
<p>This site. I planned it and checked it. Claude Code wrote the code.</p></section>

<section class="block"><h2><span class="num">3</span>How I did it</h2>
{steps([("pen", "Planned it", "Who reads it, and what they need first.", "violet"),
        ("code", "Built it plain", "HTML and CSS. No frameworks.", "teal"),
        ("globe", "Put it online", "Hosted on Netlify. Tested on a phone.", "amber")])}</section>

<section class="block"><h2><span class="num">4</span>What I learned</h2>
<p>Check every number against its source before it goes online.</p></section>

{nextlink("../inboxowner/", "InboxOwner")}

"""
page("this-site/index.html", "This site, by Tyler Bunn", "How I planned my portfolio, directed the build and put it online.", thissite, 1, theme="site")
page("index.html", "Tyler Bunn", "Tyler Bunn, Project Management student at Boise State, looking for operations, coordinator and front office roles in Seattle. Available now.", home, 0, current="projects")

# ---------------------------------------------------------------------------- 404 (Netlify serves /404.html for any missing page)
lost = f"""
<section class="retired lost">
  {orbit()}
  <p class="hello">Error 404</p>
  <h1>This page isn't here.</h1>
  <p class="lead">The link may be old. Everything current is on the home page.</p>
  <p class="actions"><a class="btn primary" href="/">{ic("home")}Go to the home page</a></p>
</section>
"""
page("404.html", "Page not found · Tyler Bunn", "This page isn't here.", lost, 0, absolute=True)
print("built 7 pages; InboxOwner page is", NOW, "words")
