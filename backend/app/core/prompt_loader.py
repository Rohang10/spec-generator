def load_prompt(path: str, **kwargs) -> str:
    with open(path, "r", encoding="utf-8") as f:
        prompt = f.read()

    for key, value in kwargs.items():
        prompt = prompt.replace(f"{{{{{key}}}}}", value)

    return prompt
