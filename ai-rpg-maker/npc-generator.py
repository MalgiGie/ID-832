import re

from OpenApiUtils import ask_model
from utils import *
from config import *

SYSTEM_PROMPT = (
    "Jesteś narratorem RPG i twórcą postaci. Twórz szczegółowe karty NPC w świecie fantasy. "
    "Każda karta zawiera: imię, nazwisko, rasę, wiek, wygląd, charakter, cechy, umiejętności, wady, marzenia, tajemnice. "
    "Twórz też relacje między NPC: przyjaźnie, rywalizacje, sojusze, konflikty. "
    "Opisuj postacie szczegółowo, spójnie, w klimacie fantasy. "
    "Zwracaj wyłącznie JSON: {'npcs':[...]}."
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
            "Na podstawie tego świata generuj 10-15 unikalnych NPC. "
            "Świat: " + json.dumps(world) +
            "Twórz szczegółowe karty postaci z imieniem, nazwiskiem, rasą, wiekiem, wyglądem, charakterem, umiejętnościami, "
            "wrodzonymi talentami, wadami, marzeniami, tajemnicami. "
            "Każdy NPC powinien mieć także relacje z innymi NPC. "
            "Dozwolone typy relacji są tylko z poniższego zbioru i żadne inne: "
            "['Przyjaźń', 'Sojusz', 'Rywalizacja', 'Konflikt', 'Wrogość', 'Nienawiść', 'Zemsta', 'Współpraca', 'Odmienne cele', 'neutral']. "
            "Dobieraj je w sposób spójny z charakterem i fabułą postaci. "
            "Zwróć JSON w formie {'npcs':[{'name':'','surname':'','race':'','age':,'appearance':'','character':'',"
            "'skills':[],'talents':[],'flaws':[],'dreams':[],'secrets':[],"
            "'relations':[{'npc_name':'','relation_type':''}]}]}"
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
