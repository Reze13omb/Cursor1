#!/usr/bin/env python3
"""Inverse / forward kinematics of the hanging planar five-bar (Week 1–3).

Geometry (metres), frozen in the CAD sketch:
    A = (-d/2, 0),  B = (d/2, 0),  ground on top
    P = A + l1 [cos θ_L, sin θ_L]
    Q = B + l2 [cos θ_R, sin θ_R]
    ||E − P|| = l3,  ||E − Q|| = l4

Angles θ_L, θ_R are from +x, counterclockwise. Gravity is −y.

Each leg has two elbows (out / in). The working assembly for this thesis
is out–out: left P more outward (−x), right Q more outward (+x).
"""

from __future__ import annotations

import math
from typing import Literal

import numpy as np

GEOM = {
    "d": 0.180,
    "l1": 0.120,
    "l2": 0.120,
    "l3": 0.180,
    "l4": 0.180,
}

Elbow = Literal["out", "in"]
TOL = 1e-9
ALIGN_TOL = 1e-6


def base_joints(geom: dict = GEOM):
    half = geom["d"] / 2.0
    return np.array([-half, 0.0]), np.array([half, 0.0])


def circle_intersections(c1, r1, c2, r2):
    c1 = np.asarray(c1, float)
    c2 = np.asarray(c2, float)
    delta = c2 - c1
    dist = float(np.linalg.norm(delta))
    if dist < TOL:
        return []
    if dist > r1 + r2 + TOL or dist < abs(r1 - r2) - TOL:
        return []
    a = (r1**2 - r2**2 + dist**2) / (2.0 * dist)
    h2 = r1**2 - a**2
    if h2 < -TOL:
        return []
    h = math.sqrt(max(h2, 0.0))
    mid = c1 + a * delta / dist
    perp = np.array([-delta[1], delta[0]]) / dist
    if h < TOL:
        return [mid]
    return [mid + h * perp, mid - h * perp]


def _pick_elbow(candidates, side: str, elbow: Elbow):
    if not candidates:
        return None
    if len(candidates) == 1:
        return np.asarray(candidates[0], float)
    key = (lambda p: p[0]) if side == "left" else (lambda p: -p[0])
    ordered = sorted(candidates, key=key)
    # left: out = smaller x; right: out = larger x (smaller key)
    chosen = ordered[0] if elbow == "out" else ordered[1]
    return np.asarray(chosen, float)


def inverse_kinematics(
    x: float,
    y: float,
    geom: dict = GEOM,
    left_elbow: Elbow = "out",
    right_elbow: Elbow = "out",
):
    """Return one assembly, or None if that elbow pair cannot be formed."""
    A, B = base_joints(geom)
    E = np.array([x, y], float)
    P_cands = circle_intersections(A, geom["l1"], E, geom["l3"])
    Q_cands = circle_intersections(B, geom["l2"], E, geom["l4"])
    P = _pick_elbow(P_cands, "left", left_elbow)
    Q = _pick_elbow(Q_cands, "right", right_elbow)
    if P is None or Q is None:
        return None
    th_L = math.atan2(P[1] - A[1], P[0] - A[0])
    th_R = math.atan2(Q[1] - B[1], Q[0] - B[0])
    return {
        "A": A,
        "B": B,
        "P": P,
        "Q": Q,
        "E": E,
        "theta_L": th_L,
        "theta_R": th_R,
        "theta_L_deg": math.degrees(th_L),
        "theta_R_deg": math.degrees(th_R),
        "phi_L_deg": math.degrees(th_L + math.pi / 2),
        "phi_R_deg": math.degrees(th_R + math.pi / 2),
        "left_elbow": left_elbow,
        "right_elbow": right_elbow,
        "left_aligned": len(P_cands) == 1,
        "right_aligned": len(Q_cands) == 1,
    }


def all_assemblies(x: float, y: float, geom: dict = GEOM):
    modes = (("out", "out"), ("out", "in"), ("in", "out"), ("in", "in"))
    found = []
    for le, re in modes:
        sol = inverse_kinematics(x, y, geom, le, re)
        if sol is not None:
            found.append(sol)
    return found


def crank_points(theta_L: float, theta_R: float, geom: dict = GEOM):
    A, B = base_joints(geom)
    P = A + geom["l1"] * np.array([math.cos(theta_L), math.sin(theta_L)])
    Q = B + geom["l2"] * np.array([math.cos(theta_R), math.sin(theta_R)])
    return A, B, P, Q


def forward_kinematics(theta_L: float, theta_R: float, geom: dict = GEOM, pick: str = "lower"):
    """Given crank angles, recover E as an intersection of the two coupler circles."""
    A, B, P, Q = crank_points(theta_L, theta_R, geom)
    cands = circle_intersections(P, geom["l3"], Q, geom["l4"])
    if not cands:
        return None
    if pick == "lower":
        E = min(cands, key=lambda p: p[1])
    elif pick == "upper":
        E = max(cands, key=lambda p: p[1])
    else:
        raise ValueError(pick)
    return {
        "A": A,
        "B": B,
        "P": P,
        "Q": np.asarray(Q),
        "E": np.asarray(E),
        "n_solutions": len(cands),
        "aligned_couplers": len(cands) == 1,
    }


def reconstruct_error(sol: dict, geom: dict = GEOM) -> float:
    """Max link-length residual after IK (should be ~0)."""
    A, B, P, Q, E = sol["A"], sol["B"], sol["P"], sol["Q"], sol["E"]
    errs = [
        abs(np.linalg.norm(P - A) - geom["l1"]),
        abs(np.linalg.norm(Q - B) - geom["l2"]),
        abs(np.linalg.norm(E - P) - geom["l3"]),
        abs(np.linalg.norm(E - Q) - geom["l4"]),
    ]
    return max(errs)


def ik_fk_error(sol: dict, geom: dict = GEOM) -> float:
    fk = forward_kinematics(sol["theta_L"], sol["theta_R"], geom, pick="lower")
    if fk is None:
        return math.inf
    return float(np.linalg.norm(fk["E"] - sol["E"]))


def leg_reach_ok(base, ee, crank, coupler) -> bool:
    dist = float(np.linalg.norm(np.asarray(ee) - np.asarray(base)))
    return abs(crank - coupler) - TOL <= dist <= crank + coupler + TOL


def is_reachable(x: float, y: float, geom: dict = GEOM, left_elbow: Elbow = "out", right_elbow: Elbow = "out") -> bool:
    return inverse_kinematics(x, y, geom, left_elbow, right_elbow) is not None


def inverse_singularity(x: float, y: float, geom: dict = GEOM, side: str = "left") -> bool:
    """True when that crank and coupler are aligned (stretched or folded)."""
    A, B = base_joints(geom)
    E = np.array([x, y], float)
    if side == "left":
        dist = float(np.linalg.norm(E - A))
        lo, hi = abs(geom["l1"] - geom["l3"]), geom["l1"] + geom["l3"]
    else:
        dist = float(np.linalg.norm(E - B))
        lo, hi = abs(geom["l2"] - geom["l4"]), geom["l2"] + geom["l4"]
    return abs(dist - lo) < 1e-4 or abs(dist - hi) < 1e-4


def couplers_aligned(sol: dict) -> bool:
    """Type-II-ish: P, E, Q nearly collinear."""
    pe = sol["E"] - sol["P"]
    qe = sol["Q"] - sol["E"]
    return abs(pe[0] * qe[1] - pe[1] * qe[0]) < 1e-6
