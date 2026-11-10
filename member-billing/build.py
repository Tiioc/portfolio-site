"""Member Billing Tracker: builds the workbook (fake data + formulas) and the answer key.

Every check is a visible spreadsheet formula. Every lookup uses the member ID, never the name.
Tabs: Fix List (first), Payments, Refunds, Members.
Output: member-billing.xlsx (upload to Google Drive to turn it into a Google Sheet) and answer_key.json.
"""
import json, datetime as dt, random
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.formatting.rule import FormulaRule

random.seed(7)
D = dt.date
PLANS = {"Tennis": 189, "Social": 95, "Family": 260}
FIRST = ["Ava", "Ben", "Carla", "Dev", "Ella", "Felix", "Gina", "Hank", "Iris", "Jake", "Kira", "Leo", "Mia",
         "Nate", "Olive", "Paul", "Quinn", "Rosa", "Sam", "Tara", "Uma", "Vic", "Wes", "Xena", "Yara", "Zack",
         "Amir", "Bea", "Cole", "Dana", "Eli", "Faye", "Gus", "Hana", "Ivan", "Jules"]
LAST = ["Ortiz", "Nguyen", "Patel", "Brooks", "Kim", "Reyes", "Hale", "Moreno", "Sato", "Price", "Lund", "Vega",
        "Shaw", "Diaz", "Fox", "Grant", "Hayes", "Iqbal", "Jensen", "Klein", "Lowe", "Mendez", "Novak", "Olsen",
        "Park", "Quint", "Ruiz", "Stone", "Tran", "Udall", "Voss", "West", "Young", "Zane", "Abbott", "Banks"]

# Plain labels used in the sheet (and in the answer key).
DISPUTE, DECLINED = "Member disputed this charge", "Card declined, not retried"
PAUSED, CANCELLED = "Charged after they paused", "Charged after they cancelled"
TWICE, WRONG_CARD = "Charged twice this month", "Paid with another member's card"
NOT_SENT = "Refund approved, never sent"

# ---- Members -------------------------------------------------------------------------------
members = []
cards = random.sample(range(1000, 9999), 36)
for i in range(36):
    plan = random.choice(list(PLANS))
    members.append(dict(id=f"M-{1001 + i}", name=f"{FIRST[i]} {LAST[i]}", dues=PLANS[plan],
                        card=f"Visa {cards[i]}", status="Active", since=D(2025, 1, 1),
                        phone=f"(661) 555-01{i:02d}"))
M = {m["id"]: m for m in members}
# Same-name pair: two different members, both named Chris Morgan.
M["M-1012"].update(name="Chris Morgan", dues=189)
M["M-1031"].update(name="Chris Morgan", dues=95, status="Paused", since=D(2026, 9, 20))
M["M-1015"].update(status="Paused", since=D(2026, 9, 15))
M["M-1030"].update(status="Cancelled", since=D(2026, 8, 20))
M["M-1033"].update(status="Paused", since=D(2026, 9, 10))   # clean case: billing stopped correctly

# ---- Payments ------------------------------------------------------------------------------
pay = []
def add(date, mid, kind, amount, result="Paid", disputed="", card=None):
    pay.append(dict(date=date, mid=mid, type=kind, period=f"{date:%Y-%m}", amount=amount,
                    card=card or M[mid]["card"], result=result, disputed=disputed))

failed_unretried = {("M-1004", 10), ("M-1011", 10), ("M-1019", 9), ("M-1027", 10)}
failed_retried = {("M-1008", 9, 4), ("M-1023", 10, 5)}     # clean cases: retried and paid
for month in (8, 9, 10):
    for m in members:
        mid = m["id"]
        if m["status"] != "Active" and D(2026, month, 1) >= m["since"]:
            if not ((mid == "M-1015" and month == 10) or (mid == "M-1030" and month in (9, 10))
                    or (mid == "M-1031" and month == 10)):
                continue
        if mid == "M-1018" and month == 10:
            continue  # M-1018's October payment got put on M-1017's account (below)
        if (mid, month) in failed_unretried:
            add(D(2026, month, 1), mid, "Dues", m["dues"], result="Declined"); continue
        r = [x for x in failed_retried if x[:2] == (mid, month)]
        if r:
            add(D(2026, month, 1), mid, "Dues", m["dues"], result="Declined")
            add(D(2026, month, r[0][2]), mid, "Dues", m["dues"]); continue
        add(D(2026, month, 1), mid, "Dues", m["dues"])

add(D(2026, 9, 2), "M-1006", "Dues", M["M-1006"]["dues"])                 # charged twice
add(D(2026, 10, 2), "M-1021", "Dues", M["M-1021"]["dues"])                # charged twice
add(D(2026, 10, 3), "M-1017", "Dues", M["M-1018"]["dues"], card=M["M-1018"]["card"])  # wrong account
for p in pay:
    if (p["mid"], p["period"]) in {("M-1013", "2026-08"), ("M-1025", "2026-10")}:
        p["disputed"] = "Yes"
add(D(2026, 10, 12), "M-1003", "Refund", 189, result="Refunded")
add(D(2026, 10, 20), "M-1012", "Refund", 95, result="Refunded")   # the OTHER Chris Morgan's $95 refund
pay.sort(key=lambda p: (p["date"], p["mid"]))
for i, p in enumerate(pay):
    p["txn"] = f"T-{2001 + i}"

refunds = [
    dict(req="R-01", date=D(2026, 10, 10), mid="M-1003", amount=189, reason="Billed during a medical freeze"),
    dict(req="R-02", date=D(2026, 10, 18), mid="M-1012", amount=95, reason="Guest fees charged by mistake"),
    dict(req="R-03", date=D(2026, 10, 22), mid="M-1009", amount=260, reason="Court booking cancelled by club"),
    dict(req="R-04", date=D(2026, 10, 5), mid="M-1031", amount=95, reason="Unused guest passes"),
]

# ---- Answer key (written from the plan above, not from the formulas) -----------------------
def txn(mid, date):
    return next(p["txn"] for p in pay if p["mid"] == mid and p["date"] == date and p["type"] == "Dues")
key = {txn(mid, D(2026, mo, 1)): DECLINED for mid, mo in failed_unretried}
key[txn("M-1015", D(2026, 10, 1))] = PAUSED
key[txn("M-1031", D(2026, 10, 1))] = PAUSED
key[txn("M-1030", D(2026, 9, 1))] = CANCELLED
key[txn("M-1030", D(2026, 10, 1))] = CANCELLED
key[txn("M-1006", D(2026, 9, 2))] = TWICE
key[txn("M-1021", D(2026, 10, 2))] = TWICE
key[txn("M-1017", D(2026, 10, 3))] = WRONG_CARD
key[txn("M-1013", D(2026, 8, 1))] = DISPUTE
key[txn("M-1025", D(2026, 10, 1))] = DISPUTE
key["R-03"] = NOT_SENT
key["R-04"] = NOT_SENT
ACTION = {DISPUTE: "Call", DECLINED: "Retry card", PAUSED: "Refund", CANCELLED: "Refund", TWICE: "Refund",
          WRONG_CARD: "Move payment", NOT_SENT: "Send refund"}

# ---- Workbook -----------------------------------------------------------------------------
HEAD, HFILL = Font(bold=True, color="FFFFFF"), PatternFill("solid", fgColor="4C1D95")
def header(ws, row, cols, widths):
    for i, (c, w) in enumerate(zip(cols, widths), 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font, cell.fill = HEAD, HFILL
        ws.column_dimensions[cell.column_letter].width = w
    ws.freeze_panes = ws.cell(row=row + 1, column=1)

def put(ws, r, values):
    for c, v in enumerate(values, 1):
        ws.cell(row=r, column=c, value=v)

wb = Workbook()
ws = wb.active; ws.title = "Fix List"
wp = wb.create_sheet("Payments"); wr = wb.create_sheet("Refunds"); wm = wb.create_sheet("Members")

# Members: A ID, B Name, C Monthly dues, D Card on file, E Status, F Since, G Phone
header(wm, 1, ["Member ID", "Name", "Monthly dues", "Card on file", "Status", "Since", "Phone"],
       [11, 18, 13, 13, 11, 13, 16])
for i, m in enumerate(members):
    put(wm, i + 2, [m["id"], m["name"], m["dues"], m["card"], m["status"], m["since"], m["phone"]])
for r in range(2, len(members) + 2):
    wm[f"C{r}"].number_format = "$#,##0"; wm[f"F{r}"].number_format = "mmm d, yyyy"

NP = len(pay) + 1
mem = lambda col, r, key="$C": f"INDEX(Members!${col}$2:${col}$200,MATCH({key}{r},Members!$A$2:$A$200,0))"
# Payments: A Payment #, B Date, C Member ID, D Name, E Kind, F Month, G Amount, H Card used,
#           I Result, J Disputed?, K Problem, L List #
header(wp, 1, ["Payment #", "Date", "Member ID", "Name", "Kind", "Month", "Amount", "Card used", "Result",
               "Disputed?", "Problem", "List #"], [10, 12, 11, 18, 8, 9, 9, 11, 10, 10, 30, 7])
for i, p in enumerate(pay):
    r = i + 2
    card, status, since = mem("D", r), mem("E", r), mem("F", r)
    paid_dues = f'$E{r}="Dues",$I{r}="Paid"'
    problem = (
        f'=IF($J{r}="Yes","{DISPUTE}",'
        f'IF(AND({paid_dues},$H{r}<>{card}),"{WRONG_CARD}",'
        f'IF(AND({paid_dues},{status}<>"Active",$B{r}>={since}),'
        f'IF({status}="Paused","{PAUSED}","{CANCELLED}"),'
        f'IF(AND({paid_dues},COUNTIFS($C$2:$C{r},$C{r},$F$2:$F{r},$F{r},$E$2:$E{r},"Dues",'
        f'$I$2:$I{r},"Paid",$H$2:$H{r},{card})>1),"{TWICE}",'
        f'IF(AND($E{r}="Dues",$I{r}="Declined",COUNTIFS($C$2:$C${NP},$C{r},$F$2:$F${NP},$F{r},'
        f'$E$2:$E${NP},"Dues",$I$2:$I${NP},"Paid")=0),"{DECLINED}","")))))').replace("'", "'")
    put(wp, r, [p["txn"], p["date"], p["mid"], f'=IFERROR({mem("B", r)},"Unknown ID")', p["type"], p["period"],
               p["amount"], p["card"], p["result"], p["disputed"], problem,
               f'=IF($K{r}="","",COUNTIF($K$2:$K{r},"?*"))'])
    wp[f"B{r}"].number_format = "mmm d, yyyy"; wp[f"G{r}"].number_format = "$#,##0"
wp.conditional_formatting.add(f"A2:L{NP}", FormulaRule(formula=['$K2<>""'], fill=PatternFill("solid", fgColor="FDE2E2")))

NR = len(refunds) + 1
# Refunds: A Request #, B Approved, C Member ID, D Name, E Amount, F Reason, G Sent?, H Problem, I List #
header(wr, 1, ["Request #", "Approved", "Member ID", "Name", "Amount", "Reason", "Sent?", "Problem", "List #"],
       [10, 13, 11, 18, 9, 32, 7, 28, 7])
for i, q in enumerate(refunds):
    r = i + 2
    sent = (f'=IF(COUNTIFS(Payments!$C$2:$C${NP},$C{r},Payments!$E$2:$E${NP},"Refund",'
            f'Payments!$G$2:$G${NP},$E{r},Payments!$B$2:$B${NP},">="&$B{r})>0,"Yes","No")')
    put(wr, r, [q["req"], q["date"], q["mid"], f'=IFERROR({mem("B", r)},"Unknown ID")', q["amount"], q["reason"], sent,
               f'=IF($G{r}="No","{NOT_SENT}","")',
               f'=IF($H{r}="","",COUNTIF(Payments!$K$2:$K${NP},"?*")+COUNTIF($H$2:$H{r},"?*"))'])
    wr[f"B{r}"].number_format = "mmm d, yyyy"; wr[f"E{r}"].number_format = "$#,##0"
wr.conditional_formatting.add(f"A2:I{NR}", FormulaRule(formula=['$H2<>""'], fill=PatternFill("solid", fgColor="FDE2E2")))

# Fix List: one row per problem, pulled from Payments then Refunds by List #.
ws["A1"] = "Today's fix list"; ws["A1"].font = Font(bold=True, size=14)
P = f'COUNTIF(Payments!$K$2:$K${NP},"?*")'
T = f'({P}+COUNTIF(Refunds!$H$2:$H${NR},"?*"))'
ws["A2"] = f'={T}&" things to fix. Look members up by ID, never by name."'
# A Do this, B Member, C Member ID, D Phone, E Why, F Amount, G Find it
header(ws, 4, ["Do this", "Member", "Member ID", "Phone", "Why", "Amount", "Find it"], [14, 18, 11, 16, 34, 9, 9])
def pick(pcol, rcol, r):
    k = f"(ROW()-4)"
    return (f'IF({k}<={P},INDEX(Payments!${pcol}$2:${pcol}${NP},MATCH({k},Payments!$L$2:$L${NP},0)),'
            f'INDEX(Refunds!${rcol}$2:${rcol}${NR},MATCH({k},Refunds!$I$2:$I${NR},0)))')
for r in range(5, 45):
    why = f'IF($C{r}="","",{pick("K", "H", r)})'
    put(ws, r, [
        f'=IF($E{r}="","",IF($E{r}="{DISPUTE}","Call",IF($E{r}="{DECLINED}","Retry card",'
        f'IF(LEFT($E{r},31)="{WRONG_CARD}","Move payment",IF($E{r}="{NOT_SENT}","Send refund","Refund")))))',
        f'=IF($C{r}="","",{mem("B", r, "$C")})',
        f'=IF(ROW()-4>{T},"",{pick("C", "C", r)})',
        f'=IF($C{r}="","",{mem("G", r, "$C")})',
        f'=IF($C{r}="","",IF({pick("K", "H", r)}="{WRONG_CARD}","{WRONG_CARD} ("&'
        f'IFERROR(INDEX(Members!$A$2:$A$200,MATCH({pick("H", "C", r)},Members!$D$2:$D$200,0)),"check")&")",'
        f'{pick("K", "H", r)}))',
        f'=IF($C{r}="","",{pick("G", "E", r)})',
        f'=IF($C{r}="","",{pick("A", "A", r)})'])
    ws[f"F{r}"].number_format = "$#,##0"
    ws[f"A{r}"].font = Font(bold=True)
COLORS = {"Call": "EDE9FE", "Retry card": "FEF3C7", "Refund": "FCE7F3", "Send refund": "FCE7F3", "Move payment": "DBEAFE"}
for label, color in COLORS.items():
    ws.conditional_formatting.add("A5:A44", FormulaRule(formula=[f'$A5="{label}"'], fill=PatternFill("solid", fgColor=color)))
ws.freeze_panes = "A5"

wb.save("/home/user/finances/member-billing/member-billing.xlsx")
json.dump({"answer_key": key, "actions": ACTION,
           "members": {m["id"]: {k: (str(v) if isinstance(v, D) else v) for k, v in m.items()} for m in members},
           "payments": [{k: (str(v) if isinstance(v, D) else v) for k, v in p.items()} for p in pay],
           "refunds": [{k: (str(v) if isinstance(v, D) else v) for k, v in q.items()} for q in refunds]},
          open("/home/user/finances/member-billing/answer_key.json", "w"), indent=1)
print(len(members), "members,", len(pay), "payments,", len(refunds), "refund requests,", len(key), "planted problems")
