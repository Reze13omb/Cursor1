# Depth vision sensors review (revised manuscript)

Revised review article corresponding to the original draft
`Manuscript_Review_Zhang_Depth Vision Sensors.docx`.

## Files

- `Zhang_Cui_Depth_Vision_Sensors_Review_revised.docx` — Sensors-oriented Word draft
- `Zhang_Cui_Depth_Vision_Sensors_Review_revised.md` — plain-text source
- `REVISION_NOTES.md` — Q4 then Q3 changes
- `refs.py` — bibliography used by the builder
- `build_manuscript.py` — regenerates Markdown and Word
- `figures/` — body figures plus `graphical_abstract.png` (MDPI GA, do not reuse as a numbered figure if the journal forbids it)

## Rebuild

```bash
python3 figures/make_figures.py
python3 build_manuscript.py
```
