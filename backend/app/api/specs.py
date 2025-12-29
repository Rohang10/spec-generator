import os
import json

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.pipelines.full_pipeline import run_pipeline, run_refinement_pipeline
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

class RefineRequest(BaseModel):
    instruction: str

@router.post("/refine")
def refine_spec_endpoint(payload: RefineRequest):
    instruction = payload.instruction.strip()   

    if len(instruction) < 5:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_REFINEMENT",
                "message": "Refinement instruction is too short."
            }
        )

    # 🔥 Load latest spec automatically
    trace_dir = "outputs/traces"
    files = sorted(
        os.listdir(trace_dir),
        key=lambda f: os.path.getmtime(os.path.join(trace_dir, f)),
        reverse=True
    )

    if not files:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "NO_EXISTING_SPEC",
                "message": "No existing spec found to refine."
            }
        )

    with open(os.path.join(trace_dir, files[0])) as f:
        existing_spec = json.load(f)

    trace_id, refined_spec = run_refinement_pipeline(
        existing_spec=existing_spec,
        instruction=instruction
    )

    return {
        "trace_id": trace_id,
        "spec": refined_spec
    }