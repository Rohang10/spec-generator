import re
import ast
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

def format_gemini_error(e: Exception) -> str:
    err_str = str(e)
    try:
        # Check if it has code/message attributes directly
        code = getattr(e, 'code', None)
        message = getattr(e, 'message', None)
        if code and message:
            return f"Gemini API Error ({code}): {message}"
            
        # Parse JSON-like dictionary representation in error string
        match = re.search(r"(\{.*\})", err_str)
        if match:
            # Safely parse the dict representation
            err_dict = ast.literal_eval(match.group(1))
            if isinstance(err_dict, dict) and 'error' in err_dict:
                inner = err_dict['error']
                code = inner.get('code', 'Unknown')
                msg = inner.get('message', '')
                status = inner.get('status', '')
                if msg:
                    return f"Gemini API Error ({code} {status}): {msg}"
    except Exception:
        pass
    return err_str

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
            
    errors = []
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
            print(f"⚠️ Model {model_name} failed with error: {e}. Trying next model...")
            errors.append((model_name, e))
            
            # Fail-fast on critical authentication/quota issues
            err_str = str(e).lower()
            if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str:
                formatted_msg = format_gemini_error(e)
                raise RuntimeError(formatted_msg)
            if "401" in err_str or "403" in err_str or "api_key_invalid" in err_str:
                formatted_msg = format_gemini_error(e)
                raise RuntimeError(formatted_msg)
            
    if not errors:
        raise RuntimeError("All models failed to respond.")
        
    # Order of priority for selecting the best error to bubble up:
    # 1. 429 / Quota / Rate Limit
    # 2. 401 / 403 / Authentication
    # 3. 503 / Unavailable / Overloaded
    # 4. First error (usually the primary model's error)
    
    for model_name, err in errors:
        err_str = str(err).lower()
        if "429" in err_str or "resource_exhausted" in err_str or "quota" in err_str:
            raise RuntimeError(format_gemini_error(err))
            
    for model_name, err in errors:
        err_str = str(err).lower()
        if "401" in err_str or "403" in err_str or "api_key_invalid" in err_str:
            raise RuntimeError(format_gemini_error(err))
            
    for model_name, err in errors:
        err_str = str(err).lower()
        if "503" in err_str or "unavailable" in err_str or "overloaded" in err_str:
            raise RuntimeError(format_gemini_error(err))
            
    # Fallback to the first error (which corresponds to the primary/configured model)
    raise RuntimeError(format_gemini_error(errors[0][1]))
