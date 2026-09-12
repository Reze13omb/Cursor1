#!/usr/bin/env python3
"""Checks for five_bar_statics.py."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from five_bar_statics import fd_torque, gravity_loads


def test_fd_matches_analytic():
    for x, y in [(0.0, -0.180), (0.0, -0.120), (0.0, -0.250), (-0.04, -0.160)]:
        data = gravity_loads(x, y)
        fd = fd_torque(x, y)
        assert data is not None and fd is not None
        err = np.linalg.norm(fd - np.array([data["T_L"], data["T_R"]]))
        assert err < 5e-6, (x, y, err)


def test_midline_symmetry():
    data = gravity_loads(0.0, -0.180)
    assert abs(data["F_x"]) < 1e-10
    assert abs(abs(data["T_L"]) - abs(data["T_R"])) < 1e-10


def test_left_right_mirror():
    L = gravity_loads(-0.060, -0.180)
    R = gravity_loads(0.060, -0.180)
    assert abs(L["T_L"] + R["T_R"]) < 1e-10
    assert abs(L["T_R"] + R["T_L"]) < 1e-10
    assert abs(L["F_y"] - R["F_y"]) < 1e-10
    assert abs(L["F_x"] + R["F_x"]) < 1e-10


def test_heavier_payload_increases_hold_force():
    from five_bar_statics import MASS

    light = dict(MASS)
    heavy = dict(MASS)
    light["m_E"] = 0.10
    heavy["m_E"] = 0.30
    a = gravity_loads(0.0, -0.180, mass=light)
    b = gravity_loads(0.0, -0.180, mass=heavy)
    assert abs(b["F_y"]) > abs(a["F_y"])


if __name__ == "__main__":
    test_fd_matches_analytic()
    print("ok test_fd_matches_analytic")
    test_midline_symmetry()
    print("ok test_midline_symmetry")
    test_left_right_mirror()
    print("ok test_left_right_mirror")
    test_heavier_payload_increases_hold_force()
    print("ok test_heavier_payload_increases_hold_force")
    print("all Tw tests passed")
