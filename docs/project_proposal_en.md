# Undergraduate Thesis Project Proposal

**Title:** Gravity Compensation of a Planar Five-Bar Mechanism Using Gear-Spring Modules: Analytical Design, Task-Oriented Optimization, and Prototype Validation

**Student:** Bo Zhang  
**Student number:** 8571260  
**Degree:** Bachelor of Engineering (Mechatronic / Mechanical), University of Wollongong  
**Supervisor:** Dr Chin-Hsing Kuo  
**Date:** August 2026

---

## 1. Abstract

This project develops a gravity-compensation design for a planar closed-loop five-bar mechanism using gear-spring modules (GSMs). The work follows the analytical approximation method established for Delta parallel robots by Nguyen, Lin and Kuo (2020), but does not reproduce that robot. The five-bar is chosen because it keeps the same design logic—compact modules, practical compression springs, and balancing at targeted configurations—while remaining simple enough for complete theoretical derivation, numerical simulation, and a 3D-printed prototype within an undergraduate thesis.

Two actuated cranks will each carry one GSM. Spring stiffness and installation angle will be determined so that spring torque approximately cancels gravitational torque at a set of symmetric targeted configurations. A dedicated chapter will then treat the targeted configuration as a design variable and select it automatically for given planar trajectories, rather than choosing it by hand.

Prototype validation will **not** use electronic force sensing, load cells, motor-current estimation, or any other sensing technology. The design will be checked by a simpler mechanical principle: residual unbalance appears as the external force required to move the mechanism slowly by hand. That force will be measured with a handheld analog mechanical force gauge (for example an IMADA PS-10N: 10 N capacity, 0.05 N resolution), comparing the GSM-on and GSM-off conditions along the same paths.

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

3. **The Delta GSM design was not built.** A planar five-bar with two GSMs is a realistic prototype. Residual unbalance can be checked mechanically by measuring the force needed to move the mechanism, without electronic sensing.

This project addresses all three. Variable-payload adaptation is acknowledged as important but is left as discussion, not as a full design objective.

---

## 4. Aim, objectives, and research questions

### 4.1 Aim

To establish a GSM-based gravity-compensation design for a planar five-bar mechanism, including analytical sizing, numerical evaluation, task-oriented selection of the targeted configuration, and a simple mechanical prototype test.

### 4.2 Objectives

1. Derive the gravitational torques at the two actuated joints of a top-fixed planar five-bar, including link weights and a payload at the end-effector.
2. Mount one GSM on each actuated crank and derive the spring-torque model under the same practical assumptions as the Delta paper (free-length initial spring, gear arm much shorter than the connecting rod).
3. Redefine targeted configurations for the five-bar and solve for spring stiffness \(k_i\) and installation angle \(\psi_i\). Examine whether gear ratio \(n_g = 2\) still follows from matching torque forms.
4. Evaluate workspace and trajectory performance using torque reduction rate (TRR), mean and peak TRR, gravity compensation density (GCD), and energy reduction rate (ERR) where joint speed is known. These indices remain numerical; they are not measured with sensors on the prototype.
5. **(Chapter on Scheme 1)** Given representative planar trajectories, treat the targeted configuration as a design variable and select it by a scan or a small optimization, subject to limits on stiffness, installation angle, and spring stroke. Compare the result with hand-picked targets.
6. 3D-print a simple five-bar with two GSMs and verify the design with a handheld mechanical force gauge, comparing the quasi-static force required to move the mechanism with the GSMs engaged and with the GSMs disconnected.

### 4.3 Research questions

- **RQ1.** Can the targeted-configuration approximation used for the Delta be reformulated so that a planar five-bar achieves useful gravity compensation with two GSMs and practical compression springs?
- **RQ2.** For a given planar trajectory, does an automatically selected targeted configuration outperform the usual symmetric hand-picked choice in mean torque, peak torque, and energy (numerical indices)?
- **RQ3.** On a 3D-printed prototype, does a handheld mechanical force gauge still show a clear drop in the force required to move the mechanism after the GSMs are fitted, despite friction and manufacturing error?

---

## 5. Scope

**In scope**

- Planar five-bar, ground link on top, two swinging actuated cranks, one GSM per crank.
- Quasi-static design; dynamics used only afterwards for numerical ERR on specified trajectories.
- Task-oriented selection of the targeted configuration (one main design variable if left–right symmetry is kept).
- One simple 3D-printed prototype, validated by handheld mechanical force-gauge tests (unbalanced vs balanced).

**Out of scope**

- Electronic force or torque sensing, load cells, strain gauges, motor-current estimation, data-acquisition systems, and any other sensing technology.
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

### WP4. Prototype and mechanical force-gauge tests

Following the supervisor’s advice, prototype tests will use a simple mechanical principle rather than sensing technology. If a gravity compensator were perfect and frictionless, no external force would be needed to move the mechanism quasi-statically. Any leftover gravitational unbalance, plus friction, appears as the force that must be applied by hand to displace the end-effector. Measuring that force with and without the GSMs is a direct check of the design.

- CAD of a desktop five-bar: 3D-printed links, metal dowels or bolts with ball bearings at the five revolute joints, off-the-shelf compression springs, printed or purchased gears for the two GSMs. Link masses and payload will be sized so that moving forces fit a 10 N mechanical gauge.
- Two test conditions: GSMs removed or springs unloaded (**unbalanced**); GSMs active (**balanced**).
- **Instrument:** a handheld analog mechanical force gauge of the IMADA PS type, specifically the PS-10N (10 N capacity, 0.05 N resolution, push/pull, real-time and peak modes, tare ring, no batteries). Product page: https://imada.com/products/ps-10n-mechanical-force-gauge/. If a trial shows that the unbalanced force exceeds 10 N, a higher-capacity mechanical gauge in the same analog family will be used. An electronic gauge, load cell, or motor will not be substituted.
- **Procedure (quasi-static, inertia negligible):**
  - Fix the five-bar in a vertical plane; fit a hook at the end-effector.
  - Mark a vertical midline path and one simple pick-and-place path.
  - Pull or push slowly through the gauge. Tare after the attachment is fitted. Use peak mode for the largest force along a path, and real-time mode at marked poses.
  - Repeat each path at least three times. Record the dial reading by hand; no data logger.
- **Metric:** force reduction \(1 - F_{\mathrm{balanced}} / F_{\mathrm{unbalanced}}\) for peak force and selected poses. Discuss leftover force from friction, backlash, and printed-part mass error.
- Optional extra check, still purely mechanical: hang a known small mass and observe whether the balanced mechanism stays at rest at the targeted configuration.
- Safety: spring covers, travel limits, no shock loading, no high-speed tests.

**Design flow (mirrors Fig. 4 of the Delta paper, rewritten for the five-bar):**

```
Five-bar dimensions + GSM geometry + targeted configuration Θ
        →  k, ψ
        →  workspace indices (TRR, GCD)
        →  trajectory indices (M-TRR, P-TRR, ERR)
        →  [WP3] scan Θ for a given task → new k, ψ
        →  prototype test with a mechanical force gauge: unbalanced vs balanced
```

---

## 7. Proposed thesis structure

1. Introduction  
2. Literature review (static balancing, Delta/GSM paper, five-bar robots)  
3. Five-bar kinematics and gravitational-torque model  
4. GSM modelling and analytical balancing design  
5. Numerical performance evaluation  
6. **Task-oriented selection of the targeted configuration**  
7. Prototype fabrication and mechanical force-gauge experiments  
8. Discussion (including variable payload as future work)  
9. Conclusions  

Chapter 6 is Scheme 1. It is not a separate project. Experimental work in Chapter 7 is limited to the handheld mechanical force-gauge procedure in WP4.

---

## 8. Expected contributions

1. A complete GSM gravity-compensation formulation for a top-fixed planar five-bar, including targeted-configuration conditions that are not copied from the Delta.
2. Evidence, on this mechanism, that trajectory-based selection of \(\Theta\) improves torque and energy indices relative to hand-picked targets.
3. A simple prototype, with the force required to move the balanced and unbalanced mechanism compared on a handheld mechanical force gauge, and with an honest account of 3D-printing limitations.
4. A compact undergraduate thesis that follows the supervisor’s gravity-compensation line without repeating the published Delta case study and without introducing sensing technology.

---

## 9. Feasibility, resources, and risks

| Item | Plan |
|---|---|
| Theory / simulation | MATLAB or Python; 2D kinematics are standard |
| Fabrication | UOW 3D printers, bearings, catalogue springs, basic workshop. Link masses sized so that moving forces fit a 10 N mechanical gauge |
| Measurement | Handheld analog mechanical force gauge (IMADA PS-10N or same-family mechanical gauge). No electronic sensors, load cells, or motor-current measurement |
| Risk: printed gear friction hides the effect | Use bearings on the five-bar joints; keep GSM gear force moderate; report leftover force as a measured offset on the gauge |
| Risk: unbalanced force exceeds 10 N | Reduce payload or printed mass first. Only if still needed, switch to a higher-range analog mechanical gauge in the same family, not to an electronic sensor |
| Risk: model and hardware disagree | Quasi-static tests first; identify mass and stiffness from the real parts and re-run the model |
| Risk: scope growth | No Delta hardware; no adaptive-stiffness device; no sensing technology; WP3 stays a 1-D scan unless time remains |

---

## 10. Timeline

The plan assumes one final-year project session (adjust to the official UOW calendar).

| Phase | Period | Work |
|---|---|---|
| 1 | Weeks 1–3 | Literature, five-bar CAD sketch, kinematics and \(T_w\) derivation |
| 2 | Weeks 4–6 | GSM torque model, targeted-configuration design, baseline simulation |
| 3 | Weeks 7–9 | WP3: trajectory scan of \(\Theta\), comparison tables and plots |
| 4 | Weeks 10–14 | Detail design, print, assemble, mechanical force-gauge tests (PS-10N) |
| 5 | Weeks 15–18 | Thesis writing, extra gauge tests, discussion of limitations and variable payload |

A mid-project review with the supervisor should freeze geometry and the set of trajectories before printing.

---

## 11. What this proposal is not

This is **not** a reconstruction of the FANUC / theoretical Delta example in Nguyen et al. (2020). The Delta paper is the **method template**. The new object is the planar five-bar; the new chapter is automatic, task-oriented choice of the targeted configuration; the new evidence is a prototype comparison of the force required to move the mechanism, measured with a handheld mechanical force gauge. Sensing technology is outside the project.

---

## 12. References (starting set)

1. V. L. Nguyen, C.-Y. Lin and C.-H. Kuo, “Gravity compensation design of Delta parallel robots using gear-spring modules,” *Mechanism and Machine Theory*, vol. 154, 104046, 2020.
2. V. L. Nguyen, C.-Y. Lin and C.-H. Kuo, “Gravity compensation design of planar articulated robotic arms using the gear-spring modules,” *ASME Journal of Mechanisms and Robotics*, vol. 12, no. 3, 031014, 2020.
3. J. L. Herder, *Energy-free Systems: Theory, Conception and Design of Statically Balanced Spring Mechanisms*, Ph.D. thesis, TU Delft, 2001.
4. V. Arakelian, “Gravity compensation in robotics,” *Advanced Robotics*, vol. 30, no. 2, pp. 79–96, 2016.
5. I. Simionescu, L. Ciupitu and L. C. Ionita, “Static balancing with elastic systems of DELTA parallel robots,” *Mechanism and Machine Theory*, vol. 87, pp. 150–162, 2015.
6. X.-J. Liu, J. Wang and G. Pritschow, “Kinematics, singularity and workspace of planar 5R symmetrical parallel mechanisms,” *Mechanism and Machine Theory*, vol. 41, no. 2, pp. 145–169, 2006.
7. R. Clavel, “A fast robot with parallel geometry,” *Proc. Int. Symp. Industrial Robots*, pp. 91–100, 1988.
8. IMADA, Inc., “PS-10N Mechanical Force Gauge,” https://imada.com/products/ps-10n-mechanical-force-gauge/ (accessed August 2026).

---

## 13. One-paragraph statement for the supervisor

I would like to take the GSM targeted-configuration method in the 2020 Delta paper as a template, not as a case to rebuild. The thesis object will be a planar five-bar with the ground link on top and one GSM on each swinging crank. I will re-derive the statics, run the same class of torque and energy indices, add one chapter that chooses the targeted angle from the task instead of by hand, and 3D-print a small prototype. Following the advice not to use sensing technology, validation will be a handheld analog mechanical force gauge (IMADA PS-10N or the same mechanical family) that measures the force required to move the balanced and unbalanced mechanism. Variable payload and a spatial Delta hardware replica remain outside the scope.
