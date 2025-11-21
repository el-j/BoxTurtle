import os
import subprocess
import sys

# Configuration
DOCS_IMG_DIR = "docs/images"
SCAD_DIR = "CAD"
STL_DIR = "STLs"

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def render_scad(scad_file, output_file):
    print(f"Rendering {scad_file} to {output_file}...")
    cmd = [
        "openscad",
        "-o", output_file,
        "--imgsize=1024,768",
        "--colorscheme=Tomorrow Night",
        "--viewall",
        "--autocenter",
        scad_file
    ]
    subprocess.run(cmd, check=True)

def render_stl(stl_file, output_file):
    print(f"Rendering {stl_file} to {output_file}...")
    # Create a temporary SCAD wrapper
    temp_scad = "temp_render.scad"
    # OpenSCAD needs absolute path or relative to the scad file. 
    # Let's use absolute path for the import to be safe
    abs_stl = os.path.abspath(stl_file)
    
    with open(temp_scad, "w") as f:
        f.write(f'import("{abs_stl}");')
    
    cmd = [
        "openscad",
        "-o", output_file,
        "--imgsize=1024,768",
        "--colorscheme=Tomorrow Night",
        "--viewall",
        "--autocenter",
        temp_scad
    ]
    try:
        subprocess.run(cmd, check=True)
    finally:
        if os.path.exists(temp_scad):
            os.remove(temp_scad)

def main():
    ensure_dir(DOCS_IMG_DIR)
    
    # 1. Render SCAD files in CAD/
    for root, dirs, files in os.walk(SCAD_DIR):
        for file in files:
            if file.endswith(".scad"):
                source_path = os.path.join(root, file)
                # Flatten output name: CAD_Shield_Mount.png
                out_name = f"CAD_{file.replace('.scad', '.png')}"
                out_path = os.path.join(DOCS_IMG_DIR, out_name)
                render_scad(source_path, out_path)

    # 2. Render STLs in STLs/Base_Build
    # We want to render all parts in Base_Build to provide a comprehensive guide
    base_build_dir = os.path.join(STL_DIR, "Base_Build")
    if os.path.exists(base_build_dir):
        for root, dirs, files in os.walk(base_build_dir):
            for file in files:
                if file.endswith(".stl") and not file.startswith("."):
                    source_path = os.path.join(root, file)
                    # Create a descriptive name: Extruder_motor_plate.png
                    # Use the parent folder name as a prefix if it's not Base_Build
                    parent_dir = os.path.basename(root)
                    if parent_dir == "Base_Build":
                        out_name = f"STL_{file.replace('.stl', '.png')}"
                    else:
                        out_name = f"STL_{parent_dir}_{file.replace('.stl', '.png')}"
                    
                    out_path = os.path.join(DOCS_IMG_DIR, out_name)
                    render_stl(source_path, out_path)

    # 3. Placeholder for Fritzing Rendering (Web-based)
    # Strategy: Use a headless browser (Playwright/Puppeteer) to load a local HTML file
    # that renders the .fz XML using a JS library (e.g., freetzing/relay or next-gen).
    # Then take a screenshot.
    #
    # Example pseudo-code:
    # run_node_script("scripts/render_fritzing.js", input="BT_Wiring/BoxTurtle_Shield_Basic.fz", output="docs/images/PCB_Basic.png")
    print("Skipping Fritzing render (Requires Node.js + Playwright setup)...")

if __name__ == "__main__":
    main()
