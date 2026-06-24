+#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════╗
║           S T R A N D E D  —  A Survival Roguelike          ║
║                    Just run: python survive.py               ║
╚══════════════════════════════════════════════════════════════╝
No installs needed. Pure Python 3. Just run it!
"""

import random
import time
import os
import sys
import json
from datetime import datetime

# ─── COLORS (works on Windows 10+, Mac, Linux) ────────────────
def enable_colors():
    if sys.platform == "win32":
        os.system("color")  # enable ANSI on Windows

enable_colors()

R  = "\033[0m"       # reset
BLD= "\033[1m"       # bold
DIM= "\033[2m"       # dim

# Foreground colors
RED   = "\033[91m"
GRN   = "\033[92m"
YLW   = "\033[93m"
BLU   = "\033[94m"
MAG   = "\033[95m"
CYN   = "\033[96m"
WHT   = "\033[97m"
DRED  = "\033[31m"
DGRN  = "\033[32m"
DYLW  = "\033[33m"
DBLU  = "\033[34m"
DMAG  = "\033[35m"
DCYN  = "\033[36m"

# Background
BG_RED  = "\033[41m"
BG_GRN  = "\033[42m"
BG_YLW  = "\033[43m"
BG_BLU  = "\033[44m"

def clr():
    os.system('cls' if os.platform == "win32" else 'clear') if hasattr(os, 'platform') else os.system('clear')

def clear():
    os.system('cls' if sys.platform == 'win32' else 'clear')

def slow(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

def bar(val, max_val, length=20, fill='█', empty='░', color=GRN):
    filled = int((val / max_val) * length)
    filled = max(0, min(filled, length))
    b = color + fill * filled + DIM + empty * (length - filled) + R
    return f"[{b}]"

def inp(prompt=""):
    try:
        return input(f"{CYN}❯ {YLW}{prompt}{R} ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print(f"\n{YLW}Thanks for playing STRANDED!{R}")
        sys.exit(0)

def pause(msg="Press ENTER to continue..."):
    try:
        input(f"{DIM}{msg}{R}")
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

# ─── GAME DATA ─────────────────────────────────────────────────

LOCATIONS = {
    "beach":    {"name": "Crashed Beach",     "emoji": "🏖️ ", "color": YLW,  "danger": 1},
    "jungle":   {"name": "Dense Jungle",      "emoji": "🌿", "color": DGRN, "danger": 3},
    "cave":     {"name": "Dark Cave",         "emoji": "🪨", "color": DIM,  "danger": 4},
    "mountain": {"name": "Rocky Mountain",    "emoji": "⛰️ ", "color": WHT,  "danger": 5},
    "ruins":    {"name": "Ancient Ruins",     "emoji": "🏛️ ", "color": DYLW, "danger": 6},
    "swamp":    {"name": "Toxic Swamp",       "emoji": "🦠", "color": DGRN, "danger": 5},
    "volcano":  {"name": "Active Volcano",    "emoji": "🌋", "color": RED,  "danger": 8},
    "camp":     {"name": "Your Camp",         "emoji": "🏕️ ", "color": GRN,  "danger": 0},
}

LOCATION_CONNECTIONS = {
    "camp":     ["beach", "jungle"],
    "beach":    ["camp", "jungle", "swamp"],
    "jungle":   ["beach", "cave", "ruins", "camp"],
    "cave":     ["jungle", "mountain"],
    "mountain": ["cave", "volcano"],
    "ruins":    ["jungle", "swamp"],
    "swamp":    ["beach", "ruins"],
    "volcano":  ["mountain"],
}

ITEMS = {
    # name: (emoji, type, value, weight, description)
    "berries":      ("🍇", "food",    15, 1, "Wild berries. Restores 15 HP."),
    "coconut":      ("🥥", "food",    25, 2, "Fresh coconut. Restores 25 HP."),
    "fish":         ("🐟", "food",    30, 2, "Raw fish. Risky but filling (+30 HP, 20% chance of sickness)."),
    "cooked_fish":  ("🍖", "food",    45, 2, "Cooked fish. Restores 45 HP safely."),
    "mushroom":     ("🍄", "food",    10, 1, "Strange mushroom. +10 HP, 30% chance of poison."),
    "water":        ("💧", "drink",   20, 1, "Clean water. Restores 20 thirst."),
    "coconut_milk": ("🥛", "drink",   30, 1, "Coconut milk. Restores 30 thirst."),
    "stick":        ("🪵", "material",0,  1, "A sturdy stick. Used for crafting."),
    "stone":        ("🪨", "material",0,  1, "Sharp stone. Used for crafting."),
    "vine":         ("🌿", "material",0,  1, "Flexible vine. Used for crafting."),
    "flint":        ("💎", "material",0,  1, "Flint. Used to make fire."),
    "cloth":        ("🧵", "material",0,  1, "Torn cloth from wreckage."),
    "knife":        ("🔪", "weapon",  15, 2, "Makeshift knife. +15 attack."),
    "spear":        ("🏹", "weapon",  25, 3, "Wooden spear. +25 attack."),
    "torch":        ("🔦", "weapon",  10, 2, "Torch. +10 attack, lights dark areas."),
    "shield":       ("🛡️ ", "armor",   20, 3, "Wooden shield. +20 defense."),
    "bandage":      ("🩹", "medical", 30, 1, "Cloth bandage. Heals 30 HP instantly."),
    "antidote":     ("💊", "medical", 0,  1, "Cures poison/sickness."),
    "signal_flare": ("🚨", "special", 0,  1, "Emergency flare. Use at the volcano to signal rescue!"),
    "map_piece":    ("🗺️ ", "special", 0,  1, "Piece of an old map. Collect all 3 to find the treasure!"),
    "treasure":     ("💰", "special", 0,  5, "Ancient treasure! Worth a fortune if you escape."),
    "rope":         ("🪢", "material",0,  2, "Strong rope. Used for crafting."),
    "fire_kit":     ("🔥", "tool",    0,  2, "Fire-starting kit. Cook food, stay warm."),
    "raft_wood":    ("🪵", "material",0,  5, "Heavy raft planks. Need 3 to build an escape raft!"),
}

CRAFTING_RECIPES = {
    "knife":       ({"stick": 1, "flint": 1},          "A sharp survival knife."),
    "spear":       ({"stick": 2, "flint": 1, "vine": 1},"A deadly throwing spear."),
    "torch":       ({"stick": 1, "cloth": 1},           "Burns bright in the dark."),
    "shield":      ({"stick": 2, "vine": 2},            "Basic wooden protection."),
    "bandage":     ({"cloth": 2},                       "Emergency wound dressing."),
    "antidote":    ({"mushroom": 1, "berries": 1},      "Cures toxins. Risky to make."),
    "fire_kit":    ({"flint": 1, "stick": 1, "cloth": 1},"Make fire anywhere."),
    "rope":        ({"vine": 3},                        "Strong braided rope."),
    "cooked_fish": ({"fish": 1, "fire_kit": 1},         "Cook a fish safely."),
}

# win condition: build raft (3 raft_wood) OR signal with flare at volcano
WIN_RAFT  = {"raft_wood": 3}
WIN_FLARE = "signal_flare"

ENEMIES = {
    "wolf":      ("🐺", 40,  15, 8,  "A hungry wolf!",           20),
    "boar":      ("🐗", 55,  20, 12, "An angry wild boar!",      15),
    "snake":     ("🐍", 25,  12, 5,  "A venomous snake! (May poison you)", 10),
    "crocodile": ("🐊", 80,  30, 20, "A massive crocodile!",     12),
    "giant_bat": ("🦇", 35,  10, 6,  "A swarm of giant bats!",   25),
    "jaguar":    ("🐆", 70,  35, 15, "A stalking jaguar!",       8),
    "golem":     ("🗿", 120, 40, 5,  "An ancient stone golem!",  5),
    "lava_crab": ("🦀", 90,  45, 10, "A fire-hardened lava crab!",7),
    "bandit":    ("💀", 60,  25, 18, "A hostile survivor!",      10),
}

LOCATION_ENEMIES = {
    "beach":    ["wolf", "giant_bat"],
    "jungle":   ["boar", "snake", "jaguar"],
    "cave":     ["giant_bat", "snake", "golem"],
    "mountain": ["wolf", "jaguar", "golem"],
    "ruins":    ["snake", "golem", "bandit"],
    "swamp":    ["crocodile", "snake", "giant_bat"],
    "volcano":  ["lava_crab", "golem"],
    "camp":     [],
}

LOCATION_LOOT = {
    "beach":    ["stick", "stone", "cloth", "coconut", "coconut_milk", "vine"],
    "jungle":   ["stick", "vine", "berries", "mushroom", "flint", "raft_wood"],
    "cave":     ["stone", "flint", "torch", "map_piece"],
    "mountain": ["flint", "stone", "map_piece", "signal_flare"],
    "ruins":    ["cloth", "bandage", "map_piece", "treasure", "knife"],
    "swamp":    ["vine", "mushroom", "stick"],
    "volcano":  ["flint", "lava_crab", "raft_wood"],
    "camp":     ["stick", "cloth"],
}

EVENTS = [
    ("🌧️  Heavy rain! You collect fresh water.", "drink", +25),
    ("☀️  Scorching sun drains you.", "thirst", -15),
    ("🌙  Cold night. You lose energy.", "hp", -10),
    ("🍀  Lucky find! You discover some berries.", "item", "berries"),
    ("💨  A strong wind blows useful debris your way.", "item", "stick"),
    ("🤢  You feel sick from the environment.", "hp", -20),
    ("✨  You feel refreshed and energised!", "hp", +15),
    ("🌊  A wave crashes in — you find driftwood!", "item", "raft_wood"),
    ("🎯  Your survival instincts sharpen. +5 attack this turn.", "attack_bonus", +5),
    ("😴  Exhaustion hits. You must rest.", "hp", -5),
]

STORY_INTRO = """
{RED}{BLD}
  ██████ ████████ ████████   ██████   ███    ██ ██████  ███████ ██████
 ██         ██    ██     ██  ██   ██  ████   ██ ██   ██ ██      ██   ██
  ██████    ██    ████████   ████████ ██ ██  ██ ██   ██ █████   ██   ██
       ██   ██    ██    ██   ██   ██  ██  ██ ██ ██   ██ ██      ██   ██
  ██████    ██    ██     ██  ██   ██  ██   ████ ██████  ███████ ██████
{R}
{YLW}              A  S U R V I V A L  R O G U E L I K E{R}
""".format(RED=RED, BLD=BLD, R=R, YLW=YLW)

# ─── PLAYER ────────────────────────────────────────────────────

class Player:
    def __init__(self, name):
        self.name       = name
        self.hp         = 100
        self.max_hp     = 100
        self.hunger     = 100   # 0 = starving
        self.thirst     = 100   # 0 = dehydrated
        self.attack     = 10
        self.defense    = 5
        self.inventory  = {}    # item_name: count
        self.location   = "camp"
        self.day        = 1
        self.actions    = 3     # actions per day
        self.score      = 0
        self.kills      = 0
        self.poisoned   = False
        self.sick       = False
        self.has_fire   = False
        self.map_pieces = 0
        self.escaped    = False
        self.log        = []

    def add_item(self, item, count=1):
        if item in self.inventory:
            self.inventory[item] += count
        else:
            self.inventory[item] = count
        if item == "map_piece":
            self.map_pieces = self.inventory.get("map_piece", 0)

    def remove_item(self, item, count=1):
        if item in self.inventory and self.inventory[item] >= count:
            self.inventory[item] -= count
            if self.inventory[item] == 0:
                del self.inventory[item]
            return True
        return False

    def has(self, item, count=1):
        return self.inventory.get(item, 0) >= count

    def weapon_bonus(self):
        bonus = 0
        for w in ["knife", "spear", "torch"]:
            if self.has(w):
                bonus += ITEMS[w][2]
                break  # only best weapon counts
        return bonus

    def armor_bonus(self):
        if self.has("shield"):

            return ITEMS["shield"][2]
        return 0

    def total_attack(self):
        return self.attack + self.weapon_bonus()

    def total_defense(self):
        return self.defense + self.armor_bonus()

    def is_alive(self):
        return self.hp > 0 and self.hunger > 0 and self.thirst > 0

    def tick_day(self):
        self.day += 1
        self.hunger -= random.randint(10, 18)
        self.thirst -= random.randint(15, 22)
        self.actions = 3
        if self.poisoned:
            self.hp -= 15
        if self.sick:
            self.hp -= 10
            self.hunger -= 5
        self.hunger = max(0, self.hunger)
        self.thirst = max(0, self.thirst)
        self.hp = min(self.hp, self.max_hp)
        self.score += 10  # +10 per day survived

    def log_event(self, msg):
        self.log.append(f"Day {self.day}: {msg}")
        if len(self.log) > 20:
            self.log = self.log[-20:]

# ─── DISPLAY ───────────────────────────────────────────────────

def print_header(player):
    clear()
    loc = LOCATIONS[player.location]
    lc  = loc["color"]
    print(f"{BLD}{RED}⚡ STRANDED {DIM}— Day {player.day} — {lc}{loc['emoji']} {loc['name']}{R}")
    print("─" * 62)

    # HP bar
    hp_color = GRN if player.hp > 50 else YLW if player.hp > 25 else RED
    print(f"  {RED}❤  HP    {R}{bar(player.hp, player.max_hp, 18, color=hp_color)} {hp_color}{BLD}{player.hp}/{player.max_hp}{R}", end="")
    # Status effects
    if player.poisoned: print(f"  {DMAG}☠ POISONED{R}", end="")
    if player.sick:     print(f"  {YLW}🤢 SICK{R}", end="")
    print()

    hunger_color = GRN if player.hunger > 40 else YLW if player.hunger > 20 else RED
    thirst_color = GRN if player.thirst > 40 else YLW if player.thirst > 20 else RED
    print(f"  {YLW}🍖 Hunger{R}{bar(player.hunger, 100, 18, color=hunger_color)} {hunger_color}{BLD}{player.hunger}/100{R}")
    print(f"  {BLU}💧 Thirst{R}{bar(player.thirst, 100, 18, color=thirst_color)} {thirst_color}{BLD}{player.thirst}/100{R}")

    # Actions left
    actions_str = f"{GRN}{'◆ ' * player.actions}{DIM}{'◇ ' * (3 - player.actions)}{R}"
    print(f"  ⚡ Actions: {actions_str}  {DIM}Score: {YLW}{player.score}{R}")

    # Fire / map pieces
    fire_str = f"{RED}🔥 Fire ready{R}" if player.has_fire else f"{DIM}No fire{R}"
    map_str  = f"{DYLW}🗺 Map: {player.map_pieces}/3{R}"
    print(f"  {fire_str}   {map_str}")
    print("─" * 62)

def print_inventory(player):
    if not player.inventory:
        print(f"  {DIM}(empty){R}")
        return
    cols = 0
    for item, count in sorted(player.inventory.items()):
        if item in ITEMS:
            emoji, itype, *_ = ITEMS[item]
            color = {
                "food": GRN, "drink": BLU, "weapon": RED,
                "armor": YLW, "medical": MAG, "material": DCYN,
                "special": DYLW, "tool": CYN
            }.get(itype, WHT)
            print(f"  {color}{emoji} {item:<16}{R} x{count}", end="   ")
            cols += 1
            if cols % 2 == 0:
                print()
    if cols % 2 != 0:
        print()

def print_map(player):
    print(f"\n{BLD}{YLW}  🗺  ISLAND MAP{R}")
    connected = LOCATION_CONNECTIONS[player.location]
    for loc_id, loc in LOCATIONS.items():
        if loc_id == player.location:
            marker = f"{BG_BLU}{WHT}{BLD} YOU {R}"
        elif loc_id in connected:
            marker = f"{GRN} ← go{R}"
        else:
            marker = ""
        danger = "⚠️ " * min(loc["danger"] // 2, 4)
        print(f"  {loc['color']}{loc['emoji']} {loc['name']:<22}{R} {danger} {marker}")

# ─── COMBAT ────────────────────────────────────────────────────

def do_combat(player, enemy_key):
    enemy_data = ENEMIES[enemy_key]
    emoji, e_hp, e_atk, e_def, e_desc, _ = enemy_data
    e_hp_max = e_hp

    clear()
    print(f"\n{RED}{BLD}⚔  COMBAT STARTED!{R}")
    print(f"  {emoji} {RED}{e_desc}{R}")
    print(f"  Enemy HP: {e_hp} | Attack: {e_atk} | Defense: {e_def}")
    print(f"  Your attack: {player.total_attack()} | Defense: {player.total_defense()}")
    pause()

    flee_chance = 40

    while e_hp > 0 and player.hp > 0:
        clear()
        print(f"\n{RED}{BLD}⚔  COMBAT  {R}— {emoji} {enemy_key.upper()}")
        print(f"  {RED}Enemy HP {R}{bar(e_hp, e_hp_max, 18, color=RED)} {RED}{e_hp}/{e_hp_max}{R}")
        print(f"  {GRN}Your HP  {R}{bar(player.hp, player.max_hp, 18)} {GRN}{player.hp}/{player.max_hp}{R}")
        print()
        print(f"  {YLW}[1]{R} Attack   {YLW}[2]{R} Heavy attack (−5 defense this turn)")
        print(f"  {YLW}[3]{R} Use item {YLW}[4]{R} Try to flee ({flee_chance}% chance)")
        choice = inp("Combat choice: ")

        player_dmg = 0
        enemy_dmg  = 0
        temp_def   = player.total_defense()

        if choice == "1":
            player_dmg = max(1, player.total_attack() - e_def + random.randint(-3, 5))
            e_hp -= player_dmg
            print(f"\n  {GRN}You strike! Dealt {player_dmg} damage.{R}")

        elif choice == "2":
            player_dmg = max(1, int(player.total_attack() * 1.6) - e_def + random.randint(-2, 8))
            e_hp -= player_dmg
            temp_def -= 5
            print(f"\n  {YLW}Heavy strike! Dealt {player_dmg} damage. (Defence reduced this turn){R}")

        elif choice == "3":
            print("\n  Items available:")
            usable = {k: v for k, v in player.inventory.items()
                      if k in ITEMS and ITEMS[k][1] in ("food", "drink", "medical")}
            if not usable:
                print(f"  {RED}Nothing usable!{R}")
                pause()
                continue
            for i, (it, cnt) in enumerate(usable.items(), 1):
                emoji2, _, val, _, desc = ITEMS[it]
                print(f"  {YLW}[{i}]{R} {emoji2} {it} x{cnt} — {desc}")
            try:
                pick = int(inp("Use which? ")) - 1
                item_name = list(usable.keys())[pick]
                use_item(player, item_name, in_combat=True)
            except:
                print(f"  {RED}Invalid choice.{R}")
            pause()
            continue  # enemy still attacks

        elif choice == "4":
            roll = random.randint(1, 100)
            if roll <= flee_chance:
                print(f"\n  {YLW}You managed to flee! Phew!{R}")
                pause()
                return "fled"
            else:
                print(f"\n  {RED}Failed to flee! The enemy blocks your path!{R}")
                flee_chance += 15  # gets easier each failed attempt
        else:
            print(f"  {RED}Invalid! You hesitate...{R}")

        # Enemy attacks
        if e_hp > 0:
            enemy_dmg = max(0, e_atk - temp_def + random.randint(-3, 4))
            player.hp -= enemy_dmg
            print(f"  {RED}Enemy deals {enemy_dmg} damage to you!{R}")

            # special effects
            if enemy_key == "snake" and random.random() < 0.3:
                player.poisoned = True
                print(f"  {DMAG}☠  The snake venom enters your blood! You are POISONED!{R}")
            if enemy_key == "crocodile" and random.random() < 0.2:
                extra = random.randint(10, 20)
                player.hp -= extra
                print(f"  {RED}The crocodile death-rolls! Extra {extra} damage!{R}")

        player.hp = max(0, player.hp)
        pause()

    if e_hp <= 0:
        loot_chance = random.random()
        loot = None
        if loot_chance > 0.5 and LOCATION_LOOT.get(player.location):
            possible = [i for i in LOCATION_LOOT[player.location] if i in ITEMS]
            if possible:
                loot = random.choice(possible)
        print(f"\n  {GRN}{BLD}✓ You defeated the {enemy_key}!{R} +30 score")
        player.score += 30
        player.kills += 1
        if loot:
            player.add_item(loot)
            print(f"  {YLW}Loot dropped: {ITEMS[loot][0]} {loot}{R}")
        pause()
        return "won"
    else:
        print(f"\n  {RED}You were knocked out...{R}")
        pause()
        return "lost"

# ─── ITEM USE ──────────────────────────────────────────────────

def use_item(player, item_name, in_combat=False):
    if not player.has(item_name):
        print(f"  {RED}You don't have that.{R}")
        return False

    emoji, itype, val, wt, desc = ITEMS[item_name]

    if itype == "food":
        if item_name == "fish" and not in_combat:
            if player.has("fire_kit") or player.has_fire:
                print(f"  {YLW}You cook the fish first...{R}")
                player.remove_item("fish")
                player.add_item("cooked_fish")
                print(f"  {GRN}Raw fish cooked into cooked_fish!{R}")
                return True
        player.remove_item(item_name)
        player.hunger = min(100, player.hunger + val)
        print(f"  {GRN}You eat {emoji} {item_name}. Hunger +{val}.{R}")
        if item_name == "fish" and random.random() < 0.2:
            player.sick = True
            print(f"  {YLW}Uh oh... the raw fish made you sick!{R}")
        if item_name == "mushroom" and random.random() < 0.3:
            player.poisoned = True
            print(f"  {DMAG}The mushroom was toxic! You're poisoned!{R}")
        return True

    elif itype == "drink":
        player.remove_item(item_name)
        player.thirst = min(100, player.thirst + val)
        print(f"  {BLU}You drink {emoji} {item_name}. Thirst +{val}.{R}")
        return True

    elif itype == "medical":
        player.remove_item(item_name)
        if item_name == "bandage":
            player.hp = min(player.max_hp, player.hp + val)
            print(f"  {MAG}You bandage your wounds. HP +{val}.{R}")
        elif item_name == "antidote":
            player.poisoned = False
            player.sick = False
            print(f"  {GRN}Antidote taken! Poison and sickness cured!{R}")
        return True

    elif itype == "tool" and item_name == "fire_kit":
        player.has_fire = True
        print(f"  {RED}You set up a fire! You can now cook fish.{R}")
        return True

    elif itype == "special" and item_name == "signal_flare":
        if player.location == "volcano":
            player.escaped = True
            print(f"  {RED}{BLD}🚨 YOU FIRE THE FLARE FROM THE VOLCANO PEAK!{R}")
            print(f"  {YLW}A rescue helicopter spots you!!!{R}")
            return True
        else:
            print(f"  {YLW}You need to be at the Volcano to signal for rescue!{R}")
            return False
    else:
        print(f"  {DIM}You can't directly use {item_name} like that.{R}")
        return False

# ─── EXPLORE ───────────────────────────────────────────────────

def explore(player):
    loc = player.location
    if loc == "camp":
        print(f"\n  {DIM}Your camp is safe — nothing new to find here. Try exploring elsewhere.{R}")
        pause()
        return

    loot_pool = LOCATION_LOOT.get(loc, [])
    enemy_pool = LOCATION_ENEMIES.get(loc, [])
    danger = LOCATIONS[loc]["danger"]

    roll = random.random() * 10

    if roll < danger and enemy_pool:
        # Enemy encounter
        enemy_key = random.choice(enemy_pool)
        result = do_combat(player, enemy_key)
        if result == "lost":
            dmg = random.randint(15, 30)
            player.hp -= dmg
            print(f"  {RED}You crawl back injured. -{dmg} HP.{R}")
            pause()

    elif loot_pool and random.random() < 0.75:
        # Find loot
        found = random.choice(loot_pool)
        # special: raft wood is rare
        if found == "raft_wood" and random.random() < 0.6:
            found = random.choice([i for i in loot_pool if i != "raft_wood"] or loot_pool)
        player.add_item(found)
        emoji = ITEMS[found][0] if found in ITEMS else "?"
        player.score += 5
        print(f"\n  {GRN}You search the area and find: {emoji} {BLD}{found}{R}")
        if found == "map_piece":
            print(f"  {DYLW}🗺  Map piece collected! Total: {player.map_pieces}/3{R}")
        pause()
    else:
        print(f"\n  {DIM}You search thoroughly but find nothing useful this time.{R}")
        pause()

# ─── CRAFTING ──────────────────────────────────────────────────

def craft_menu(player):
    clear()
    print(f"\n{BLD}{CYN}🔨 CRAFTING BENCH{R}\n")
    print(f"  {'Recipe':<18} {'Ingredients':<40} {'Result'}")
    print("  " + "─" * 70)
    craftable = []
    for result, (mats, desc) in CRAFTING_RECIPES.items():
        can = all(player.has(m, c) for m, c in mats.items())
        mat_str = ", ".join(f"{c}x {m}" for m, c in mats.items())
        color = GRN if can else DIM
        marker = f"{GRN}✓{R}" if can else f"{DIM}✗{R}"
        print(f"  {marker} {color}{result:<18}{R} {mat_str:<40} {desc}")
        if can:
            craftable.append(result)
    print()
    if not craftable:
        print(f"  {RED}You don't have materials to craft anything yet.{R}")
        pause()
        return
    choice = inp("Craft what? (or 'back'): ")
    if choice in craftable:
        mats, _ = CRAFTING_RECIPES[choice]
        for m, c in mats.items():
            player.remove_item(m, c)
        player.add_item(choice)
        emoji = ITEMS[choice][0] if choice in ITEMS else "🔧"
        print(f"\n  {GRN}{BLD}✓ Crafted: {emoji} {choice}!{R}")
        player.score += 10
        pause()
    elif choice != "back":
        print(f"  {RED}Can't craft that.{R}")
        pause()

# ─── TRAVEL ────────────────────────────────────────────────────

def travel(player):
    connected = LOCATION_CONNECTIONS[player.location]
    clear()
    print(f"\n{BLD}{BLU}🧭 TRAVEL{R}  — Where do you want to go?\n")
    for i, loc_id in enumerate(connected, 1):
        loc = LOCATIONS[loc_id]
        danger = loc["danger"]
        d_str  = f"{RED}{'⚠ ' * min(danger // 2, 4)}{R}" if danger > 0 else f"{GRN}Safe{R}"
        print(f"  {YLW}[{i}]{R} {loc['color']}{loc['emoji']} {loc['name']:<22}{R} Danger: {d_str}")
    print(f"\n  {YLW}[0]{R} Stay here")
    choice = inp("Travel to: ")
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        dest = connected[idx]
        player.location = dest
        loc = LOCATIONS[dest]
        print(f"\n  {loc['color']}You travel to {loc['emoji']} {loc['name']}.{R}")
        # Random event on travel
        if random.random() < 0.35:
            trigger_random_event(player)
        pause()
    except:
        print(f"  {RED}Invalid choice.{R}")
        pause()

# ─── RANDOM EVENT ──────────────────────────────────────────────

def trigger_random_event(player):
    evt = random.choice(EVENTS)
    desc, etype, val = evt
    print(f"\n  {YLW}EVENT: {desc}{R}")
    if etype == "hp":
        player.hp = max(0, min(player.max_hp, player.hp + val))
        c = GRN if val > 0 else RED
        print(f"  {c}HP {'+' if val>0 else ''}{val}{R}")
    elif etype == "thirst":
        player.thirst = max(0, min(100, player.thirst + val))
        c = GRN if val > 0 else RED
        print(f"  {c}Thirst {'+' if val>0 else ''}{val}{R}")
    elif etype == "drink":
        player.thirst = min(100, player.thirst + val)
        print(f"  {BLU}Thirst +{val}{R}")
    elif etype == "item":
        player.add_item(val)
        emoji = ITEMS[val][0] if val in ITEMS else "?"
        print(f"  {GRN}Found: {emoji} {val}{R}")
    elif etype == "attack_bonus":
        player.attack += val
        print(f"  {YLW}Attack +{val} for now!{R}")

# ─── REST ──────────────────────────────────────────────────────

def rest(player):
    heal = random.randint(15, 25)
    player.hp = min(player.max_hp, player.hp + heal)
    print(f"\n  {GRN}You rest and recover. HP +{heal}.{R}")
    if player.has_fire or player.location == "camp":
        extra = 10
        player.hp = min(player.max_hp, player.hp + extra)
        print(f"  {RED}The fire keeps you warm. Extra +{extra} HP.{R}")
    pause()

# ─── WIN CHECK ─────────────────────────────────────────────────

def check_win_raft(player):
    return all(player.has(item, count) for item, count in WIN_RAFT.items())

# ─── GAME OVER SCREEN ──────────────────────────────────────────

def game_over(player, reason="You have perished."):
    clear()
    print(f"\n{BG_RED}{WHT}{BLD}  GAME OVER  {R}\n")
    slow(f"  {RED}{reason}{R}", 0.04)
    print(f"\n  {YLW}You survived {BLD}{player.day}{R}{YLW} days.{R}")
    print(f"  {YLW}Enemies defeated: {BLD}{player.kills}{R}")
    print(f"  {CYN}Final score: {BLD}{player.score}{R}")
    print()
    print(f"  {DIM}Last adventure log:{R}")
    for entry in player.log[-5:]:
        print(f"    {DIM}• {entry}{R}")
    print()

def win_screen(player, method):
    clear()
    print(f"\n{BG_GRN}{WHT}{BLD}  YOU ESCAPED! YOU WIN!  {R}\n")
    if method == "raft":
        slow(f"  {GRN}You launch your handbuilt raft and paddle to safety!{R}", 0.04)
    else:
        slow(f"  {YLW}The rescue helicopter lands at the volcano! You're saved!{R}", 0.04)
    print(f"\n  {YLW}Days survived: {BLD}{player.day}{R}")
    print(f"  {YLW}Enemies defeated: {BLD}{player.kills}{R}")
    bonus = player.day * 5 + player.kills * 20
    if player.has("treasure"):
        bonus += 200
        print(f"  {DYLW}+200 treasure bonus!{R}")
    if player.map_pieces == 3:
        bonus += 100
        print(f"  {DYLW}+100 full map bonus!{R}")
    player.score += bonus
    print(f"\n  {CYN}{BLD}FINAL SCORE: {player.score}{R}")
    if player.score > 500:
        print(f"  {YLW}{BLD}★ LEGENDARY SURVIVOR ★{R}")
    elif player.score > 300:
        print(f"  {YLW}★ Expert Survivor ★{R}")
    else:
        print(f"  {DIM}Survivor{R}")
    print()

# ─── MAIN MENU ─────────────────────────────────────────────────

def main_menu():
    clear()
    print(STORY_INTRO)
    print(f"  {DIM}You were the sole survivor of a plane crash.{R}")
    print(f"  {DIM}Stranded on a mysterious island, you must survive{R}")
    print(f"  {DIM}and find a way to escape before it's too late.{R}\n")
    print(f"  {YLW}[1]{R} New game")
    print(f"  {YLW}[2]{R} How to play")
    print(f"  {YLW}[3]{R} Quit\n")
    return inp("Choice: ")

def how_to_play():
    clear()
    print(f"\n{BLD}{YLW}  📖 HOW TO PLAY{R}\n")
    tips = [
        ("🎯 Goal",        "Build a raft (3 raft wood) OR use a signal flare at the volcano."),
        ("❤  Survive",     "Manage HP, hunger, and thirst. All 3 hitting 0 = death."),
        ("🗓  Days",        "Each day you get 3 actions. End day to rest and eat."),
        ("🔨 Craft",       "Combine materials to make weapons, tools, and medicine."),
        ("⚔  Combat",      "Fight enemies for loot. Flee if outnumbered!"),
        ("🗺  Explore",     "Search locations for materials. Higher danger = better loot."),
        ("💡 Tips",        "Build fire early. Cook fish. Avoid the swamp at first."),
        ("🏆 Win",         "Raft = collect 3 raft_wood + build at camp. Flare = reach volcano."),
        ("🗺  Secret",      "Collect all 3 map pieces for a massive score bonus."),
    ]
    for title, desc in tips:
        print(f"  {YLW}{title:<16}{R} {desc}")
    print()
    pause()

# ─── MAIN GAME LOOP ────────────────────────────────────────────

def game_loop():
    clear()
    print(f"\n{YLW}  Enter your survivor's name:{R}")
    name = inp("Name: ").title() or "Survivor"
    player = Player(name)

    # Give starting items
    player.add_item("stick", 2)
    player.add_item("stone", 1)
    player.add_item("cloth", 1)
    player.add_item("coconut")
    player.add_item("water")

    clear()
    slow(f"\n  {GRN}Welcome, {BLD}{player.name}{R}{GRN}.{R}", 0.04)
    slow(f"  {DIM}You wake up on a beach surrounded by plane wreckage.{R}", 0.04)
    slow(f"  {DIM}Your head throbs. You need to find food, shelter, and a way off this island.{R}", 0.04)
    pause()

    while player.is_alive() and not player.escaped:
        # Check raft win
        if check_win_raft(player) and player.location == "camp":
            clear()
            print(f"\n  {GRN}{BLD}You have 3 raft wood at your camp!{R}")
            choice = inp("Build your escape raft? (yes/no): ")
            if choice in ("yes", "y"):
                win_screen(player, "raft")
                break

        # Check flare win
        if player.escaped:
            win_screen(player, "flare")
            break

        # Main turn
        print_header(player)

        if player.actions <= 0:
            print(f"  {YLW}No actions left. End day to continue.{R}\n")
            print(f"  {YLW}[e]{R} End day (rest, eat, sleep)")
            choice = inp()
        else:
            print(f"  {YLW}[1]{R} Explore current area   {YLW}[2]{R} Travel to new area")
            print(f"  {YLW}[3]{R} Craft something        {YLW}[4]{R} Use an item")
            print(f"  {YLW}[5]{R} View inventory         {YLW}[6]{R} Rest (+HP)")
            print(f"  {YLW}[e]{R} End day               {YLW}[m]{R} View map")
            print(f"  {YLW}[l]{R} Adventure log         {YLW}[q]{R} Quit")
            choice = inp()

        if choice == "1" and player.actions > 0:
            explore(player)
            player.actions -= 1
            player.log_event(f"Explored {LOCATIONS[player.location]['name']}")

        elif choice == "2" and player.actions > 0:
            travel(player)
            player.actions -= 1

        elif choice == "3" and player.actions > 0:
            craft_menu(player)
            player.actions -= 1

        elif choice == "4":
            clear()
            print(f"\n{BLD}{MAG}  USE ITEM{R}\n")
            print_inventory(player)
            if player.inventory:
                item = inp("Use which item? ")
                if item in player.inventory:
                    used = use_item(player, item)
                    if used:
                        player.log_event(f"Used {item}")
                else:
                    print(f"  {RED}You don't have that.{R}")
                pause()

        elif choice == "5":
            clear()
            print(f"\n{BLD}{CYN}  INVENTORY{R}\n")
            print_inventory(player)
            print(f"\n  {DIM}Tip: Craft knife or spear to fight better. Build fire_kit to cook.{R}")
            pause()

        elif choice == "6" and player.actions > 0:
            rest(player)
            player.actions -= 1
            player.log_event("Rested")

        elif choice in ("e", "end"):
            player.tick_day()
            # warnings
            clear()
            print(f"\n  {DIM}━━━  Day {player.day - 1} ends. Day {player.day} begins.  ━━━{R}\n")
            if player.hunger < 25:
                print(f"  {RED}⚠  You are starving! Find food urgently!{R}")
            if player.thirst < 25:
                print(f"  {RED}⚠  You are severely dehydrated! Find water!{R}")
            if player.poisoned:
                print(f"  {DMAG}☠  Poison damages you in your sleep (-15 HP)!{R}")
            if player.sick:
                print(f"  {YLW}🤢 Sickness drains you (-10 HP)!{R}")
            # random daily event
            if random.random() < 0.5:
                trigger_random_event(player)
            player.log_event(f"Ended day. HP={player.hp}, Hunger={player.hunger}, Thirst={player.thirst}")
            pause()

        elif choice == "m":
            clear()
            print_map(player)
            pause()

        elif choice == "l":
            clear()
            print(f"\n{BLD}{CYN}  ADVENTURE LOG{R}\n")
            for entry in player.log[-15:]:
                print(f"  {DIM}• {entry}{R}")
            pause()

        elif choice in ("q", "quit"):
            print(f"\n  {YLW}Quitting... Your score: {player.score}{R}")
            break

        # Death checks
        if not player.is_alive():
            if player.hp <= 0:
                reason = "Your wounds were too severe. You breathed your last on this island."
            elif player.hunger <= 0:
                reason = "You starved to death. The island claimed another soul."
            else:
                reason = "Dehydration took you. You were so close..."
            game_over(player, reason)
            break

    # Post-game
    play_again = inp("\nPlay again? (yes/no): ")
    if play_again in ("yes", "y"):
        game_loop()

# ─── ENTRY POINT ───────────────────────────────────────────────

def main():
    while True:
        choice = main_menu()
        if choice == "1":
            game_loop()
        elif choice == "2":
            how_to_play()
        elif choice in ("3", "q", "quit"):
            clear()
            print(f"\n  {YLW}Thanks for playing {BLD}STRANDED{R}{YLW}! Stay alive out there. ✈️{R}\n")
            break

if __name__ == "__main__":
    main()
    