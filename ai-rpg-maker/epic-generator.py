import re
import OpenApiUtils
from utils import *
from config import *

SYSTEM_PROMPT = (
    "Jesteś mistrzem gry RPG i pisarzem fantasy. Twoim zadaniem jest rozbudować każdą misję "
    "w stylu powieściowym, epickim. Opis fabularny min. kilka akapitów, linie dialogu NPC i "
    "opcje gracza min. 5 zdań każda, pełne emocji i odniesień do historii bohatera i relacji z NPC. "
    "Cele i nagrody pozostają, ale możesz je epicko ubarwić. Zwróć wyłącznie poprawny JSON "
    "w formacie {\"missions\": [ ... ]}."
)

def clean_filename(text: str) -> str:
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "_")

def safe_load_json(raw_text):
    raw_text = raw_text.strip()
    raw_text = re.sub(r"[\x00-\x1f]", "", raw_text)
    raw_text = re.sub(r"```json|```", "", raw_text)
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as e:
        print("❌ Błąd parsowania JSON:", e)
        print("Oto surowa odpowiedź AI (pierwsze 1000 znaków):")
        print(raw_text[:1000])
        return None

def expand_mission(world_json, npc_list, player_json, mission):
    npc_names = [f"{npc['name']} {npc['surname']}" for npc in npc_list]
    prompt = (
        f"Świat gry:\n{json.dumps(world_json, ensure_ascii=False)}\n\n"
        f"NPC:\n{json.dumps(npc_names, ensure_ascii=False)}\n\n"
        f"Bohater:\n{json.dumps(player_json, ensure_ascii=False)}\n\n"
        f"Rozwiń poniższą misję w EPICKĄ, powieściową wersję. "
        f"Każda linia dialogu min. 5 zdań. Zachowaj cele i nagrody, "
        f"rozbuduj opis fabularny i dialogi:\n"
        f"{json.dumps(mission, ensure_ascii=False)}\n\n"
        "Zwróć wyłącznie poprawny JSON w formacie {\"missions\": [ ... ]}."
    )

    raw = OpenApiUtils.ask_model(system_prompt=SYSTEM_PROMPT, prompt=prompt, temperature=EPIC_TEMPERATURE, max_tokens=EPIC_NPC_TOKENS, label="epic-generator")
    missions_expanded = safe_load_json(raw)
    if missions_expanded is None:
        return None
    return missions_expanded.get("missions", [])


def save_mission(mission, folder=None):
    if folder is None:
        folder = os.path.join(ROOT_DIRECTORY, "missions_epic")

    os.makedirs(folder, exist_ok=True)

    mid = mission.get("id", "X")
    title = clean_filename(mission.get("title", "untitled"))
    filename = os.path.join(folder, f"mission_{mid}_{title}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(mission, f, indent=4, ensure_ascii=False)

    print(f"💾 Zapisano {filename}")

def main():
    # Wczytaj świat
    world_json =load_world()
    # Wczytaj NPC
    npc_list = load_npcs()
    # Wczytaj bohatera
    player_json = load_hero()
    # Wczytaj misje
    mission_list = load_missions()
    # Sortowanie po ID misji
    mission_list.sort(key=lambda x: x.get("id", 0))

    all_expanded_missions = []

    for mission in mission_list:
        print(f"🔹 Rozwijam misję: {mission.get('title', mission.get('id'))}")
        expanded = expand_mission(world_json, npc_list, player_json, mission)
        if expanded:
            for m in expanded:
                save_mission(m)
                all_expanded_missions.append(m)

    if all_expanded_missions:
        print("✅ Wszystkie misje zostały rozbudowane i zapisane.")
        print(json.dumps({"missions": all_expanded_missions}, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
