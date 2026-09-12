#!/usr/bin/env python3
"""Self-contained checks for five_bar_kinematics.py (no extra test runner)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from five_bar_kinematics import (
    GEOM,
    all_assemblies,
    crank_points,
    forward_kinematics,
    ik_fk_error,
    inverse_kinematics,
    reconstruct_error,
)


def assert_close(a, b, tol, msg):
    if abs(a - b) > tol:
        raise AssertionError(f"{msg}: {a} vs {b}")


def test_cad_pose():
    sol = inverse_kinematics(0.0, -0.180)
    assert sol is not None
    assert_close(sol["theta_L_deg"], -125.66986453515187, 1e-6, "CAD θL")
    assert_close(sol["theta_R_deg"], -54.33013546484812, 1e-6, "CAD θR")
    assert reconstruct_error(sol) < 1e-12
    assert ik_fk_error(sol) < 1e-12


def test_five_checkpoints():
    pts = [
        (0.0, -0.180),
        (0.0, -0.080),
        (0.0, -0.250),
        (-0.060, -0.180),
        (0.060, -0.180),
    ]
    for x, y in pts:
        sol = inverse_kinematics(x, y)
        assert sol is not None, (x, y)
        assert reconstruct_error(sol) < 1e-12
        assert ik_fk_error(sol) < 1e-12
        A, B, P, Q = crank_points(sol["theta_L"], sol["theta_R"])
        assert np.allclose(P, sol["P"])
        assert np.allclose(Q, sol["Q"])


def test_left_right_mirror():
    left = inverse_kinematics(-0.060, -0.180)
    right = inverse_kinematics(0.060, -0.180)
    assert left and right
    assert_close(left["theta_L_deg"] + right["theta_R_deg"], -180.0, 1e-6, "mirror L")
    assert_close(left["theta_R_deg"] + right["theta_L_deg"], -180.0, 1e-6, "mirror R")


def test_four_modes_at_sample():
    sols = all_assemblies(0.0, -0.180)
    assert len(sols) == 4
    keys = {(s["left_elbow"], s["right_elbow"]) for s in sols}
    assert keys == {("out", "out"), ("out", "in"), ("in", "out"), ("in", "in")}


def test_unreachable_and_fk_two_solutions():
    assert inverse_kinematics(0.0, -0.40) is None
    assert inverse_kinematics(0.25, 0.05) is None
    sol = inverse_kinematics(0.0, -0.180)
    fk = forward_kinematics(sol["theta_L"], sol["theta_R"])
    assert fk["n_solutions"] == 2


def test_loop_equations():
    sol = inverse_kinematics(-0.040, -0.160)
    P = sol["P"]
    A = sol["A"]
    E = sol["E"]
    assert_close(float(np.linalg.norm(P - A)), GEOM["l1"], 1e-12, "|AP|")
    assert_close(float(np.linalg.norm(E - P)), GEOM["l3"], 1e-12, "|EP|")


if __name__ == "__main__":
    tests = [
        test_cad_pose,
        test_five_checkpoints,
        test_left_right_mirror,
        test_four_modes_at_sample,
        test_unreachable_and_fk_two_solutions,
        test_loop_equations,
    ]
    for fn in tests:
        fn()
        print("ok", fn.__name__)
    print("all IK tests passed")
