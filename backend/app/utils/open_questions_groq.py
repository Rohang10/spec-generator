import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


def generate_open_questions(
    requirements_text: str,
    features: dict,
    user_stories: dict,
    api_endpoints: list,
    db_schema: list,
) -> list[str]:
    """
    Generate 3–4 intelligent open questions based on the generated spec.
    Runs ONLY after the pipeline succeeds.
    """

    prompt = f"""
You are a senior product manager reviewing a generated software specification.

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

Task:
Generate exactly 3–4 insightful open questions that help clarify
missing decisions, edge cases, or product scope.

Rules:
- Questions must be concise and actionable
- Do NOT repeat existing features
- Do NOT ask obvious or generic questions
- Output ONLY a JSON array of strings
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You generate high-quality product clarification questions.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.25,
    )

    content = response.choices[0].message.content.strip()

    try:
        questions = json.loads(content)
        return questions[:4]
    except Exception:
        # Safe fallback (never break pipeline)
        return [
            "Are there different user roles with varying permissions?",
            "Should notifications or reminders be configurable?",
            "Are audit logs or activity tracking required?",
            "Are there scalability or performance constraints?"
        ]
