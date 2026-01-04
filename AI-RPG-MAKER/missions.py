import re

import OpenApiUtils
from utils import *
from config import *
from prompts import get_prompt


def parse_ai_json(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw, flags=re.IGNORECASE).strip()
    raw = re.sub(r"```$", "", raw).strip()
    try:
        data = json.loads(raw)
        return data.get("missions", [])
    except json.JSONDecodeError as e:
        print("Error while parsing JSON", e)
        return []


def clean_filename(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "_")


def generate_missions(world_json, npc_list, player_json):
    system_prompt, user_prompt = get_prompt("missions", lang=LANGUAGE)
    npc_names = [f"{npc['name']} {npc['surname']}" for npc in npc_list]
    prompt = (
        f"{user_prompt}\n\n"
        f"Game world:\n{json.dumps(world_json, ensure_ascii=False)}\n\n"
        f"NPCs:\n{json.dumps(npc_names, ensure_ascii=False)}\n\n"
        f"Hero:\n{json.dumps(player_json, ensure_ascii=False)}"
    )

    print(f"Generating storyline...")

    raw = OpenApiUtils.ask_model(
        system_prompt=system_prompt,
        prompt=prompt,
        temperature=QUESTS_TEMPERATURE,
        max_tokens=QUESTS_TOKENS,
        label=f"quests-generator-{LANGUAGE.lower()}"
    )
    save_raw(raw, "raw", "missions_raw.txt")
    return parse_ai_json(raw)


def save_missions(missions):
    os.makedirs(f"{ROOT_DIRECTORY}/missions", exist_ok=True)
    for mission in missions:
        mid = mission.get("id", "X")
        title = clean_filename(mission.get("title", f"mission_{mid}"))
        filename = f"{ROOT_DIRECTORY}/missions/mission_{mid}_{title}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(mission, f, indent=4, ensure_ascii=False)
        print(f"Saved {filename}")


def main():
    world_json = load_world()
    npc_list = load_npcs()
    player_json = load_hero()
    missions = generate_missions(world_json, npc_list, player_json)
    save_missions(missions)
    if missions:
        save_missions(missions)
        print(json.dumps(missions, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
