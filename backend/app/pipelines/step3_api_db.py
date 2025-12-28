import json
import os

from app.core.groq_client import call_groq
from app.core.prompt_loader import load_prompt
from app.schemas.spec_schema import APIEndpoint, DBTable
from app.pipelines.utils import extract_json

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "v1_api_db.md")


def generate_api_db(features: dict) -> dict:
    prompt = load_prompt(
        PROMPT_PATH,
        features_json=json.dumps(features, indent=2)
    )

    raw = call_groq(prompt)
    raw_json = extract_json(raw)

    data = json.loads(raw_json)

    for api in data["api_endpoints"]:
        APIEndpoint(**api)

    for table in data["db_schema"]:
        DBTable(**table)

    return data
