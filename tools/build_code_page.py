"""Builds site/member-billing/code/index.html from the real source files and the latest test run."""
import html, re
SRC = "/home/user/finances/member-billing/"
FILES = [("Code.gs", "The Apps Script: a Front desk menu and the 8am fix list email."),
         ("build.py", "Builds the sheet: fake members and payments, the planted mistakes, and every formula."),
         ("test_tracker.py", "Checks the results against the planted mistakes, a separate copy of the rules, and the same-name tests."),
         ("test_script.js", "Tests the Apps Script with stand-ins for Google."),
         ("test-results.txt", "The latest test run: LibreOffice, Google Sheets and the Apps Script.")]
shell = open("/home/user/finances/site/inboxowner/code/index.html").read()
head = shell.split("<body>")[0]
head = re.sub(r"<title>.*?</title>", "<title>Member Billing Tracker: the code</title>", head)
head = re.sub(r'<meta name="description"[^>]*>', '<meta name="description" content="Source code and test results for the Member Billing Tracker.">', head)
nav = re.search(r'<nav class="site".*?</nav>', shell, flags=re.S).group(0)
out = [head, "<body>\n<div class=\"page\">", nav,
       '<h1>Member Billing Tracker: the code</h1><p><a href="../">Back to the project</a></p>',
       "<p>Written with Claude Code to my rules. I directed and checked it; I didn't write it. All data is fake.</p><ul>"]
out += [f'<li><a href="#f{i}">{f}</a>: {d}</li>' for i, (f, d) in enumerate(FILES)] + ["</ul>"]
out += [f'<h2 id="f{i}">{f}</h2><p class="muted">{d}</p><pre><code>{html.escape(open(SRC + f).read())}</code></pre>'
        for i, (f, d) in enumerate(FILES)]
out.append(shell[shell.index("<footer>"):])
open("/home/user/finances/site/member-billing/code/index.html", "w").write("\n".join(out))
print("built member-billing code page")
