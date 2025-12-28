from groq import Groq
from app.core.config import settings

client = Groq(api_key=settings.GROQ_API_KEY)


SYSTEM_MESSAGE = (
    "You must return ONLY valid JSON. "
    "No explanations. No markdown. No text outside JSON. "
    "If the response is not pure JSON, it is invalid."
)

def call_groq(prompt: str) -> str:
    response = client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        temperature=0,
        max_tokens=4000,
    )
    return response.choices[0].message.content
