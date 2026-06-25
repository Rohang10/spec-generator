from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api.specs import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    banner = """
    \033[94m\033[1m
    ┌────────────────────────────────────────────────────────┐
    │                                                        │
    │   🚀  AI Spec Generator Backend Running Successfully!   │
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

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    host_url = str(request.base_url).rstrip("/")
    docs_url = f"{host_url}/docs"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Spec Generator Backend</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-color: #0b0f19;
                --card-bg: rgba(17, 24, 39, 0.75);
                --border-color: rgba(255, 255, 255, 0.08);
                --accent-color: #3b82f6;
                --accent-glow: rgba(59, 130, 246, 0.15);
                --text-color: #f3f4f6;
                --text-muted: #9ca3af;
                --success-color: #10b981;
                --success-glow: rgba(16, 185, 129, 0.2);
            }}

            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}

            body {{
                background-color: var(--bg-color);
                color: var(--text-color);
                font-family: 'Outfit', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                position: relative;
            }}

            body::before {{
                content: '';
                position: absolute;
                width: 300px;
                height: 300px;
                background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
                top: 20%;
                left: 20%;
                z-index: 0;
                pointer-events: none;
            }}

            body::after {{
                content: '';
                position: absolute;
                width: 400px;
                height: 400px;
                background: radial-gradient(circle, rgba(16, 185, 129, 0.08) 0%, transparent 70%);
                bottom: 10%;
                right: 15%;
                z-index: 0;
                pointer-events: none;
            }}

            .container {{
                z-index: 10;
                width: 100%;
                max-width: 650px;
                padding: 2rem;
            }}

            .status-card {{
                background: var(--card-bg);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid var(--border-color);
                border-radius: 24px;
                padding: 3rem 2.5rem;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3),
                            0 0 50px var(--accent-glow);
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            }}

            .status-card:hover {{
                transform: translateY(-4px);
                box-shadow: 0 24px 48px rgba(0, 0, 0, 0.4),
                            0 0 60px rgba(59, 130, 246, 0.2);
            }}

            .pulse-indicator {{
                width: 16px;
                height: 16px;
                background-color: var(--success-color);
                border-radius: 50%;
                margin: 0 auto 1.5rem auto;
                box-shadow: 0 0 0 0 var(--success-glow);
                animation: pulse 2s infinite;
            }}

            @keyframes pulse {{
                0% {{
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 var(--success-glow);
                }}
                70% {{
                    transform: scale(1);
                    box-shadow: 0 0 0 12px transparent;
                }}
                100% {{
                    transform: scale(0.95);
                    box-shadow: 0 0 0 0 transparent;
                }}
            }}

            h1 {{
                font-size: 2.2rem;
                font-weight: 800;
                margin-bottom: 0.5rem;
                letter-spacing: -0.5px;
                background: linear-gradient(135deg, #ffffff 30%, #a5b4fc 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}

            p.subtitle {{
                color: var(--text-muted);
                font-size: 1.1rem;
                margin-bottom: 2.5rem;
            }}

            .terminal-block {{
                background: rgba(0, 0, 0, 0.45);
                border: 1px solid rgba(255, 255, 255, 0.05);
                border-radius: 16px;
                padding: 1.5rem;
                text-align: left;
                font-family: 'JetBrains Mono', monospace;
                font-size: 0.9rem;
                line-height: 1.6;
                color: #38bdf8;
                margin-bottom: 2.5rem;
                overflow-x: auto;
                white-space: pre-wrap;
                word-break: break-all;
                box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.5);
            }}
            
            .terminal-block a {{
                color: #60a5fa;
                text-decoration: none;
                border-bottom: 1px dashed rgba(96, 165, 250, 0.4);
                transition: color 0.2s, border-color 0.2s;
            }}
            
            .terminal-block a:hover {{
                color: #93c5fd;
                border-color: #93c5fd;
            }}

            .links-group {{
                display: flex;
                gap: 1rem;
                justify-content: center;
            }}

            .btn {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                padding: 0.75rem 1.5rem;
                border-radius: 12px;
                font-weight: 600;
                text-decoration: none;
                transition: all 0.2s ease;
                font-size: 0.95rem;
                cursor: pointer;
            }}

            .btn-primary {{
                background-color: var(--accent-color);
                color: white;
                box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            }}

            .btn-primary:hover {{
                background-color: #2563eb;
                transform: translateY(-1px);
                box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4);
            }}

            .btn-secondary {{
                background-color: rgba(255, 255, 255, 0.05);
                color: var(--text-color);
                border: 1px solid var(--border-color);
            }}

            .btn-secondary:hover {{
                background-color: rgba(255, 255, 255, 0.1);
                border-color: rgba(255, 255, 255, 0.2);
                transform: translateY(-1px);
            }}

            .btn svg {{
                margin-right: 8px;
                width: 18px;
                height: 18px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="status-card">
                <div class="pulse-indicator"></div>
                <h1>AI Spec Generator</h1>
                <p class="subtitle">API service is active and healthy</p>
                
                <div class="terminal-block">🚀  AI Spec Generator Backend Running Successfully!   
🌍  Local API:   http://127.0.0.1:8000               📚  Swagger API: http://127.0.0.1:8000/docs</div>
                
                <div class="links-group">
                    <a href="/docs" class="btn btn-primary">
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                        </svg>
                        Swagger API Docs
                    </a>
                    <a href="/redoc" class="btn btn-secondary">
                        <svg fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"></path>
                        </svg>
                        Redoc
                    </a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
