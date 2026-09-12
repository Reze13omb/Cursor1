#!/usr/bin/env python3
"""Gravitational generalized torques of the hanging five-bar (Week 1–3).

Potential (y upward):
    V = g ( m_a y_aL + m_a y_aR + m_b y_bL + m_b y_bR + m_E y_E )

Holding motor torques (static):
    T_w = ∂V/∂θ = (T_wL, T_wR)

If the cranks are free, the force F at E that holds the mechanism satisfies
    J^T F = T_w
where Ė = J θ̇.  F is what a mechanical force gauge at E would read
in a slow hold (no GSM, no motor torque).
"""

from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from five_bar_kinematics import GEOM, inverse_kinematics

MASS = {
    "m_a": 0.040,
    "m_b": 0.050,
    "m_E": 0.300,
    "s_a": 0.50,
    "s_b": 0.50,
    "g": 9.81,
}


def _com_and_jacobian(sol: dict, geom: dict, mass: dict):
    """Return V, T_w, F_E, and the EE Jacobian for one assembly."""
    A, B = sol["A"], sol["B"]
    P, Q, E = sol["P"], sol["Q"], sol["E"]
    th_L, th_R = sol["theta_L"], sol["theta_R"]
    l1, l2 = geom["l1"], geom["l2"]
    s_a, s_b = mass["s_a"], mass["s_b"]
    m_a, m_b, m_E, g = mass["m_a"], mass["m_b"], mass["m_E"], mass["g"]

    dP_dL = l1 * np.array([-math.sin(th_L), math.cos(th_L)])
    dQ_dR = l2 * np.array([-math.sin(th_R), math.cos(th_R)])

    Jx = np.vstack([E - P, E - Q])
    Jth = np.diag([(E - P) @ dP_dL, (E - Q) @ dQ_dR])
    if abs(np.linalg.det(Jx)) < 1e-12:
        return None
    J = np.linalg.solve(Jx, Jth)  # columns ∂E/∂θ_L, ∂E/∂θ_R

    dCaL = np.column_stack([s_a * dP_dL, np.zeros(2)])
    dCaR = np.column_stack([np.zeros(2), s_a * dQ_dR])
    dCbL = (1.0 - s_b) * np.column_stack([dP_dL, np.zeros(2)]) + s_b * J
    dCbR = (1.0 - s_b) * np.column_stack([np.zeros(2), dQ_dR]) + s_b * J
    dE = J

    CaL = A + s_a * (P - A)
    CaR = B + s_a * (Q - B)
    CbL = (1.0 - s_b) * P + s_b * E
    CbR = (1.0 - s_b) * Q + s_b * E

    V = g * (m_a * CaL[1] + m_a * CaR[1] + m_b * CbL[1] + m_b * CbR[1] + m_E * E[1])
    # T_i = g * Σ m * ∂y/∂θ_i
    Tw = g * (
        m_a * dCaL[1]
        + m_a * dCaR[1]
        + m_b * dCbL[1]
        + m_b * dCbR[1]
        + m_E * dE[1]
    )
    F = np.linalg.solve(J.T, Tw)
    return {
        "V": float(V),
        "T_L": float(Tw[0]),
        "T_R": float(Tw[1]),
        "F_x": float(F[0]),
        "F_y": float(F[1]),
        "F_norm": float(np.linalg.norm(F)),
        "J": J,
        "CaL": CaL,
        "CaR": CaR,
        "CbL": CbL,
        "CbR": CbR,
        "singular": False,
    }


def gravity_loads(x: float, y: float, geom: dict = GEOM, mass: dict = MASS):
    sol = inverse_kinematics(x, y, geom)
    if sol is None:
        return None
    loads = _com_and_jacobian(sol, geom, mass)
    if loads is None:
        return None
    return {**sol, **loads}


def potential(x: float, y: float, geom: dict = GEOM, mass: dict = MASS):
    data = gravity_loads(x, y, geom, mass)
    return None if data is None else data["V"]


def fd_torque(x: float, y: float, geom: dict = GEOM, mass: dict = MASS, h: float = 1e-7):
    """Finite-difference T_w from V(θ), for verification only."""
    sol = inverse_kinematics(x, y, geom)
    if sol is None:
        return None
    from five_bar_kinematics import forward_kinematics

    def V_of_theta(th_L, th_R):
        fk = forward_kinematics(th_L, th_R, geom, pick="lower")
        if fk is None:
            return None
        s = {
            "A": fk["A"],
            "B": fk["B"],
            "P": fk["P"],
            "Q": fk["Q"],
            "E": fk["E"],
            "theta_L": th_L,
            "theta_R": th_R,
        }
        out = _com_and_jacobian(s, geom, mass)
        return None if out is None else out["V"]

    th_L, th_R = sol["theta_L"], sol["theta_R"]
    Vp = V_of_theta(th_L + h, th_R)
    Vm = V_of_theta(th_L - h, th_R)
    Up = V_of_theta(th_L, th_R + h)
    Um = V_of_theta(th_L, th_R - h)
    if None in (Vp, Vm, Up, Um):
        return None
    return np.array([(Vp - Vm) / (2 * h), (Up - Um) / (2 * h)])


def midline_scan(y_min=-0.260, y_max=-0.100, n=80, geom: dict = GEOM, mass: dict = MASS):
    ys = np.linspace(y_min, y_max, n)
    rows = []
    for y in ys:
        data = gravity_loads(0.0, float(y), geom, mass)
        if data is None:
            continue
        rows.append(data)
    return rows
