import os
import sys
import base64
from pathlib import Path
import argparse

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
EX_USAGE = f"Usage: Run this script to generate TI4 trophy plaques.{NEWLN}   Example: python {SCRIPT_NAME} -w FUSSEL -d DD-MM-YYYY -i Arborec -r Creuss Xxcha Nekro -o filename"

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

def encode_image_to_base64(image_path):
    """Read an image file and return a Base64 encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print_fatal_error(f"File not found: {image_path}")
    except Exception as e:
        print_fatal_error(f"Error encoding image {image_path}: {e}")

def generate_trophy_plaque(winner, date, winner_icon, runner_up_icons, output_file):
    dwg = svgwrite.Drawing(str(output_file), size=CANVAS_SIZE, profile='tiny')

    # Map races to icons
    winner_icon_file = find_icon_filename(winner_icon)
    runner_up_files = [find_icon_filename(icon) for icon in runner_up_icons]

    if not winner_icon_file:
        raise FileNotFoundError(f"Winner icon '{winner_icon}' not found.")
    runner_up_files = [icon for icon in runner_up_files if icon is not None]

    # Encode images
    winner_icon_base64 = encode_image_to_base64(winner_icon_file)
    runner_up_base64 = [encode_image_to_base64(icon) for icon in runner_up_files]

    # Winner icon
    dwg.add(dwg.image(href=f"data:image/png;base64,{winner_icon_base64}",
                       insert=(f"{4}mm", f"{2}mm"),
                       size=(f"{ICON_SIZE_WINNER}mm", f"{ICON_SIZE_WINNER}mm")))

    # Winner name
    dwg.add(dwg.text(winner, insert=(f"{30}mm", f"{7}mm"),
                     font_size=f"{TEXT_FONT_SIZE}mm",
                     font_family="Handel Gothic D",
                     text_anchor="middle",
                     font_weight=TEXT_FONT_WEIGHT))

    # Date
    dwg.add(dwg.text(date, insert=(f"{30}mm", f"{11}mm"),
                     font_size=f"{TEXT_FONT_SIZE_DATE}mm",
                     font_family="Handel Gothic D",
                     text_anchor="middle",
                     font_weight=TEXT_FONT_WEIGHT))

    # "Vs"
    dwg.add(dwg.text("Vs", insert=(f"{10}mm", f"{17}mm"),
                     font_size=f"{TEXT_FONT_SIZE_DATE}mm",
                     font_family="Handel Gothic D",
                     text_anchor="middle"))

    # Runner-up icons
    for i, base64_icon in enumerate(runner_up_base64):
        x_pos = 17 + i * 10
        dwg.add(dwg.image(href=f"data:image/png;base64,{base64_icon}",
                           insert=(f"{x_pos}mm", f"{14}mm"),
                           size=(f"{ICON_SIZE_RUNNER_UP}mm", f"{ICON_SIZE_RUNNER_UP}mm")))

    # Save the SVG
    dwg.save()
    print_info(f"Plaque saved as {output_file}")

def generate_from_rounds_file(rounds_file, force=False):
    """Generate a plaque for every round in the rounds file that doesn't already have one."""
    import json
    try:
        rounds = json.loads(Path(rounds_file).read_text(encoding="utf-8"))
    except Exception as e:
        print_fatal_error(f"Could not read {rounds_file}: {e}")

    for rnd in rounds:
        output_path = OUTPUT_DIR / f"{rnd['id']}.svg"
        if output_path.exists() and not force:
            print_info(f"Skipping {rnd['id']} - {output_path} already exists")
            continue
        generate_trophy_plaque(
            winner=rnd["winner"],
            date=rnd["date"],
            winner_icon=rnd["winner_icon"],
            runner_up_icons=rnd["runners"],
            output_file=output_path
        )

def main():
    print_header(f"Script by: {AUTHOR}{NEWLN}   {EX_USAGE}")
    print_separator()
    
    parser = argparse.ArgumentParser(description="Generate a TI4 trophy plaque.")
    parser.add_argument("-w", "--winner", help="Winner's name")
    parser.add_argument("-d", "--date", help="Date of the event")
    parser.add_argument("-i", "--winner-icon", help="Winner's race icon")
    parser.add_argument("-r", "--runner-up-icons", nargs="+", help="Runner-up race icons")
    parser.add_argument("-o", "--output-file", help="Output filename (without extension)")
    parser.add_argument("--rounds-file", help="Generate missing plaques for every round in this JSON file (e.g. rounds.json)")
    parser.add_argument("--force", action="store_true", help="With --rounds-file, regenerate plaques that already exist")

    args = parser.parse_args()

    if args.rounds_file:
        generate_from_rounds_file(args.rounds_file, force=args.force)
        print_separator()
        print_success("Script reached the end.")
        return

    missing = [f"--{n.replace('_', '-')}" for n in ("winner", "date", "winner_icon", "runner_up_icons", "output_file") if not getattr(args, n)]
    if missing:
        parser.error(f"the following arguments are required: {', '.join(missing)}")

    output_path = OUTPUT_DIR / f"{args.output_file}.svg"

    generate_trophy_plaque(
        winner=args.winner,
        date=args.date,
        winner_icon=args.winner_icon,
        runner_up_icons=args.runner_up_icons,
        output_file=output_path
    )

    print_separator()
    print_success("Script reached the end.")

if __name__ == "__main__":
    main()
