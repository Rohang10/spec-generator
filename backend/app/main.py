from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.specs import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    banner = """
    \033[94m\033[1m
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
    │   🚀  AI Spec Generator Backend Running Successfully!  │
    │                                                        │
    │   🌍  Local API:   http://127.0.0.1:8000               │
    │   📚  Swagger API: http://127.0.0.1:8000/docs          │
    │                                                        │
    └────────────────────────────────────────────────────────┘
    \033[0m
    """
    print(banner)
    yield

app = FastAPI(
    title="AI Spec Generator",
    description="Generate structured API specs + DB schema from messy requirements",
    version="1.0",
    lifespan=lifespan
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

@app.get("/", response_class=PlainTextResponse)
def read_root():
    return "🚀  AI Spec Generator Backend Running Successfully!\n"
