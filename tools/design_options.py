"""Five homepage design options, same content, to compare side by side.
Option A is the current site. This script builds B, C, D and E into designs/.
Run: python3 tools/design_options.py
"""
import os
OUT = "/home/user/finances/designs/"
os.makedirs(OUT, exist_ok=True)

ROLE = "Project Management student at Boise State, living in Mukilteo. I'm looking for operations, coordinator or front office roles in Seattle."
HEAD = "I learn how things work, then make them easier to get right."
PROJECTS = [
    ("InboxOwner", "Shows who owns each email in a shared inbox, and who is still waiting.", "18.7 hrs", "cancel emails waited"),
    ("Member Billing Tracker", "Catches billing mistakes and makes a daily fix list for the front desk.", "15 of 15", "mistakes caught"),
    ("This site", "My portfolio, rebuilt until a recruiter could read it on a phone.", "1,349 → 268", "words on one page"),
]
PASEO = ["All department emails came through the front desk, which got messy.",
         "I once charged the wrong member. Two members had the exact same name.",
         "I learned how everything worked first, then shared ideas with my manager. I later moved into membership."]
STEPS = [("Spot it", "A real problem from work"), ("Write the rules", "What counts as a mistake"),
         ("Direct the build", "Claude Code writes the code"), ("Test it", "On new cases, then fix")]
JOBS = [("Outback Steakhouse", "Dec 2025 – Jun 2026", "Busser, promoted to food runner within six months."),
        ("The Paseo Club", "Dec 2024 – Oct 2025", "Front Desk, then Membership Advisor."),
        ("Cooksey's Lifeguard & Swim Academy", "Mar 2023 – Mar 2024", "Lifeguard and swim instructor."),
        ("Boise State University", "Expected Spring 2028", "B.S. in Project Management.")]
EMAIL = "itstylerbunn@gmail.com"
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@500;600;700&display=swap">'

def doc(name, title, css, body):
    open(OUT + name, "w").write(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>{FONTS}
<style>*{{box-sizing:border-box;margin:0}}img{{max-width:100%}}a{{color:inherit}}ul,ol{{list-style:none;padding:0}}{css}</style></head><body>{body}</body></html>""")

# ------------------------------------------------------------------ B. Editorial light
b_css = """
body{background:#f6f7f9;color:#0b1220;font:17px/1.55 Inter,system-ui,sans-serif}
.wrap{max-width:1040px;margin:0 auto;padding:0 20px 80px}
.top{display:flex;justify-content:space-between;align-items:center;padding:22px 0;border-bottom:1px solid #0b122022;font-size:.92rem}
.top b{font-family:'Space Grotesk';font-size:1.05rem}.top nav{display:flex;gap:22px;color:#4a5568}
.kick{font:500 .76rem 'JetBrains Mono';letter-spacing:.1em;text-transform:uppercase;color:#1d4ed8;margin:56px 0 18px;display:flex;gap:10px;align-items:center}
.kick i{width:9px;height:9px;border-radius:50%;background:#16a34a;display:inline-block}
h1{font:700 clamp(2.3rem,7.2vw,4.7rem)/1.02 'Space Grotesk';letter-spacing:-.035em;max-width:15ch}
.who{display:flex;gap:18px;align-items:center;margin-top:30px;max-width:560px;color:#3b4658}
.who img{width:64px;height:64px;border-radius:50%;object-fit:cover;flex:none}
h2{font:500 .76rem 'JetBrains Mono';letter-spacing:.12em;text-transform:uppercase;color:#4a5568;margin:72px 0 6px}
.index li{border-top:1px solid #0b122022}.index li:last-child{border-bottom:1px solid #0b122022}
.index a{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;padding:22px 0;text-decoration:none}
.index .n{font:500 .8rem 'JetBrains Mono';color:#1d4ed8;padding-top:9px}
.index h3{font:700 1.6rem/1.15 'Space Grotesk';letter-spacing:-.02em}.index p{color:#4a5568;margin-top:4px}
.index .st{grid-column:2;margin-top:8px;font:500 .82rem 'JetBrains Mono';color:#4a5568}.index .st b{font:700 1.5rem 'Space Grotesk';color:#0b1220;margin-right:8px}
.two{display:grid;gap:0 60px}.plain li{padding:14px 0;border-top:1px solid #0b122022}.plain li:first-child{border-top:0}
.plain small{display:block;font:500 .74rem 'JetBrains Mono';letter-spacing:.06em;color:#1d4ed8;margin:2px 0}
.mail{font:700 clamp(1.5rem,5.4vw,3rem) 'Space Grotesk';letter-spacing:-.03em;text-decoration:underline;text-decoration-color:#1d4ed8;text-underline-offset:8px;word-break:break-all}
@media(min-width:760px){.index a{grid-template-columns:60px 1fr 260px;align-items:center}.index .st{grid-column:3;margin:0;text-align:right}.index .st b{display:block;margin:0;font-size:2rem}.two{grid-template-columns:1fr 1fr}}
"""
b_body = f"""<div class="wrap"><header class="top"><b>Tyler Bunn</b><nav><span>Projects</span><span>Work</span><span>Contact</span></nav></header>
<p class="kick"><i></i>Available now · Seattle area</p><h1>{HEAD}</h1>
<div class="who"><img src="../site/me.jpg" alt=""><p>{ROLE}</p></div>
<h2>Projects</h2><ol class="index">{"".join(f'<li><a href="#"><span class="n">0{i+1}</span><div><h3>{n}</h3><p>{d}</p></div><div class="st"><b>{s}</b>{l}</div></a></li>' for i,(n,d,s,l) in enumerate(PROJECTS))}</ol>
<div class="two"><div><h2>At The Paseo Club</h2><ul class="plain">{"".join(f"<li>{x}</li>" for x in PASEO)}</ul></div>
<div><h2>Experience and school</h2><ul class="plain">{"".join(f"<li><b>{n}</b><small>{w}</small>{d}</li>" for n,w,d in JOBS)}</ul></div></div>
<h2>Contact</h2><a class="mail" href="#">{EMAIL}</a></div>"""
doc("b-editorial.html", "B. Editorial light", b_css, b_body)

# ------------------------------------------------------------------ C. Bento
c_css = """
body{background:#0d0e11;color:#f1f2f4;font:16px/1.5 Inter,system-ui,sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:18px 16px 60px}
.grid{display:grid;gap:12px}.t{background:#17191e;border-radius:22px;padding:22px;border:1px solid #23262d}
.lab{font:500 .7rem 'JetBrains Mono';letter-spacing:.12em;text-transform:uppercase;color:#8b93a1;margin-bottom:10px}
.hero{background:linear-gradient(135deg,#1b1e25,#15171c)}.hero img{width:72px;height:72px;border-radius:20px;object-fit:cover;margin-bottom:16px}
.hero h1{font:700 clamp(2rem,6vw,3.2rem)/1.05 'Space Grotesk';letter-spacing:-.03em}.hero p{color:#aab1bd;margin-top:12px;max-width:46ch}
.status{background:#12241b;border-color:#1f4a35;display:flex;flex-direction:column;justify-content:space-between;gap:18px}
.status b{font:700 1.5rem 'Space Grotesk';color:#7ee2a8;display:flex;align-items:center;gap:10px}.status b i{width:11px;height:11px;border-radius:50%;background:#34d399;box-shadow:0 0 0 5px #34d39933}
.p{display:flex;flex-direction:column;gap:6px;text-decoration:none;min-height:200px}.p h3{font:600 1.05rem 'Space Grotesk'}.p p{color:#aab1bd;font-size:.9rem}
.p .big{font:700 clamp(2rem,6vw,2.7rem)/1 'Space Grotesk';letter-spacing:-.03em;margin-top:auto;padding-top:18px}.p small{color:#8b93a1;font:500 .72rem 'JetBrains Mono';letter-spacing:.06em}
.p1{background:#14222b;border-color:#1e3d4d}.p1 .big{color:#6fd3f5}.p2{background:#1c1a2e;border-color:#322e55}.p2 .big{color:#a9a2ff}.p3{background:#2a2014;border-color:#4b3820}.p3 .big{color:#ffc46b}
.t li{padding:9px 0;border-top:1px solid #23262d;font-size:.94rem}.t li:first-child{border-top:0;padding-top:0}.t li small{display:block;color:#8b93a1;font:500 .7rem 'JetBrains Mono';margin-top:2px}
.steps{display:grid;grid-template-columns:1fr 1fr;gap:10px}.steps div{background:#0f1114;border-radius:14px;padding:12px}.steps b{display:block;font-size:.92rem}.steps span{color:#8b93a1;font-size:.8rem}
.contact{background:#f1f2f4;color:#0d0e11;display:flex;flex-direction:column;justify-content:space-between;gap:18px}.contact .lab{color:#5c6470}.contact b{font:700 1.25rem 'Space Grotesk';word-break:break-all}
@media(min-width:820px){.grid{grid-template-columns:repeat(6,1fr)}.hero{grid-column:span 4}.status{grid-column:span 2}.p{grid-column:span 2}.s3{grid-column:span 3}.s4{grid-column:span 4}.s2{grid-column:span 2}}
"""
c_body = f"""<div class="wrap"><div class="grid">
<div class="t hero"><img src="../site/me.jpg" alt=""><h1>Tyler Bunn</h1><p>{ROLE}</p></div>
<div class="t status"><p class="lab">Status</p><b><i></i>Available now</b><p style="color:#9fd9b8">Mukilteo, WA. In Seattle on short notice.</p></div>
{"".join(f'<a class="t p p{i+1}" href="#"><p class="lab">Project {i+1}</p><h3>{n}</h3><p>{d}</p><div class="big">{s}</div><small>{l}</small></a>' for i,(n,d,s,l) in enumerate(PROJECTS))}
<div class="t s3"><p class="lab">At The Paseo Club</p><ul>{"".join(f"<li>{x}</li>" for x in PASEO)}</ul></div>
<div class="t s3"><p class="lab">How I work</p><div class="steps">{"".join(f"<div><b>{a}</b><span>{b}</span></div>" for a,b in STEPS)}</div></div>
<div class="t s4"><p class="lab">Experience and school</p><ul>{"".join(f"<li><b>{n}</b> · {d}<small>{w}</small></li>" for n,w,d in JOBS)}</ul></div>
<div class="t contact s2"><p class="lab">Contact</p><b>{EMAIL}</b><span>linkedin.com/in/tdbunn</span></div>
</div></div>"""
doc("c-bento.html", "C. Bento", c_css, c_body)

# ------------------------------------------------------------------ D. Blueprint
d_css = """
body{color:#eaf2ff;font:16px/1.55 Inter,system-ui,sans-serif;background-color:#0f3d82;
background-image:linear-gradient(#ffffff14 1px,transparent 1px),linear-gradient(90deg,#ffffff14 1px,transparent 1px),linear-gradient(#ffffff26 1px,transparent 1px),linear-gradient(90deg,#ffffff26 1px,transparent 1px);
background-size:20px 20px,20px 20px,100px 100px,100px 100px}
.wrap{max-width:1000px;margin:0 auto;padding:20px 16px 70px}.m{font-family:'JetBrains Mono',monospace;letter-spacing:.08em;text-transform:uppercase;font-size:.7rem;color:#b9d2ff}
.sheet{border:2px solid #eaf2ff;background:#0f3d82e6}
.title{display:grid;border-bottom:2px solid #eaf2ff}.title>div{padding:14px 16px;border-top:1px solid #eaf2ff66}.title>div:first-child{border-top:0}
.title h1{font:700 clamp(2rem,7vw,3.4rem)/1 'Space Grotesk';letter-spacing:-.02em;margin-top:6px}.title b{font:600 1rem 'Space Grotesk';display:block;margin-top:4px}
.title .ok{color:#ffe066}
.pad{padding:18px 16px}.role{max-width:60ch;font-size:1.05rem}
.figs{display:grid;gap:14px;margin-top:22px}.fig{border:1.5px solid #eaf2ff;padding:16px;text-decoration:none;display:block;position:relative}
.fig h3{font:700 1.25rem 'Space Grotesk';margin:6px 0 4px}.fig p{color:#cfe0ff;font-size:.92rem}
.dim{margin-top:16px;display:flex;align-items:center;gap:10px}.dim::before,.dim::after{content:"";flex:1;height:1.5px;background:#ffe066}.dim b{font:700 1.5rem 'JetBrains Mono';color:#ffe066;white-space:nowrap}
.fig small{display:block;text-align:center;margin-top:4px}
.cols{display:grid;gap:22px;margin-top:26px}.cols li{padding:9px 0;border-top:1px dashed #eaf2ff66;font-size:.94rem}.cols li:first-child{border-top:0}.cols h2{margin-bottom:8px}
.foot{border-top:2px solid #eaf2ff;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;padding:12px 16px}.foot b{font:600 1rem 'JetBrains Mono';color:#ffe066;word-break:break-all}
@media(min-width:800px){.title{grid-template-columns:2fr 1fr 1fr 1fr}.title>div{border-top:0;border-left:1px solid #eaf2ff66}.title>div:first-child{border-left:0}.figs{grid-template-columns:repeat(3,1fr)}.cols{grid-template-columns:1fr 1fr}}
"""
d_body = f"""<div class="wrap"><div class="sheet">
<div class="title"><div><span class="m">Name</span><h1>Tyler Bunn</h1></div><div><span class="m">Field</span><b>Project Management, Boise State</b></div>
<div><span class="m">Location</span><b>Mukilteo, WA</b></div><div><span class="m">Status</span><b class="ok">● Available now</b></div></div>
<div class="pad"><span class="m">Summary</span><p class="role">{ROLE}</p>
<div class="figs">{"".join(f'<a class="fig" href="#"><span class="m">Fig. {i+1}</span><h3>{n}</h3><p>{d}</p><div class="dim"><b>{s}</b></div><small class="m">{l}</small></a>' for i,(n,d,s,l) in enumerate(PROJECTS))}</div>
<div class="cols"><div><h2 class="m">Notes · At The Paseo Club</h2><ul>{"".join(f"<li>{x}</li>" for x in PASEO)}</ul></div>
<div><h2 class="m">Revisions · Experience and school</h2><ul>{"".join(f'<li><b>{n}</b> <span class="m">{w}</span><br>{d}</li>' for n,w,d in JOBS)}</ul></div></div></div>
<div class="foot"><span class="m">Contact</span><b>{EMAIL}</b><span class="m">Sheet 1 of 4</span></div></div></div>"""
doc("d-blueprint.html", "D. Blueprint", d_css, d_body)

# ------------------------------------------------------------------ E. Type-only minimal dark
e_css = """
body{background:#08090b;color:#f3f4f6;font:17px/1.6 Inter,system-ui,sans-serif}
.wrap{max-width:980px;margin:0 auto;padding:0 20px 90px}
.top{display:flex;justify-content:space-between;padding:24px 0;font:500 .78rem 'JetBrains Mono';letter-spacing:.1em;text-transform:uppercase;color:#8d94a0}
.top span:first-child{color:#f3f4f6}
h1{font:800 clamp(3rem,13vw,7.5rem)/.95 Inter;letter-spacing:-.055em;margin:48px 0 26px}
.role{font-size:1.2rem;color:#b6bcc6;max-width:34ch}.av{display:inline-flex;align-items:center;gap:10px;margin-top:22px;font:500 .8rem 'JetBrains Mono';letter-spacing:.08em;text-transform:uppercase;color:#7ee2a8}
.av i{width:9px;height:9px;border-radius:50%;background:#34d399}
.row{display:grid;gap:8px 30px;border-top:1px solid #23262c;padding:34px 0;margin-top:0}.sec{margin-top:70px}
.row>h2{font:500 .76rem 'JetBrains Mono';letter-spacing:.12em;text-transform:uppercase;color:#8d94a0;padding-top:6px}
.proj a{display:grid;grid-template-columns:1fr auto;gap:2px 20px;align-items:baseline;padding:16px 0;border-top:1px solid #23262c;text-decoration:none}
.proj a:first-child{border-top:0;padding-top:0}.proj h3{font:700 1.45rem/1.2 Inter;letter-spacing:-.02em}
.proj b{font:700 1.3rem 'JetBrains Mono';color:#7fe7f5;white-space:nowrap;text-align:right}.proj p{color:#8d94a0;font-size:.95rem}.proj small{color:#8d94a0;font:500 .7rem 'JetBrains Mono';text-align:right}
.txt li{padding:8px 0;color:#d5d9e0}.txt small{color:#8d94a0;font:500 .74rem 'JetBrains Mono';margin-left:8px}
.mail{font:700 clamp(1.3rem,5vw,2.2rem) Inter;letter-spacing:-.02em;text-decoration:underline;text-decoration-color:#7fe7f5;text-underline-offset:8px;word-break:break-all}
@media(min-width:760px){.row{grid-template-columns:200px 1fr}}
"""
e_body = f"""<div class="wrap"><div class="top"><span>Tyler Bunn</span><span>Projects · Work · Contact</span></div>
<h1>Tyler Bunn</h1><p class="role">{ROLE}</p><p class="av"><i></i>Available now</p>
<div class="sec"><div class="row"><h2>Projects</h2><div class="proj">{"".join(f'<a href="#"><h3>{n}</h3><b>{s}</b><p>{d}</p><small>{l}</small></a>' for n,d,s,l in PROJECTS)}</div></div>
<div class="row"><h2>At The Paseo Club</h2><ul class="txt">{"".join(f"<li>{x}</li>" for x in PASEO)}</ul></div>
<div class="row"><h2>Experience and school</h2><ul class="txt">{"".join(f"<li><b>{n}</b><small>{w}</small><br>{d}</li>" for n,w,d in JOBS)}</ul></div>
<div class="row"><h2>Contact</h2><a class="mail" href="#">{EMAIL}</a></div></div></div>"""
doc("e-minimal.html", "E. Type-only minimal", e_css, e_body)
print("built 4 option pages in designs/")
