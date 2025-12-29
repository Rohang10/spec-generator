import os
import json
import re

from groq import Groq
from dotenv import load_dotenv

from app.schemas.spec_schema import SpecOutput
from app.core.config import settings  # noqa: F401

# ----------------------------------
# Load environment variables
# ----------------------------------
load_dotenv()

# ----------------------------------
# Groq client initialization
# ----------------------------------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


# ----------------------------------
# Helper: extract JSON object safely
# ----------------------------------
def extract_json_object(text: str) -> dict:
    """
    Extract the first valid JSON object from LLM output.
    Handles cases where the model wraps JSON with text.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError("No JSON object found in LLM output")
    return json.loads(match.group())


# ----------------------------------
# Main refinement function
# ----------------------------------
def refine_spec(existing_spec: dict, instruction: str) -> dict:
    """
    Uses LLM to refine an existing spec based on user instruction.
    """

    prompt = f"""
You are refining an existing software specification.

Current spec:
{json.dumps(existing_spec, indent=2)}

User instruction:
{instruction}

Tasks:
1. Modify ONLY relevant parts of the spec
2. Preserve unchanged sections
3. If instruction lacks information, add open questions
4. If instruction contradicts existing design, list contradictions clearly
5. Return a FULL updated spec JSON

Refinement Rules:

1. Analyze the user instruction and determine its primary intent.

2. Modify ONLY the relevant sections of the spec based on intent:

- Authentication / Authorization / Security:
  → Update api_endpoints
  → Update user_stories
  → Update db_schema ONLY if roles or permissions are needed

- Error handling / Validation:
  → Update api_endpoints
  → Update user_stories

- Roles / Permissions:
  → Update modules
  → Update features_by_module
  → Update db_schema
  → Update api_endpoints

- Performance / Scalability:
  → Update api_endpoints
  → Update db_schema ONLY if required

- Notifications / Alerts:
  → Update modules
  → Update features_by_module
  → Update user_stories

- Logging / Auditing:
  → Update api_endpoints
  → Update db_schema ONLY if required

- UI / UX:
  → Update user_stories ONLY

3. Preserve all unrelated sections unchanged.

4. If the instruction lacks sufficient detail:
  → Do NOT guess
  → Add 3–4 open_questions instead

5. If the instruction contradicts the existing spec:
  → Add clear entries to contradictions[]

6. Return a FULL updated spec JSON.

Rules:
- Do NOT remove valid existing features
- Maintain schema structure exactly
- Output ONLY valid JSON (no text outside JSON)
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You refine technical specifications safely.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content.strip()

    updated_spec = extract_json_object(raw_output)

    # ----------------------------------
    # Validate refined spec strictly
    # ----------------------------------
    SpecOutput(**updated_spec)

    return updated_spec
