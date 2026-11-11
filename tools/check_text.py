"""Checks the visible text on the main pages: words, banned words, long sentences, reading level, em dashes."""
import re, html, sys
ROOT = "/home/user/finances/site/"
PAGES = ["index.html", "inboxowner/index.html", "member-billing/index.html", "inboxowner/demo/index.html", "order-to-cash/index.html"]
BANNED = ["system", "optimiz", "efficien", "workflow", "reconcil", "validat", "flag", "escalat", "digest",
          "threshold", "automat", "leverag", "robust", "streamlin", "data-driven"]
GIVEN = ("These are small projects I built by combining my personal experience", "I've since reworked this project")  # lines Tyler gave word for word

def visible(src):
    s = re.sub(r"<(head|nav|footer|svg|script)[^>]*>.*?</\1>", " ", src, flags=re.S)
    det = " ".join(re.findall(r"<details>(.*?)</details>", s, flags=re.S))
    s = re.sub(r"<details>.*?</details>", " ", s, flags=re.S)
    t = lambda x: re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x))).strip()
    return t(s), t(det)

def blocks(src):
    s = re.sub(r"<(head|nav|svg|script)[^>]*>.*?</\1>", " ", src, flags=re.S)
    return [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", b))).strip()
            for b in re.findall(r"<(?:p|li|span class=\"flow-label\"|figcaption)[^>]*>(.*?)</(?:p|li|span|figcaption)>", s, flags=re.S)]

def syllables(w):
    w = w.lower().strip(".,!?\"'():;")
    if not w: return 0
    if re.fullmatch(r"[\d.%,/]+", w): return 1
    v = re.findall(r"[aeiouy]+", w); n = len(v)
    if w.endswith("e") and n > 1 and not w.endswith("le"): n -= 1
    return max(1, n)

bad = 0
for p in PAGES:
    src = open(ROOT + p).read()
    vis, det = visible(src)
    print(f"\n== {p}: {len(vis.split())} visible words, {len(det.split())} in the collapsed section")
    low = (vis + " " + det).lower()
    hits = [b for b in BANNED if b in low]
    print("   banned words:", hits or "none"); bad += len(hits)
    print("   em dashes:", src.count("—")); bad += src.count("—")
    sents = []
    for b in blocks(src):
        sents += [x for x in re.split(r"(?<=[.!?])[\"\u201d]?\s+", b.replace('."', '. ').replace(".\u201d", ". ")) if len(x.split()) > 2]
    long = [x for x in sents if len(x.split()) > 15 and not x.startswith(GIVEN)]
    for x in long: print(f"   LONG ({len(x.split())} words): {x}")
    bad += len(long)
    words = [w for x in sents for w in x.split()]
    if sents:
        grade = 0.39 * len(words) / len(sents) + 11.8 * sum(map(syllables, words)) / len(words) - 15.59
        print(f"   reading level (Flesch-Kincaid grade): {grade:.1f} over {len(sents)} sentences")
print("\nRESULT:", "clean" if not bad else f"{bad} problems")
