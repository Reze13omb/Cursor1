#!/usr/bin/env python3
"""Figures for MECH 470 Lab 2 robotic sorting report."""

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def box(ax, x, y, w, h, text, fc="#F4F7FB", ec="#1F4E79", lw=1.2, fs=8.2, bold=False):
    p = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.012,rounding_size=0.04",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
    )
    ax.add_patch(p)
    ax.text(
        x + w / 2,
        y + h / 2,
        text,
        ha="center",
        va="center",
        fontsize=fs,
        fontweight="bold" if bold else "normal",
        color="#1A1A1A",
        wrap=True,
    )


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=10,
            linewidth=1.1,
            color="#333333",
        )
    )


def control_diagram():
    fig, ax = plt.subplots(figsize=(7.2, 4.15), dpi=180)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    box(ax, 0.15, 4.55, 2.35, 1.35, "Operator PBs\nStart  I1.0\nStop   I1.1\nReset  I1.2", fc="#E8F0FE")
    box(ax, 0.15, 2.55, 2.35, 1.55, "Robot feedback\nAt pickup/home\nAt painted/unpainted\nMoving  I0.4", fc="#E8F0FE")
    box(ax, 0.15, 0.35, 2.35, 1.7, "Shade sensor\nAnalogue IW64\nNORM_X / SCALE_X\n0–27648 → 0–10 V", fc="#E8F0FE")

    box(
        ax,
        3.15,
        1.55,
        3.7,
        3.35,
        "Siemens S7-1200\nCPU 1214C  |  OB1 LAD\n\nStep sequencer  MW40\nThreshold compare\nVacuum SET/RESET\nFault / empty flags",
        fc="#FFF6E5",
        lw=1.6,
        fs=8.4,
        bold=False,
    )

    box(ax, 7.45, 4.45, 2.4, 1.45, "Robot motion I/O\nQ0.0 Pickup\nQ0.1 Painted drop\nQ0.2 Unpainted\nQ0.3 Home", fc="#E9F7EF")
    box(ax, 7.45, 2.45, 2.4, 1.5, "End effector\nQ0.4 Illumination\nQ0.5 Vacuum", fc="#E9F7EF")
    box(ax, 7.45, 0.35, 2.4, 1.7, "HMI lamps\nRunning / Fault\nPainted / Empty", fc="#E9F7EF")

    arrow(ax, 2.5, 5.2, 3.15, 4.15)
    arrow(ax, 2.5, 3.3, 3.15, 3.3)
    arrow(ax, 2.5, 1.2, 3.15, 2.2)
    arrow(ax, 6.85, 4.15, 7.45, 5.1)
    arrow(ax, 6.85, 3.3, 7.45, 3.2)
    arrow(ax, 6.85, 2.2, 7.45, 1.2)

    ax.set_title("Figure 1. Control architecture of the robotic sorting cell", fontsize=10, pad=6, color="#1F4E79")
    fig.tight_layout()
    fig.savefig(OUT / "fig1_control_architecture.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


def sequence_diagram():
    fig, ax = plt.subplots(figsize=(7.2, 3.35), dpi=180)
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 5.4)
    ax.axis("off")
    fig.patch.set_facecolor("white")

    steps = [
        (0.2, 3.35, "0\nIdle"),
        (2.15, 3.35, "10\nHome"),
        (4.1, 3.35, "20\nPickup"),
        (6.05, 3.35, "30\nSettle\n1 s"),
        (8.0, 3.35, "40\nClassify"),
        (10.0, 3.35, "50\nVacuum\n1 s"),
    ]
    for x, y, t in steps:
        box(ax, x, y, 1.7, 1.45, t, fc="#F4F7FB", fs=7.6)

    box(ax, 8.0, 1.15, 1.7, 1.25, "90\nEmpty\nstop", fc="#FDEDEC", fs=7.6)
    box(ax, 10.0, 1.15, 1.7, 1.25, "60→70\nDrop &\nrelease", fc="#E9F7EF", fs=7.6)
    box(ax, 0.2, 1.15, 1.7, 1.25, "900\nFault", fc="#FDEDEC", fs=7.6)

    # main flow
    for x1, x2, y in [
        (1.9, 2.15, 4.05),
        (3.85, 4.1, 4.05),
        (5.8, 6.05, 4.05),
        (7.75, 8.0, 4.05),
        (9.7, 10.0, 4.05),
    ]:
        arrow(ax, x1, y, x2, y)

    arrow(ax, 8.85, 3.35, 8.85, 2.4)  # 40 -> 90
    arrow(ax, 10.85, 3.35, 10.85, 2.4)  # 50 -> 60
    # loop 70 back to 20
    ax.annotate(
        "",
        xy=(4.95, 3.35),
        xytext=(10.85, 1.15),
        arrowprops=dict(arrowstyle="-|>", color="#333333", lw=1.1, connectionstyle="arc3,rad=0.18"),
    )
    ax.text(7.6, 0.55, "loop until empty", fontsize=7.4, color="#333333")
    ax.text(8.95, 2.72, "no block", fontsize=6.8, color="#922B21")

    ax.set_title("Figure 2. Integer step sequence used in OB1", fontsize=10, pad=4, color="#1F4E79")
    fig.tight_layout()
    fig.savefig(OUT / "fig2_step_sequence.png", bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    control_diagram()
    sequence_diagram()
    print("wrote", list(OUT.glob("*.png")))
