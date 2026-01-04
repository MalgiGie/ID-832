import random
import re

import OpenApiUtils
from utils import *
from config import *
from prompts import get_prompt


def clean_filename(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "_")


def generate_player_card(world_json, npc_list):
    system_prompt, user_prompt = get_prompt("hero", lang=LANGUAGE)

    char_class = random.choice(CLASSES)
    k = min(3, len(npc_list))
    npc_sample = random.sample(npc_list, k=k) if npc_list else []
    npc_names = [f"{npc['name']} {npc['surname']}" for npc in npc_sample]

    prompt = (
        f"{user_prompt}\n\n"
        f"Game world:\n{json.dumps(world_json, ensure_ascii=False)}\n\n"
        f"Selected NPCs:\n{json.dumps(npc_names, ensure_ascii=False)}\n\n"
        f"Class: {char_class}\n\n"
        f"Return only valid JSON, no text or markdown."
    )

    raw = OpenApiUtils.ask_model(
        system_prompt=system_prompt,
        prompt=prompt,
        temperature=HERO_TEMPERATURE,
        max_tokens=HERO_TOKENS,
        label=f"hero-generation-{LANGUAGE.lower()}"
    )

    save_raw(raw, "raw", "hero_raw.txt")

    try:
        player_card = json.loads(raw)
    except json.JSONDecodeError as e:
        print("Error while JSON parsing:", e)
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                player_card = json.loads(match.group(0))
                print("Retrieved JSON file successfully")
            except Exception:
                print("Failed to retrieve JSON file")
                return None
        else:
            print("JSON not found in raw file")
            return None

    return player_card


def save_player_card(player_card):
    char_name = clean_filename(player_card.get("name", "Unknown"))
    char_surname = clean_filename(player_card.get("surname", "Unknown"))
    char_class = clean_filename(player_card.get("class", "Unknown"))
    player_folder = os.path.join(ROOT_DIRECTORY, "player")
    os.makedirs(player_folder, exist_ok=True)

    filename = os.path.join(player_folder, f"{char_name}_{char_surname}_{char_class}.json")
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(player_card, f, indent=4, ensure_ascii=False)
    print(f"Saved hero: {filename}")
    return filename


def main():
    world_json = load_world()
    npc_list = load_npcs()

    print("Generating hero...")

    player_card = generate_player_card(world_json, npc_list)
    if player_card:
        save_player_card(player_card)
        print(json.dumps(player_card, indent=4, ensure_ascii=False))
    else:
        print("Generating hero failed, see raw response to get more information")


if __name__ == "__main__":
    main()
