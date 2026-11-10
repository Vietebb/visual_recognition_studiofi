"""
Vercel Serverless Function: License Plate Recognition
Uses Gemini REST API + Supabase REST API directly (no heavy SDKs).
"""

import base64
import json
import os
import httpx
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

# Load local .env if present (ignored in production / serverless environments)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(title="ALPR Serverless")

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")

EXTRACTION_PROMPT = (
    "Extract the license plate number from this vehicle. "
    "Return ONLY the alphanumeric characters of the plate with no spaces "
    "or punctuation. If no plate is visible, return 'NONE'."
)

CANDIDATE_MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.5-flash",
]


@app.get("/")
@app.get("/api")
@app.get("/api/index")
async def health_check():
    return {
        "status": "online",
        "service": "ALPR Serverless",
        "gemini_configured": bool(GEMINI_API_KEY),
        "supabase_configured": bool(SUPABASE_URL and SUPABASE_SERVICE_KEY),
    }


@app.post("/api/index")
@app.post("/api/recognize_plate")
@app.post("/api/recognize-plate")
@app.post("/")
@app.post("/recognize-plate")
async def recognize_plate(file: UploadFile = File(...)):
    """Extract plate from uploaded image via Gemini, store in Supabase."""

    # Dynamic validation check
    current_gemini_key = os.environ.get("GEMINI_API_KEY", GEMINI_API_KEY)
    current_supabase_url = os.environ.get("SUPABASE_URL", SUPABASE_URL)
    current_supabase_key = os.environ.get("SUPABASE_SERVICE_KEY") or os.environ.get("SUPABASE_SERVICE_ROLE_KEY", SUPABASE_SERVICE_KEY)

    if not current_gemini_key:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured. Please set GEMINI_API_KEY in your .env file or Vercel environment variables.",
        )

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Upload a valid image file (JPEG, PNG, WebP).")

    image_bytes = await file.read()
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    # --- Gemini REST API with Model Fallback ---
    b64_image = base64.b64encode(image_bytes).decode("utf-8")
    gemini_payload = {
        "contents": [{
            "parts": [
                {"text": EXTRACTION_PROMPT},
                {"inline_data": {"mime_type": file.content_type, "data": b64_image}}
            ]
        }]
    }

    plate_text = None
    last_error = None

    async with httpx.AsyncClient(timeout=25) as client:
        for model_name in CANDIDATE_MODELS:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={current_gemini_key}"
            try:
                resp = await client.post(url, json=gemini_payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates and "content" in candidates[0]:
                        parts = candidates[0]["content"].get("parts", [])
                        if parts and "text" in parts[0]:
                            plate_text = parts[0]["text"].strip()
                    if plate_text is None:
                        plate_text = "NONE"
                    break
                else:
                    last_error = f"{model_name} returned {resp.status_code}: {resp.text[:150]}"
            except Exception as exc:
                last_error = f"{model_name} request failed: {exc}"

    if plate_text is None:
        raise HTTPException(status_code=502, detail=f"Gemini API error: {last_error}")

    # --- Supabase REST API ---
    db_success = False
    db_message = ""
    if current_supabase_url and current_supabase_key:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(
                    f"{current_supabase_url}/rest/v1/plate_reads",
                    headers={
                        "apikey": current_supabase_key,
                        "Authorization": f"Bearer {current_supabase_key}",
                        "Content-Type": "application/json",
                        "Prefer": "return=representation",
                    },
                    json={"plate_text": plate_text, "confidence": "gemini-3.5-flash-lite"},
                )
                if resp.status_code in (200, 201):
                    db_success = True
                    db_message = "Record inserted successfully."
                else:
                    db_message = f"Supabase returned {resp.status_code}: {resp.text[:150]}"
        except Exception as exc:
            db_message = f"Supabase error: {exc}"
    else:
        db_message = "Supabase credentials not configured."

    return JSONResponse(content={
        "plate_text": plate_text,
        "db_success": db_success,
        "message": db_message,
    })
