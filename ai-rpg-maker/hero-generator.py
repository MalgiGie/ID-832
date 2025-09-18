import random
import re

import OpenApiUtils
from utils import *
from config import *

SYSTEM_PROMPT = (
    "Jesteś narratorem RPG. Twoim zadaniem jest stworzenie bardzo szczegółowej karty postaci gracza "
    "w świecie fantasy. Historia postaci ma mieć kilkadziesiąt zdań, być powiązana ze światem i wybranymi NPC, "
    "fabularnie spójna, z relacjami do 2–3 NPC. Uwzględnij wygląd, znaki szczególne, klasę postaci, "
    "ekwipunek z opisami, 10 głównych cech (0-10, rozkład wg klasy), 5 cech miękkich, ambicje, wady, marzenia i tajemnice. "
    "Zwróć wyłącznie poprawny JSON, zgodny z podaną strukturą i kompletny."
)

def clean_filename(text: str) -> str:
    """Usuwa niedozwolone znaki i spacje z nazw plików."""
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    return text.strip().replace(" ", "_")

def generate_player_card(world_json, npc_list):
    char_class = random.choice(CLASSES)
    k = min(3, len(npc_list))
    npc_sample = random.sample(npc_list, k=k) if npc_list else []
    npc_names = [f"{npc['name']} {npc['surname']}" for npc in npc_sample]

    prompt = (
        f"Świat gry:\n{json.dumps(world_json, ensure_ascii=False)}\n\n"
        f"Wybrane NPC:\n{json.dumps(npc_names, ensure_ascii=False)}\n\n"
        f"Stwórz główną postać gracza w formacie JSON zgodnym z poniższą strukturą. "
        f"Zachowaj wszystkie pola, uzupełnij je szczegółowo i spójnie fabularnie:\n\n"
        f"{{\n"
        f'  "name": "Imię",\n'
        f'  "surname": "Nazwisko",\n'
        f'  "age": 25,\n'
        f'  "race": "Rasa",\n'
        f'  "appearance": {{\n'
        f'    "description": "Szczegółowy opis wyglądu postaci",\n'
        f'    "distinctive_signs": "Znaki szczególne"\n'
        f"  }},\n"
        f'  "class": "{char_class}",\n'
        f'  "history": "Długa historia postaci, kilkadziesiąt zdań, powiązana ze światem i wybranymi NPC",\n'
        f'  "equipment": [\n'
        f'    {{"name": "Nazwa przedmiotu", "description": "Opis przedmiotu"}},\n'
        f'    {{"name": "Nazwa przedmiotu", "description": "Opis przedmiotu"}}\n'
        f"  ],\n"
        f'  "main_attributes": {{\n'
        f'    "strength": 0,\n'
        f'    "agility": 0,\n'
        f'    "constitution": 0,\n'
        f'    "intelligence": 0,\n'
        f'    "wisdom": 0,\n'
        f'    "charisma": 0,\n'
        f'    "dexterity": 0,\n'
        f'    "endurance": 0,\n'
        f'    "perception": 0,\n'
        f'    "luck": 0\n'
        f"  }},\n"
        f'  "soft_skills": [\n'
        f'    "cecha miękka 1",\n'
        f'    "cecha miękka 2",\n'
        f'    "cecha miękka 3",\n'
        f'    "cecha miękka 4",\n'
        f'    "cecha miękka 5"\n'
        f"  ],\n"
        f'  "relationships": {{\n'
        f'    "NPC 1": "Opis relacji",\n'
        f'    "NPC 2": "Opis relacji"\n'
        f"  }},\n"
        f'  "ambitions": "Ambicje postaci",\n'
        f'  "flaws": "Wady postaci",\n'
        f'  "dreams": "Marzenia postaci",\n'
        f'  "secrets": "Sekrety postaci"\n'
        f"}}\n"
        f"Nie dodawaj żadnych dodatkowych obiektów ani komentarzy. "
        f"Zwróć wyłącznie poprawny JSON."
    )

    raw = OpenApiUtils.ask_model(system_prompt=SYSTEM_PROMPT, prompt=prompt, temperature=HERO_TEMPERATURE, max_tokens=HERO_TOKENS, label="hero-generation")

    try:
        player_card = json.loads(raw)
    except json.JSONDecodeError:
        print("❌ Błąd parsowania JSON, sprawdź surową odpowiedź AI:")
        print(raw)
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
    print(f"Zapisano kartę gracza: {filename}")
    return filename

def main():
    # Wczytaj świat
    world_json = load_world()
    # Wczytaj NPC
    npc_list = load_npcs()
    # Generuj i zapisz postać
    player_card = generate_player_card(world_json, npc_list)
    if player_card:
        save_player_card(player_card)
        print(json.dumps(player_card, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()
