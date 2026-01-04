import re

import OpenApiUtils
from utils import *
from config import *
from prompts import get_prompt


def clean_filename(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "_")

def normalize_missions(obj):
    if obj is None:
        return []

    if isinstance(obj, dict):
        if "missions" in obj and isinstance(obj["missions"], list):
            return obj["missions"]

        if "id" in obj and "title" in obj:
            return [obj]

    if isinstance(obj, list):
        return obj

    print("Unknown file format: ", type(obj))
    return []


def safe_load_json(raw_text: str):
    if not raw_text:
        return None

    text = raw_text.strip()
    text = re.sub(r"```json|```", "", text, flags=re.IGNORECASE).strip()
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        first = text.find("{")
        last = text.rfind("}")
        if first == -1 or last == -1:
            print("❌ No JSON object found")
            return None
        try:
            obj = json.loads(text[first:last + 1])
        except json.JSONDecodeError as e:
            print("❌ JSON parsing error after cleanup:", e)
            print(text[:1000])
            return None

    if isinstance(obj, str):
        obj = obj.strip()
        if obj.startswith("{") or obj.startswith("["):
            try:
                obj = json.loads(obj)
            except json.JSONDecodeError as e:
                print("❌ Nested JSON string could not be parsed:", e)
                print(obj[:1000])
                return None

    return obj


def expand_mission(world_json, npc_list, player_json, mission):
    system_prompt, user_prompt = get_prompt("mission_epic", lang=LANGUAGE)

    npc_names = [f"{npc['name']} {npc['surname']}" for npc in npc_list]

    prompt = (
        f"{user_prompt}\n\n"
        f"Game world:\n{json.dumps(world_json, ensure_ascii=False)}\n\n"
        f"NPCs:\n{json.dumps(npc_names, ensure_ascii=False)}\n\n"
        f"Player character:\n{json.dumps(player_json, ensure_ascii=False)}\n\n"
        f"Mission to expand:\n{json.dumps(mission, ensure_ascii=False)}"
    )

    print("Sending request to OpenAI...")
    raw = OpenApiUtils.ask_model(
        system_prompt=system_prompt,
        prompt=prompt,
        temperature=EPIC_TEMPERATURE,
        max_tokens=EPIC_NPC_TOKENS,
        label=f"mission-expander-{LANGUAGE.lower()}"
    )

    save_raw(raw, "raw", f"mission_epic_{mission.get('id', 'X')}")

    missions_raw = safe_load_json(raw)
    missions = normalize_missions(missions_raw)

    if not missions:
        print("Error while normalizing missions:")
        print(raw[:1000])
        return None

    return missions

def save_mission(mission, folder=None):
    if folder is None:
        folder = os.path.join(ROOT_DIRECTORY, "missions_epic")
    os.makedirs(folder, exist_ok=True)

    mid = mission.get("id", "X")
    title = clean_filename(mission.get("title", "untitled"))
    filename = os.path.join(folder, f"mission_{mid}_{title}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(mission, f, indent=4, ensure_ascii=False)

    print(f"Saved {filename}")


def main():
    print(f"Generating extended campaign...")

    world_json = load_world()
    npc_list = load_npcs()
    player_json = load_hero()
    mission_list = load_missions()

    mission_list.sort(key=lambda x: x.get("id", 0))
    all_expanded_missions = []

    for mission in mission_list:
        print(f"Extending mission: {mission.get('title', mission.get('id'))}")
        expanded = expand_mission(world_json, npc_list, player_json, mission)
        if expanded:
            for m in expanded:
                save_mission(m)
                all_expanded_missions.append(m)

    if all_expanded_missions:
        print("All of the missions are extended successfully")


if __name__ == "__main__":
    main()
