from google.genai import Client, types
from app.core.config import settings

# Initialize Google GenAI client
# It will load GEMINI_API_KEY automatically from settings
client = Client(api_key=settings.GEMINI_API_KEY)

SYSTEM_MESSAGE = (
    "You must return ONLY valid JSON. "
    "No explanations. No markdown. No text outside JSON. "
    "If the response is not pure JSON, it is invalid."
)

def call_gemini(
    prompt: str,
    system_instruction: str = SYSTEM_MESSAGE,
    temperature: float = 0.0,
) -> str:
    config = types.GenerateContentConfig(
        system_instruction=system_instruction,
        temperature=temperature,
        response_mime_type="application/json",
    )
    
    # Try the configured main model first, then try standard stable fallbacks
    models_to_try = [settings.GEMINI_MODEL]
    for fallback in ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]:
        if fallback != settings.GEMINI_MODEL:
            models_to_try.append(fallback)
            
    last_error = None
    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=config,
            )
            if response.text is None:
                raise ValueError(f"Model {model_name} returned an empty response.")
            return response.text
        except Exception as e:
            last_error = e
            print(f"⚠️ Model {model_name} failed with error: {e}. Trying next model...")
            
    if last_error is None:
        raise RuntimeError("All models failed to respond.")
    raise last_error
