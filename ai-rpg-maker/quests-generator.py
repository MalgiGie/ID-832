import re

import OpenApiUtils
from utils import *
from config import *


SYSTEM_PROMPT = (
    "Jesteś mistrzem gry RPG i tworzysz główną linię fabularną w świecie fantasy. "
    "Wygeneruj minimum 10 spójnych misji w formacie JSON, ponumerowanych od 1 wzwyż. "
    "Każda misja musi być obszerna, rozbudowana i zanurzona w świecie (świat, NPC, bohater). "
    "Każda misja zawiera: id, tytuł, quest_giver (NPC), description (długi opis), "
    "objectives (lista), dialogue (npc_lines + choices z player_choice i npc_response), "
    "connections (previous, next), rewards (lista). "
    "Fabuła musi łączyć się między misjami, tworząc spójną historię. "
    "Dialogi muszą nawiązywać do cech bohatera i relacji z NPC. "
    "Zwróć wyłącznie poprawny JSON: tablica misji w obiekcie {\"missions\": [...]}."
)

def parse_ai_json(raw: str):
    raw = raw.strip()
    raw = re.sub(r"^```json", "", raw, flags=re.IGNORECASE).strip()
    raw = re.sub(r"```$", "", raw).strip()
    try:
        data = json.loads(raw)
        return data.get("missions", [])
    except json.JSONDecodeError as e:
        print("Błąd parsowania JSON:", e)
        print("Surowa odpowiedź AI:")
        print(raw)
        return []

def clean_filename(text: str) -> str:
    """Usuwa niedozwolone znaki i spacje z nazw plików."""
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "_")

def generate_missions(world_json, npc_list, player_json):
    npc_names = [f"{npc['name']} {npc['surname']}" for npc in npc_list]
    prompt = (
        f"Świat gry:\n{json.dumps(world_json, ensure_ascii=False)}\n\n"
        f"NPC:\n{json.dumps(npc_names, ensure_ascii=False)}\n\n"
        f"Bohater:\n{json.dumps(player_json, ensure_ascii=False)}\n\n"
        "Stwórz zestaw minimum 10 misji głównej linii fabularnej w formacie JSON, "
        "zgodnym z przykładem poniżej. Każda misja powinna być **bardzo rozbudowana** i fabularnie bogata, "
        "z długim opisem sytuacji, tłem świata, emocjami bohatera, jego przemyśleniami i decyzjami, "
        "oraz spójnym powiązaniem z poprzednimi i kolejnymi misjami. "
        "Dialogi muszą być szczegółowe, wielowątkowe, odzwierciedlać charakter bohatera, jego relacje z NPC, "
        "emocje i możliwe konflikty. Cele misji powinny być rozbudowane i zróżnicowane, "
        "a nagrody fabularnie uzasadnione. W każdym zadaniu uwzględnij elementy historii bohatera, "
        "jego umiejętności i ekwipunku. Fabuła ma prowadzić przez główną linię historii, "
        "tworząc spójną, epicką opowieść.\n\n"
        "Przykładowa struktura jednej misji:\n"
        "{\n"
        "  \"id\": 1,\n"
        "  \"title\": \"Tytuł misji\",\n"
        "  \"quest_giver\": \"Imię i nazwisko NPC\",\n"
        "  \"description\": \"Długi, fabularny opis misji, minimum kilka akapitów, z emocjami, opisem świata, "
        "przemyśleniami bohatera i napięciem...\",\n"
        "  \"objectives\": [\"Cel 1 opisany szczegółowo\", \"Cel 2 opisany szczegółowo\"],\n"
        "  \"dialogue\": {\n"
        "    \"npc_lines\": [\"Kilka linii dialogowych NPC, opis emocji i tonu głosu\"],\n"
        "    \"choices\": [\n"
        "      {\"player_choice\": \"Opcja bohatera z uwzględnieniem jego charakteru\", "
        "\"npc_response\": \"Szczegółowa reakcja NPC z emocjami i konsekwencjami\"}\n"
        "    ]\n"
        "  },\n"
        "  \"connections\": {\"previous\": null, \"next\": 2},\n"
        "  \"rewards\": [\"Nagroda fabularna lub przedmiot opisany w kontekście świata\"]\n"
        "}\n\n"
        "Bardzo ważne: generuj wyłącznie poprawny JSON, w formie obiektu "
        "{\"missions\": [ {...}, {...}, ... ]}. Nie dodawaj żadnego tekstu przed lub po JSON."
    )

    raw = OpenApiUtils.ask_model(SYSTEM_PROMPT, prompt, temperature=QUESTS_TEMPERATURE, max_tokens=QUESTS_TOKENS, label="quests-generator")
    missions = parse_ai_json(raw)
    return missions

def save_missions(missions):
    os.makedirs(f"{ROOT_DIRECTORY}/missions", exist_ok=True)
    for mission in missions:
        mid = mission.get("id", "X")
        title = clean_filename(mission.get("title", f"mission_{mid}"))
        filename = f"{ROOT_DIRECTORY}/missions/mission_{mid}_{title}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(mission, f, indent=4, ensure_ascii=False)
        print(f"💾 Zapisano {filename}")

def main():
    # Wczytaj świat
    world_json = load_world()
    # Wczytaj NPC
    npc_list = load_npcs()
    # Wczytaj bohatera
    player_json = load_hero()
    # Generuj misje
    missions = generate_missions(world_json, npc_list, player_json)
    if missions:
        save_missions(missions)
        print(json.dumps(missions, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()