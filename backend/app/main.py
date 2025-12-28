from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.specs import router

app = FastAPI(
    title="AI Spec Generator",
    description="Generate structured API specs + DB schema from messy requirements",
    version="1.0"
    )

#CORS middleware    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all origins
    allow_credentials=True,
    allow_methods=["*"],          # allow all HTTP methods
    allow_headers=["*"],          # allow all headers
)

app.include_router(router)
