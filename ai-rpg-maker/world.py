import re
import uuid

import OpenApiUtils
from utils import *
from config import *

SYSTEM_PROMPT = (
    "Jesteś narratorem fantasy i twórcą świata RPG. "
    "Twórz spójne, rozbudowane opisy miast, okolic, budynków i polityki/gildii. "
    "Dodawaj historie, legendy, zależności i konflikty. "
    "Zawsze generuj wynik w poprawnym formacie JSON (RFC 8259). "
    "Używaj tylko cudzysłowów (\") do oznaczania kluczy i wartości tekstowych. "
    "Nie dodawaj żadnego tekstu przed ani po JSON. "
    "Nie dodawaj komentarzy, markdowna, kodu ani objaśnień — tylko czysty JSON."
)

prompt = (
    "Wygeneruj rozbudowany świat fantasy jako **czysty JSON**.\n"
    "Zawartość:\n"
    "- city: pełny opis miasta (historia, architektura, mieszkańcy)\n"
    "- surroundings: lista min. 5 lokacji, każda z legendą, historią lub ciekawostką\n"
    "- buildings: lista min. 5 charakterystycznych budynków, z ich znaczeniem, mieszkańcami i historią\n"
    "- politics: lista min. 5 gildii lub frakcji, z opisem ich roli, konfliktów i zależności między nimi\n"
    "- ciekawostki i zależności między lokacjami, budynkami i gildiiami\n\n"
    "Format JSON (dokładnie taki, bez apostrofów):\n"
    "{\n"
    "  \"city\": \"\",\n"
    "  \"surroundings\": [ ... ],\n"
    "  \"buildings\": [ ... ],\n"
    "  \"politics\": [ ... ]\n"
    "}\n\n"
    "Zwróć **wyłącznie** poprawny JSON — bez dodatkowych opisów ani tekstu."
)
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
    print(f"Świat zapisany w pliku: {filename}")
    return filename

def main():
    print("Generuję rozbudowany świat fantasy...")
    raw = OpenApiUtils.ask_model(SYSTEM_PROMPT, prompt, temperature=WORLD_TEMPERATURE, max_tokens=WORLD_TOKENS, label="world-generator")
    parsed = extract_json(raw)
    if not parsed:
        print("Błąd parsowania JSON. Surowa odpowiedź:\n", raw)
        return

    save_world(parsed)
    print("Podgląd miasta:", parsed.get("city"))
    print("Liczba lokacji:", len(parsed.get("surroundings",[])))
    print("Liczba budynków:", len(parsed.get("buildings",[])))
    print("Liczba gildii:", len(parsed.get("politics",[])))

if __name__ == "__main__":
    main()
