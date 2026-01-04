import json
from pathlib import Path

from config import *

def load_world():
    world_files = [f for f in os.listdir(f"{ROOT_DIRECTORY}/world") if f.endswith(".json")]
    if not world_files:
        print("Directory /world is empty!")
        return
    latest_world_file = os.path.join(f"{ROOT_DIRECTORY}/world", sorted(world_files)[-1])
    with open(latest_world_file, "r", encoding="utf-8") as f:
        world_json = json.load(f)
    return world_json

def load_npcs():
    npc_files = [f for f in os.listdir(f"{ROOT_DIRECTORY}/npcs") if f.endswith(".json") and f != "relations.json"]
    npc_list = []
    for nf in npc_files:
        with open(os.path.join(f"{ROOT_DIRECTORY}/npcs", nf), "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                npc_list.append(data)
    return npc_list

def load_hero():
    player_files = [f for f in os.listdir(f"{ROOT_DIRECTORY}/player") if f.endswith(".json")]
    if not player_files:
        print("Directory /player is empty!")
        return
    latest_player_file = os.path.join(f"{ROOT_DIRECTORY}/player", sorted(player_files)[-1])
    with open(latest_player_file, "r", encoding="utf-8") as f:
        player_json = json.load(f)
    return player_json

def load_missions():
    mission_list = []
    for mf in os.listdir(f"{ROOT_DIRECTORY}/missions"):
        if mf.endswith(".json"):
            with open(os.path.join(f"{ROOT_DIRECTORY}/missions", mf), "r", encoding="utf-8") as f:
                data = json.load(f)
                mission_list.append(data)
    return mission_list

def save_raw(data, dir, name):
    base_dir = Path(ROOT_DIRECTORY) / dir
    base_dir.mkdir(parents=True, exist_ok=True)

    filename = base_dir / name

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Saving {name} output inside: {filename}")
    return filename