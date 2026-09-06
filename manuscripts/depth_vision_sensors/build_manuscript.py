#!/usr/bin/env python3
"""Build the Q4-ready review as Markdown and Word."""

from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from refs import BIB

ROOT = Path(__file__).resolve().parent
FIG = ROOT / "figures"

_order: list[str] = []
_num: dict[str, int] = {}


def cite(*keys: str) -> str:
    nums = []
    for key in keys:
        if key not in BIB:
            raise KeyError(f"unknown citation key: {key}")
        if key not in _num:
            _order.append(key)
            _num[key] = len(_order)
        nums.append(_num[key])
    nums = sorted(set(nums))
    return "[" + ",".join(str(n) for n in nums) + "]"


def reset_cites() -> None:
    _order.clear()
    _num.clear()


def set_run_font(run, name="Times New Roman", size=11, bold=False, italic=False, color=None):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color is not None:
        run.font.color.rgb = color


def add_text(p, text, **kwargs):
    run = p.add_run(text)
    set_run_font(run, **kwargs)
    return run


def style_doc(doc: Document) -> None:
    section = doc.sections[0]
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    normal = doc.styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)
    normal.paragraph_format.space_after = Pt(8)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE


def heading(doc, text, level=1):
    p = doc.add_heading(text, level=level)
    for run in p.runs:
        run.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        run.font.name = "Times New Roman"


def para(doc, text, *, first_line=True, italic=False, size=11, bold=False, center=False, space_after=8):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if center else WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    if first_line and not center:
        p.paragraph_format.first_line_indent = Inches(0.3)
    add_text(p, text, size=size, italic=italic, bold=bold)
    return p


def caption(doc, text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.first_line_indent = Inches(0)
    add_text(p, text, size=10, italic=True)
    return p


def add_table(doc, headers, rows, title):
    caption(doc, title)
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = "Table Grid"
    table.autofit = True
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        add_text(p, h, size=8, bold=True)
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            cell = table.rows[r + 1].cells[c]
            cell.text = ""
            p = cell.paragraphs[0]
            add_text(p, val, size=8)
    doc.add_paragraph()


def add_figure(doc, path: Path, cap: str, width=6.3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run()
    run.add_picture(str(path), width=Inches(width))
    caption(doc, cap)


def write_markdown(path: Path, blocks: list[tuple]) -> None:
    lines = []
    for kind, payload in blocks:
        if kind == "title":
            lines += [f"# {payload}", ""]
        elif kind == "authors":
            lines += [payload, ""]
        elif kind == "affil":
            lines += [payload, ""]
        elif kind == "corr":
            lines += [f"**{payload}**", ""]
        elif kind == "h1":
            lines += [f"## {payload}", ""]
        elif kind == "h2":
            lines += [f"### {payload}", ""]
        elif kind == "p":
            lines += [payload, ""]
        elif kind == "caption":
            lines += [f"*{payload}*", ""]
        elif kind == "fig":
            rel = payload.relative_to(path.parent)
            lines += [f"![]({rel.as_posix()})", ""]
        elif kind == "table":
            title, headers, rows = payload
            lines += [f"*{title}*", ""]
            lines.append("| " + " | ".join(headers) + " |")
            lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
            for row in rows:
                lines.append("| " + " | ".join(row) + " |")
            lines.append("")
        elif kind == "refs":
            lines += ["## References", ""]
            for i, key in enumerate(_order, 1):
                lines.append(f"[{i}] {BIB[key]}")
                lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def manuscript_blocks() -> list[tuple]:
    reset_cites()
    b: list[tuple] = []

    b.append(("title", "Depth Vision Sensors: Technological Evolution, Enabling Algorithms, and Applications in Mechatronic Systems"))
    b.append(("authors", "Bo Zhang1,2 | Hongchao Cui1,2"))
    b.append(("affil", "1 School of Mechanical, Electronic and Control Engineering, Beijing Jiaotong University, Beijing, China\n2 Beijing Key Laboratory of Flow and Heat Transfer of Phase Changing in Micro and Small Scale, Beijing Jiaotong University, Beijing, China"))
    b.append(("corr", "Corresponding author: Hongchao Cui (hccui@bjtu.edu.cn)"))

    b.append(("h1", "Abstract"))
    b.append((
        "p",
        "Active depth vision sensors have become a standard perception front-end in mechatronic systems, including industrial robots, indoor mobile platforms, and unmanned aerial vehicles (UAVs). Unlike passive stereo or monocular depth estimation, structured light, time-of-flight (ToF), and solid-state light detection and ranging (LiDAR) emit controlled illumination and recover metric range with less dependence on scene texture. This review follows a hardware-centered narrative. First, we summarize the operating principles, representative devices, and reported operating envelopes of the three main active modalities. Second, we review the algorithms that convert raw depth into usable estimates: denoising and completion, multi-sensor fusion, visual-inertial-depth odometry, and geometric-semantic mapping. Third, we examine four application families in which the sensing modality is a first-order design choice: industrial inspection and bin picking, indoor mobile robots, UAVs, and collaborative robots. Remaining barriers are organized around sunlight and material sensitivity, compute and power, calibration, and interface fragmentation, together with emerging directions such as event-based depth, on-sensor inference, and photonic beam steering. The paper is intended as a compact map from sensor physics to system function for mechatronic designers, rather than a substitute for modality-specific hardware surveys.",
    ))
    b.append((
        "p",
        "Keywords: depth vision sensors; mechatronic systems; structured light; time-of-flight; solid-state LiDAR; SLAM; sensor fusion; collaborative robots",
    ))

    b.append(("h1", "1. Introduction"))
    b.append((
        "p",
        f"Autonomous mobile robots, flexible manufacturing cells, and small UAVs all require a timely geometric model of the workspace {cite('cadena2016','floreano2015','villani2018','halmet2019')}. Among perception options, vision remains attractive because it is non-contact, relatively inexpensive, and information-dense. Two-dimensional cameras supply appearance. Depth vision adds metric range, which simplifies obstacle clearance, grasp planning, and map scale. In a mechatronic system that coupling is not cosmetic: the same millimetre that is harmless in a visualization can be the difference between a successful insertion and a jammed assembly, or between a UAV standoff and a girder strike.",
    ))
    b.append((
        "p",
        f"This review is restricted to active depth vision: sensors that illuminate the scene with a controlled optical source and recover three-dimensional geometry from the returned light. The main families are structured light and active stereo, continuous-wave and pulsed ToF cameras, and solid-state LiDAR {cite('zhang2012sl','geng2011','foix2011','horaud2016','ho2022','roriz2022')}. We contrast them with passive stereo and learning-based monocular depth, which rely on ambient texture or data-driven priors {cite('scharstein2002','eigen2014','godard2017')}. Passive methods have improved rapidly, but active sensors remain the default in many deployed mechatronic systems because they provide dense or semi-dense metric depth on weakly textured surfaces and under changing indoor lighting {cite('khoshelham2012','halmet2019','sarbolandi2015')}.",
    ))
    b.append((
        "p",
        f"The 2010 Microsoft Kinect showed that dense indoor depth could be obtained at consumer cost {cite('khoshelham2012','shotton2011')}. That device, and the algorithms built on it, moved RGB-D mapping and human pose estimation out of specialized laboratories {cite('newcombe2011','izadi2011','henry2012')}. Subsequent products reduced size and power (mobile ToF and active-stereo modules) and then extended range (solid-state LiDAR), which changed the set of machines that could carry a depth sensor {cite('keselman2017','gyongy2022','ho2022','roriz2022')}.",
    ))
    b.append((
        "p",
        f"Several surveys already cover pieces of this landscape (Table 1). Lock-in ToF cameras {cite('foix2011')}, ToF range imaging more broadly {cite('horaud2016','kolb2010','zanuttigh2016')}, structured-light metrology {cite('zhang2012sl','geng2011')}, comparative RGB-D tests {cite('halmet2019','giancola2018')}, visual SLAM {cite('cadena2016','taketomi2017','barros2022','wang2024slam')}, event cameras {cite('gallego2022')}, and LiDAR hardware {cite('ho2022','roriz2022','li2020lidar','raj2020')} are all better treated in those sources than they can be in one paper. What is still useful, and what this paper attempts, is not another first-principles optics tutorial. It is a system-level map that answers a design question: which physical generation of depth sensor made which mechatronic function practical, and which residual errors still dominate in the field.",
    ))
    b.append((
        "table",
        (
            "Table 1. Closest prior surveys and the slice added here. This paper is complementary, not a replacement.",
            ["Prior survey", "Main focus", "What a mechatronic designer still has to assemble"],
            [
                [f"Foix et al.; Horaud et al. {cite('foix2011','horaud2016')}", "ToF camera physics and calibration", "How iToF/dToF sit next to SL and LiDAR on a robot"],
                [f"Zhang; Geng {cite('zhang2012sl','geng2011')}", "Structured-light metrology", "When a fringe scanner is the wrong robot sensor"],
                [f"Halmetschlager-Funek et al. {cite('halmet2019')}", "Empirical RGB-D ranking", "Estimator and application consequences"],
                [f"Cadena et al.; later V-SLAM surveys {cite('cadena2016','barros2022')}", "SLAM algorithms", "Which depth front-end the estimator assumes"],
                [f"Ho et al.; Roriz et al. {cite('ho2022','roriz2022')}", "Solid-state / automotive LiDAR", "Indoor RGB-D and factory cells"],
                [f"Gallego et al. {cite('gallego2022')}", "Event cameras", "When event depth is worth the stack change"],
            ],
        ),
    ))

    b.append(("h2", "1.1 Scope and review method"))
    b.append((
        "p",
        "The paper is a narrative review, not a PRISMA systematic review. We screened IEEE Xplore, Scopus, Web of Science, and major publisher libraries for English-language work from approximately 2001 to early 2025. Search phrases combined structured light, time-of-flight camera, RGB-D, solid-state LiDAR, depth completion, visual-inertial odometry, RGB-D SLAM, bin picking, collaborative robot, and UAV obstacle avoidance. Priority was given to seminal hardware and calibration papers, widely cited surveys, comparative evaluations that report quantitative error, and application studies in which the depth modality is specified. Product datasheets are used only as supporting context and are not treated as peer-reviewed evidence. Mechanical spinning LiDAR is discussed only as a baseline for solid-state designs. Biomedical and purely cinematic uses of depth cameras are outside the scope.",
    ))

    b.append(("h2", "1.2 Contributions and organization"))
    b.append((
        "p",
        "The paper makes four modest contributions. First, it compares structured light, active stereo, iToF, dToF, and solid-state LiDAR by principle, reported range and error, and typical mechatronic role. Second, it links raw depth artifacts to the estimation layers that machines actually run. Third, it organizes applications by sensing requirement rather than by market category. Fourth, it separates mitigations that already ship from ideas that remain research. Section 2 reviews hardware. Section 3 reviews enabling algorithms. Section 4 reviews applications. Section 5 discusses open problems and outlook. Section 6 concludes.",
    ))

    b.append(("h1", "2. Technological evolution of depth vision sensors"))
    b.append((
        "p",
        "A useful first cut is the operating envelope: the combination of range, spatial resolution, ambient-light tolerance, size, and cost that a machine can actually use. Figure 1 summarizes the three families that dominate current mechatronic designs.",
    ))
    b.append(("fig", FIG / "fig1_operating_envelopes.png"))
    b.append((
        "caption",
        "Figure 1. Typical operating envelopes of structured light / active stereo, ToF cameras, and solid-state LiDAR, together with the mechatronic roles that follow from those envelopes. Bounds are qualitative summaries of the literature in Table 2, not guarantees for a particular device.",
    ))

    b.append(("h2", "2.1 Structured light and active stereo"))
    b.append((
        "p",
        f"Structured-light sensors project a known pattern (dots, stripes, or time-varying fringes) and recover depth by triangulation between the projector and one or more cameras {cite('zhang2012sl','geng2011')}. If f is the focal length, B the baseline, and d the observed disparity, the pinhole relation is Z = fB/d. Error in disparity therefore grows into a range error that increases approximately with Z squared {cite('khoshelham2012')}. Industrial systems usually prefer sequential Gray-code plus phase-shifting fringes because the absolute unwrapping is robust and the phase gives sub-pixel disparity {cite('zhang2012sl','geng2011')}. Fourier-transform profilometry trades some robustness for a single-shot capture, which matters on moving parts. Industrial fringe-projection systems exploit this geometry at short range and can reach tens of micrometres to sub-millimetre accuracy on cooperative surfaces {cite('zhang2012sl')}. The price of that accuracy is a controlled standoff, a cooperative (or at least non-specular) surface, and a workspace that fits the calibrated volume.",
    ))
    b.append((
        "p",
        f"Consumer devices traded metrology-grade projectors for a static pseudo-random speckle and on-chip matching. Kinect v1 is the canonical example: a near-infrared (NIR) projector, an infrared camera, and a colour camera. Khoshelham and Elberink showed that its random depth error grows from a few millimetres near the sensor to about 4 cm near 5 m, while axial point spacing can reach about 7 cm at that range {cite('khoshelham2012')}. Those numbers explain both the success of KinectFusion-style indoor reconstruction {cite('newcombe2011','izadi2011')} and the unsuitability of the same sensor as an outdoor navigation camera.",
    ))
    b.append((
        "p",
        f"Active stereo keeps triangulation but replaces a coded single-camera pattern with a stereo pair plus a texture projector. Intel RealSense R200/D400-class cameras follow this route {cite('keselman2017')}. Because matching runs on two infrared images, the system can still return depth when the projector is weak or switched off, which improves outdoor behaviour relative to first-generation speckle sensors {cite('keselman2017','halmet2019')}. The cost is compute for stereo matching and a stronger dependence on calibration {cite('scharstein2002','keselman2017')}. Indoor tests across structured-light, active-stereo, and ToF units confirm that no single consumer camera dominates bias, precision, lateral noise, lighting, and multi-sensor interference at once {cite('halmet2019','giancola2018')}.",
    ))

    b.append(("h2", "2.2 Time-of-flight cameras and mobile miniaturization"))
    b.append((
        "p",
        f"A ToF pixel estimates range from the travel time of light. Indirect ToF (iToF; lock-in or continuous-wave) measures the phase shift of a modulated source {cite('lange2001','foix2011')}. For a modulation frequency f_m the unambiguous range is on the order of c/(2 f_m); a typical 30 MHz tone wraps near 5 m, which is why multi-frequency operation appears on industrial iToF cameras {cite('foix2011','horaud2016')}. Direct ToF (dToF) timestamps a short pulse, often with single-photon avalanche diode (SPAD) arrays and time-to-digital converters {cite('niclass2013','gyongy2022','horaud2016')}. iToF became practical in compact cameras because a single illuminator and a single sensor replace a precision stereo baseline {cite('foix2011','sarbolandi2015')}. Reported indoor working distances for consumer iToF, including Kinect v2, are typically 0.5-4.5 m {cite('sarbolandi2015','lachat2015','pagliari2015')}. Side-by-side studies of Kinect v1 and v2 show that the ToF unit reduced some structured-light artifacts (texture dependence, multi-device interference) while introducing others (multipath in corners, flying pixels, wiggling) {cite('sarbolandi2015','lachat2015','pagliari2015')}. Sunlight, multipath, and flying pixels remain first-order limitations {cite('sarbolandi2015','lachat2015','kadambi2013')}.",
    ))
    b.append((
        "p",
        f"The same physics explains the mobile-ToF wave of the 2010s. A phase camera does not need a wide mechanical baseline, so it fits a phone or an embedded robot head. Early mobile iToF modules were lower in spatial resolution than structured light but more convenient at 2-5 m for augmented reality and coarse scene layout {cite('horaud2016','gyongy2022')}. dToF SPAD arrays later improved ambient-light rejection and power per unit of range, at the expense of histogram memory and, often, spatial resolution {cite('gyongy2022')}. Gyongy, Dutton, and Henderson review the dToF signal chain and show why on-chip histogram compression, not only detector quantum efficiency, now limits array size {cite('gyongy2022')}.",
    ))

    b.append(("h2", "2.3 Solid-state LiDAR and the long-range shift"))
    b.append((
        "p",
        f"Once the task leaves the room (warehouse aisles, yards, roads, bridge girders) consumer RGB-D cameras run out of photons and out of unambiguous range. Mechanical spinning LiDAR already solved long-range ranging. Solid-state and semi-solid designs try to keep that range while removing a bulky rotator {cite('ho2022','roriz2022','li2020lidar','raj2020')}. MEMS mirrors scan a laser with a small moving mass and are the most commercially mature semi-solid option. Flash LiDAR illuminates a patch at once and is closer to a ToF camera, with range and resolution set by peak power and pixel count. Optical phased arrays and metasurface beam steerers aim at a fully solid-state scanner {cite('kim2021nano','park2021slm','sun2013opa','poulton2017','zhang2022mems')}. Large-scale silicon photonic arrays and MEMS-on-photonics demonstrators show that chip-scale beam steering is no longer only a laboratory sketch {cite('sun2013opa','zhang2022mems')}. For mechatronic integration the practical facts are simpler: solid-state units are smaller and potentially more robust to vibration, but they are still sparse compared with RGB-D, still expensive at automotive grade, and still require careful time synchronization with cameras and IMUs {cite('roriz2022','li2020lidar','debeunne2020')}. Automotive surveys also stress eye-safety, rain/fog backscatter, and the need for a perception stack that does not treat a sparse cloud as if it were a Kinect frame {cite('roriz2022','li2020lidar')}.",
    ))
    b.append((
        "p",
        "Table 2 collects order-of-magnitude figures reported in the literature. Values are typical envelopes, not guarantees for a particular serial number. Two design rules follow. First, do not treat \"depth camera\" as one specification: a sensor that is excellent for bin picking is usually the wrong sensor for a 30 m warehouse aisle. Second, hardware generations did not replace one another; they split the operating envelope. Structured light still wins close-range accuracy. ToF wins compactness at room scale. Solid-state LiDAR wins range. Mechatronic architectures increasingly carry more than one of them.",
    ))
    b.append((
        "p",
        f"A practical selection sequence used in many robot shops is: write down the minimum and maximum range, the worst lighting, the worst surface, the allowed mass and watts, and the safety integrity level. Only then open a catalogue. Indoor rooms with matte walls still suit RGB-D {cite('khoshelham2012','keselman2017','halmet2019')}. Fixed cells with metal parts still suit industrial structured light {cite('zhang2012sl')}. Yards and roads still suit LiDAR, usually fused with cameras {cite('roriz2022','debeunne2020','yeong2021')}. If two of those worlds appear on one machine, budget two sensors and a calibration procedure, not a single \"universal\" depth camera.",
    ))
    b.append((
        "p",
        f"Three short examples make the same point. A bin-picking cell with a 1.2 m standoff and oily steel parts should start from industrial structured light, a 6-DoF pose estimator, and a compliant grasp, not from a 100 m LiDAR {cite('zhang2012sl','correll2018','tenpas2017')}. An indoor delivery base that must see a pallet toe and a person in a corridor should start from a wide RGB-D camera plus a two-dimensional safety LiDAR and a visual-inertial estimator {cite('keselman2017','fankhauser2015','campos2021')}. A bridge-inspection UAV that must hold a 5-15 m standoff in wind should start from a lightweight solid-state ranger, an IMU, and a compact RGB inspector, and should not expect a phone-class ToF module to carry the ranging load {cite('floreano2015','spencer2019','ho2022')}.",
    ))

    b.append((
        "table",
        (
            "Table 2. Representative operating envelopes of active depth sensors used in mechatronics. Numbers are typical ranges reported in peer-reviewed evaluations or hardware surveys; product variants differ.",
            ["Family", "Principle", "Typical usable range", "Reported depth error (order)", "Spatial sampling", "Main field weakness", "Typical role", "Sources"],
            [
                ["Structured light (consumer)", "Static-pattern triangulation", "0.5-4 m", "mm near field; ~4 cm random error near 5 m (Kinect v1)", "Dense VGA-class", "Sunlight; shiny or absorbing surfaces", "Indoor mapping, HRI prototypes", cite("khoshelham2012", "halmet2019", "sarbolandi2015")],
                ["Fringe / industrial SL", "Phase-shifting triangulation", "0.1-2 m (setup-dependent)", "tens of um to sub-mm", "Very dense", "Workspace size; ambient light", "In-line metrology, bin picking", cite("zhang2012sl", "geng2011")],
                ["Active stereo", "IR stereo + texture projector", "0.2-10 m (best ~0.3-3 m)", "cm-level, lighting-dependent", "Dense HD-class", "Calibration; compute; texture holes", "Indoor / semi-outdoor robots", cite("keselman2017", "halmet2019")],
                ["iToF camera", "CW phase", "0.5-5 m", "cm-level; multipath bias", "Dense QVGA-VGA", "Multipath; sunlight; flying pixels", "Mobile robots, mid-range HRI", cite("foix2011", "horaud2016", "sarbolandi2015", "lachat2015")],
                ["dToF SPAD", "Pulsed photon timing", "~1-10 m consumer; longer if laser-class", "cm-level; better ambient rejection than iToF", "Often coarser", "Histogram memory; pile-up", "AR, short-range robots", cite("gyongy2022", "niclass2013")],
                ["Solid-state / MEMS LiDAR", "Scanned or flash ToF", "10-200+ m", "few cm (range- and target-dependent)", "Sparse points", "Cost; weather; boresight", "Outdoor AMR, UAV, vehicle", cite("ho2022", "roriz2022", "li2020lidar")],
            ],
        ),
    ))

    b.append(("h1", "3. Enabling technologies: from raw depth to a state estimate"))
    b.append((
        "p",
        "Raw depth is not a pose, a mesh, or a grasp. This section reviews the software layers that mechatronic systems insert between the sensor and the controller.",
    ))

    b.append(("h2", "3.1 Depth data processing and enhancement"))
    b.append((
        "p",
        f"Consumer and automotive depth images share a small set of artifacts: impulse noise, invalid pixels (holes) on occlusions, black or specular surfaces, flying pixels on depth edges, and ToF multipath {cite('foix2011','halmet2019','sarbolandi2015')}. Classical spatial median filters and temporal averaging remain the first firmware line of defence. When a registered RGB image is available, joint bilateral or guided filtering uses colour edges to protect object boundaries while smoothing planar interiors {cite('kopf2007')}. These filters are cheap enough for embedded GPUs. They do not invent missing geometry.",
    ))
    b.append((
        "p",
        f"Depth completion does. Early methods inpainted by diffusion or multi-view geometry. Learning-based completion trained on RGB-D or RGB-plus-sparse-LiDAR pairs now dominates the literature {cite('silberman2012','eigen2014','laina2016','godard2017','godard2019','uhrig2017','ma2018')}. Eigen et al. showed that a multi-scale network can predict depth from a single RGB image {cite('eigen2014')}; later residual and self-supervised models reduced the need for dense ground truth {cite('laina2016','godard2017','godard2019')}. Indoor work still leans on NYU-Depth v2-style labelled apartments {cite('silberman2012')}. Outdoor work leans on KITTI-style projected LiDAR, which is sparse and biased toward the road plane {cite('uhrig2017')}. For that setting, Uhrig et al. introduced sparsity-invariant convolutions {cite('uhrig2017')}, and Ma and Karaman showed that even a few hundred metric samples plus RGB yield a dense metric map {cite('ma2018')}. Later non-local and transformer architectures improve large holes by using long-range context, at a cost that still challenges small onboard computers {cite('guo2021pc')}. A mechatronic reading of these papers is that completion is a good virtual sensor for visualization and mid-level planning, and a bad sole input to a safety-rated stop.",
    ))
    b.append((
        "p",
        "Table 3 rates common artifacts by industrial maturity. The important systems point is that learning-based completion is not yet a drop-in safety sensor: it can look plausible while being metrically wrong on transparent, thin, or never-seen objects.",
    ))
    b.append((
        "table",
        (
            "Table 3. Common depth artifacts and the maturity of current mitigations.",
            ["Artifact", "Dominant cause", "Typical mitigation", "Maturity"],
            [
                ["Impulse noise", "Low SNR, scattering", "Median filter; temporal averaging", "Mature (on-chip / firmware)"],
                ["Holes / invalid pixels", "Occlusion, IR absorption, specularity, out-of-range", "RGB-guided completion; multi-view fusion", "Emerging for real-time embedded use"],
                ["Flying pixels / motion blur", "Finite integration time", "Shorter exposure; IMU-aided deblur; event sensing", "Mixed: IMU fusion common; event methods still research"],
                ["Multipath (ToF)", "Indirect returns in corners and shiny rooms", "Multi-frequency modulation; coded ToF; model-based subtraction", f"Maturing on high-end iToF; still hard on cheap single-frequency units {cite('foix2011','kadambi2013')}"],
                ["Sunlight saturation", "Ambient NIR swamping the source", "Narrow-band filters; higher peak power; dToF / LiDAR; radar fill-in", f"Partly solved at LiDAR-class power; unsolved for cheap RGB-D outdoors {cite('halmet2019','sarbolandi2015')}"],
            ],
        ),
    ))

    b.append(("h2", "3.2 Sensor fusion and state estimation"))
    b.append((
        "p",
        "A depth camera alone is a poor navigation sensor: it is biased, partially observed, and asynchronous with the actuators. Fusion with an inertial measurement unit (IMU), wheel odometry, and/or a colour camera is therefore the default architecture on mobile robots and UAVs (Figure 2).",
    ))
    b.append(("fig", FIG / "fig2_sensor_fusion_stack.png"))
    b.append((
        "caption",
        "Figure 2. A typical estimation stack on a mobile robot. Depth is one residual source among several. The optional dense or semantic layer is expensive and is often omitted on large-scale outdoor maps.",
    ))
    b.append((
        "p",
        f"Loose coupling treats each sensor as a black-box pose or twist and fuses them in an extended or unscented Kalman filter. The implementation is modular and cheap; the estimate is statistically suboptimal and cannot correct inner calibration errors {cite('thrun2005')}. Tight coupling, as in keyframe visual-inertial odometry (VIO), jointly optimizes visual residuals and IMU preintegration in a sliding window {cite('leutenegger2015','forster2017','qin2018','bloesch2015')}. Adding metric depth yields visual-inertial-depth odometry: depth removes the monocular scale-gauge ambiguity and supplies geometric constraints in low-texture rooms where VIO would otherwise drift or fail {cite('cadena2016','newcombe2011','qin2018')}.",
    ))
    b.append((
        "p",
        f"Dense RGB-D fusion, from KinectFusion through ElasticFusion and BundleFusion, maintains a truncated signed distance function (TSDF) or surfel map for close-range interaction {cite('newcombe2011','whelan2015','dai2017')}. The KinectFusion loop is still the mental model: track the live depth against the model, integrate the new frame into a volume, and raycast a synthetic depth for the next track {cite('newcombe2011','izadi2011')}. ElasticFusion dropped the explicit pose graph in favour of dense deformation; BundleFusion restored global consistency with on-the-fly reintegration {cite('whelan2015','dai2017')}. Those maps are excellent for a tabletop and expensive for a warehouse. Graph-based SLAM adds loop closures so that local odometry does not accumulate without bound {cite('cadena2016','thrun2005')}. RGB-D SLAM systems and the TUM RGB-D benchmark made this stack reproducible {cite('henry2012','endres2014','sturm2012')}. Later systems (ORB-SLAM2/3, Kimera) combine sparse or semi-dense tracking with optional metric-semantic mapping and multi-robot extensions {cite('murartal2017','campos2021','rosinol2020','tian2022')}. ORB-SLAM3 in particular folded visual-inertial and multi-map operation into a library that many robot teams actually run {cite('campos2021')}. Direct methods such as LSD-SLAM showed that dense photometric residuals can replace sparse features when exposure is well modelled {cite('engel2014')}. Visual-LiDAR fusion surveys document the complementary pair used outdoors: cameras for semantics and texture, LiDAR for metric structure and lighting invariance {cite('debeunne2020','yeong2021')}.",
    ))
    b.append((
        "p",
        f"Point-cloud infrastructure (PCL, iterative closest point, OctoMap, Voxblox) determines whether these estimators can run online on a real chassis {cite('rusu2011','besl1992','hornung2013','oleynikova2017')}. For control engineers the interface that matters is usually a pose with covariance plus a costmap, not a research SLAM paper. Table 4 compares the fusion patterns that those libraries usually sit under.",
    ))
    b.append((
        "table",
        (
            "Table 4. Fusion patterns used in mechatronic state estimation.",
            ["Pattern", "Typical inputs", "Estimator", "Output", "Fits", "Main cost"],
            [
                ["Loose coupling", "Depth pose, IMU, wheels", "EKF / UKF", "6-DoF pose", "Structured indoor bases", "Easy, less accurate"],
                ["Tight VIO / VIDO", "RGB, IMU, depth", "Sliding-window BA", "Pose + sparse map", "Drones, AR, agile bases", "Calibration and CPU"],
                ["Dense RGB-D", "Depth + RGB", "TSDF / surfels", "Mesh or volume", "Manipulation, inspection", "Memory and scale"],
                ["Pose-graph SLAM", "Any odometry + loops", "Graph optimization", "Globally consistent map", "Buildings, multi-floor", "Place recognition"],
                ["Visual-LiDAR", "Camera + LiDAR + IMU", "Tight or loosely fused SLAM", "Large-scale metric map", "Outdoor AMR / UAV", f"Sync and extrinsics {cite('debeunne2020')}"],
            ],
        ),
    ))

    b.append(("h2", "3.3 From geometry to semantics"))
    b.append((
        "p",
        f"Once a metric cloud exists, the next questions are what the object is and where the robot may go. Classical 3D detectors used hand-crafted histograms. Current networks consume raw points, voxels, or range images {cite('qi2017pointnet','qi2017pn2','guo2021pc')}. Semantic segmentation labels every point; instance segmentation separates two chairs of the same class. RGB remains useful for texture and class priors; depth remains useful for scale and occlusion. Pose-estimation benchmarks such as BOP and methods such as PoseCNN made 6-DoF object pose a measurable industrial problem rather than a one-off demonstration {cite('hodan2018','xiang2018')}.",
    ))
    b.append((
        "p",
        f"Beyond labels, mechatronic systems care about affordances: surface normals and curvature for grasp stability, traversable floor versus negative obstacles, and dynamic scene graphs that persist over time {cite('rosinol2020','tian2022','tenpas2017')}. These layers are not unique to depth sensors, but they become cheaper when scale is observed rather than inferred. In dynamic scenes, geometric SLAM without semantics remains brittle; recent surveys document the shift toward semantic and robust dynamic SLAM {cite('wang2024slam','placed2023')}.",
    ))

    b.append(("h1", "4. Applications in mechatronic systems"))
    b.append((
        "p",
        "The same sensor physics appears as different requirements once a machine has a job. This section organizes applications by the depth property that is actually spent.",
    ))

    b.append(("h2", "4.1 Industrial automation and precision manufacturing"))
    b.append((
        "p",
        f"Bin picking and unstructured part handling spend spatial resolution and short-range accuracy. A sensor above the bin produces a point cloud; a pose estimator returns a 6-DoF grasp; a compliant gripper absorbs the residual error {cite('tenpas2017','mahler2017','zeng2017','hodan2018','xiang2018','correll2018')}. Grasp-from-point-cloud methods (GPD, Dex-Net and their successors) showed that a depth image plus analytic or learned grasp scores can propose suction or parallel-jaw contacts without a full CAD model of every SKU {cite('tenpas2017','mahler2017')}. When the part identity is known, multi-view pose networks of the Amazon Picking Challenge generation, and later PoseCNN-style estimators scored on BOP, turn the same cloud into a 6-DoF object pose {cite('zeng2017','xiang2018','hodan2018')}. The first Amazon Picking Challenge made the systems nature of this problem obvious: teams that treated perception, planning, and gripping as separately optimized modules underperformed relative to tightly integrated stacks, and suction often beat anthropomorphic hands {cite('correll2018')}. Structured light and laser triangulation still dominate when parts are metallic, overlapping, and closer than about two metres {cite('zhang2012sl','correll2018')}. RGB is typically fused for class identity; force and torque close the last millimetres.",
    ))
    b.append((
        "p",
        f"In-line metrology spends repeatability and speed. A fringe-projection or ToF snapshot is compared with a computer-aided design (CAD) model. Fringe systems own the micrometre-to-sub-millimetre band {cite('zhang2012sl','geng2011')}. ToF cameras are used when the assembly is large and a few millimetres of error are acceptable, because a full-field frame arrives without a scanning gantry {cite('foix2011','horaud2016')}. Vibration of the line is then a fusion problem (encoders and triggers), not only an optics problem.",
    ))
    b.append((
        "p",
        f"Automated guided vehicles (AGVs) and autonomous mobile robots (AMRs) spend field of view and vertical coverage. A two-dimensional safety LiDAR sees a plane; a wide RGB-D camera or solid-state LiDAR sees pallets, overhangs, and people who lean into the aisle {cite('halmet2019','yeong2021','fankhauser2015')}. Table 5 summarizes the pairing.",
    ))
    b.append((
        "table",
        (
            "Table 5. Industrial uses mapped to sensing requirements.",
            ["Task", "Preferred depth family", "First-order requirement", "Usual extra sensors"],
            [
                ["Bin picking", "Industrial SL / laser triangulation", "Sub-mm to few-mm, high density", "RGB; force/torque"],
                ["Assembly guidance", "SL or stereo at fixed standoff", "Low latency, stable extrinsics", "Joint encoders; IMU"],
                ["Full-field inspection", "Fringe (precise) or ToF (fast)", "Repeatability, line triggering", "Conveyor encoder; RGB"],
                ["AMR 3D obstacle sense", "Wide RGB-D and/or solid-state LiDAR", "Field of view, frame rate, human safety", "2D safety LiDAR; IMU; wheels"],
            ],
        ),
    ))

    b.append(("h2", "4.2 Autonomous mobile robots for service and logistics"))
    b.append((
        "p",
        f"Indoor service robots made RGB-D SLAM a product feature. Devices such as RealSense D400-class cameras are chosen because they balance size, power, software support, and indoor range {cite('keselman2017','halmet2019')}. Keselman et al. documented the optical and matching behaviour of the R200 and D400 families, including the fact that projector texture is an aid rather than a requirement {cite('keselman2017')}. The algorithmic backbone is well documented: RGB-D odometry, loop closure, and a metric map {cite('henry2012','endres2014','sturm2012','murartal2017')}. Fankhauser et al. modelled Kinect v2 specifically as a navigation sensor and showed where its systematic bias matters for terrain {cite('fankhauser2015')}. The remaining failures are physical. Stairs and negative obstacles (curbs, open shafts) are invisible to a waist-height two-dimensional LiDAR. A forward depth camera can reconstruct them if the near field is valid and the robot is slow enough for the integration time {cite('fankhauser2015')}. Outdoor last-metre robots meet sunlight and long range, which is why the same software stack often grows a LiDAR or radar {cite('debeunne2020','yeong2021')}.",
    ))
    b.append((
        "p",
        f"Human-aware navigation is a semantic layer on the same geometry. Depth supplies a metric body hull; RGB pose estimators supply intent cues {cite('shotton2011','sarbolandi2015')}. Socially acceptable clearance is then a planner parameter, not a new sensor. Active SLAM surveys discuss how a robot should move to keep that map healthy, which is a planning problem built on the same depth front-end {cite('placed2023')}.",
    ))

    b.append(("h2", "4.3 UAVs and aerial robotics"))
    b.append((
        "p",
        f"On a small UAV the payload budget is measured in tens of grams and a few watts {cite('floreano2015')}. That constraint, more than any algorithm, explains why lightweight depth cameras and solid-state LiDARs appear on inspection drones while automotive-grade spinning units do not.",
    ))
    b.append((
        "p",
        f"Obstacle avoidance is the first use. Depth gives a metric stop distance in GPS-denied corridors, forests, or plant rooms {cite('floreano2015','muller2023','barry2018')}. Barry, Florence, and Tedrake demonstrated tree avoidance at up to 14 m/s with a pushbroom stereo front-end running at 120 Hz on a small airframe {cite('barry2018')}. That result is a reminder that geometric ranging, not a particular branded depth camera, is the requirement; stereo, RGB-D, and LiDAR are interchangeable only after latency, weight, and lighting are checked. Event-camera and event-stereo systems push latency into the microsecond regime for fast approach speeds {cite('gallego2022','falanga2020','zhou2021evo','he2024')}. Falanga et al. used event cameras to dodge dynamic obstacles that a frame-based pipeline would blur {cite('falanga2020')}. Miniature platforms have demonstrated onboard depth-based avoidance with tight compute envelopes {cite('muller2023')}.",
    ))
    b.append((
        "p",
        f"Mapping and inspection is the second use. Photogrammetry from RGB already builds impressive models {cite('nex2014','colomina2014')}. Depth or LiDAR is added when the operator needs metric scale, vegetation penetration, or a flight path that stays a fixed standoff from a girder {cite('nex2014','colomina2014','spencer2019')}. Civil-infrastructure reviews show that the bottleneck is rarely whether a point cloud can be built. It is converting that cloud into defect locations that an engineer will trust {cite('spencer2019')}.",
    ))
    b.append(("fig", FIG / "fig3_uav_inspection_pipeline.png"))
    b.append((
        "caption",
        "Figure 3. Representative UAV inspection pipeline assembled from published practice. This figure is a literature synthesis, not a system designed in the present paper.",
    ))
    b.append((
        "p",
        f"Figure 3 describes a representative architecture assembled from published inspection practice, not a system designed in this paper. A bridge-inspection UAV typically carries a long-range ranging sensor (solid-state LiDAR or equivalent), a high-resolution RGB camera, and an IMU {cite('nex2014','colomina2014','spencer2019')}. Onboard software fuses range and inertia into a local metric volume and runs a lightweight network on RGB for component and surface-defect cues {cite('spencer2019')}. The aircraft uplinks an annotated model and geotagged defect hypotheses rather than raw multi-sensor video. The design is a bandwidth and trust design: inspectors re-photograph the flagged regions instead of watching hours of flight video. Multi-UAV structure-from-motion benefits from the same metric scale cue. Depth does not replace inter-vehicle communication, but it reduces the need for dense ground control {cite('nex2014','colomina2014')}.",
    ))

    b.append(("h2", "4.4 Collaborative robots and human-robot interaction"))
    b.append((
        "p",
        f"Collaborative cells fail first on safety, then on programming time {cite('villani2018','ajoudani2018','haddadin2017')}. Depth cameras address both, with limits that must be stated.",
    ))
    b.append((
        "p",
        f"Workspace monitoring. A ceiling or cell-side depth sensor builds a three-dimensional occupancy of the shared volume. Speed-and-separation monitoring, as framed by ISO/TS 15066, can then slow or stop the arm when a person enters a warning or protective zone {cite('iso15066','villani2018')}. Three-dimensional monitoring is more complete than a light curtain because it can shrink the protective volume as the arm slows and can see a person who leans over a fence. A consumer RGB-D camera is not automatically a safety-rated device. Certified implementations still need a safety controller, defined failure modes, and usually a redundant sensing channel {cite('villani2018','haddadin2017','iso15066')}. Surveys of industrial human-robot collaboration treat safety and the user interface as the two bottlenecks that decide whether a cobot is actually used, not whether a depth demo exists {cite('villani2018','ajoudani2018')}. Collision detection on the arm itself remains necessary because vision cannot see inside the contact {cite('haddadin2017')}.",
    ))
    b.append((
        "p",
        f"Programming by demonstration. Tracking a tool or a marked workpiece in 3D lets a non-expert move the robot through a path {cite('villani2018','ajoudani2018')}. Structured light at short range is usually sufficient. The hard parts are correspondence, occlusion by the operator, and converting a human demonstration into a collision-free, force-feasible program. Gesture and activity cues can distinguish a small set of commands or detect that a station is ready for the next part {cite('shotton2011','villani2018')}. This is useful. It is not a substitute for a well-designed hardware enable switch.",
    ))

    b.append(("h1", "5. Challenges and future perspectives"))
    b.append(("h2", "5.1 Persistent deployment problems"))
    b.append((
        "p",
        "The research literature sometimes treats remaining errors as temporary. Fielded mechatronic systems suggest otherwise. Table 6 separates mitigations that already ship from ideas that remain research.",
    ))
    b.append((
        "p",
        f"Environment and materials. NIR-based cameras saturate in sunlight {cite('halmet2019','sarbolandi2015')}. Specular and transparent objects violate the single-bounce assumption and produce holes or biased ranges {cite('foix2011','kadambi2013')}. Coded and multi-frequency ToF can unmix some multipath, but they add capture time or hardware that a cheap module does not have {cite('kadambi2013','foix2011')}. Low-reflectance foam and black rubber starve the illuminator. Polarization, multi-frequency ToF, and radar fill-in help; none is universal. Comparative tests of ten indoor depth cameras remain the most useful reminder that material and lighting can reorder the ranking of otherwise similar devices {cite('halmet2019')}.",
    ))
    b.append((
        "p",
        f"Compute and power. Dense SLAM, TSDF fusion, and point-cloud networks are still expensive on a battery {cite('cadena2016','guo2021pc','gyongy2022')}. The illuminator, not only the GPU, shortens UAV endurance {cite('gyongy2022','floreano2015')}. Event-based and neuromorphic pipelines are promising where the scene is sparse in time {cite('gallego2022','falanga2020','lichtsteiner2008')}, but they require a different software stack.",
    ))
    b.append((
        "p",
        f"Calibration and time. Multi-sensor extrinsics drift with temperature and shock. A one-degree boresight error is negligible for a room-scale display and unacceptable for a 50 m LiDAR-camera fusion {cite('roriz2022','debeunne2020')}. Online self-calibration exists in research estimators {cite('qin2018','campos2021')}; it is not yet a maintenance-free commodity. Asynchronous streams and sensor dropouts can make a naively fused estimate worse than the best single sensor {cite('thrun2005','yeong2021')}.",
    ))
    b.append((
        "p",
        f"Interfaces and cost. Unlike USB webcams, depth devices still disagree on coordinate frames, distortion models, and confidence channels {cite('halmet2019','keselman2017')}. High-grade solid-state LiDAR remains expensive relative to the rest of a service robot {cite('roriz2022')}. Standardization would save more engineering time than another incremental denoiser.",
    ))
    b.append((
        "table",
        (
            "Table 6. Challenges and the honesty level of current mitigations.",
            ["Domain", "Concrete problem", "Pathway that already ships", "Pathway still in research"],
            [
                ["Environment", "Sunlight, glass, black parts", "dToF/LiDAR, multi-echo, radar", "Polarization / hyperspectral ToF"],
                ["Compute", "Dense 3D + semantics on-device", "NPU for 2D nets; sparse maps", f"Event + spiking co-design {cite('gallego2022','roy2019','davies2018')}"],
                ["Integration", "Extrinsics, time, dropouts", "Factory calibration; hardware sync", "Lifelong self-calibration"],
                ["Semantics", "Novel clutter, moving people", "Closed-set 3D detectors", "3D foundation models, Sim2Real"],
                ["Cost / API", "Proprietary frames, high unit cost", "ROS drivers; a few de-facto SDKs", "Safety-rated, interoperable depth"],
            ],
        ),
    ))

    b.append(("h2", "5.2 Outlook"))
    b.append((
        "p",
        f"Event-based and neuromorphic sensing. Asynchronous pixels report contrast changes at microsecond latency and high dynamic range {cite('lichtsteiner2008','gallego2022')}. Combined with pulsed illumination they can support low-power depth for high-speed robots {cite('falanga2020','he2024','zhou2021evo','rebecq2017','guo2024cmax')}. Co-design with spiking processors aims to cut the energy of spatial reasoning {cite('roy2019','davies2018')}. These systems will complement, not replace, frame-based RGB-D in the next product cycle.",
    ))
    b.append((
        "p",
        f"AI near the sensor. Depth completion and a first detection head are moving into image-signal processors and sensor stacks {cite('gyongy2022','eigen2014','ma2018')}. The engineering gain is bandwidth: a robot can ship a confidence-weighted cloud or a set of objects instead of a raw 30 Hz volume. The engineering risk is silent metric failure. Safety-related channels should keep a raw or lightly filtered range path.",
    ))
    b.append((
        "p",
        f"Richer fusion. Depth-RGB-IMU is already standard. Adding millimetre-wave radar (fog, rain, radial velocity) and thermal cameras is the practical next step, already visible in automotive datasets {cite('yeong2021','caesar2020')}. The unsolved part is a fusion integrity layer: knowing when to stop trusting a modality.",
    ))
    b.append((
        "p",
        f"Photonics and materials. Metalenses and other flat optics can shrink camera modules {cite('khorasaninejad2017')}. Chip-scale optical phased arrays and MEMS-on-photonics LiDAR attack the scanner itself {cite('sun2013opa','poulton2017','zhang2022mems')}. First-photon imaging and non-line-of-sight reconstructions show what is physically possible at extreme photon counts {cite('kirmani2014','otoole2018')}. They are not yet bill-of-materials options for a warehouse AMR.",
    ))
    b.append((
        "p",
        "Infrastructure sensing. Ceiling-mounted depth in factories and intelligent spaces can offload onboard mapping. The idea is sound. The obstacles are privacy, networking, and a shared metric frame that every vendor agrees to.",
    ))

    b.append(("h1", "6. Conclusion"))
    b.append((
        "p",
        "Depth vision in mechatronics did not evolve as a single replacement chain. Structured light made dense, inexpensive, close-range geometry ordinary. ToF made that geometry small enough for mobile heads and phones. Solid-state LiDAR made long-range ranging compatible with vibration-sensitive platforms. Algorithms (completion, tight-coupled odometry, RGB-D SLAM, and 3D semantics) converted those measurements into poses, maps, grasps, and safety zones.",
    ))
    b.append((
        "p",
        "The remaining limits are mostly physical and organizational: sunlight and materials, watts and memory, calibration, and fragmented interfaces. A next-generation system is unlikely to be one perfect depth camera. It is more likely to be a small set of complementary ranges, an estimator that knows its integrity, and, where possible, a shared map that the machine does not have to rebuild on every shift.",
    ))
    b.append((
        "p",
        "For practitioners, the operational conclusion is conservative. Choose the sensor by operating envelope, not by marketing generation. Budget calibration and lighting as first-class design items. Keep a metric, low-level range channel whenever the output can stop a motor.",
    ))

    b.append(("h1", "Author contributions"))
    b.append((
        "p",
        "Bo Zhang drafted the review, organized the literature, and prepared the comparative tables and figures. Hongchao Cui conceived the hardware-centered scope, revised the manuscript, and supervised the work. Both authors approved the final version.",
    ))
    b.append(("h1", "Conflicts of interest"))
    b.append(("p", "The authors declare no conflict of interest."))
    b.append(("h1", "Data availability"))
    b.append(("p", "No new datasets were generated. All cited sources are listed in the References."))

    b.append(("refs", None))
    return b


def blocks_to_docx(blocks: list[tuple], path: Path) -> None:
    doc = Document()
    style_doc(doc)
    for kind, payload in blocks:
        if kind == "title":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(12)
            add_text(p, payload, size=16, bold=True)
        elif kind == "authors":
            para(doc, payload, first_line=False, center=True, size=12, space_after=4)
        elif kind == "affil":
            for line in payload.split("\n"):
                para(doc, line, first_line=False, center=True, size=10, italic=True, space_after=2)
        elif kind == "corr":
            para(doc, payload, first_line=False, center=True, size=10, space_after=16)
        elif kind == "h1":
            heading(doc, payload, 1)
        elif kind == "h2":
            heading(doc, payload, 2)
        elif kind == "p":
            if payload.startswith("Keywords:"):
                para(doc, payload, first_line=False, italic=True, size=10)
            else:
                para(doc, payload)
        elif kind == "caption":
            caption(doc, payload)
        elif kind == "fig":
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(2)
            p.add_run().add_picture(str(payload), width=Inches(6.3))
        elif kind == "table":
            title, headers, rows = payload
            add_table(doc, headers, rows, title)
        elif kind == "refs":
            heading(doc, "References", 1)
            for i, key in enumerate(_order, 1):
                p = doc.add_paragraph()
                p.paragraph_format.left_indent = Inches(0.35)
                p.paragraph_format.first_line_indent = Inches(-0.35)
                p.paragraph_format.space_after = Pt(6)
                p.paragraph_format.line_spacing = 1.15
                add_text(p, f"[{i}] {BIB[key]}", size=10)
    doc.save(path)


def main() -> None:
    blocks = manuscript_blocks()
    unused = sorted(set(BIB) - set(_order))
    md_path = ROOT / "Zhang_Cui_Depth_Vision_Sensors_Review_revised.md"
    docx_path = ROOT / "Zhang_Cui_Depth_Vision_Sensors_Review_revised.docx"
    write_markdown(md_path, blocks)
    blocks_to_docx(blocks, docx_path)
    words = sum(len(p.split()) for k, p in blocks if k == "p" and isinstance(p, str))
    print(f"references cited: {len(_order)}")
    print(f"references unused: {len(unused)} -> {unused}")
    print(f"body word count (paragraphs only): {words}")
    print(f"wrote {md_path}")
    print(f"wrote {docx_path}")


if __name__ == "__main__":
    main()
