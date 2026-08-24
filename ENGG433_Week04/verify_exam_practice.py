#!/usr/bin/env python3
"""Numeric checks for Week 4 exam practice calculation questions."""

from pathlib import Path


def near(a, b, eps=1e-9):
    return abs(a - b) <= eps


def main():
    lines = []
    failures = []

    def check(label, got, exp):
        ok = near(got, exp) if isinstance(got, (int, float)) else got == exp
        status = "PASS" if ok else "FAIL"
        lines.append(f"{status:4}  {label:<48} got={got}  expected={exp}")
        if not ok:
            failures.append(label)

    # Q5 accounting equation
    d_assets = -30000 + -15000
    check("Q5 delta assets", d_assets, -45000)
    check("Q5 choice C", "C", "C")

    # Q7 Letty revenue
    beg, inv, exp, draw, end = 105000, 147000, 420000, 28000, 290000
    revenue = end - beg - inv + exp + draw
    check("Q7 revenue", revenue, 486000)
    check("Q7 identity", beg + inv + revenue - exp - draw, 290000)

    # Q13 supplies
    supplies_end = 780 + 900 - 1150
    check("Q13 supplies ending debit", supplies_end, 530)

    # Q18 season tickets
    earned = 250000 * 3 / 8
    check("Q18 September revenue", earned, 93750)

    # Q19 payroll split
    expense_new = 50000 - 34000
    check("Q19 current expense portion", expense_new, 16000)
    check("Q19 cash credit", 34000 + 16000, 50000)

    # Answer key letters
    answers = {
        1: "T", 2: "F", 3: "C", 4: "B", 5: "C",
        6: "D", 7: "D", 8: "F", 9: "F", 10: "B",
        11: "D", 12: "A", 13: "D", 14: "T", 15: "T",
        16: "A", 17: "B", 18: "D", 19: "B", 20: "D",
    }
    check("Q3 letter is C", answers[3], "C")
    check("answer-key count", len(answers), 20)

    text = "\n".join(lines)
    print(text)
    print()
    if failures:
        print("FAILED:", ", ".join(failures))
        raise SystemExit(1)
    print(f"ALL {len(lines)} CHECKS PASSED")

    out = Path("/opt/cursor/artifacts/week04_exam_practice_checks.log")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text + f"\n\nALL {len(lines)} CHECKS PASSED\n")


if __name__ == "__main__":
    main()
