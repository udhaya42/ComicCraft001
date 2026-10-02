import json, os
from google import genai
from google.genai import types

def generate_story(outline, character_name, tone):
    key=os.getenv("GEMINI_API_KEY")
    if not key: raise RuntimeError("GEMINI_API_KEY is missing.")
    client=genai.Client(api_key=key)
    model=os.getenv("GEMINI_STORY_MODEL","gemini-2.5-flash")
    prompt=f"""
Expand this 5-panel outline into polished comic narration.
Main character: {character_name}
Tone: {tone}
Outline: {json.dumps(outline,ensure_ascii=False)}
Return ONLY JSON:
{{"panels":[{{"panel_number":1,"caption":"short ambient caption","narration":"2-4 sentences of narration and/or dialogue"}}]}}
Keep exactly 5 panels and maintain story continuity.
"""
    r=client.models.generate_content(model=model,contents=prompt,
        config=types.GenerateContentConfig(temperature=0.85,response_mime_type="application/json"))
    try: panels=json.loads(r.text)["panels"]
    except Exception as e: raise RuntimeError("Gemini returned invalid story JSON.") from e
    if len(panels)!=5: raise RuntimeError("Gemini did not return exactly 5 story panels.")
    return panels
