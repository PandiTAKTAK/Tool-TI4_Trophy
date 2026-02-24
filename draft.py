import os
import sys
import argparse
import random

# Colour Codes
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

NEWLN = "\n"
AUTHOR = "Marsden"
SCRIPT_NAME = os.path.basename(__file__)
EX_USAGE = (
    f"Usage: Run this script to generate TI4 faction draft options.{NEWLN}"
    f"   Example: python {SCRIPT_NAME} -p4 -c4 --pok --codex --seed 1337 -b Nekro Titans Hacan Jol Sol Empyr Muaat Vuil --names TAKTAK FUSS DERZ PAW"
)

######################

FACTIONS = {
    # Base game
    "Arborec": {"icon": "Arborec", "slug": "ab", "expansion": "base"},
    "Barony of Letnev": {"icon": "Letnev", "slug": "bl", "expansion": "base"},
    "Clan of Saar": {"icon": "Saar", "slug": "cs", "expansion": "base"},
    "Embers of Muaat": {"icon": "Muaat", "slug": "mu", "expansion": "base"},
    "Emirates of Hacan": {"icon": "Hacan", "slug": "eh", "expansion": "base"},
    "Federation of Sol": {"icon": "Sol", "slug": "fs", "expansion": "base"},
    "Ghosts of Creuss": {"icon": "Creuss", "slug": "gc", "expansion": "base"},
    "L1Z1X Mindnet": {"icon": "L1Z1X", "slug": "lm", "expansion": "base"},
    "Mentak Coalition": {"icon": "Mentak", "slug": "mc", "expansion": "base"},
    "Naalu Collective": {"icon": "Naalu", "slug": "nc", "expansion": "base"},
    "Nekro Virus": {"icon": "Nekro", "slug": "nv", "expansion": "base"},
    "Sardakk N'orr": {"icon": "Sardakk", "slug": "sn", "expansion": "base"},
    "Universities of Jol-Nar": {"icon": "Jol Nar", "slug": "jn", "expansion": "base"},
    "Winnu": {"icon": "Winnu", "slug": "wn", "expansion": "base"},
    "Xxcha Kingdom": {"icon": "Xxcha", "slug": "xk", "expansion": "base"},
    "Yin Brotherhood": {"icon": "Yin", "slug": "yb", "expansion": "base"},
    "Yssaril Tribes": {"icon": "Yssaril", "slug": "yt", "expansion": "base"},

    # PoK
    "Argent Flight": {"icon": "Argent", "slug": "af", "expansion": "pok"},
    "Empyrean": {"icon": "Empyrean", "slug": "em", "expansion": "pok"},
    "Mahact Gene-Sorcerers": {"icon": "Mahact", "slug": "mg", "expansion": "pok"},
    "Naaz-Rokha Alliance": {"icon": "Naaz-Rokha", "slug": "nr", "expansion": "pok"},
    "Nomad": {"icon": "Nomad", "slug": "no", "expansion": "pok"},
    "Titans of Ul": {"icon": "Titans", "slug": "tu", "expansion": "pok"},
    "Vuil'Raith Cabal": {"icon": "Vuil'Raith", "slug": "vc", "expansion": "pok"},

    # Codex
    "Council Keleres": {"icon": "Keleres", "slug": "ck", "expansion": "codex"},
}

######################

def print_header(msg):
    print(f"{PURPLE}{BOLD}{msg}{RESET}", flush=True)

def print_info(msg):
    print(f"{BLUE}{msg}{RESET}", flush=True)

def print_warning(msg):
    print(f"{YELLOW}{BOLD}Warning: {msg}{RESET}", flush=True)

def print_fatal_error(msg):
    print(f"{RED}{BOLD}Fatal Error: {msg}{RESET}", flush=True)
    sys.exit(1)

def print_success(msg):
    print(f"{GREEN}{BOLD}{msg}{RESET}", flush=True)

def print_separator():
    print(f"{CYAN}------------------------------------{RESET}", flush=True)

######################

def build_faction_pool(include_pok, include_codex):
    pool = [name for name, data in FACTIONS.items() if data["expansion"] == "base"]
    if include_pok:
        pool.extend(name for name, data in FACTIONS.items() if data["expansion"] == "pok")
    if include_codex:
        pool.extend(name for name, data in FACTIONS.items() if data["expansion"] == "codex")
    return pool

######################

def generate_draft(players, choices_per_player, factions, banned, seed=None):
    if seed is None:
        seed = random.randint(0, 999999)
    random.seed(seed)
    print_success(f"Seed used for draft -> {seed}")

    available = [f for f in factions if f not in banned]
    required = players * choices_per_player
    if required > len(available):
        print_fatal_error(
            f"Not enough factions available.\nRequired: {required}\nAvailable: {len(available)}"
        )
    random.shuffle(available)
    draft = {}
    index = 0
    for i in range(1, players + 1):
        draft[f"Player {i}"] = available[index:index + choices_per_player]
        index += choices_per_player
    return draft

def generate_faction_url(factions):
    slugs = [FACTIONS[f]["slug"] for f in factions]
    return "https://ti4.basicallyfine.com/factions/" + ",".join(slugs) + ";ti-c3"
    # Need to fix the above for non POK and Codex - Meh
    
def select_speaker(players):
    speaker = random.choice(list(players))
    print_success(f"Speaker -> {speaker}")
    return speaker

######################

def main():
    print_header(f"Script by: {AUTHOR}\n{EX_USAGE}")
    print_separator()

    parser = argparse.ArgumentParser(description="Generate TI4 faction draft options.")
    parser.add_argument("-p", "--players", type=int, required=True)
    parser.add_argument("-c", "--choices", type=int, default=4)
    parser.add_argument("-b", "--banned", nargs="*", default=[])
    parser.add_argument("--pok", action="store_true")
    parser.add_argument("--codex", action="store_true")
    parser.add_argument("--seed", type=int)
    parser.add_argument("-n", "--names", nargs="*")
    parser.add_argument("-s", "--speaker", action="store_true")
    args = parser.parse_args()

    faction_pool = build_faction_pool(args.pok, args.codex)

    # Partialmatch bans
    resolved_banned = set()
    for ban in args.banned:
        matches = [f for f in faction_pool if ban.lower() in f.lower()]
        if matches:
            resolved_banned.update(matches)
        else:
            print_warning(f"Banned faction '{ban}' not found in pool")
    banned = resolved_banned
    print_success(f"Banning -> {', '.join(sorted(banned))}")
    print_separator()
    print_info(f"Players: {args.players}")
    print_info(f"Choices per player: {args.choices}")
    print_info(f"Faction pool size: {len(faction_pool)}")
    print_info(f"Banned factions count: {len(banned)}")
    print_separator()

    draft = generate_draft(args.players, args.choices, faction_pool, banned, args.seed)

    if args.names:
        if len(args.names) != args.players:
            print_warning(
                f"Number of player names ({len(args.names)}) does not match "
                f"number of players ({args.players}), ignoring custom names."
            )
        else:
            print_success(
                f"Using -> ({args.names}) "
            )
            draft = {name: options for name, options in zip(args.names, draft.values())}

    # RN-Jesus already set globally for seed
    speaker = None
    if args.speaker:
        print_separator()
        speaker = select_speaker(draft.keys())
        print_separator()

    for player, options in draft.items():
        tag = " (Speaker)" if player == speaker else ""
        print_info(f"{player}{tag}")
        for f in options:
            print_info(f"  - {f}")
        url = generate_faction_url(options)
        print_success(f"  View picks -> {url}")

    print_separator()
    
    print_success("Script reached the end.")

if __name__ == "__main__":
    main()