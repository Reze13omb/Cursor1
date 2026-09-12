#!/usr/bin/env python3
"""Run Week 1–3 inverse-kinematics checks and write figures / a checkpoint table."""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
from five_bar_kinematics import (  # noqa: E402
    GEOM,
    all_assemblies,
    couplers_aligned,
    forward_kinematics,
    ik_fk_error,
    inverse_kinematics,
    inverse_singularity,
    reconstruct_error,
)

OUT = Path("/workspace/docs/week1-3")
FIG = OUT / "figures"
ART = Path("/opt/cursor/artifacts")

CHECKPOINTS = [
    ("C1 midline sample (CAD pose)", 0.000, -0.180),
    ("C2 midline high", 0.000, -0.080),
    ("C3 midline low", 0.000, -0.250),
    ("C4 left of midline", -0.060, -0.180),
    ("C5 right of midline", 0.060, -0.180),
]


def _draw_mech(ax, sol, color_crank="#1f4e79", color_coupler="#c45911", lw=3.2):
    A, B, P, Q, E = sol["A"], sol["B"], sol["P"], sol["Q"], sol["E"]
    ax.plot([A[0], B[0]], [0, 0], color="#333", lw=3.5, zorder=1)
    ax.plot([A[0], P[0]], [A[1], P[1]], color=color_crank, lw=lw, zorder=2)
    ax.plot([B[0], Q[0]], [B[1], Q[1]], color=color_crank, lw=lw, zorder=2)
    ax.plot([P[0], E[0]], [P[1], E[1]], color=color_coupler, lw=lw, zorder=2)
    ax.plot([Q[0], E[0]], [Q[1], E[1]], color=color_coupler, lw=lw, zorder=2)
    for pt in (A, B, P, Q, E):
        ax.plot(pt[0], pt[1], "o", ms=6, color="white", markeredgecolor="#111", zorder=4)


def draw_checkpoints(rows, path: Path):
    fig, axes = plt.subplots(2, 3, figsize=(11.2, 7.2), dpi=150)
    axes = axes.ravel()
    for ax, (name, x, y, sol) in zip(axes, rows):
        _draw_mech(ax, sol)
        ax.plot(x, y, "o", ms=7, color="#c00000", zorder=5)
        ax.set_title(
            f"{name}\nθL={sol['theta_L_deg']:.1f}°, θR={sol['theta_R_deg']:.1f}°",
            fontsize=9,
        )
        ax.set_aspect("equal")
        ax.set_xlim(-0.26, 0.26)
        ax.set_ylim(-0.32, 0.06)
        ax.grid(True, ls=":", alpha=0.4)
        ax.tick_params(labelsize=7)
    axes[5].axis("off")
    axes[5].text(
        0.05,
        0.75,
        "Working mode: out–out\nRed dot = commanded E\nIK residual / IK→FK error\nare in the checkpoint table.",
        fontsize=10,
        va="top",
        transform=axes[5].transAxes,
    )
    fig.suptitle("Five-bar inverse kinematics — five checkpoint poses (out–out)", fontsize=13)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def draw_modes(x, y, path: Path):
    sols = all_assemblies(x, y)
    fig, axes = plt.subplots(2, 2, figsize=(9.2, 7.6), dpi=150)
    axes = axes.ravel()
    for ax, sol in zip(axes, sols):
        _draw_mech(ax, sol)
        ax.set_title(f"{sol['left_elbow']}–{sol['right_elbow']}\nθL={sol['theta_L_deg']:.1f}°, θR={sol['theta_R_deg']:.1f}°", fontsize=10)
        ax.set_aspect("equal")
        ax.set_xlim(-0.26, 0.26)
        ax.set_ylim(-0.32, 0.06)
        ax.grid(True, ls=":", alpha=0.4)
    fig.suptitle(f"Four elbow assemblies at E = ({x*1000:.0f}, {y*1000:.0f}) mm", fontsize=13)
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def draw_workspace(path: Path):
    xs = np.linspace(-0.16, 0.16, 81)
    ys = np.linspace(-0.30, -0.02, 73)
    X, Y = np.meshgrid(xs, ys)
    reach = np.zeros_like(X, dtype=bool)
    for i in range(Y.shape[0]):
        for j in range(X.shape[1]):
            reach[i, j] = inverse_kinematics(float(X[i, j]), float(Y[i, j])) is not None
    fig, ax = plt.subplots(figsize=(7.6, 6.4), dpi=150)
    ax.contourf(X * 1000, Y * 1000, reach.astype(float), levels=[-0.5, 0.5, 1.5], colors=["#f4f4f4", "#deebf7"])
    ax.plot([-90, 90], [0, 0], color="#333", lw=4, solid_capstyle="butt")
    for name, x, y, _ in []:
        pass
    for name, x, y in [(r[0], r[1], r[2]) for r in CHECKPOINTS]:
        ax.plot(x * 1000, y * 1000, "o", color="#c00000", ms=5)
        ax.annotate(name.split()[0], (x * 1000 + 3, y * 1000 + 3), fontsize=8)
    ax.set_aspect("equal")
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_title("Reachable workspace in the out–out assembly")
    ax.grid(True, ls=":", alpha=0.4)
    ax.legend(
        handles=[
            Line2D([0], [0], color="#9dc3e6", lw=8, label="reachable (out–out)"),
            Line2D([0], [0], marker="o", color="#c00000", ls="", label="checkpoints"),
        ],
        loc="lower right",
        fontsize=8,
    )
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return float(reach.mean())


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    rows = []
    table_rows = []
    print(f"{'name':<32} {'x_mm':>7} {'y_mm':>7} {'thL':>8} {'thR':>8} {'len_err':>10} {'fk_err':>10}")
    for name, x, y in CHECKPOINTS:
        sol = inverse_kinematics(x, y)
        if sol is None:
            raise SystemExit(f"Checkpoint not reachable: {name}")
        e_len = reconstruct_error(sol)
        e_fk = ik_fk_error(sol)
        if e_len > 1e-9 or e_fk > 1e-9:
            raise SystemExit(f"Check failed at {name}: len={e_len}, fk={e_fk}")
        fk = forward_kinematics(sol["theta_L"], sol["theta_R"])
        print(
            f"{name:<32} {x*1000:7.1f} {y*1000:7.1f} "
            f"{sol['theta_L_deg']:8.2f} {sol['theta_R_deg']:8.2f} {e_len:10.2e} {e_fk:10.2e}"
        )
        rows.append((name, x, y, sol))
        table_rows.append(
            {
                "name": name,
                "x_mm": x * 1000,
                "y_mm": y * 1000,
                "theta_L_deg": sol["theta_L_deg"],
                "theta_R_deg": sol["theta_R_deg"],
                "P_x_mm": sol["P"][0] * 1000,
                "P_y_mm": sol["P"][1] * 1000,
                "Q_x_mm": sol["Q"][0] * 1000,
                "Q_y_mm": sol["Q"][1] * 1000,
                "link_residual_m": e_len,
                "ik_fk_error_m": e_fk,
                "left_inverse_singular": inverse_singularity(x, y, side="left"),
                "right_inverse_singular": inverse_singularity(x, y, side="right"),
                "couplers_aligned": couplers_aligned(sol),
                "n_fk_solutions": fk["n_solutions"] if fk else 0,
            }
        )

    # Unreachable point should fail
    if inverse_kinematics(0.0, -0.40) is not None:
        raise SystemExit("Expected (0, -400) mm to be unreachable")
    if inverse_kinematics(0.25, 0.05) is not None:
        raise SystemExit("Expected (250, 50) mm to be unreachable")

    # Midline symmetry
    s = inverse_kinematics(0.0, -0.180)
    if abs((s["theta_L_deg"] + s["theta_R_deg"]) + 180.0) > 1e-6:
        raise SystemExit("Midline cranks are not mirrors")

    frac = draw_workspace(FIG / "five_bar_ik_workspace.png")
    draw_checkpoints(rows, FIG / "five_bar_ik_checkpoints.png")
    draw_modes(0.0, -0.180, FIG / "five_bar_ik_four_modes.png")

    csv_path = OUT / "ik_checkpoints.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table_rows[0].keys()))
        w.writeheader()
        w.writerows(table_rows)

    if ART.is_dir():
        import shutil

        for name in (
            "five_bar_ik_workspace.png",
            "five_bar_ik_checkpoints.png",
            "five_bar_ik_four_modes.png",
        ):
            shutil.copy(FIG / name, ART / name)

    print(f"workspace fill (grid) = {frac:.3f}")
    print("wrote", csv_path)
    print("IK verification passed")


if __name__ == "__main__":
    main()
