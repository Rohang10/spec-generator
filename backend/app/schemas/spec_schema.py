from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class Module(BaseModel):
    name: str
    description: Optional[str] = None

class UserStory(BaseModel):
    role: str
    goal: str
    benefit: str

class APIEndpoint(BaseModel):
    method: str
    path: str
    auth_required: bool
    request_schema: Dict
    response_schema: Dict
    error_cases: List[str]

class DBColumn(BaseModel):
    name: str
    type: str
    constraints: Optional[str] = None


class DBTable(BaseModel):
    table_name: str
    columns: List[DBColumn]

class SpecOutput(BaseModel):
    modules: List[Module]
    features_by_module: Dict[str, List[str]]
    user_stories: List[UserStory]
    api_endpoints: List[APIEndpoint]
    db_schema: List[DBTable]
    open_questions: List[str] = Field(
        description="Missing, unclear, or ambiguous requirements"
    )
