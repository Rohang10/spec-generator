import json
import os

from app.core.groq_client import call_groq
from app.core.prompt_loader import load_prompt
from app.schemas.feature_schema import FeatureExtractionOutput
from app.pipelines.utils import extract_json

# Absolute path resolution (HF-safe)
BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
PROMPT_PATH = os.path.join(BASE_DIR, "prompts", "v1_features.md")


def generate_features(requirements_text: str) -> dict:
    prompt = load_prompt(
        PROMPT_PATH,
        requirements_text=requirements_text
    )

    raw = call_groq(prompt)

    # ✅ Defensive extraction
    raw_json = extract_json(raw)
    data = json.loads(raw_json)

    # ✅ Schema validation
    FeatureExtractionOutput(**data)

    return data
