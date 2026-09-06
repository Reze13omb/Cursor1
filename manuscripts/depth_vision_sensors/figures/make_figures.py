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


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    print("wrote", list(OUT.glob("fig*.png")))
