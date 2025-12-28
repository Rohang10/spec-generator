import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# ---------- Groq Client ----------
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


# ---------- Helper: Safe JSON Extraction ----------
def extract_json_array(text: str) -> list[str]:
    """
    Extract the first valid JSON array from LLM output.
    This handles cases where the model wraps JSON with text.
    """
    match = re.search(r"\[[\s\S]*\]", text)
    if not match:
        raise ValueError("No JSON array found in LLM output")
    return json.loads(match.group())


# ---------- Main Function ----------
def generate_open_questions(
    requirements_text: str,
    features: dict,
    user_stories: dict,
    api_endpoints: list,
    db_schema: list,
) -> list[str]:
    """
    Generate 3–4 intelligent, context-specific open questions.
    Runs ONLY after the pipeline succeeds.
    """

    prompt = f"""
You are a senior product manager reviewing a generated software specification.

Your goal is to identify missing decisions, unclear requirements,
or product scope gaps specific to THIS system.

Original requirement:
{requirements_text}

Generated features:
{json.dumps(features, indent=2)}

User stories:
{json.dumps(user_stories, indent=2)}

API endpoints:
{json.dumps(api_endpoints, indent=2)}

Database schema:
{json.dumps(db_schema, indent=2)}

Instructions:
- Generate exactly 3 or 4 clarification questions
- Questions MUST be specific to this product and domain
- Do NOT repeat listed features
- Do NOT ask generic SaaS questions
- Focus on permissions, workflows, edge cases, and business rules

Output format (STRICT):
Return ONLY valid JSON.
Do NOT include explanations, headings, or extra text.

Example output:
[
  "Should tasks support recurring schedules?",
  "Do priority levels affect deadline notifications?",
  "Is task deletion permanent or soft-deleted?"
]
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You generate precise, context-aware product clarification questions.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    raw_output = response.choices[0].message.content.strip()

    try:
        questions = extract_json_array(raw_output)
        return questions[:4]

    except Exception :
        # ---------- Fallback (never break pipeline) ----------
        print("⚠️ Open-question parsing failed. Raw output:")
        print(raw_output)

        return [
            "Are there different user roles with varying permissions?",
            "Should notifications or reminders be configurable?",
            "Are audit logs or activity tracking required?",
        ]
