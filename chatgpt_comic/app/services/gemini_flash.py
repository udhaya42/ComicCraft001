import json, os
from google import genai
from google.genai import types

def _client():
    key = os.getenv("GEMINI_API_KEY")
    if not key: raise RuntimeError("GEMINI_API_KEY is missing. Add it to .env.")
    return genai.Client(api_key=key)

def generate_outline(story_prompt, character_name, setting, tone, art_style):
    client = _client()
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    prompt = f"""
Create exactly 5 connected comic panels.
Story idea: {story_prompt}
Main character: {character_name}
Setting: {setting}
Tone: {tone}
Art style: {art_style}
Return ONLY valid JSON:
{{"panels":[{{"panel_number":1,"title":"short title","scene_description":"visual scene description","image_prompt":"detailed image-generation prompt"}}]}}
Requirements: exactly five panels numbered 1-5; maintain character and setting continuity; image_prompt describes composition, subject, lighting and style; do not put text, speech bubbles, logos, signatures or watermarks in images.
"""
    r=client.models.generate_content(model=model, contents=prompt,
        config=types.GenerateContentConfig(temperature=0.9,response_mime_type="application/json"))
    try: panels=json.loads(r.text)["panels"]
    except Exception as e: raise RuntimeError(f"Gemini returned invalid outline JSON: {(r.text or '')[:500]}") from e
    if len(panels)!=5: raise RuntimeError("Gemini did not return exactly 5 panels.")
    for i,p in enumerate(panels,1):
        p["panel_number"]=i
        for k in ("title","scene_description","image_prompt"):
            if not p.get(k): raise RuntimeError(f"Panel {i} is missing '{k}'.")
    return panels
