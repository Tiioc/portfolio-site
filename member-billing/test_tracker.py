"""Tests for the Member Billing Tracker.

  python3 test_tracker.py                  # answer key vs a separate Python version of the rules
  python3 test_tracker.py results.xlsx     # also check a spreadsheet engine's computed values
                                           # (LibreOffice recalc, or a Google Sheets export)
"""
import json, sys, collections
from openpyxl import load_workbook

data = json.load(open("/home/user/finances/member-billing/answer_key.json"))
KEY, MEM, PAY, REF = data["answer_key"], data["members"], data["payments"], data["refunds"]
ACTION = data["actions"]
import build_labels as L
fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + (f"  ({detail})" if detail and not ok else ""))
    if not ok: fails.append(name)

# ---- A separate version of the rules, written in Python -----------------------------------
def rules(by):
    """by='id' looks members up by ID (the real rule). by='name' looks them up by name, first match."""
    first_by_name = {}
    for m in MEM.values(): first_by_name.setdefault(m["name"], m)
    who = (lambda p: MEM[p["mid"]]) if by == "id" else (lambda p: first_by_name[MEM[p["mid"]]["name"]])
    same = (lambda a, b: a["mid"] == b["mid"]) if by == "id" else \
           (lambda a, b: MEM[a["mid"]]["name"] == MEM[b["mid"]]["name"])
    out, seen = {}, collections.Counter()
    for p in PAY:
        m = who(p); dues_paid = p["type"] == "Dues" and p["result"] == "Paid"
        if dues_paid and p["card"] == m["card"]:
            seen[(m["id"], p["period"])] += 1
        if p["disputed"] == "Yes": out[p["txn"]] = L.DISPUTE
        elif dues_paid and p["card"] != m["card"]: out[p["txn"]] = L.WRONG_CARD
        elif dues_paid and m["status"] != "Active" and p["date"] >= m["since"]:
            out[p["txn"]] = L.PAUSED if m["status"] == "Paused" else L.CANCELLED
        elif dues_paid and p["card"] == m["card"] and seen[(m["id"], p["period"])] > 1:
            out[p["txn"]] = L.TWICE
        elif p["type"] == "Dues" and p["result"] == "Declined" and not any(
                same(q, p) and q["period"] == p["period"] and q["type"] == "Dues" and q["result"] == "Paid" for q in PAY):
            out[p["txn"]] = L.DECLINED
    for q in REF:
        sent = any(same(p, q) and p["type"] == "Refund" and p["amount"] == q["amount"] and p["date"] >= q["date"] for p in PAY)
        if not sent: out[q["req"]] = L.NOT_SENT
    return out

def compare(label, got):
    caught = {k for k in KEY if got.get(k) == KEY[k]}
    wrong_label = {k for k in KEY if k in got and got[k] != KEY[k]}
    missed = set(KEY) - set(got)
    extra = set(got) - set(KEY)
    print(f"  {label}: caught {len(caught)} of {len(KEY)} planted, missed {len(missed)}, "
          f"wrong label {len(wrong_label)}, false flags {len(extra)}")
    return caught, missed, wrong_label, extra

def same_name_tests(label, got):
    a = next(p["txn"] for p in PAY if p["mid"] == "M-1012" and p["period"] == "2026-10" and p["type"] == "Dues")
    b = next(p["txn"] for p in PAY if p["mid"] == "M-1031" and p["period"] == "2026-10" and p["type"] == "Dues")
    check(f"{label} same-name 1: active Chris Morgan (M-1012) October charge is not flagged", a not in got)
    check(f"{label} same-name 2: paused Chris Morgan (M-1031) October charge is flagged", got.get(b) == L.PAUSED)
    check(f"{label} same-name 3: M-1031's refund is still owed even though M-1012 got a $95 refund",
          got.get("R-04") == L.NOT_SENT)
    check(f"{label} same-name 4: M-1012's refund counts as sent", "R-02" not in got)
    m31 = [p["txn"] for p in PAY if p["mid"] == "M-1031" and p["period"] != "2026-10"]
    check(f"{label} same-name 5: M-1031's earlier charges are not flagged as another member's card",
          all(t not in got for t in m31))

print("1. Answer key vs the Python version of the rules (lookups by member ID)")
by_id = rules("id")
c, mi, wl, ex = compare("by ID", by_id)
check("python: every planted problem caught with the right label", len(c) == len(KEY))
check("python: no false flags", not ex, ex)
same_name_tests("python", by_id)

print("\n2. What goes wrong if you look members up by name instead (for comparison only)")
by_name = rules("name")
c, mi, wl, ex = compare("by name", by_name)
print("  missed:", sorted(mi), " false flags:", sorted(ex))

if len(sys.argv) > 1:
    path = sys.argv[1]
    print(f"\n3. Spreadsheet results from {path}")
    wb = load_workbook(path, data_only=True)
    got = {}
    for row in wb["Payments"].iter_rows(min_row=2, values_only=True):
        if row[0] and row[10]: got[row[0]] = row[10]
    for row in wb["Refunds"].iter_rows(min_row=2, values_only=True):
        if row[0] and row[7]: got[row[0]] = row[7]
    c, mi, wl, ex = compare("sheet", got)
    check("sheet: every planted problem caught with the right label", len(c) == len(KEY), sorted(mi | wl))
    check("sheet: no false flags", not ex, sorted(ex))
    check("sheet: matches the Python version row for row", got == by_id)
    same_name_tests("sheet", got)
    fl = [r for r in wb["Fix List"].iter_rows(min_row=5, values_only=True) if r[1]]
    check("sheet: fix list has one row per problem", len(fl) == len(KEY), len(fl))
    refs = {r[6]: r for r in fl}
    check("sheet: fix list covers every planted problem", set(refs) == set(KEY), set(KEY) ^ set(refs))
    check("sheet: fix list names and phones come from the member ID",
          all(r[1] == MEM[r[2]]["name"] and r[3] == MEM[r[2]]["phone"] for r in fl))
    check("sheet: every fix list row has the right action (Call, Refund, Retry card...)",
          all(r[0] == ACTION[KEY[r[6]]] for r in fl), [(r[0], r[6]) for r in fl if r[0] != ACTION[KEY[r[6]]]])
    check("sheet: Fix List is the first tab", wb.sheetnames[0] == "Fix List", wb.sheetnames)
    wa = next(r for r in fl if r[0] == "Move payment")
    check("sheet: wrong-account row points to M-1018", wa[4] == L.WRONG_CARD + " (M-1018)", wa[4])
    print("  header line:", wb["Fix List"]["A2"].value)
    print("  sample fix list rows:")
    for r in fl[:15]: print("   ", r)

print("\nRESULT:", "all passed" if not fails else f"{len(fails)} failed: {fails}")
sys.exit(1 if fails else 0)
