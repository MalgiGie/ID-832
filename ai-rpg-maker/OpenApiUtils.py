import uuid
from openai import OpenAI
from dotenv import load_dotenv
from utils import *
from config import *

load_dotenv()
STATS_FILE = os.path.join(ROOT_DIRECTORY, "stats.jsonl")
TOTAL_TOKENS = 0

def make_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Nie znaleziono OPENAI_API_KEY!")
    return OpenAI(api_key=api_key) if api_key else OpenAI()

def ask_model(system_prompt, prompt, temperature, max_tokens, label=None):
    global TOTAL_TOKENS
    client = make_client()
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    text = resp.choices[0].message.content
    usage = getattr(resp, "usage", None)

    if usage:
        usage_dict = {
            "total_tokens": getattr(usage, "total_tokens", 0),
            "prompt_tokens": getattr(usage, "prompt_tokens", 0),
            "completion_tokens": getattr(usage, "completion_tokens", 0),
        }
        TOTAL_TOKENS += usage_dict["total_tokens"]
        save_usage_stats(MODEL, system_prompt, prompt, usage_dict, label=label)
        print(f"Całość użytych tokenów (łącznie): {TOTAL_TOKENS}")
    else:
        usage_dict = {}

    return text



def save_usage_stats(model, system_prompt, user_prompt, usage, label=None):
    """Zapisuje statystyki tokenów do pliku JSONL."""
    os.makedirs(ROOT_DIRECTORY, exist_ok=True)
    stats = {
        "id": str(uuid.uuid4()) if not label else None,
        "label": label,
        "timestamp": datetime.utcnow().isoformat(),
        "model": model,
        "system_prompt_length": len(system_prompt),
        "user_prompt_length": len(user_prompt),
        "total_tokens": usage.get("total_tokens", 0),
        "prompt_tokens": usage.get("prompt_tokens", 0),
        "completion_tokens": usage.get("completion_tokens", 0),
    }
    with open(STATS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(stats, ensure_ascii=False) + "\n")