# Box Turtle Top Hat (Lid) Build Guide

This guide outlines the process for constructing the "Top Hat" modification for the Box Turtle 3D printer, based on the design files in this repository.

## Phase 1: Preparation & Sourcing

### 1. Bill of Materials (BOM)
Source the following hardware before assembly:

**Panels**
*   **2x** Acrylic Discs (3mm thick, 220mm diameter) - *For the sides.*
*   **1x** PETG Sheet (1.5mm thick, 533mm x 384mm) - *For the main canopy. Must be PETG to bend correctly without heating.*

**Fasteners**
*   **60x** M3 Heat Set Inserts
*   **18x** M3 x 8mm Bolts
*   **16x** M3 x 10mm Bolts
*   **28x** M3 x 12mm Bolts

### 2. Decision Points (Before Printing)
Choose the correct files based on your printer size and frame type:

*   **Gable Style**:
    *   *Option A (Unibody)*: Use `Inner Gables/Unibody Gables/` if your printer bed is large enough to fit the full gable.
    *   *Option B (Multipart)*: Use `Inner Gables/Multipart LH/` and `RH/` if you need to print in smaller sections.
*   **Trim Style**:
    *   *Option A (Stock)*: Use `Trim/Front Trim/` and `Trim/Rear Trim/`.
    *   *Option B (Euro)*: Use `Trim/Euro V-Slot Trim/` if your Box Turtle uses Euro-style V-slot extrusions.

---

## Phase 2: 3D Printing Strategy

**Material Recommendation**: ABS or ASA is recommended for structural parts, especially if the printer will be enclosed or heated. PETG is acceptable for the Top Hat if high heat resistance isn't critical.

### Print List

| Component | Files to Print | Notes |
| :--- | :--- | :--- |
| **Outer Gables** | `Gable/Outer Gables/` (4 files: Front/Rear, LH/RH) | Main structural exterior. |
| **Inner Gables** | `Gable/Inner Gables/` (Unibody or Multipart) | Forms the inner frame. |
| **Trims** | `Trim/[Your_Choice]/` (Front & Rear sets) | Includes Fascias, Cleats, and Centre Cleats. |
| **Corners** | `BT_Replacement_Corner_section/` (x4) | Replaces stock corners to match the lid's chamfer. |
| **Template** | `End_Panel_Template.stl` | *Optional*: Print if you are cutting acrylic by hand. |

**Print Settings**:
*   **Infill**: 40%+ for structural rigidity.
*   **Walls**: 3-4 perimeters.
*   **Supports**: The README notes that supports are included in the CAD (colored green), but check your slicer. The Gables likely need support for overhangs.

---

## Phase 3: Fabrication (Non-Printed Parts)

1.  **Side Windows (Acrylic)**:
    *   **Laser Cut**: Use the `.lbrn2` files in `Box Turtle Lid/Lightbox Files/` if you have a laser cutter.
    *   **Manual Cut**: Use the printed `End_Panel_Template.stl` to mark and cut the 3mm acrylic discs. Note the flat cut-off section at the bottom.
2.  **Canopy (PETG Sheet)**:
    *   Cut the 1.5mm PETG sheet to exactly **533mm x 384mm**.
    *   *Note*: Do not heat bend this. It is designed to be cold-formed by the frame tension.

---

## Phase 4: Assembly

### Step 1: Frame Pre-Assembly
1.  Install **M3 Heat Set Inserts** into all designated holes in the printed parts (approx. 60 inserts).
2.  Assemble the **Inner Gables** (Orange parts in CAD).
    *   If using *Multipart* gables, bolt the `Upper` and `Lower` liners together using the `Inner Brace` parts.
3.  Attach the **Cross Members** (Trims) to the Inner Gables loosely. Do not fully tighten yet.

### Step 2: Canopy Installation
1.  Insert the **PETG Sheet** into the rear slot of the frame until it bottoms out.
2.  Gently bend the sheet over the curved Inner Gable formers.
3.  Tuck the front edge of the sheet into the front slot.
4.  Ensure the sheet is seated evenly.

### Step 3: Final Structural Assembly
1.  Place the **Acrylic Side Panels** into position.
2.  Bolt the **Outer Gables** (Red parts in CAD) to the Inner Gables, sandwiching the acrylic and locking the structure together.
    *   *Tip*: Fix from the inside.
3.  **Tighten** the cross-member assemblies. The tension will make the canopy rigid.

### Step 4: Mounting to Printer
1.  Remove the existing corner sections of your Box Turtle.
2.  Install the printed **Replacement Corner Sections** (`BT_Lid_Replacement_corner_x4.stl`).
3.  Place the assembled Top Hat onto the printer.
4.  Adjust the frame tension if necessary to ensure it sits level on the Box Turtle frame.
