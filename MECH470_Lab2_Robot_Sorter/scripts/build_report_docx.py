#!/usr/bin/env python3
"""Build MECH 470 Lab 2 robotic sorting laboratory report (.docx)."""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Inches, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
APP = ROOT / "appendix"
OUT_DIR = ROOT


def set_run_font(run, name="Times New Roman", size=11, bold=False, italic=False):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(0, 0, 0)


def add_para(
    doc,
    text,
    *,
    bold=False,
    italic=False,
        size=11,
        space_after=5,
        space_before=0,
        align=None,
        first_line=True,
    ):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = 1.08
    if first_line and align is None:
        pf.first_line_indent = Cm(0.62)
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def add_mixed(doc, parts, *, space_after=6, space_before=0, first_line=True, size=11):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_after = Pt(space_after)
    pf.space_before = Pt(space_before)
    pf.line_spacing = 1.08
    if first_line:
        pf.first_line_indent = Cm(0.62)
    for text, bold, italic in parts:
        run = p.add_run(text)
        set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def heading(doc, text):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(8)
    pf.space_after = Pt(3)
    pf.line_spacing = 1.08
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    set_run_font(run, size=12, bold=True)
    return p


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(8)
    pf.first_line_indent = Cm(0)
    run = p.add_run(text)
    set_run_font(run, size=9, italic=True)
    return p


def add_picture(doc, path, width_in=6.3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.first_line_indent = Cm(0)
    run = p.add_run()
    run.add_picture(str(path), width=Inches(width_in))
    return p


def shade_header(cell, color="1F4E79"):
    tc = cell._tePr if hasattr(cell, "_tePr") else cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), color)
    shd.set(qn("w:val"), "clear")
    tcPr.append(shd)


def set_cell(cell, text, *, bold=False, size=9, color=None, center=False):
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold)
    if color:
        run.font.color.rgb = RGBColor(*color)


def add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, h in enumerate(headers):
        set_cell(table.rows[0].cells[i], h, bold=True, size=9, color=(255, 255, 255), center=True)
        shade_header(table.rows[0].cells[i])
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            set_cell(table.rows[r + 1].cells[c], val, size=8.5)
    if col_widths:
        for row in table.rows:
            for i, w in enumerate(col_widths):
                row.cells[i].width = Inches(w)
    return table


def set_narrow_margins(section):
    section.top_margin = Cm(1.6)
    section.bottom_margin = Cm(1.6)
    section.left_margin = Cm(1.9)
    section.right_margin = Cm(1.9)
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)


def add_page_number(section):
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("MECH 470/970  ·  Lab 2 Robotic Sorting System  ·  Page ")
    set_run_font(run, size=8)
    fld1 = OxmlElement("w:fldChar")
    fld1.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld2 = OxmlElement("w:fldChar")
    fld2.set(qn("w:fldCharType"), "end")
    r2 = p.add_run()
    r2._r.append(fld1)
    r2._r.append(instr)
    r2._r.append(fld2)
    set_run_font(r2, size=8)


def build():
    doc = Document()
    section = doc.sections[0]
    set_narrow_margins(section)
    add_page_number(section)

    add_para(
        doc,
        "University of Wollongong  ·  School of Mechanical, Materials, Mechatronic and Biomedical Engineering",
        bold=False,
        size=10,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        first_line=False,
        space_after=2,
    )
    add_para(
        doc,
        "MECH 470/970  Advanced Applied Topics in Mechatronics",
        bold=True,
        size=12,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        first_line=False,
        space_after=2,
    )
    add_para(
        doc,
        "Laboratory Report No. 2 — Robotic Sorting System",
        bold=True,
        size=14,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        first_line=False,
        space_after=6,
    )
    add_para(
        doc,
        "Author: Bo Zhang (8571260)    Group members: ____________    Lecturer: Zengxi (Stephen) Pan    Date: 8 September 2026",
        size=10,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        first_line=False,
        space_after=8,
    )

    heading(doc, "1. Introduction")
    add_para(
        doc,
        "A wooden-block manufacturer has added a painted product line and therefore needs an automatic cell that separates painted blocks from unpainted ones. A six-axis manipulator is already installed by a robotics supplier. Its motions are not programmed in the PLC; they are triggered through a 24 V digital I/O handshake. The PLC must request a destination, wait until the robot reports that it has arrived and is no longer moving, operate a vacuum gripper, and classify each block from a shade sensor.",
    )
    add_para(
        doc,
        "This report describes the Siemens S7-1200 (CPU 1214C DC/DC/DC) program written in TIA Portal ladder (OB1). The work covers the three main laboratory tasks—shade-sensor commissioning, robot-motion handshake, and closed-loop sorting—and the extra diagnostic features that could be finished in the three-hour session. A step-integer sequencer was chosen as the control policy because the robot can occupy only one taught pose at a time and every move must be confirmed before the next output is issued. That policy is safer and easier to commission than a purely combinatorial interlock of all I/O bits.",
    )

    heading(doc, "2. System description and control strategy")
    add_para(
        doc,
        "The plant I/O matches the laboratory brief. Four digital inputs report the taught poses (pickup, painted drop, unpainted drop, home) and a fifth bit reports that the robot is in motion. Four digital outputs request those same poses (Q0.0–Q0.3). Q0.4 switches the sensor lamp and Q0.5 the vacuum. Analogue word IW64 is the shade sensor. Start, stop and reset push-buttons occupy I1.0–I1.2; status lamps occupy Q0.6, Q0.7, Q1.0 and Q1.1. The full tag list is given in Appendix Table A1.",
    )

    add_picture(doc, FIG / "fig1_control_architecture.png", 5.55)
    caption(doc, "Figure 1. Control architecture: operator, robot handshake, analogue shade path, and PLC outputs.")

    add_mixed(
        doc,
        [
            (
                "The control law is a discrete step sequencer stored in MW40, not a continuous controller. ",
                False,
                False,
            ),
            (
                "Justification: ",
                True,
                False,
            ),
            (
                "the robot trajectories are already taught, so the PLC does not close a Cartesian loop. It only issues mutually exclusive pose requests and waits for the corresponding in-position bit with Robot_Moving = 0. Integer steps (10, 20, 30, …) make the scan image easy to monitor online and prevent two request outputs from being true in the same cycle. Faults jump the sequencer to step 900 so that motion requests are dropped until Reset_PB is pressed.",
                False,
                False,
            ),
        ],
    )

    heading(doc, "3. Main Task 1 — Shade sensor commissioning")
    add_para(
        doc,
        "Illumination is switched from Network 5: whenever the running flag is set, Q0.4 Light_on is energised. The raw analogue word IW64 is copied every scan into MW42 (shade_raw). NORM_X maps the Siemens unipolar range 0–27648 onto 0.0–1.0 (MD44), and SCALE_X converts that fraction to 0–10 V in MD48 (shade_volt). This is the standard S7-1200 analogue path and was used so that a voltage, rather than a raw count, could be discussed at the bench.",
    )
    add_para(
        doc,
        "With the lamp on, empty, painted and unpainted surfaces occupy different reflectance bands. In the submitted online print, Th_empty (MW50) is 910 counts, which corresponds to 910/27648 × 10 ≈ 0.33 V. Live shade_raw values of 13984 and 21887 counts were captured on different networks, i.e. about 5.06 V and 7.91 V. The darker painted face sits in the mid band; the lighter unpainted wood returns the higher voltage; a vacant slide falls below Th_empty. Classification at step 40 therefore uses three comparisons: shade_raw < Th_empty → slide empty; a window at or above Th_empty and at or below th_paint (MW54) → painted (SET is_painted); shade_raw > th_paint → unpainted (RESET is_painted). The threshold word rather than a hard-coded constant was used so that the trip point can be retuned without editing every network.",
    )

    heading(doc, "4. Main Task 2 — Robot motion handshake")
    add_para(
        doc,
        "Each taught pose is requested by a dedicated coil that is true only in its step. Arrival is not assumed from time alone. After a request is raised, a TON of 500 ms filters contact bounce and the scan delay of the robot I/O, then the PLC requires the matching At_* input and a normally-closed Robot_Moving contact before MW40 is advanced. The same pattern is used for home (step 10 → 20), pickup (20 → 30) and the two drop poses (60 → 70). The 500 ms delay is a deliberate choice: it is long enough for the motion bit to rise after a new request, and short compared with the physical travel time, so the sequencer cannot skip a pose if the previous in-position bit is still true for one scan.",
    )
    add_para(
        doc,
        "Start_PB is accepted only when step = 0 and fault is false; it loads step 10 and SETs runnning. Stop_PB writes step 0, RESETs runnning and immediately RESETs vacuum_on so that a block cannot remain gripped after an operator stop. This handshake was first tested pose-by-pose (home, pickup, painted, unpainted) before the shade decision was enabled, which is the commissioning order required by the brief.",
    )

    heading(doc, "5. Main Task 3 — Sorting with shade detection")
    add_picture(doc, FIG / "fig2_step_sequence.png", 5.55)
    caption(doc, "Figure 2. Sorting cycle. After a successful drop the sequencer returns to step 20 until the slide is empty.")

    add_para(
        doc,
        "The production cycle is: home once at start; move to pickup; dwell 1 s at pickup so the analogue reading can settle (step 30); classify (step 40); SET vacuum_on and dwell 1 s to build vacuum (step 50); request painted or unpainted drop according to is_painted (step 60); confirm the correct At_* bit with Robot_Moving = 0; RESET vacuum_on and dwell 1 s so the block is released (step 70); then jump back to step 20. Parallel contacts at step 60 prevent a painted block from being accepted at the unpainted fixture and vice versa. The vacuum is implemented with SET/RESET rather than a held coil so that it survives the step change from 50 to 60 and is only dropped at the unload pose. The cycle repeats until Network 16 finds shade_raw < Th_empty, SETs slide_empty, and sends the sequencer to step 90.",
    )

    heading(doc, "6. Extra activities — diagnostics")
    add_para(
        doc,
        "Three diagnostic behaviours were requested: sensor/illumination failure, robot malfunction, and an empty slide. The empty-slide case is complete. At step 40 a low shade reading SETs slide_empty, step 90 requests home, energises lamp_empty (Q1.1) and RESETs runnning so the cell stops instead of hunting an empty fixture. lamp_running (Q0.6) tracks the running flag. lamp_painted (Q1.0) follows is_painted so the operator can see the classification before the drop move. If fault (M52.2) is set, Network 3 forces step 900 and lamp_fault flashes with the 1 Hz clock M0.5. Reset_PB is accepted only in step 900 and clears fault, fault_robot and fault_sensor before returning to idle.",
    )
    add_para(
        doc,
        "What was not finished in the session is the logic that SETs those fault bits. The reset coils and the flashing lamp are in OB1, but there is no watchdog such as “request on for longer than T and still not At_*” to SET fault_robot, and no check such as “lamp commanded on yet shade_raw stuck at 0 or 27648” to SET fault_sensor. Those networks were prepared as tags but not commissioned. With more time they would be added as TON watchdogs in parallel with each motion step, which is a small extension of the existing 500 ms handshake timers.",
    )

    heading(doc, "7. Discussion")
    add_para(
        doc,
        "The step sequencer was the right control policy for this plant: the robot OEM owns the trajectories, and the PLC only owns sequencing, gripping and classification. Using analogue counts for the trip points, while still scaling to volts for display, avoided rounding error in the compare blocks. Dwell times of 1 s at pickup, grip and release were conservative; they cost cycle time but made the vacuum and the shade reading repeatable on the laboratory hardware. Two limitations remain. First, IEC_Timer_0_DB_3 is reused at steps 30 and 60. The steps are mutually exclusive so the timer is reset when the step changes, but a dedicated instance would be clearer. Second, self-diagnosis of the robot and the lamp is only an interface, not a working detector. Both points would be the first items on a follow-up commissioning list. All main tasks (sensor scaling, motion handshake, and sort-until-empty) were demonstrated from the printed OB1.",
    )

    heading(doc, "8. Conclusion")
    add_para(
        doc,
        "A Siemens S7-1200 ladder program was commissioned to sort painted and unpainted blocks with a pre-taught robot. Illumination, analogue scaling to 0–10 V, threshold classification, vacuum grip/release, and a confirmed pose handshake were implemented as a step sequencer. The empty-slide stop and operator lamps were completed; robot and sensor watchdogs were only partially implemented. The program listing is given in the Appendix.",
        space_after=4,
    )

    heading(doc, "References")
    add_para(
        doc,
        "Pan, Z. (2026). MECH 470/970 Lab No. 2 — Robotic Sorting System. University of Wollongong.",
        first_line=False,
        space_after=2,
        italic=False,
    )
    add_para(
        doc,
        "Siemens AG. (n.d.). SIMATIC S7-1200 analogue input scaling (NORM_X / SCALE_X), unipolar range 0–27648 for 0–10 V.",
        first_line=False,
        space_after=10,
    )

    doc.add_page_break()
    add_para(
        doc,
        "Appendix A — Step list of Main [OB1]",
        bold=True,
        size=12,
        first_line=False,
        space_after=6,
    )
    add_para(
        doc,
        "This appendix lists the I/O map, the sequencer, and the TIA Portal print that was saved before leaving the laboratory. Tag spellings follow the TIA project (for example runnning, At_Unplainted).",
        first_line=False,
        space_after=4,
    )

    add_table(
        doc,
        ["Signal", "Address", "Direction", "Function"],
        [
            ["At_Pickup / At_Painted / At_Unpainted / At_home", "I0.0–I0.3", "DI", "Robot-in-position bits"],
            ["Robot_Moving", "I0.4", "DI", "High while a motion is executing"],
            ["Start_PB / Stop_PB / Reset_PB", "I1.0–I1.2", "DI", "Operator commands"],
            ["shade_raw_in", "IW64", "AI", "Shade sensor, 0–27648 counts"],
            ["Req_Pickup / Req_Painted / Req_unpainted / Req_home", "Q0.0–Q0.3", "DO", "Motion requests to the robot"],
            ["Light_on / vacuum_on", "Q0.4 / Q0.5", "DO", "Illumination and vacuum gripper"],
            ["lamp_running / lamp_fault / lamp_painted / lamp_empty", "Q0.6, Q0.7, Q1.0, Q1.1", "DO", "Status lamps"],
            ["step / shade_raw / shade_volt", "MW40 / MW42 / MD48", "M", "Sequencer and scaled voltage"],
            ["is_painted / runnning / fault / slide_empty", "M52.0–M52.5", "M", "Classification and mode flags"],
            ["Th_empty / th_paint", "MW50 / MW54", "M", "Empty and paint thresholds"],
        ],
        col_widths=[2.55, 1.15, 0.7, 1.9],
    )
    caption(doc, "Table A1. PLC tags used in Main [OB1].")

    add_table(
        doc,
        ["Step", "Action in OB1", "Advance condition"],
        [
            ["0", "Idle. Accept Start_PB if not fault.", "Start → 10; Stop → 0"],
            ["10", "Req_home. TON 500 ms.", "Timer + At_home + not moving → 20"],
            ["20", "Req_Pickup. TON 500 ms.", "Timer + At_Pickup + not moving → 30"],
            ["30", "Dwell TON 1 s for analogue settle.", "Timer → 40"],
            ["40", "Compare shade_raw with Th_empty / th_paint.", "Empty → 90; else SET/RESET is_painted → 50"],
            ["50", "SET vacuum_on. TON 1 s.", "Timer → 60"],
            ["60", "Req_Painted or Req_unpainted. TON 500 ms.", "Correct At_* + not moving → 70"],
            ["70", "RESET vacuum_on. TON 1 s.", "Timer → 20 (next block)"],
            ["90", "Req_home, lamp_empty, RESET runnning.", "Operator must restart"],
            ["900", "Fault park. lamp_fault flashes at 1 Hz.", "Reset_PB → 0"],
        ],
        col_widths=[0.7, 3.0, 2.6],
    )
    caption(doc, "Table A2. Sequencer implemented in Networks 1–29.")

    add_para(
        doc,
        "Network summary: N1 start; N2 stop and vacuum off; N3 fault → 900; N4 reset faults; N5 Light_on; N6–N7 analogue sample and 0–10 V scale; N8–N10 home handshake; N11–N13 pickup handshake; N14–N15 settle; N16 empty; N17 painted window; N18 unpainted; N19–N21 grip; N22–N25 drop handshake; N26–N28 release and loop; N29 empty stop; N30–N32 running / flashing fault / painted lamps.",
        first_line=False,
        space_after=8,
    )

    add_para(
        doc,
        "Appendix B — TIA Portal print of Main [OB1]",
        bold=True,
        size=12,
        first_line=False,
        space_after=6,
    )
    add_para(
        doc,
        "The following pages are the laboratory print of PLC_1 / Program blocks / Main [OB1] (LAD). Live values visible in grey boxes were captured while the CPU was in online monitoring and are not constants.",
        first_line=False,
        space_after=6,
    )

    for i in range(1, 9):
        img = APP / f"tia_page_{i:02d}.png"
        add_picture(doc, img, 6.3)
        caption(doc, f"Figure B{i}. TIA Portal Main [OB1], printed page {i} of 8.")

    out = OUT_DIR / "MECH470_Lab2_Robot_Sorter_Report_Bo_Zhang.docx"
    doc.save(out)
    print("wrote", out)
    return out


if __name__ == "__main__":
    build()
