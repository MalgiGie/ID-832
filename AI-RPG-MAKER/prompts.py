# ===============================
# PROMPTS — WORLD GENERATOR
# ===============================

SYSTEM_PROMPTS_WORLD = {
    "PL": (
        "Jesteś narratorem fantasy i twórcą świata RPG. "
        "Twórz spójne, rozbudowane opisy miast, okolic, budynków i polityki/gildii. "
        "Dodawaj historie, legendy, zależności i konflikty. "
        "Zawsze generuj wynik w poprawnym formacie JSON (RFC 8259). "
        "Używaj tylko cudzysłowów (\") do oznaczania kluczy i wartości tekstowych. "
        "Nie dodawaj żadnego tekstu przed ani po JSON. "
        "Nie dodawaj komentarzy, markdowna, kodu ani objaśnień — tylko czysty JSON."
    ),
    "EN": (
        "You are a fantasy worldbuilder and RPG narrator. "
        "Create consistent, detailed descriptions of cities, surroundings, buildings, and politics/factions. "
        "Include history, legends, dependencies, and conflicts. "
        "Always return a valid JSON (RFC 8259). "
        "Use only double quotes (\") for keys and string values. "
        "Do not add any text before or after the JSON. "
        "Do not include markdown, code blocks, or explanations — only pure JSON."
    ),
}

USER_PROMPTS_WORLD = {
    "PL": (
        "Wygeneruj rozbudowany świat fantasy jako czysty JSON.\n"
        "- city: opis miasta\n"
        "- surroundings: min. 5 lokacji z historią\n"
        "- buildings: min. 5 budynków z opisem\n"
        "- politics: min. 5 gildii lub frakcji\n"
        "Format JSON:\n"
        "{ \"city\": \"\", \"surroundings\": [...], \"buildings\": [...], \"politics\": [...] }\n"
        "Zwróć wyłącznie poprawny JSON — bez dodatkowego tekstu."
    ),
    "EN": (
        "Generate a detailed fantasy world as pure JSON.\n"
        "- city: full description of the main city\n"
        "- surroundings: at least 5 locations with legends\n"
        "- buildings: at least 5 key structures\n"
        "- politics: at least 5 guilds or factions\n"
        "JSON format:\n"
        "{ \"city\": \"\", \"surroundings\": [...], \"buildings\": [...], \"politics\": [...] }\n"
        "Return only valid JSON — no explanations."
    ),
}

# ===============================
# PROMPTS — NPC GENERATOR
# ===============================

SYSTEM_PROMPTS_NPC = {
    "PL": (
        "Jesteś narratorem RPG i twórcą postaci fantasy. "
        "Generujesz WYŁĄCZNIE poprawny JSON (RFC 8259). "
        "WAŻNE: KLUCZE JSON MUSZĄ BYĆ ZAWSZE PO ANGIELSKU, "
        "dokładnie takie jak w schemacie poniżej. "
        "TREŚĆ (opisy) może być po polsku.\n\n"

        "Każdy NPC MUSI zawierać DOKŁADNIE te pola:\n"
        "- name\n"
        "- surname\n"
        "- race\n"
        "- age\n"
        "- appearance\n"
        "- character\n"
        "- traits (list)\n"
        "- skills (list)\n"
        "- talents (list)\n"
        "- flaws (list)\n"
        "- dreams (list)\n"
        "- secrets (list)\n"
        "- relations (list of objects with keys: npc_name, relation_type)\n\n"

        "NIE używaj kluczy takich jak: imię, nazwisko, rasa, wiek, wygląd itd.\n"
        "NIE dodawaj żadnych komentarzy, opisów ani tekstu poza JSON.\n"
        "Zwróć WYŁĄCZNIE JSON."
    ),
    "EN": (
        "You are an RPG narrator and creator of fantasy NPCs. "
        "Generate ONLY valid JSON (RFC 8259 compliant). "
        "Each NPC must include exactly these fields:\n"
        "name, surname, race, age, appearance, character, traits, skills, talents, "
        "flaws, dreams, secrets, relations.\n"
        "Relations must be a list of objects with keys npc_name and relation_type.\n"
        "Do not add any text before or after the JSON."
    ),
}

USER_PROMPTS_NPC = {
    "PL": (
        "Na podstawie świata wygeneruj 10–15 NPC w klimacie fantasy.\n\n"

        "BARDZO WAŻNE:\n"
        "- KLUCZE JSON MUSZĄ BYĆ PO ANGIELSKU (name, surname, race, age itd.)\n"
        "- TYLKO TREŚĆ (opisy) ma być po polsku\n\n"

        "Każdy NPC musi mieć:\n"
        "- name (string)\n"
        "- surname (string)\n"
        "- race (string)\n"
        "- age (number)\n"
        "- appearance (string, po polsku)\n"
        "- character (string, po polsku)\n"
        "- traits (array of strings, po polsku)\n"
        "- skills (array of strings, po polsku)\n"
        "- talents (array of strings, po polsku)\n"
        "- flaws (array of strings, po polsku)\n"
        "- dreams (array of strings, po polsku)\n"
        "- secrets (array of strings, po polsku)\n"
        "- relations:\n"
        "  [ { \"npc_name\": \"Full Name\", \"relation_type\": \"Relation\" } ]\n\n"

        "Dozwolone relation_type:\n"
        "[\"Friendship\", \"Alliance\", \"Rivalry\", \"Conflict\", \"Hostility\", "
        "\"Hatred\", \"Revenge\", \"Cooperation\", \"Different goals\", \"neutral\"].\n\n"

        "Zwróć WYŁĄCZNIE JSON w strukturze:\n"
        "{ \"npcs\": [ { ... } ] }"
    ),
    "EN": (
        "Based on the given world, generate 10–15 fantasy NPCs.\n\n"
        "Each NPC must include:\n"
        "- name and surname,\n"
        "- race and age,\n"
        "- appearance and character,\n"
        "- lists of skills, talents, flaws, dreams, and secrets,\n"
        "- relations in JSON format:\n"
        "  \"relations\": [\n"
        "    {\"npc_name\": \"Full Name\", \"relation_type\": \"Alliance\"}\n"
        "  ]\n\n"
        "Relations allowed: [\"Friendship\", \"Alliance\", \"Rivalry\", \"Conflict\", \"Hostility\", \"Hatred\", \"Revenge\", \"Cooperation\", \"Different goals\", \"neutral\"].\n\n"
        "Return **only** valid JSON of the structure:\n"
        "{ \"npcs\": [ { ... } ] }"
    ),
}
# ===============================
# PROMPTS — HERO GENERATOR
# ===============================

SYSTEM_PROMPTS_HERO = {
    "PL": (
        "Jesteś narratorem RPG i ekspertem w tworzeniu kart postaci graczy. "
        "Twoim zadaniem jest wygenerować kompletny, poprawny JSON zawierający szczegółową kartę bohatera fantasy. "
        "Odpowiedź MUSI zawierać wyłącznie jeden obiekt JSON — żadnego tekstu, markdowna, komentarzy ani kodu przed lub po. "
        "Każdy klucz i wartość tekstowa muszą być ujęte w podwójne cudzysłowy. "
        "JSON musi być w pełni zgodny ze standardem RFC 8259. "
        "Jeśli wynik nie jest poprawny (np. json.loads() zwróci błąd), popraw go wewnętrznie i wygeneruj ponownie, "
        "aż powstanie poprawna struktura. "
        "Nie używaj ```json``` ani innych znaczników — tylko czysty JSON zaczynający się od '{' i kończący na '}'."
    ),
    "EN": (
        "You are an RPG narrator and expert in generating player character sheets. "
        "Your task is to produce a fully valid JSON containing a detailed fantasy hero profile. "
        "The output MUST be one single JSON object — no markdown, comments, or text before/after it. "
        "All keys and string values must use double quotes. "
        "The JSON must be fully compliant with RFC 8259. "
        "If the result is invalid (e.g. json.loads() fails), reformat and regenerate it internally "
        "until a valid JSON is produced. "
        "Do not use ```json``` or any other code markers — only pure JSON starting with '{' and ending with '}'."
    ),
}

USER_PROMPTS_HERO = {
    "PL": (
        "Na podstawie świata i wybranych NPC stwórz głównego bohatera gracza. "
        "Wypełnij wszystkie pola, zachowując spójność z fabułą świata i relacjami z NPC. "
        "Zanim zwrócisz odpowiedź, sprawdź czy:\n"
        "1. JSON zaczyna się znakiem '{' i kończy '}'.\n"
        "2. Nie zawiera żadnego tekstu poza strukturą JSON.\n"
        "3. Wszystkie cudzysłowy są podwójne i poprawnie sparowane.\n"
        "4. Każdy obiekt i tablica są poprawnie zamknięte.\n"
        "5. Wynik przechodzi test json.loads() w Pythonie bez błędu.\n\n"
        "Struktura (dokładnie taka):\n"
        "{\n"
        "  \"name\": \"\",\n"
        "  \"surname\": \"\",\n"
        "  \"age\": 0,\n"
        "  \"race\": \"\",\n"
        "  \"appearance\": {\"description\": \"\", \"distinctive_signs\": \"\"},\n"
        "  \"class\": \"\",\n"
        "  \"history\": \"...\",\n"
        "  \"equipment\": [{\"name\": \"\", \"description\": \"\"}],\n"
        "  \"main_attributes\": {\"strength\":0, \"agility\":0, \"constitution\":0, \"intelligence\":0, \"wisdom\":0, \"charisma\":0, \"dexterity\":0, \"endurance\":0, \"perception\":0, \"luck\":0},\n"
        "  \"soft_skills\": [\"\", \"\", \"\"],\n"
        "  \"relationships\": {\"NPC Name\": \"Opis relacji\"},\n"
        "  \"ambitions\": \"\",\n"
        "  \"flaws\": \"\",\n"
        "  \"dreams\": \"\",\n"
        "  \"secrets\": \"\"\n"
        "}\n\n"
        "Zwróć tylko kompletny, poprawny JSON — nic więcej."
    ),
    "EN": (
        "Based on the world and selected NPCs, create a main player hero. "
        "Fill all fields coherently with the world’s lore and relationships. "
        "Before sending your answer, verify that:\n"
        "1. The JSON starts with '{' and ends with '}'.\n"
        "2. There is no text before or after the JSON.\n"
        "3. All quotes are double and correctly paired.\n"
        "4. All arrays and objects are properly closed.\n"
        "5. The structure passes json.loads() in Python without error.\n\n"
        "Expected structure:\n"
        "{\n"
        "  \"name\": \"\",\n"
        "  \"surname\": \"\",\n"
        "  \"age\": 0,\n"
        "  \"race\": \"\",\n"
        "  \"appearance\": {\"description\": \"\", \"distinctive_signs\": \"\"},\n"
        "  \"class\": \"\",\n"
        "  \"history\": \"...\",\n"
        "  \"equipment\": [{\"name\": \"\", \"description\": \"\"}],\n"
        "  \"main_attributes\": {\"strength\":0, \"agility\":0, \"constitution\":0, \"intelligence\":0, \"wisdom\":0, \"charisma\":0, \"dexterity\":0, \"endurance\":0, \"perception\":0, \"luck\":0},\n"
        "  \"soft_skills\": [\"\", \"\", \"\"],\n"
        "  \"relationships\": {\"NPC Name\": \"Relationship description\"},\n"
        "  \"ambitions\": \"\",\n"
        "  \"flaws\": \"\",\n"
        "  \"dreams\": \"\",\n"
        "  \"secrets\": \"\"\n"
        "}\n\n"
        "Return only one complete, valid JSON — nothing else."
    ),
}


# ===============================
# PROMPTS — MISSION GENERATOR
# ===============================

SYSTEM_PROMPTS_MISSION_EPIC = {
    "PL": (
        "Jesteś mistrzem gry RPG i pisarzem fantasy wysokiej klasy. "
        "Generujesz ZAWSZE DOKŁADNIE JEDNĄ misję jako POJEDYNCZY obiekt JSON (root). "

        "NIE używaj tablicy 'missions'. "
        "NIE dodawaj żadnych wrapperów ani dodatkowych pól. "

        "Każda misja MUSI zawierać: "
        "id, title, quest_giver, description, objectives, dialogue, choices, connections, rewards. "

        "ID misji musi być zachowane DOKŁADNIE (np. M6, M10, M12) i nie wolno go zmieniać ani interpretować. "
        "Kolejność misji NIE MA znaczenia — identyfikacja odbywa się WYŁĄCZNIE przez pole 'id'. "

        "Każdy dialog NPC i każda opcja wyboru gracza MUSI zawierać minimum 5 pełnych zdań. "
        "Nie skracaj opisów, nie streszczaj, nie usuwaj treści. "

        "Zwróć WYŁĄCZNIE poprawny JSON zgodny z RFC 8259. "
        "Używaj WYŁĄCZNIE podwójnych cudzysłowów (\"). "
        "Nie dodawaj markdowna, komentarzy, opisów ani żadnego tekstu poza JSON-em. "
        "Output MUSI przejść json.loads() w Pythonie bez żadnego błędu. "

        "JSON MUSI zaczynać się od '{' i kończyć na '}'."
    ),

    "EN": (
        "You are a high-level RPG game master and fantasy writer. "
        "You ALWAYS generate EXACTLY ONE mission as a SINGLE JSON root object. "

        "DO NOT use a 'missions' array. "
        "DO NOT wrap the mission in any additional structure. "

        "The mission MUST contain exactly these fields: "
        "id, title, quest_giver, description, objectives, dialogue, choices, connections, rewards. "

        "The mission ID (e.g. M6, M10, M12) MUST be preserved exactly as provided. "
        "Never infer order from filenames or position — missions are identified ONLY by 'id'. "

        "Each NPC dialogue entry and each player choice MUST contain at least 5 full sentences. "
        "Do not shorten, summarize, or omit content. "

        "Return ONLY valid RFC 8259 compliant JSON. "
        "Use ONLY double quotes (\") for all keys and string values. "
        "No markdown, no explanations, no preamble. "

        "The output MUST start with '{' and end with '}' and pass json.loads() in Python."
    ),
}



USER_PROMPTS_MISSION_EPIC = {
    "PL": (
        "Na podstawie świata, bohatera i listy NPC przekształć poniższą misję w epicką, rozbudowaną wersję.\n"
        "- Zachowaj wszystkie pola struktury JSON zgodnie z poniższym schematem.\n"
        "- Każdy dialog NPC i każda opcja gracza musi mieć minimum 5 zdań.\n"
        "- Cele i nagrody pozostają zgodne z oryginałem (możesz je poetycko opisać, ale nie zmieniaj sensu).\n"
        "- Odpowiedź: tylko poprawny JSON, dokładnie w tej strukturze:\n\n"
        "{\n"
        "  \"missions\": [\n"
        "    {\n"
        "      \"id\": \"\",\n"
        "      \"title\": \"\",\n"
        "      \"quest_giver\": {\"name\": \"\", \"affiliation\": \"\"},\n"
        "      \"description\": \"\",\n"
        "      \"objectives\": [\"\", \"\"],\n"
        "      \"dialogue\": [\n"
        "        {\"speaker\": \"\", \"lines\": \"\"}\n"
        "      ],\n"
        "      \"choices\": [\n"
        "        {\"id\": \"\", \"title\": \"\", \"text\": \"\", \"outcome\": \"\"}\n"
        "      ],\n"
        "      \"connections\": {\"previous\": [\"\"], \"next\": [\"\"]},\n"
        "      \"rewards\": [\n"
        "        {\"type\": \"\", \"description\": \"\"}\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Zwróć wyłącznie poprawny JSON — bez dodatkowego tekstu, markdowna, ani wyjaśnień."
    ),
    "EN": (
        "Based on the provided world, hero, and NPCs, expand the following mission into an epic version.\n"
        "- Keep all fields exactly as in the structure below.\n"
        "- Each NPC dialogue and player choice must contain at least 5 sentences.\n"
        "- Keep the same goals and rewards (you may enrich them poetically, but do not change meaning).\n"
        "- Output must be valid JSON in the exact structure below:\n\n"
        "{\n"
        "  \"missions\": [\n"
        "    {\n"
        "      \"id\": \"\",\n"
        "      \"title\": \"\",\n"
        "      \"quest_giver\": {\"name\": \"\", \"affiliation\": \"\"},\n"
        "      \"description\": \"\",\n"
        "      \"objectives\": [\"\", \"\"],\n"
        "      \"dialogue\": [\n"
        "        {\"speaker\": \"\", \"lines\": \"\"}\n"
        "      ],\n"
        "      \"choices\": [\n"
        "        {\"id\": \"\", \"title\": \"\", \"text\": \"\", \"outcome\": \"\"}\n"
        "      ],\n"
        "      \"connections\": {\"previous\": [\"\"], \"next\": [\"\"]},\n"
        "      \"rewards\": [\n"
        "        {\"type\": \"\", \"description\": \"\"}\n"
        "      ]\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Return **only** a single valid JSON — no markdown, no explanations, no preamble."
    ),
}


# ===============================
# PROMPTS — QUESTS GENERATOR
# ===============================

SYSTEM_PROMPTS_MISSION = {
    "PL": (
        "Jesteś mistrzem gry RPG i tworzysz główną linię fabularną w świecie fantasy. "
        "Twoim zadaniem jest stworzenie zestawu minimum 10 spójnych, rozbudowanych misji w formacie JSON. "
        "Każda misja powinna być emocjonująca, z bogatymi opisami świata, głębią psychologiczną bohatera "
        "i relacjami z NPC. Dialogi muszą być obszerne (po kilka zdań), a fabuła wszystkich misji połączona. "
        "Każda misja zawiera: id, title, quest_giver, description, objectives, dialogue, connections, rewards. "
        "Wynik musi być wyłącznie poprawnym JSON-em w formacie {\"missions\": [ ... ]}, bez żadnych komentarzy ani tekstu przed lub po."
    ),
    "EN": (
        "You are an RPG game master creating the main storyline in a fantasy world. "
        "Your task is to generate at least 10 coherent, detailed missions in JSON format. "
        "Each mission should be emotionally engaging, rich in worldbuilding and character depth, "
        "and connected to the hero and NPCs. Dialogues must be extensive (several sentences each), "
        "and all missions should form one overarching story. "
        "Each mission includes: id, title, quest_giver, description, objectives, dialogue, connections, rewards. "
        "Return only valid JSON in the format {\"missions\": [ ... ]}, with no extra text or commentary."
    ),
}

USER_PROMPTS_MISSION = {
    "PL": (
        "Na podstawie świata, bohatera i NPC stwórz zestaw minimum 10 połączonych misji głównej linii fabularnej.\n"
        "- Każda misja musi być długa, z rozbudowanym opisem, emocjami, relacjami i dialogami (po kilka zdań)\n"
        "- Misje muszą być spójne i logicznie powiązane (connections previous/next)\n"
        "- Zachowaj realistyczne nagrody i cele fabularne\n"
        "- Odpowiedź: wyłącznie poprawny JSON {\"missions\": [ ... ]}, bez żadnego tekstu przed ani po"
    ),
    "EN": (
        "Based on the world, hero, and NPCs, create at least 10 interconnected main storyline missions.\n"
        "- Each mission should have a long, rich description with emotions and detailed dialogues (several sentences each)\n"
        "- Missions must be coherent and connected through previous/next relationships\n"
        "- Keep realistic story-driven goals and rewards\n"
        "- Return only valid JSON {\"missions\": [ ... ]}, with no additional text before or after"
    ),
}


# ===============================
# UNIVERSAL PROMPT ACCESSOR
# ===============================


def get_prompt(category: str, lang: str = "EN"):
    """
    Returns (system_prompt, user_prompt) pair for a given category and language.
    Supported categories: 'world', 'npc', 'hero', 'mission_epic', 'mission'
    """
    lang = lang.upper()

    if category == "world":
        return (
            SYSTEM_PROMPTS_WORLD.get(lang, SYSTEM_PROMPTS_WORLD["EN"]),
            USER_PROMPTS_WORLD.get(lang, USER_PROMPTS_WORLD["EN"])
        )
    if category == "npc":
        return (
            SYSTEM_PROMPTS_NPC.get(lang, SYSTEM_PROMPTS_NPC["EN"]),
            USER_PROMPTS_NPC.get(lang, USER_PROMPTS_NPC["EN"])
        )
    if category == "hero":
        return (
            SYSTEM_PROMPTS_HERO.get(lang, SYSTEM_PROMPTS_HERO["EN"]),
            USER_PROMPTS_HERO.get(lang, USER_PROMPTS_HERO["EN"])
        )
    if category == "mission_epic":
        return (
            SYSTEM_PROMPTS_MISSION_EPIC.get(lang, SYSTEM_PROMPTS_MISSION_EPIC["EN"]),
            USER_PROMPTS_MISSION_EPIC.get(lang, USER_PROMPTS_MISSION_EPIC["EN"])
        )
    if category == "missions":
        return (
            SYSTEM_PROMPTS_MISSION.get(lang, SYSTEM_PROMPTS_MISSION["EN"]),
            USER_PROMPTS_MISSION.get(lang, USER_PROMPTS_MISSION["EN"])
        )


    raise ValueError(f"Unknown prompt category: {category}")