def extract_json(raw: str) -> str:
    """
    Safely extract JSON from LLM output.
    Handles accidental text before/after JSON.
    """
    start = raw.find("{")
    end = raw.rfind("}")

    if start == -1 or end == -1 or end < start:
        raise ValueError("No valid JSON object found in LLM output")

    return raw[start : end + 1]
