"""Member Billing Tracker: builds the workbook (fake data + formulas) and the answer key.

Every check is a visible spreadsheet formula. Every lookup uses the member ID, never the name.
Output: member-billing.xlsx (upload to Google Drive to convert it to a Google Sheet) and answer_key.json.
"""
import json, datetime as dt, random
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.datavalidation import DataValidation

random.seed(7)
D = dt.date
PLANS = {"Tennis": 189, "Social": 95, "Family": 260}
FIRST = ["Ava", "Ben", "Carla", "Dev", "Ella", "Felix", "Gina", "Hank", "Iris", "Jake", "Kira", "Leo", "Mia",
         "Nate", "Olive", "Paul", "Quinn", "Rosa", "Sam", "Tara", "Uma", "Vic", "Wes", "Xena", "Yara", "Zack",
         "Amir", "Bea", "Cole", "Dana", "Eli", "Faye", "Gus", "Hana", "Ivan", "Jules"]
LAST = ["Ortiz", "Nguyen", "Patel", "Brooks", "Kim", "Reyes", "Hale", "Moreno", "Sato", "Price", "Lund", "Vega",
        "Shaw", "Diaz", "Fox", "Grant", "Hayes", "Iqbal", "Jensen", "Klein", "Lowe", "Mendez", "Novak", "Olsen",
        "Park", "Quint", "Ruiz", "Stone", "Tran", "Udall", "Voss", "West", "Young", "Zane", "Abbott", "Banks"]

# ---- Members -------------------------------------------------------------------------------
members = []
cards = random.sample(range(1000, 9999), 36)
for i in range(36):
    mid = f"M-{1001 + i}"
    plan = random.choice(list(PLANS))
    members.append(dict(id=mid, name=f"{FIRST[i]} {LAST[i]}", plan=plan, dues=PLANS[plan],
                        card=f"Visa {cards[i]}", status="Active", since=D(2025, 1, 1),
                        phone=f"(661) 555-01{i:02d}"))
M = {m["id"]: m for m in members}
# Same-name pair: two different members, both named Chris Morgan.
M["M-1012"].update(name="Chris Morgan", plan="Tennis", dues=189)
M["M-1031"].update(name="Chris Morgan", plan="Social", dues=95, status="Paused", since=D(2026, 9, 20))
# Pauses and cancellations.
M["M-1015"].update(status="Paused", since=D(2026, 9, 15))
M["M-1030"].update(status="Cancelled", since=D(2026, 8, 20))
M["M-1033"].update(status="Paused", since=D(2026, 9, 10))   # clean case: no charge after the pause

# ---- Payments ------------------------------------------------------------------------------
pay = []
def add(date, mid, typ, amount, result="Paid", disputed="", card=None, note=""):
    pay.append(dict(date=date, mid=mid, type=typ, period=f"{date:%Y-%m}", amount=amount,
                    card=card or M[mid]["card"], result=result, disputed=disputed, note=note))

planted = []   # (member ID, period or None, kind) resolved to row IDs after sorting
failed_unretried = {("M-1004", 10), ("M-1011", 10), ("M-1019", 9), ("M-1027", 10)}
failed_retried = {("M-1008", 9, 4), ("M-1023", 10, 5)}     # clean cases: retried and paid
for month in (8, 9, 10):
    for m in members:
        mid = m["id"]
        if m["status"] != "Active" and D(2026, month, 1) >= m["since"]:
            # Correctly stopped billing, except the planted mistakes below.
            if not ((mid == "M-1015" and month == 10) or (mid == "M-1030" and month in (9, 10))
                    or (mid == "M-1031" and month == 10)):
                continue
        if mid == "M-1018" and month == 10:
            continue  # M-1018's October payment got posted to M-1017 (below)
        if (mid, month) in failed_unretried:
            add(D(2026, month, 1), mid, "Dues", m["dues"], result="Failed")
            continue
        r = [x for x in failed_retried if x[:2] == (mid, month)]
        if r:
            add(D(2026, month, 1), mid, "Dues", m["dues"], result="Failed")
            add(D(2026, month, r[0][2]), mid, "Dues", m["dues"], note="Retried")
            continue
        add(D(2026, month, 1), mid, "Dues", m["dues"])

add(D(2026, 9, 2), "M-1006", "Dues", M["M-1006"]["dues"])                 # duplicate
add(D(2026, 10, 2), "M-1021", "Dues", M["M-1021"]["dues"])                # duplicate
add(D(2026, 10, 3), "M-1017", "Dues", M["M-1018"]["dues"], card=M["M-1018"]["card"])  # wrong account
for p in pay:  # disputes
    if (p["mid"], p["period"]) in {("M-1013", "2026-08"), ("M-1025", "2026-10")}:
        p["disputed"] = "Yes"
# Refunds that were sent
add(D(2026, 10, 12), "M-1003", "Refund", 189, result="Sent")
add(D(2026, 10, 20), "M-1012", "Refund", 95, result="Sent")   # the OTHER Chris Morgan's $95 refund
pay.sort(key=lambda p: (p["date"], p["mid"]))
for i, p in enumerate(pay):
    p["txn"] = f"T-{2001 + i}"

refunds = [
    dict(req="R-01", date=D(2026, 10, 10), mid="M-1003", amount=189, reason="Billed during a medical freeze"),
    dict(req="R-02", date=D(2026, 10, 18), mid="M-1012", amount=95, reason="Guest fees charged by mistake"),
    dict(req="R-03", date=D(2026, 10, 22), mid="M-1009", amount=260, reason="Court booking cancelled by club"),
    dict(req="R-04", date=D(2026, 10, 5), mid="M-1031", amount=95, reason="Unused guest passes"),
]

# ---- Answer key (written from the plan, not from the formulas) ------------------------------
def txn(mid, date):
    return next(p["txn"] for p in pay if p["mid"] == mid and p["date"] == date and p["type"] == "Dues"
                and (p["result"] == "Failed" or True))
key = {}
for mid, mo in failed_unretried:
    key[txn(mid, D(2026, mo, 1))] = "Card failed, not retried"
key[txn("M-1015", D(2026, 10, 1))] = "Charged after pausing"
key[txn("M-1031", D(2026, 10, 1))] = "Charged after pausing"
key[txn("M-1030", D(2026, 9, 1))] = "Charged after cancelling"
key[txn("M-1030", D(2026, 10, 1))] = "Charged after cancelling"
key[txn("M-1006", D(2026, 9, 2))] = "Charged twice this month"
key[txn("M-1021", D(2026, 10, 2))] = "Charged twice this month"
key[txn("M-1017", D(2026, 10, 3))] = "Paid with another member's card"
key[txn("M-1013", D(2026, 8, 1))] = "Disputed charge"
key[txn("M-1025", D(2026, 10, 1))] = "Disputed charge"
key["R-03"] = "Refund approved but never sent"
key["R-04"] = "Refund approved but never sent"

# ---- Workbook -----------------------------------------------------------------------------
HEAD = Font(bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="4C1D95")
def header(ws, cols, widths):
    ws.append(cols)
    for i, c in enumerate(ws[1], 1):
        c.font, c.fill = HEAD, HFILL
        ws.column_dimensions[c.column_letter].width = widths[i - 1]
    ws.freeze_panes = "A2"

wb = Workbook()
ws = wb.active; ws.title = "Fix List"
wm = wb.create_sheet("Members"); wp = wb.create_sheet("Payments"); wr = wb.create_sheet("Refunds Owed")

header(wm, ["Member ID", "Name", "Plan", "Monthly dues", "Card on file", "Status", "Status since", "Phone"],
       [11, 18, 9, 13, 13, 11, 13, 16])
for m in members:
    wm.append([m["id"], m["name"], m["plan"], m["dues"], m["card"], m["status"], m["since"], m["phone"]])
for r in range(2, len(members) + 2):
    wm[f"D{r}"].number_format = "$#,##0"; wm[f"G{r}"].number_format = "mmm d, yyyy"

NP = len(pay) + 1
lk = lambda col, r: f"INDEX(Members!${col}$2:${col}$200,MATCH($C{r},Members!$A$2:$A$200,0))"
header(wp, ["Txn ID", "Date", "Member ID", "Name", "Type", "Month", "Amount", "Card used", "Result",
            "Disputed", "Problem", "What to do", "Fix #"], [9, 12, 11, 18, 8, 9, 9, 11, 8, 9, 30, 34, 6])
for i, p in enumerate(pay):
    r = i + 2
    onfile, status, since = lk("E", r), lk("F", r), lk("G", r)
    problem = (
        f'=IF($J{r}="Yes","Disputed charge",'
        f'IF(AND($E{r}="Dues",$I{r}="Paid",$H{r}<>{onfile}),"Paid with another member\'s card",'
        f'IF(AND($E{r}="Dues",$I{r}="Paid",{status}<>"Active",$B{r}>={since}),'
        f'"Charged after "&IF({status}="Paused","pausing","cancelling"),'
        f'IF(AND($E{r}="Dues",$I{r}="Paid",COUNTIFS($C$2:$C{r},$C{r},$F$2:$F{r},$F{r},$E$2:$E{r},"Dues",'
        f'$I$2:$I{r},"Paid",$H$2:$H{r},{onfile})>1),"Charged twice this month",'
        f'IF(AND($E{r}="Dues",$I{r}="Failed",COUNTIFS($C$2:$C${NP},$C{r},$F$2:$F${NP},$F{r},'
        f'$E$2:$E${NP},"Dues",$I$2:$I${NP},"Paid")=0),"Card failed, not retried","")))))')
    amt = f'TEXT($G{r},"$#,##0")'
    fix = (f'=IF($K{r}="","",IF($K{r}="Disputed charge","Call member about this "&{amt}&" charge",'
           f'IF($K{r}="Card failed, not retried","Call to update card, then retry "&{amt},'
           f'IF($K{r}="Charged twice this month","Refund the extra "&{amt},'
           f'IF($K{r}="Paid with another member\'s card","Move this payment to "&'
           f'IFERROR(INDEX(Members!$A$2:$A$200,MATCH($H{r},Members!$E$2:$E$200,0)),"the right member"),'
           f'"Refund "&{amt})))))')
    wp.append([p["txn"], p["date"], p["mid"], f"=IFERROR({lk('B', r)},\"Unknown ID\")", p["type"], p["period"],
               p["amount"], p["card"], p["result"], p["disputed"], problem, fix,
               f'=IF($K{r}="","",COUNTIF($K$2:$K{r},"?*"))'])
    wp[f"B{r}"].number_format = "mmm d, yyyy"; wp[f"G{r}"].number_format = "$#,##0"
wp.conditional_formatting.add(f"A2:M{NP}", FormulaRule(formula=['$K2<>""'], fill=PatternFill("solid", fgColor="FDE2E2")))

NR = len(refunds) + 1
header(wr, ["Request", "Approved on", "Member ID", "Name", "Amount", "Reason", "Sent?", "Problem", "What to do", "Fix #"],
       [9, 13, 11, 18, 9, 32, 7, 30, 24, 6])
for i, q in enumerate(refunds):
    r = i + 2
    sent = (f'=IF(COUNTIFS(Payments!$C$2:$C${NP},$C{r},Payments!$E$2:$E${NP},"Refund",'
            f'Payments!$G$2:$G${NP},$E{r},Payments!$B$2:$B${NP},">="&$B{r})>0,"Yes","No")')
    wr.append([q["req"], q["date"], q["mid"], f"=IFERROR({lk('B', r)},\"Unknown ID\")", q["amount"], q["reason"], sent,
               f'=IF($G{r}="No","Refund approved but never sent","")',
               f'=IF($H{r}="","","Send the "&TEXT($E{r},"$#,##0")&" refund")',
               f'=IF($H{r}="","",COUNTIF(Payments!$K$2:$K${NP},"?*")+COUNTIF($H$2:$H{r},"?*"))'])
    wr[f"B{r}"].number_format = "mmm d, yyyy"; wr[f"E{r}"].number_format = "$#,##0"
wr.conditional_formatting.add(f"A2:J{NR}", FormulaRule(formula=['$H2<>""'], fill=PatternFill("solid", fgColor="FDE2E2")))

# Fix List: one row per problem, pulled from both tabs by Fix #.
ws["A1"] = "Front desk fix list"; ws["A1"].font = Font(bold=True, size=14)
ws["A2"] = (f'=COUNTIF(Payments!$K$2:$K${NP},"?*")+COUNTIF(\'Refunds Owed\'!$H$2:$H${NR},"?*")&'
            f'" things to fix. Every lookup uses the member ID, never the name."')
cols = ["#", "Member ID", "Name", "Phone", "What's wrong", "What to do", "Ref"]
ws.append([]); ws.append(cols)
for i, c in enumerate(ws[4], 1):
    c.font, c.fill = HEAD, HFILL
    ws.column_dimensions[c.column_letter].width = [5, 11, 18, 16, 30, 36, 8][i - 1]
P = f'COUNTIF(Payments!$K$2:$K${NP},"?*")'
T = f'({P}+COUNTIF(\'Refunds Owed\'!$H$2:$H${NR},"?*"))'
def pick(pcol, rcol, r):
    return (f'IF($A{r}<={P},INDEX(Payments!${pcol}$2:${pcol}${NP},MATCH($A{r},Payments!$M$2:$M${NP},0)),'
            f'INDEX(\'Refunds Owed\'!${rcol}$2:${rcol}${NR},MATCH($A{r},\'Refunds Owed\'!$J$2:$J${NR},0)))')
for k in range(1, 41):
    r = k + 4
    ws.append([k,
               f'=IF($A{r}>{T},"",{pick("C", "C", r)})',
               f'=IF($B{r}="","",INDEX(Members!$B$2:$B$200,MATCH($B{r},Members!$A$2:$A$200,0)))',
               f'=IF($B{r}="","",INDEX(Members!$H$2:$H$200,MATCH($B{r},Members!$A$2:$A$200,0)))',
               f'=IF($B{r}="","",{pick("K", "H", r)})',
               f'=IF($B{r}="","",{pick("L", "I", r)})',
               f'=IF($B{r}="","",{pick("A", "A", r)})'])
ws.freeze_panes = "A5"

wb.save("/home/user/finances/member-billing/member-billing.xlsx")
json.dump({"answer_key": key,
           "members": {m["id"]: {k: (str(v) if isinstance(v, D) else v) for k, v in m.items()} for m in members},
           "payments": [{k: (str(v) if isinstance(v, D) else v) for k, v in p.items()} for p in pay],
           "refunds": [{k: (str(v) if isinstance(v, D) else v) for k, v in q.items()} for q in refunds]},
          open("/home/user/finances/member-billing/answer_key.json", "w"), indent=1)
print(len(members), "members,", len(pay), "payments,", len(refunds), "refund requests,", len(key), "planted problems")
