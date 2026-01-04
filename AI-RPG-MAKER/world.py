import re
import uuid

import OpenApiUtils
from utils import *
from config import *
from prompts import get_prompt

def extract_json(text):
    try:
        return json.loads(text)
    except Exception:
        m = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if m:
            try:
                return json.loads(m.group(0))
            except:
                return None
        return None


def save_world(data):
    os.makedirs(f"{ROOT_DIRECTORY}/world", exist_ok=True)
    world_id = str(uuid.uuid4())
    filename = f"{ROOT_DIRECTORY}/world/world_{world_id}.json"
    with open(filename,"w",encoding="utf-8") as f:
        json.dump(data,f,indent=4,ensure_ascii=False)
    print(f"Saving world inside: {filename}")
    return filename

def main():
    lang = LANGUAGE if 'LANGUAGE' in globals() else "EN"
    system_prompt, prompt = get_prompt("world", lang)
    raw = OpenApiUtils.ask_model(system_prompt, prompt, temperature=WORLD_TEMPERATURE, max_tokens=WORLD_TOKENS, label="world-generator")
    save_raw(raw, "raw", "world_raw.txt")
    parsed = extract_json(raw)
    if not parsed:
        print("JSON error parsing. Result: :\n", raw)
        return

    save_world(parsed)
    print("City stats: \n")
    print("Preview of the city:", parsed.get("city"))
    print("Locations:", len(parsed.get("surroundings",[])))
    print("Buildings:", len(parsed.get("buildings",[])))
    print("Guilds:", len(parsed.get("politics",[])))

if __name__ == "__main__":
    main()
