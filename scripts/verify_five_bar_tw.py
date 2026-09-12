#!/usr/bin/env python3
"""Week 1–3 gravitational-torque plots and checkpoint table."""

from __future__ import annotations

import csv
import math
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from five_bar_statics import fd_torque, gravity_loads, midline_scan

OUT = Path("/workspace/docs/week1-3")
FIG = OUT / "figures"
ART = Path("/opt/cursor/artifacts")

CHECKPOINTS = [
    ("C1 CAD sample", 0.000, -0.180),
    ("C2 midline high", 0.000, -0.120),
    ("C3 midline low", 0.000, -0.250),
    ("C4 left", -0.060, -0.180),
    ("C5 right", 0.060, -0.180),
]


def draw_midline(rows, path: Path):
    y = np.array([r["E"][1] * 1000 for r in rows])
    tL = np.array([r["T_L"] * 1000 for r in rows])
    tR = np.array([r["T_R"] * 1000 for r in rows])
    fy = np.array([r["F_y"] for r in rows])
    fx = np.array([r["F_x"] for r in rows])
    fig, axes = plt.subplots(2, 1, figsize=(8.4, 7.2), dpi=150, sharex=True)
    ax = axes[0]
    ax.plot(y, tL, color="#1f4e79", lw=2.0, label=r"$T_{w,L}$")
    ax.plot(y, tR, color="#c45911", lw=2.0, ls="--", label=r"$T_{w,R}$")
    ax.axhline(0, color="#999", lw=0.7)
    ax.set_ylabel("holding torque (mN·m)")
    ax.set_title("Unbalanced gravitational loads on the midline  $x=0$")
    ax.legend(fontsize=9)
    ax.grid(True, ls=":", alpha=0.45)
    ax = axes[1]
    ax.plot(y, fy, color="#c00000", lw=2.0, label=r"$F_y$ at E (free cranks)")
    ax.plot(y, fx, color="#548235", lw=1.6, ls="--", label=r"$F_x$ at E")
    ax.axhline(0, color="#999", lw=0.7)
    ax.set_xlabel("end-effector $y$ (mm)")
    ax.set_ylabel("hold force at E (N)")
    ax.legend(fontsize=9)
    ax.grid(True, ls=":", alpha=0.45)
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)


def main():
    FIG.mkdir(parents=True, exist_ok=True)
    rows = midline_scan()
    if len(rows) < 10:
        raise SystemExit("midline scan too short")
    draw_midline(rows, FIG / "five_bar_tw_midline.png")

    table = []
    print(f"{'name':<18} {'T_L mNm':>10} {'T_R mNm':>10} {'Fx N':>8} {'Fy N':>8} {'FD err':>10}")
    for name, x, y in CHECKPOINTS:
        data = gravity_loads(x, y)
        if data is None:
            raise SystemExit(f"no Tw at {name}")
        fd = fd_torque(x, y)
        err = float(np.linalg.norm(fd - np.array([data["T_L"], data["T_R"]]))) if fd is not None else float("nan")
        print(
            f"{name:<18} {data['T_L']*1000:10.3f} {data['T_R']*1000:10.3f} "
            f"{data['F_x']:8.4f} {data['F_y']:8.4f} {err:10.2e}"
        )
        if err > 5e-6:
            raise SystemExit(f"FD mismatch at {name}: {err}")
        table.append(
            {
                "name": name,
                "x_mm": x * 1000,
                "y_mm": y * 1000,
                "T_L_Nm": data["T_L"],
                "T_R_Nm": data["T_R"],
                "F_x_N": data["F_x"],
                "F_y_N": data["F_y"],
                "F_norm_N": data["F_norm"],
                "V_J": data["V"],
                "fd_error_Nm": err,
            }
        )

    # Midline: Fx ~ 0 and T_L + T_R ~ 0? Check C1
    c1 = gravity_loads(0.0, -0.180)
    if abs(c1["F_x"]) > 1e-8:
        raise SystemExit(f"midline Fx should vanish, got {c1['F_x']}")
    if abs(abs(c1["T_L"]) - abs(c1["T_R"])) > 1e-8:
        raise SystemExit("midline |T_L| != |T_R|")

    # Left/right poses should mirror
    left, right = gravity_loads(-0.060, -0.180), gravity_loads(0.060, -0.180)
    if abs(left["T_L"] + right["T_R"]) > 1e-8 or abs(left["T_R"] + right["T_L"]) > 1e-8:
        raise SystemExit("left/right torque mirror failed")
    if abs(left["F_x"] + right["F_x"]) > 1e-8 or abs(left["F_y"] - right["F_y"]) > 1e-8:
        raise SystemExit("left/right force mirror failed")

    csv_path = OUT / "tw_checkpoints.csv"
    with csv_path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0].keys()))
        w.writeheader()
        w.writerows(table)

    if ART.is_dir():
        import shutil

        shutil.copy(FIG / "five_bar_tw_midline.png", ART / "five_bar_tw_midline.png")

    print("wrote", csv_path)
    print("Tw verification passed")


if __name__ == "__main__":
    main()
