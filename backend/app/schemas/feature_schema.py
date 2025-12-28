from pydantic import BaseModel
from typing import List, Dict
from app.schemas.spec_schema import Module


class FeatureExtractionOutput(BaseModel):
    modules: List[Module]
    features_by_module: Dict[str, List[str]]
