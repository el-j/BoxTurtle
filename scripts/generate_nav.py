import os
import json

DOCS_DIR = "docs"
NAV_FILE = "docs/_data/navigation.json"

def get_title(filepath):
    """Extract title from front matter or filename."""
    try:
        with open(filepath, 'r') as f:
            lines = f.readlines()
            if lines and lines[0].strip() == "---":
                for line in lines[1:]:
                    if line.strip() == "---":
                        break
                    if line.startswith("title:"):
                        return line.split(":", 1)[1].strip().strip('"')
    except Exception:
        pass
    
    # Fallback to filename
    filename = os.path.basename(filepath)
    name = os.path.splitext(filename)[0]
    return name.replace('_', ' ').title()

def main():
    nav_items = []
    
    # Define order if needed, otherwise alphabetical
    # Let's try to find specific files first to enforce order
    priority_files = ["index.md", "hardware_assembly.md", "electronics_design.md", "firmware_setup.md", "configuration.md", "user_manual.md"]
    
    # Get all md files
    all_files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".md")]
    
    # Process priority files first
    for filename in priority_files:
        if filename in all_files:
            path = os.path.join(DOCS_DIR, filename)
            title = get_title(path)
            url = f"/{filename.replace('.md', '.html')}"
            if filename == "index.md":
                url = "/"
            
            nav_items.append({"title": title, "url": url})
            all_files.remove(filename)
            
    # Process remaining files
    for filename in sorted(all_files):
        path = os.path.join(DOCS_DIR, filename)
        title = get_title(path)
        url = f"/{filename.replace('.md', '.html')}"
        nav_items.append({"title": title, "url": url})

    # Ensure _data directory exists
    os.makedirs(os.path.dirname(NAV_FILE), exist_ok=True)
    
    with open(NAV_FILE, 'w') as f:
        json.dump(nav_items, f, indent=2)
    
    print(f"Generated navigation with {len(nav_items)} items.")

if __name__ == "__main__":
    main()
