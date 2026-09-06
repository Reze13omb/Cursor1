// Hanging planar five-bar — Week 1–3 kinematic sketch (mm)
// Not a final print file. GSM is omitted.
// Ground on top. Open in OpenSCAD, F5 preview, F6 render.

d = 180.0;
l1 = 120.0;
l2 = l1;
l3 = 180.0;
l4 = l3;
w  = 20.0;
t  = 8.0;
hole = 8.2;

module link(len) {
    difference() {
        hull() {
            translate([0,0,0]) cylinder(h=t, d=w, center=true);
            translate([len,0,0]) cylinder(h=t, d=w, center=true);
        }
        translate([0,0,0]) cylinder(h=t+2, d=hole, center=true);
        translate([len,0,0]) cylinder(h=t+2, d=hole, center=true);
    }
}

module ground() {
    difference() {
        hull() {
            translate([-d/2,0,0]) cylinder(h=t+2, d=w+8, center=true);
            translate([ d/2,0,0]) cylinder(h=t+2, d=w+8, center=true);
        }
        translate([-d/2,0,0]) cylinder(h=t+6, d=hole, center=true);
        translate([ d/2,0,0]) cylinder(h=t+6, d=hole, center=true);
    }
}

// Preview pose: left/right cranks at sample IK (approx.)
theta_L = -120.0; // replace after Week 1–3 IK script
theta_R = 180 - theta_L;

color("dimgray") ground();
translate([-d/2,0,t]) rotate([0,0,theta_L]) color("steelblue") link(l1);
translate([ d/2,0,t]) rotate([0,0,theta_R]) color("steelblue") link(l2);
// Couplers are left as separate parts for the student to assemble after IK is coded.
