# Undergraduate Thesis Project Proposal

**Title:** Gravity Compensation of a Planar Five-Bar Mechanism Using Gear-Spring Modules: Analytical Design, Task-Oriented Optimization, and Prototype Validation

**Student:** [Your Name]  
**Degree:** Bachelor of Engineering (Mechatronic / Mechanical), University of Wollongong  
**Supervisor:** Dr Chin-Hsing Kuo  
**Date:** August 2026

---

## 1. Abstract

This project develops a gravity-compensation design for a planar closed-loop five-bar mechanism using gear-spring modules (GSMs). The work follows the analytical approximation method established for Delta parallel robots by Nguyen, Lin and Kuo (2020), but does not reproduce that robot. The five-bar is chosen because it keeps the same design logic—compact modules, practical compression springs, and balancing at targeted configurations—while remaining simple enough for complete theoretical derivation, numerical simulation, and a 3D-printed prototype within an undergraduate thesis.

Two actuated cranks will each carry one GSM. Spring stiffness and installation angle will be determined so that spring torque approximately cancels gravitational torque at a set of symmetric targeted configurations. A dedicated chapter will then treat the targeted configuration as a design variable and select it automatically for given planar trajectories, rather than choosing it by hand. A simple prototype will be printed and tested under quasi-static motion to measure how much actuation effort is reduced with and without the GSMs.

The expected outcome is a complete theory–simulation–experiment study, and a clear design rule for task-oriented selection of the targeted configuration on a planar five-bar.

---

## 2. Background and motivation

Gravity compensation (static balancing) reduces the motor torque needed to support a robot’s own weight. Springs or counterweights store and release energy so that gravitational potential varies less over the workspace. This improves energy efficiency, allows smaller actuators, and can make physical human–robot interaction safer.

The GSM is a compact geared five-bar / gear-slider module with a practical compression spring. It was first shown on planar serial arms, then applied to Delta parallel robots (Nguyen et al., 2020). For the Delta, three identical GSMs are mounted on the proximal links. Perfect balancing over the whole workspace is not achievable, so the design enforces zero residual gravitational torque only at symmetric targeted configurations, and accepts an approximation nearby. Torque- and energy-reduction indices are then used to evaluate performance.

That Delta study is numerical. Building a spatial Delta with three parallelogram legs, spherical joints and three GSMs is too heavy for a reliable undergraduate prototype: alignment error and 3D-printed gear friction would likely mask the balancing effect that one intends to measure. A planar five-bar avoids this trap while still being a closed-loop parallel mechanism.

A planar five-bar with five revolute joints has two degrees of freedom. In the layout used here, the ground link is fixed at the top and two cranks hang and swing beneath it. The remaining two links close the loop; the end-effector sits at the coupler joint. This is kinematically simpler than a Delta (two actuated legs instead of three, planar instead of spatial), yet gravity compensation is still non-trivial because the two legs are coupled. The same GSM idea can be installed on the two actuated joints. Because the five-bar does not have the Delta’s three-fold symmetry, the gravitational-torque model, the definition of targeted configurations, and even whether a gear ratio of 2 remains the right choice must be re-derived. That re-derivation is the core of this thesis, not a copy of the Delta formulae.

---

## 3. Research gap

From Nguyen et al. (2020) and related GSM work, three gaps are relevant to this project:

1. **The method has not been carried through on a planar closed-loop five-bar.** Existing GSM papers treat serial arms and the spatial Delta. A hanging five-bar needs a new static model and a new notion of targeted configuration (for example, symmetric poses with the end-effector on the midline).

2. **The targeted configuration is still chosen by hand.** The Delta paper already shows that different tasks prefer different target angles, but only compares a few discrete values. There is no systematic, trajectory-based selection rule.

3. **The Delta GSM design was not built.** A planar five-bar with two GSMs is a realistic prototype on which quasi-static force or torque reduction can actually be measured.

This project addresses all three. Variable-payload adaptation is acknowledged as important but is left as discussion, not as a full design objective.

---

## 4. Aim, objectives, and research questions

### 4.1 Aim

To establish a GSM-based gravity-compensation design for a planar five-bar mechanism, including analytical sizing, numerical evaluation, task-oriented selection of the targeted configuration, and simple prototype tests.

### 4.2 Objectives

1. Derive the gravitational torques at the two actuated joints of a top-fixed planar five-bar, including link weights and a payload at the end-effector.
2. Mount one GSM on each actuated crank and derive the spring-torque model under the same practical assumptions as the Delta paper (free-length initial spring, gear arm much shorter than the connecting rod).
3. Redefine targeted configurations for the five-bar and solve for spring stiffness \(k_i\) and installation angle \(\psi_i\). Examine whether gear ratio \(n_g = 2\) still follows from matching torque forms.
4. Evaluate workspace and trajectory performance using torque reduction rate (TRR), mean and peak TRR, gravity compensation density (GCD), and energy reduction rate (ERR) where joint speed is known.
5. **(Chapter on Scheme 1)** Given representative planar trajectories, treat the targeted configuration as a design variable and select it by a scan or a small optimization, subject to limits on stiffness, installation angle, and spring stroke. Compare the result with hand-picked targets.
6. 3D-print a simple five-bar with two GSMs and measure quasi-static actuation effort with and without springs.

### 4.3 Research questions

- **RQ1.** Can the targeted-configuration approximation used for the Delta be reformulated so that a planar five-bar achieves useful gravity compensation with two GSMs and practical compression springs?
- **RQ2.** For a given planar trajectory, does an automatically selected targeted configuration outperform the usual symmetric hand-picked choice in mean torque, peak torque, and energy?
- **RQ3.** On a 3D-printed prototype, is the predicted reduction in balancing effort still visible after friction and manufacturing error are present?

---

## 5. Scope

**In scope**

- Planar five-bar, ground link on top, two swinging actuated cranks, one GSM per crank.
- Quasi-static design; dynamics used only afterwards for ERR on specified trajectories.
- Task-oriented selection of the targeted configuration (one main design variable if left–right symmetry is kept).
- One simple 3D-printed prototype and comparative quasi-static tests.

**Out of scope**

- Reproducing or 3D-printing the spatial Delta in Nguyen et al. (2020).
- A full variable-payload adaptive stiffness mechanism (to be discussed only).
- Surgical or rehabilitation hardware as the main object.
- High-speed dynamic control or industrial-grade metrology.

---

## 6. Methodology

The project has four work packages. Package 3 is the chapter that absorbs the “automatic target-angle” idea.

### WP1. Mechanism definition and analytical design

- Fix the five-bar geometry: ground length, crank lengths, coupler lengths, mass properties, and payload.
- Inverse kinematics from end-effector position \((x, y)\) to crank angles \((\theta_L, \theta_R)\).
- Gravitational torque \(T_{w,L}\) and \(T_{w,R}\) by statics (link centres of mass and payload).
- GSM geometry on each crank; spring torque \(T_{s,i}(\theta_i; k_i, \psi_i, n_g)\).
- Define targeted configurations by symmetry: end-effector on the vertical midline, \(\theta_L = \theta_R = \Theta\). This replaces the Delta condition that the three legs share one angle on the vertical axis.
- Enforce \(T_s \approx T_w\) at the target, solve for \(k_i\) and \(\psi_i\), and state the assumptions (no friction in the design model, \(n_g\) chosen by form matching or checked numerically).

### WP2. Numerical simulation

- Map TRR over the reachable workspace; identify the balancing region (TRR \(> 0\)) and GCD for several thresholds.
- Simulate at least three planar tasks, for example: vertical lift on the midline; a pick-and-place path (side–up–across–down); a curved path in the lower workspace.
- Report mean TRR, peak TRR, and ERR (using Jacobian mapping from end-effector velocity to crank rates).
- Sensitivity to payload and to GSM dimensions, as a bridge to the discussion of variable payload.

### WP3. Task-oriented selection of the targeted configuration (embedded Scheme 1)

This chapter is a new contribution on top of repeating the paper’s method for the five-bar.

- Decision variable: targeted angle \(\Theta\) (symmetric case). Optional extension: a pair \((\Theta_L, \Theta_R)\) if symmetry is relaxed.
- Objective: maximise a weighted sum of mean TRR, peak TRR, and ERR on a given trajectory.
- Constraints: \(k \le k_{\max}\), \(\psi\) inside a mountable range, spring force and stroke within catalogue limits, \(\Theta\) inside the reachable interval.
- Solution: dense one-dimensional scan of \(\Theta\) first (clear plots for the thesis); a simple optimiser only if needed.
- Comparison: hand-picked targets (e.g. cranks horizontal, a mid-workspace pose, a lower pose) versus the trajectory-optimal \(\Theta\).
- Expected design rule: the target should be chosen from the task, not fixed once for all motions.

### WP4. Prototype and simple measurement

- CAD of a desktop five-bar: 3D-printed links, metal dowels or bolts with ball bearings at the five revolute joints, off-the-shelf compression springs, printed or purchased gears for the two GSMs.
- Two test conditions: GSMs removed or springs unloaded (**unbalanced**); GSMs active (**balanced**).
- Quasi-static tests (slow motion so inertia is small):
  - Hold or slowly move a known payload along the midline and along one pick-and-place path.
  - Measure actuation effort by at least one of: a force gauge at a known lever arm; hanging-mass equilibrium; motor current if geared motors are used as sensors.
- Report reduction in peak and mean effort, and discuss discrepancy caused by gear friction, backlash, and printed-part mass error.
- Safety: spring covers, travel limits, no high-speed tests.

**Design flow (mirrors Fig. 4 of the Delta paper, rewritten for the five-bar):**

```
Five-bar dimensions + GSM geometry + targeted configuration Θ
        →  k, ψ
        →  workspace indices (TRR, GCD)
        →  trajectory indices (M-TRR, P-TRR, ERR)
        →  [WP3] scan Θ for a given task → new k, ψ
        →  prototype test: unbalanced vs balanced
```

---

## 7. Proposed thesis structure

1. Introduction  
2. Literature review (static balancing, Delta/GSM paper, five-bar robots)  
3. Five-bar kinematics and gravitational-torque model  
4. GSM modelling and analytical balancing design  
5. Numerical performance evaluation  
6. **Task-oriented selection of the targeted configuration**  
7. Prototype fabrication and quasi-static experiments  
8. Discussion (including variable payload as future work)  
9. Conclusions  

Chapter 6 is Scheme 1. It is not a separate project.

---

## 8. Expected contributions

1. A complete GSM gravity-compensation formulation for a top-fixed planar five-bar, including targeted-configuration conditions that are not copied from the Delta.
2. Evidence, on this mechanism, that trajectory-based selection of \(\Theta\) improves torque and energy indices relative to hand-picked targets.
3. A simple prototype and measured reduction in quasi-static balancing effort, with an honest account of 3D-printing limitations.
4. A compact undergraduate thesis that follows the supervisor’s gravity-compensation line without repeating the published Delta case study.

---

## 9. Feasibility, resources, and risks

| Item | Plan |
|---|---|
| Theory / simulation | MATLAB or Python; 2D kinematics are standard |
| Fabrication | UOW 3D printers, bearings, catalogue springs, basic workshop |
| Sensing | Force gauge and/or motor current; no expensive 6-axis sensor required |
| Risk: printed gear friction hides the effect | Use bearings on the five-bar joints; keep GSM gear force moderate; report friction as a measured offset |
| Risk: model and hardware disagree | Quasi-static tests first; identify mass and stiffness from the real parts and re-run the model |
| Risk: scope growth | No Delta hardware; no adaptive-stiffness device; WP3 stays a 1-D scan unless time remains |

---

## 10. Timeline

The plan assumes one final-year project session (adjust to the official UOW calendar).

| Phase | Period | Work |
|---|---|---|
| 1 | Weeks 1–3 | Literature, five-bar CAD sketch, kinematics and \(T_w\) derivation |
| 2 | Weeks 4–6 | GSM torque model, targeted-configuration design, baseline simulation |
| 3 | Weeks 7–9 | WP3: trajectory scan of \(\Theta\), comparison tables and plots |
| 4 | Weeks 10–14 | Detail design, print, assemble, debug, quasi-static tests |
| 5 | Weeks 15–18 | Thesis writing, extra tests, discussion of limitations and variable payload |

A mid-project review with the supervisor should freeze geometry and the set of trajectories before printing.

---

## 11. What this proposal is not

This is **not** a reconstruction of the FANUC / theoretical Delta example in Nguyen et al. (2020). The Delta paper is the **method template**. The new object is the planar five-bar; the new chapter is automatic, task-oriented choice of the targeted configuration; the new evidence is a prototype measurement.

---

## 12. References (starting set)

1. V. L. Nguyen, C.-Y. Lin and C.-H. Kuo, “Gravity compensation design of Delta parallel robots using gear-spring modules,” *Mechanism and Machine Theory*, vol. 154, 104046, 2020.
2. V. L. Nguyen, C.-Y. Lin and C.-H. Kuo, “Gravity compensation design of planar articulated robotic arms using the gear-spring modules,” *ASME Journal of Mechanisms and Robotics*, vol. 12, no. 3, 031014, 2020.
3. J. L. Herder, *Energy-free Systems: Theory, Conception and Design of Statically Balanced Spring Mechanisms*, Ph.D. thesis, TU Delft, 2001.
4. V. Arakelian, “Gravity compensation in robotics,” *Advanced Robotics*, vol. 30, no. 2, pp. 79–96, 2016.
5. I. Simionescu, L. Ciupitu and L. C. Ionita, “Static balancing with elastic systems of DELTA parallel robots,” *Mechanism and Machine Theory*, vol. 87, pp. 150–162, 2015.
6. X.-J. Liu, J. Wang and G. Pritschow, “Kinematics, singularity and workspace of planar 5R symmetrical parallel mechanisms,” *Mechanism and Machine Theory*, vol. 41, no. 2, pp. 145–169, 2006.
7. R. Clavel, “A fast robot with parallel geometry,” *Proc. Int. Symp. Industrial Robots*, pp. 91–100, 1988.

---

## 13. One-paragraph statement for the supervisor

I would like to take the GSM targeted-configuration method in the 2020 Delta paper as a template, not as a case to rebuild. The thesis object will be a planar five-bar with the ground link on top and one GSM on each swinging crank. I will re-derive the statics, run the same class of torque and energy indices, add one chapter that chooses the targeted angle from the task instead of by hand, and 3D-print a small prototype for a quasi-static comparison of balanced and unbalanced effort. Variable payload and a spatial Delta hardware replica are outside the scope.
