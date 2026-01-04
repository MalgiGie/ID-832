import re

from OpenApiUtils import ask_model
from utils import *
from config import *
from prompts import get_prompt

def extract_json(text):
    try:
        return json.loads(text)
    except:
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except:
                return None
        return None


def save_individual_npcs(npcs):
    saved_files = []
    relations = []
    npc_folder = os.path.join(ROOT_DIRECTORY, "npcs")
    os.makedirs(npc_folder, exist_ok=True)

    for npc in npcs:
        name = npc.get("name") or npc.get("imię") or "UNKNOWN"
        surname = npc.get("surname") or npc.get("nazwisko") or "UNKNOWN"
        race = npc.get("race") or npc.get("rasa") or "UNKNOWN"
        age = npc.get("age") or npc.get("wiek") or "0"

        safe_name = f"{name}_{surname}_{race}_{age}".replace(" ", "_")
        filename = os.path.join(npc_folder, f"{safe_name}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(npc, f, indent=4, ensure_ascii=False)
        saved_files.append(filename)
        for rel in npc.get("relations", []):
            relations.append({
                "from": f"{name} {surname}",
                "to": rel["npc_name"],
                "type": rel["relation_type"]
            })

    relations_file = os.path.join(npc_folder, "relations.json")
    with open(relations_file, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=4, ensure_ascii=False)

    print(f"Saved {len(saved_files)} NPC and relations graph: {relations_file}")
    return saved_files, relations_file


def main():
    world = load_world()
    if not world:
        return

    system_prompt, user_prompt = get_prompt("npc", lang=LANGUAGE)

    user_prompt = user_prompt + "\n\nWorld (JSON format):\n" + json.dumps(world, ensure_ascii=False)

    print(f"Generating NPCs...")

    raw = ask_model(
        system_prompt=system_prompt,
        prompt=user_prompt,
        temperature=BASIC_NPC_TEMPERATURE,
        max_tokens=BASIC_NPC_TOKENS,
        label=f"npc-generator-{LANGUAGE.lower()}"
    )

    save_raw(raw, "raw", "npc_raw.txt")

    parsed = extract_json(raw)

    if not parsed or "npcs" not in parsed:
        print("NPC response parsed without key data :\n", raw)
        return

    save_individual_npcs(parsed["npcs"])


if __name__ == "__main__":
    main()
