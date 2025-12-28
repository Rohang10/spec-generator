import uuid
import json
import os

from app.schemas.spec_schema import SpecOutput
from app.core.config import settings
from app.pipelines.step1_features import generate_features
from app.pipelines.step2_user_stories import generate_user_stories
from app.pipelines.step3_api_db import generate_api_db
from app.utils.open_questions_groq import generate_open_questions


def run_pipeline(requirements_text: str):
    trace_id = str(uuid.uuid4())

    # ---- STEP 1: FEATURES ----
    for _ in range(settings.MAX_RETRIES):
        try:
            features = generate_features(requirements_text)
            break
        except Exception as e:
            print("Feature retry failed:", e)
    else:
        raise Exception("Feature extraction failed")

    # ---- STEP 2: USER STORIES ----
    for _ in range(settings.MAX_RETRIES):
        try:
            stories = generate_user_stories(features)
            break
        except Exception as e:
            print("Story retry failed:", e)
    else:
        raise Exception("User story generation failed")

    # ---- STEP 3: API + DB ----
    for _ in range(settings.MAX_RETRIES):
        try:
            api_db = generate_api_db(features)
            break
        except Exception as e:
            print("API/DB retry failed:", e)
    else:
        raise Exception("API/DB generation failed")

    # ---- STEP 4: OPEN QUESTIONS (ONLY AFTER SUCCESS) ----
    open_questions = generate_open_questions(
        requirements_text=requirements_text,
        features=features,
        user_stories=stories,
        api_endpoints=api_db["api_endpoints"],
        db_schema=api_db["db_schema"],
    )

    final_spec = {
        **features,
        **stories,
        **api_db,
        "open_questions": open_questions,
    }

    # ---- FINAL VALIDATION ----
    SpecOutput(**final_spec)

    # ---- SAVE TRACE ----
    os.makedirs("outputs/traces", exist_ok=True)
    with open(f"outputs/traces/{trace_id}.json", "w") as f:
        json.dump(final_spec, f, indent=2)

    return trace_id, final_spec
