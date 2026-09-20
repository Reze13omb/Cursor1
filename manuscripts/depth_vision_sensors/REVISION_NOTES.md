# Revision notes

## Q3 target (this revision)

Primary journal: **Sensors (MDPI)**, CAS Q3 / JCR Q2.
Secondary: **Machines**, **IEEE Sensors Journal** only if the authors add original metrology data.

What was added on top of the Q4 draft:

- Structured abstract (Background / Methods / Results / Conclusions) at about 200 words.
- Highlights (4 bullets) and a separate graphical abstract (MDPI size).
- Honest structured-narrative methods: databases, stems, inclusion/exclusion table. No fake PRISMA counts.
- Device-level Table 3 from peer-reviewed Kinect / Azure Kinect / RealSense studies.
- Selection flowchart (Figure 4), hardware-to-function figure (Figure 5), and a 10-point checklist (Section 4.5).
- Calibration treated as its own subsection.
- LiDAR-inertial odometry (LOAM / LIO-SAM / FAST-LIO2), neural SLAM, depth-completion networks, GraspNet / DenseFusion, bridge-inspection UAV papers, HRI/safety standards.
- Bibliography expanded from 97 to ~170 cited items.
- Added Table 8 (benchmarks and what they do not measure), ICP/LVI estimators, and more application numbers so the body sits in the Sensors review band rather than at the floor.

## Still required of the authors before upload

1. Funding numbers and author-contribution CRediT codes in the Sensors template.
2. Optional paid English edit (recommended for Sensors).
3. Institutional check on MDPI reimbursement / warning lists.
4. Do not convert this into a PRISMA paper unless you actually run a registered protocol.
5. Graphical abstract file: `figures/graphical_abstract.png` (do not reuse a body figure).
6. Similarity and AI-detector checks (iThenticate via the library; authors must personally rewrite intro/methods/conclusion after this draft).

## Similarity and AI-detector notes

- Do **not** strip citations to lower a similarity score. Quoted algorithm names, ISO titles, and Table 3 numbers will match the source papers; that is expected if they are cited.
- Do **not** upload the manuscript to public 知网/万方 pools before journal submission; some services deposit the file.
- Do **not** run the text through “AI humanizer” websites. Those tools often raise both similarity and AI flags.
- After this rewrite, Zhang and Cui should each edit the Introduction, Section 1.1, and Section 6 in their own wording, keeping every citation. That author pass is what actually lowers AI-detector scores.
