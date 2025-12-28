from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.pipelines.full_pipeline import run_pipeline
from app.validators.requirement_validator import validate_requirements_text

router = APIRouter(prefix="/specs", tags=["Specs"])


class SpecRequest(BaseModel):
    requirements_text: str


@router.post("/generate")
def generate_spec(payload: SpecRequest):
    text = payload.requirements_text.strip()

    # ---------- Basic length guards ----------
    if len(text) < 20:
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

    if len(text) > 5000:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "REQUIREMENT_TOO_LONG",
                "message": (
                    "Requirement is too long. "
                    "Please keep it under 5000 characters."
                )
            }
        )

    # ---------- Semantic validation (BLOCKS PIPELINE) ----------
    try:
        validate_requirements_text(text)
    except HTTPException as e:
        # ⛔ Do NOT call pipeline if validation fails
        raise e

    # ---------- Run AI pipeline ----------
    try:
        trace_id, spec = run_pipeline(text)
        return {
            "trace_id": trace_id,
            "spec": spec
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "code": "SPEC_GENERATION_FAILED",
                "message": "Spec generation failed during processing.",
                "error": str(e)
            }
        )
