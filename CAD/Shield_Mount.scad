// Box Turtle Pico Shield v2 Case/Mount
// PCB Dimensions: 100mm x 90mm

pcb_width = 100;
pcb_depth = 90;
wall = 2;
standoff_height = 5;
hole_offset = 4;

module pcb_case() {
    difference() {
        // Main Shell
        cube([pcb_width + 2*wall, pcb_depth + 2*wall, 10]);
        
        // Inner Cavity
        translate([wall, wall, 2])
            cube([pcb_width, pcb_depth, 10]);
    }

    // Standoffs
    translate([wall + hole_offset, wall + hole_offset, 0]) standoff();
    translate([wall + pcb_width - hole_offset, wall + hole_offset, 0]) standoff();
    translate([wall + hole_offset, wall + pcb_depth - hole_offset, 0]) standoff();
    translate([wall + pcb_width - hole_offset, wall + pcb_depth - hole_offset, 0]) standoff();
}

module standoff() {
    difference() {
        cylinder(h=standoff_height, r=3, $fn=20);
        cylinder(h=standoff_height+1, r=1.5, $fn=20); // M3 Hole
    }
}

pcb_case();
