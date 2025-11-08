import re

from OpenApiUtils import ask_model
from utils import *
from config import *

SYSTEM_PROMPT = (
    "Jesteś narratorem RPG i twórcą postaci w świecie fantasy. "
    "Tworzysz szczegółowe, spójne i klimatyczne karty postaci (NPC). "
    "Każda karta zawiera pola: imię, nazwisko, rasa, wiek, wygląd, charakter, cechy, umiejętności, "
    "wrodzone talenty, wady, marzenia, tajemnice oraz relacje z innymi NPC. "
    "Relacje mają jeden z dozwolonych typów: "
    "[\"Przyjaźń\", \"Sojusz\", \"Rywalizacja\", \"Konflikt\", \"Wrogość\", \"Nienawiść\", "
    "\"Zemsta\", \"Współpraca\", \"Odmienne cele\", \"neutral\"]. "
    "Zawsze generuj wynik w poprawnym formacie JSON (zgodnym z RFC 8259). "
    "Używaj wyłącznie cudzysłowów (\") do oznaczania kluczy i wartości tekstowych. "
    "Nie dodawaj żadnego tekstu, komentarzy ani markdowna przed ani po JSON. "
    "Nie formatuj jako blok kodu (bez ```json```). "
    "Zwróć dokładnie jeden obiekt JSON o strukturze:\n"
    "{\n"
    "  \"npcs\": [\n"
    "    {\n"
    "      \"name\": \"\",\n"
    "      \"surname\": \"\",\n"
    "      \"race\": \"\",\n"
    "      \"age\": liczba,\n"
    "      \"appearance\": \"\",\n"
    "      \"character\": \"\",\n"
    "      \"skills\": [\"...\"],\n"
    "      \"talents\": [\"...\"],\n"
    "      \"flaws\": [\"...\"],\n"
    "      \"dreams\": [\"...\"],\n"
    "      \"secrets\": [\"...\"],\n"
    "      \"relations\": [\n"
    "        {\"npc_name\": \"\", \"relation_type\": \"jedna z dozwolonych wartości\"}\n"
    "      ]\n"
    "    }\n"
    "  ]\n"
    "}\n"
    "Zwróć wyłącznie czysty JSON — bez dodatkowego tekstu ani objaśnień. "
    "Jeśli nie możesz wygenerować poprawnego JSON, zwróć pusty obiekt: {}"
)
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
        safe_name = f"{npc['name']}_{npc['surname']}_{npc['race']}_{npc['age']}".replace(" ", "_")
        filename = os.path.join(npc_folder, f"{safe_name}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(npc, f, indent=4, ensure_ascii=False)
        saved_files.append(filename)
        for rel in npc.get("relations", []):
            relations.append({
                "from": f"{npc['name']} {npc['surname']}",
                "to": rel["npc_name"],
                "type": rel["relation_type"]
            })

    relations_file = os.path.join(npc_folder, "relations.json")
    with open(relations_file, "w", encoding="utf-8") as f:
        json.dump(relations, f, indent=4, ensure_ascii=False)

    print(f"💾 Zapisano {len(saved_files)} kart NPC oraz graf relacji w {relations_file}")
    return saved_files, relations_file


def main():
    world = load_world()
    if not world:
        return
    prompt = (
            "Na podstawie tego świata wygeneruj 10–15 unikalnych NPC w klimacie fantasy.\n\n"
            "Świat (dane w JSON): " + json.dumps(world) + "\n\n"
                                                          "Każdy NPC musi mieć:\n"
                                                          "- imię i nazwisko,\n"
                                                          "- rasę i wiek,\n"
                                                          "- wygląd i charakter,\n"
                                                          "- listy umiejętności, talentów, wad, marzeń i tajemnic,\n"
                                                          "- relacje z innymi NPC (minimum 2 relacje na postać).\n\n"
                                                          "Dozwolone typy relacji (i tylko te): "
                                                          "[\"Przyjaźń\", \"Sojusz\", \"Rywalizacja\", \"Konflikt\", \"Wrogość\", "
                                                          "\"Nienawiść\", \"Zemsta\", \"Współpraca\", \"Odmienne cele\", \"neutral\"].\n\n"
                                                          "Dobieraj relacje logicznie i spójnie z charakterem i fabułą postaci. "
                                                          "Zwróć wyłącznie poprawny JSON o strukturze:\n"
                                                          "{\n"
                                                          "  \"npcs\": [ { ... } ]\n"
                                                          "}\n"
                                                          "Nie dodawaj żadnego tekstu, objaśnień ani komentarzy poza JSON."
    )

    print("Generuję karty NPC...")
    raw = ask_model(system_prompt=SYSTEM_PROMPT, prompt=prompt, temperature=BASIC_NPC_TEMPERATURE, max_tokens=BASIC_NPC_TOKENS, label="npc-generator")
    parsed = extract_json(raw)
    if not parsed or "npcs" not in parsed:
        print("Błąd parsowania JSON. Surowa odpowiedź:\n", raw)
        return
    save_individual_npcs(parsed["npcs"])
    print("Podgląd pierwszego NPC:", parsed["npcs"][0]["name"])

if __name__ == "__main__":
    main()
