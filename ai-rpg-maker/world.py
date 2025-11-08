import re
import uuid

import OpenApiUtils
from utils import *
from config import *

SYSTEM_PROMPT = (
    "Jesteś narratorem fantasy i twórcą świata RPG. Twórz spójne, rozbudowane opisy miasta, okolic, budynków i polityki/gildii. "
    "Dodawaj historie, legendy, zależności i konflikty. Twórz JSON w formacie podanym w prompt, "
    "z dużą ilością szczegółów i ciekawymi nazwami."
)

prompt = (
    "Wygeneruj rozbudowany świat fantasy w JSON.\n"
    "Miasto: pełny opis, historia, architektura, mieszkańcy.\n"
    "Otoczenie: min. 5 lokacji, każda z legendą, historią lub ciekawym faktem.\n"
    "Budynki: min. 5 charakterystycznych budynków, ich znaczenie, mieszkańcy, historia.\n"
    "Polityka/gildie: min. 5 gildii, ich role, konflikty, zależności między nimi.\n"
    "Dodaj kilka ciekawostek i zależności między lokacjami, budynkami i gildiiami.\n"
    "Zwróć wyłącznie JSON w formacie:\n"
    "{'city':'','surroundings':[...],'buildings':[...],'politics':[...]}."
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
