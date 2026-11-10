"""
Visual Recognition Studio - FastAPI ALPR Service (Local Development Entrypoint)

Runs the Automated License Plate Recognition service locally with model fallback
(Gemini 3.5 Flash Lite -> Gemini 3.5 Flash) and Supabase persistence.

Usage:
    uvicorn main:app --reload --port 8000
    or
    python main.py
"""

import os
import sys

# Load environment variables from .env
from dotenv import load_dotenv
load_dotenv()

# Import the core ASGI application from the api package
from api.index import app

# Verify configuration on startup
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

missing = []
if not GEMINI_API_KEY:
    missing.append("GEMINI_API_KEY")
if not SUPABASE_URL:
    missing.append("SUPABASE_URL")
if not SUPABASE_SERVICE_KEY:
    missing.append("SUPABASE_SERVICE_KEY (or SUPABASE_SERVICE_ROLE_KEY)")

if missing:
    print(f"\n[WARNING] Missing environment variables: {', '.join(missing)}")
    print("[WARNING] Copy .env.example to .env and configure your keys to enable full recognition and database storage.\n")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Visual Recognition Studio ALPR on http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
