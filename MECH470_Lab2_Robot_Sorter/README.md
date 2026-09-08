# MECH 470/970 Lab 2 — Robotic Sorting System

English laboratory report written from the TIA Portal `Main [OB1]` print (`123.pdf`) and the Lab 2 brief (`Robot Sorter - Questions.pdf`).

## Submit these files

- `MECH470_Lab2_Robot_Sorter_Report_Bo_Zhang.docx` — editable Word copy
- `MECH470_Lab2_Robot_Sorter_Report_Bo_Zhang.pdf` — print-ready PDF

The **report body is 3 pages**. The remaining pages are Appendix A (I/O map and step list) and Appendix B (the eight-page TIA Portal code print).

Fill in **group members** on the title line before submitting. Change the student name/number in `scripts/build_report_docx.py` if needed, then rebuild.

## Rebuild

```bash
python3 scripts/build_figures.py
python3 scripts/build_report_docx.py
libreoffice --headless --convert-to pdf MECH470_Lab2_Robot_Sorter_Report_Bo_Zhang.docx
```

## Source of the program description

The implementation details (I/O addresses, step numbers, timers, thresholds, lamps) are taken from the laboratory TIA Portal print stored at `appendix/TIA_Portal_Main_OB1_code.pdf`.
