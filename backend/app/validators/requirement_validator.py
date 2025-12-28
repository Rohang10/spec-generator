from fastapi import HTTPException

GENERIC_PHRASES = [
    "build a task management system",
    "build task management system",
    "build a system",
    "build an application",
    "build a platform",
]

ACTION_KEYWORDS = [
    "create", "edit", "update", "delete", "manage",
    "view", "assign", "track", "export", "priority",
    "due date", "deadline", "notification"
]


def validate_requirements_text(text: str):
    text_lower = text.lower().strip()

    # 1️⃣ Too short → always invalid
    if len(text_lower) < 20:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "REQUIREMENT_TOO_SHORT",
                "message": (
                    "Requirement is too brief. "
                    "Please describe what users can do in the system."
                )
            }
        )

    # 2️⃣ Generic phrase ONLY (no real detail)
    for phrase in GENERIC_PHRASES:
        if text_lower.startswith(phrase):
            remainder = text_lower[len(phrase):].strip()

            # If nothing meaningful follows → reject
            if not remainder or not any(
                action in remainder for action in ACTION_KEYWORDS
            ):
                raise HTTPException(
                    status_code=400,
                    detail={
                        "code": "REQUIREMENT_TOO_VAGUE",
                        "message": (
                            "Requirement is too generic. "
                            "Please include specific user actions and behavior."
                        )
                    }
                )

    # ✅ Otherwise ACCEPT
    return
