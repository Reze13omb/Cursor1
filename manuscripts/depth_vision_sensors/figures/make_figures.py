#!/usr/bin/env python3
"""Publication-style figures for the depth-vision review."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parent
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.linewidth": 0.8,
        "figure.dpi": 200,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "savefig.facecolor": "white",
    }
)


def rounded(ax, x, y, w, h, text, fc, ec="#1f2937", fs=8, bold=False):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.08",
        facecolor=fc,
        edgecolor=ec,
        linewidth=0.9,
    )
    ax.add_patch(box)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        fontweight="bold" if bold else "normal",
        color="#111827",
        wrap=True,
    )


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=10,
            linewidth=0.9,
            color="#374151",
        )
    )


def fig1():
    fig, ax = plt.subplots(figsize=(10.2, 4.6))
    ax.set_xlim(0, 10.2)
    ax.set_ylim(0, 4.6)
    ax.axis("off")
    ax.set_title(
        "Active depth sensing: typical operating envelope and mechatronic role",
        fontsize=11,
        pad=8,
        fontweight="bold",
    )

    columns = [
        {
            "x": 0.25,
            "title": "Structured light\n& active stereo",
            "fc": "#DBEAFE",
            "items": [
                "Triangulation + known pattern",
                "Best: 0.2–2 m, sub-mm to cm",
                "Weak outdoors / strong NIR",
                "Role: bin picking, inspection,\nclose-range cobot cells",
            ],
        },
        {
            "x": 3.55,
            "title": "Time-of-Flight\n(iToF / dToF)",
            "fc": "#D1FAE5",
            "items": [
                "Phase or pulse timing",
                "Best: 0.3–5 m (to ~10 m dToF)",
                "Compact; multipath, sunlight",
                "Role: indoor robots, AR,\nmobile / mid-range HRI",
            ],
        },
        {
            "x": 6.85,
            "title": "Solid-state LiDAR\n(MEMS / flash / OPA)",
            "fc": "#FDE68A",
            "items": [
                "Scanned or flash ToF",
                "Best: 10–200+ m, sparse cloud",
                "Weather, cost, calibration",
                "Role: outdoor AMRs, UAVs,\nlong-range mapping",
            ],
        },
    ]
    for col in columns:
        rounded(ax, col["x"], 0.25, 3.05, 3.95, "", col["fc"], fs=8)
        ax.text(
            col["x"] + 1.525,
            3.75,
            col["title"],
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
        )
        for i, line in enumerate(col["items"]):
            ax.text(
                col["x"] + 0.16,
                3.15 - i * 0.7,
                "•  " + line,
                ha="left",
                va="top",
                fontsize=8,
            )
    fig.savefig(OUT / "fig1_operating_envelopes.png")
    plt.close(fig)


def fig2():
    fig, ax = plt.subplots(figsize=(10.4, 5.0))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 5.0)
    ax.axis("off")
    ax.set_title(
        "Typical multi-sensor estimation stack on a mobile robot",
        fontsize=11,
        pad=6,
        fontweight="bold",
    )

    sensors = [
        (0.25, 3.55, "RGB camera"),
        (0.25, 2.45, "Depth / RGB-D"),
        (0.25, 1.35, "IMU"),
        (0.25, 0.25, "Wheel odometry\n(optional)"),
    ]
    for x, y, t in sensors:
        rounded(ax, x, y, 2.15, 0.95, t, "#E0E7FF", fs=8, bold=True)
        arrow(ax, 2.45, y + 0.48, 3.15, 2.55)

    rounded(ax, 3.2, 1.85, 2.35, 1.7, "Front-end\nsync, undistort,\nfeature / residual", "#DBEAFE", fs=8, bold=True)
    arrow(ax, 5.55, 2.7, 6.2, 2.7)
    rounded(
        ax,
        6.25,
        1.7,
        2.45,
        2.0,
        "Estimator\nEKF / sliding window\n/ pose-graph SLAM",
        "#D1FAE5",
        fs=8,
        bold=True,
    )
    arrow(ax, 8.7, 2.7, 9.15, 2.7)
    rounded(ax, 9.15, 1.95, 1.1, 1.5, "Pose\n& map", "#FDE68A", fs=8, bold=True)

    rounded(
        ax,
        3.2,
        0.2,
        5.5,
        1.25,
        "Optional dense / semantic layer\nTSDF or occupancy map  ·  3D detection / segmentation  ·  costmap for planning",
        "#F3F4F6",
        fs=8,
    )
    arrow(ax, 7.45, 1.7, 6.0, 1.45)
    fig.savefig(OUT / "fig2_sensor_fusion_stack.png")
    plt.close(fig)


def fig3():
    fig, ax = plt.subplots(figsize=(10.4, 4.8))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    ax.set_title(
        "Representative UAV inspection pipeline reported in the literature",
        fontsize=11,
        pad=6,
        fontweight="bold",
    )

    boxes = [
        (0.2, 3.35, 2.3, 1.15, "Onboard sensors\nLiDAR / RGB-D\n+ RGB + IMU", "#DBEAFE"),
        (2.9, 3.35, 2.3, 1.15, "Local mapping\nTSDF / occupancy\n+ visual odometry", "#D1FAE5"),
        (5.6, 3.35, 2.3, 1.15, "Scene analysis\nsegmentation /\ncrack or defect cues", "#FDE68A"),
        (8.3, 3.35, 1.9, 1.15, "Compact report\nannotated 3D\n+ geotags", "#F3F4F6"),
    ]
    for i, (x, y, w, h, t, fc) in enumerate(boxes):
        rounded(ax, x, y, w, h, t, fc, fs=8, bold=True)
        if i < 3:
            arrow(ax, x + w, y + h / 2, boxes[i + 1][0], y + h / 2)

    rounded(
        ax,
        0.2,
        0.25,
        10.0,
        2.7,
        "",
        "#F9FAFB",
    )
    ax.text(
        5.2,
        2.55,
        "Why depth is kept in the loop (not RGB-only photogrammetry)",
        ha="center",
        fontsize=9,
        fontweight="bold",
    )
    notes = [
        "Metric scale without a dense set of ground control points",
        "Obstacle clearance in GPS-denied or cluttered approach paths",
        "A sparse long-range cloud plus RGB texture is cheaper to uplink than raw video",
        "Defect locations can be attached to a 3D model for repeat inspections",
    ]
    for i, n in enumerate(notes):
        ax.text(0.45, 2.1 - i * 0.45, "•   " + n, ha="left", va="center", fontsize=8.5)
    fig.savefig(OUT / "fig3_uav_inspection_pipeline.png")
    plt.close(fig)


def fig4_selection():
    fig, ax = plt.subplots(figsize=(10.6, 5.4))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    ax.set_title("Sensor-family selection from the operating envelope", fontsize=11, pad=6, fontweight="bold")
    rounded(ax, 3.7, 4.35, 3.2, 0.85, "Write range, lighting,\nsurface, mass, SIL", "#E0E7FF", fs=8, bold=True)
    rounded(ax, 0.25, 2.55, 3.0, 1.2, "Standoff < 2 m and\nsub-mm to few-mm?", "#DBEAFE", fs=8, bold=True)
    rounded(ax, 3.8, 2.55, 3.0, 1.2, "Indoor 0.3-5 m,\nsize/power limited?", "#D1FAE5", fs=8, bold=True)
    rounded(ax, 7.35, 2.55, 3.0, 1.2, "Outdoor / >10 m\nor strong sunlight?", "#FDE68A", fs=8, bold=True)
    rounded(ax, 0.25, 0.35, 3.0, 1.55, "Industrial structured light\nor laser triangulation\n+ RGB / F-T", "#DBEAFE", fs=8)
    rounded(ax, 3.8, 0.35, 3.0, 1.55, "RGB-D: active stereo\nor iToF/dToF\n+ IMU / 2D safety LiDAR", "#D1FAE5", fs=8)
    rounded(ax, 7.35, 0.35, 3.0, 1.55, "Solid-state or spinning\nLiDAR + camera + IMU\n(+ radar if weather)", "#FDE68A", fs=8)
    arrow(ax, 5.3, 4.35, 1.75, 3.75)
    arrow(ax, 5.3, 4.35, 5.3, 3.75)
    arrow(ax, 5.3, 4.35, 8.85, 3.75)
    arrow(ax, 1.75, 2.55, 1.75, 1.9)
    arrow(ax, 5.3, 2.55, 5.3, 1.9)
    arrow(ax, 8.85, 2.55, 8.85, 1.9)
    fig.savefig(OUT / "fig4_selection_flowchart.png")
    plt.close(fig)


def fig5_hw_function():
    fig, ax = plt.subplots(figsize=(10.6, 4.8))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 4.8)
    ax.axis("off")
    ax.set_title("What each hardware step made newly practical", fontsize=11, pad=6, fontweight="bold")
    rows = [
        (0.2, "#DBEAFE", "Consumer structured light\n(2010-)", "Dense indoor RGB-D mapping,\npose from depth, low-cost HRI labs"),
        (2.85, "#D1FAE5", "Compact iToF / active stereo\n(2014-)", "Mobile heads, AR, indoor AMRs\nwithout a stereo bench"),
        (5.5, "#FDE68A", "dToF SPAD / SSL\n(2018-)", "Outdoor metres, UAV standoff,\nwarehouse aisles"),
        (8.15, "#E0E7FF", "Event + photonics\n(emerging)", "Microsecond reaction; chip-scale\nbeam steering (not yet BOM)"),
    ]
    for x, fc, t, d in rows:
        rounded(ax, x, 2.55, 2.45, 1.9, t, fc, fs=8, bold=True)
        rounded(ax, x, 0.25, 2.45, 2.0, d, "#F9FAFB", fs=8)
        arrow(ax, x + 1.22, 2.55, x + 1.22, 2.25)
    fig.savefig(OUT / "fig5_hardware_functions.png")
    plt.close(fig)


def graphical_abstract():
    # MDPI GA: min 1100 x 560 (W x H). Export 2200 x 1120.
    fig = plt.figure(figsize=(11.0, 5.6), dpi=200)
    ax = fig.add_axes([0.03, 0.06, 0.94, 0.88])
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 5.6)
    ax.axis("off")
    ax.text(5.5, 5.25, "Active depth vision  →  estimators  →  mechatronic function", ha="center", fontsize=13, fontweight="bold")
    cols = [
        (0.25, "#DBEAFE", "Sense", "Structured light\nToF (iToF / dToF)\nSolid-state LiDAR"),
        (2.95, "#D1FAE5", "Estimate", "Completion & denoise\nVIO / RGB-D SLAM\nLiDAR-inertial odometry"),
        (5.65, "#FDE68A", "Act", "Bin picking / metrology\nIndoor AMR / cobot cell\nUAV inspect & avoid"),
        (8.35, "#E0E7FF", "Limit", "Sunlight & materials\nWatts, calibration\nIntegrity of fusion"),
    ]
    for x, fc, h, t in cols:
        rounded(ax, x, 1.15, 2.4, 3.55, "", fc, fs=9)
        ax.text(x + 1.2, 4.3, h, ha="center", fontsize=12, fontweight="bold")
        ax.text(x + 1.2, 2.7, t, ha="center", va="center", fontsize=9)
    ax.text(5.5, 0.45, "Choose by operating envelope, not by marketing generation", ha="center", fontsize=9, style="italic")
    fig.savefig(OUT / "graphical_abstract.png")
    plt.close(fig)


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4_selection()
    fig5_hw_function()
    graphical_abstract()
    print("wrote", sorted(p.name for p in OUT.glob("*.png")))
