import os
import sys
from pathlib import Path

# Colour Codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
# Styles
UNDERLINE = '\033[4m'
BOLD = '\033[1m'
RESET = '\033[0m'

# Script Variables
NEWLN = "\n"
AUTHOR = "Marsden"
SCRIPT_NAME = os.path.basename(__file__)
EX_USAGE = f"Usage: Run this script to generate TI4 trophy plaques.{NEWLN}   Example: python {SCRIPT_NAME}"

# Paths
ICON_DIR = Path("_media/TI4_Icons/Black/Race Icons/")
FONT_PATH = Path("_media/Handel Gothic D Bold.otf")
OUTPUT_DIR = Path("outputs/")

# Config - Only change if plates change...
ICON_SIZE_WINNER = 11
ICON_SIZE_RUNNER_UP = 5
CANVAS_SIZE = ("47mm", "23mm")
TEXT_FONT_SIZE = 5
TEXT_FONT_SIZE_DATE = 3
TEXT_FONT_WEIGHT = "bold"

def print_header(message):
    print(f"{PURPLE}{BOLD}{message}{RESET}", flush=True)

def print_fatal_error(message):
    print(f"{RED}{BOLD}Fatal Error: {message}{RESET}", flush=True)
    sys.exit(1)

def print_error(message):
    print(f"{RED}{BOLD}Error: {message}{RESET}", flush=True)

def print_warning(message):
    print(f"{YELLOW}{BOLD}Warning: {message}{RESET}", flush=True)

def print_success(message):
    print(f"{GREEN}{BOLD}{message}{RESET}", flush=True)

def print_info(message):
    print(f"{BLUE}{message}{RESET}", flush=True)

def print_separator():
    print(f"{CYAN}------------------------------------{RESET}", flush=True)

######################

try:
    import svgwrite
except ImportError:
    print_fatal_error(f"'svgwrite' module not installed.{NEWLN}   Please install it via pip.")

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def find_icon_filename(race_name):
    """Find the correct filename for a race icon in the directory."""
    for filename in ICON_DIR.iterdir():
        if race_name.lower() in filename.stem.lower():
            print_info(f"Mapped {race_name} to: {filename.resolve().as_posix()}")
            return filename.resolve().as_posix()
    print_fatal_error(f"No mapping found for {race_name} in {ICON_DIR}")
    return None

def generate_trophy_plaque(winner, date, winner_icon, runner_up_icons, output_file):
    dwg = svgwrite.Drawing(str(output_file), size=CANVAS_SIZE, profile='tiny')
    
    # Map races to icons
    winner_icon_file = find_icon_filename(winner_icon)
    runner_up_files = [find_icon_filename(icon) for icon in runner_up_icons]
    
    if not winner_icon_file:
        raise FileNotFoundError(f"Winner icon '{winner_icon}' not found.")
    runner_up_files = [icon for icon in runner_up_files if icon is not None]
    
    winner_icon_x = 4
    winner_icon_y = 2
    
    text_x = 30
    text_y_name = 7
    text_y_date = 11
    
    vs_x = 10
    vs_y = 17
    
    runner_up_start_x = 17
    runner_up_y = 14
    runner_up_spacing = 10
    
    # Winner icon
    dwg.add(dwg.image(href=winner_icon_file, insert=(f"{winner_icon_x}mm", f"{winner_icon_y}mm"), size=(f"{ICON_SIZE_WINNER}mm", f"{ICON_SIZE_WINNER}mm")))
    # Winner name
    dwg.add(dwg.text(winner, insert=(f"{text_x}mm", f"{text_y_name}mm"), font_size=f"{TEXT_FONT_SIZE}mm", font_family="Handel Gothic D", text_anchor="middle", font_weight=TEXT_FONT_WEIGHT))
    # Date
    dwg.add(dwg.text(date, insert=(f"{text_x}mm", f"{text_y_date}mm"), font_size=f"{TEXT_FONT_SIZE_DATE}mm", font_family="Handel Gothic D", text_anchor="middle", font_weight=TEXT_FONT_WEIGHT))
    # "Vs"
    dwg.add(dwg.text("Vs", insert=(f"{vs_x}mm", f"{vs_y}mm"), font_size=f"{TEXT_FONT_SIZE_DATE}mm", font_family="Handel Gothic D", text_anchor="middle"))
    
    # Loser icons
    for i, icon_file in enumerate(runner_up_files):
        x_pos = runner_up_start_x + i * runner_up_spacing
        dwg.add(dwg.image(href=icon_file, insert=(f"{x_pos}mm", f"{runner_up_y}mm"), size=(f"{ICON_SIZE_RUNNER_UP}mm", f"{ICON_SIZE_RUNNER_UP}mm")))
    
    # Save the SVG
    dwg.save()
    print_info(f"Plaque saved as {output_file}")

def main():
    print_header(f"Script by: {AUTHOR}{NEWLN}   {EX_USAGE}")
    print_separator()

###
        
    generate_trophy_plaque(
        winner="MARSDEN",
        date="13-08-2023",
        winner_icon="Jol",
        runner_up_icons=["Arborec", "Letnev", "Yssaril"],
        output_file=OUTPUT_DIR / "Rnd1.svg"
    )
    
    print_separator()
    print_success("Script reached the end.")


if __name__ == "__main__":
    main()