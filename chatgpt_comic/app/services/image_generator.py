import io, os, re
from pathlib import Path
import httpx
from PIL import Image

BASE_DIR=Path(__file__).resolve().parents[2]
OUT_DIR=BASE_DIR/"static"/"panels"; OUT_DIR.mkdir(parents=True,exist_ok=True)

def _safe_name(text):
    return (re.sub(r"[^a-zA-Z0-9_-]+","_",text).strip("_") or "panel")[:60]

def generate_image(image_prompt, panel_number):
    token=os.getenv("HF_API_KEY")
    if not token: raise RuntimeError("HF_API_KEY is missing. Add a Hugging Face token to .env.")
    model=os.getenv("HF_IMAGE_MODEL","stabilityai/stable-diffusion-xl-base-1.0")
    url=f"https://router.huggingface.co/hf-inference/models/{model}"
    payload={"inputs":image_prompt,"parameters":{"num_inference_steps":25,"guidance_scale":7.0}}
    try:
        with httpx.Client(timeout=180.0) as c: r=c.post(url,headers={"Authorization":f"Bearer {token}"},json=payload)
        r.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Hugging Face image generation failed ({e.response.status_code}): {e.response.text[:800]}") from e
    except Exception as e: raise RuntimeError(f"Could not reach Hugging Face: {e}") from e
    if "image" not in r.headers.get("content-type",""): raise RuntimeError(f"Hugging Face returned non-image data: {r.text[:500]}")
    try:
        image=Image.open(io.BytesIO(r.content)).convert("RGB")
        path=OUT_DIR/f"panel_{panel_number}_{_safe_name(image_prompt[:30])}.png"; image.save(path,"PNG")
    except Exception as e: raise RuntimeError("Image service returned invalid image data.") from e
    return f"/static/panels/{path.name}"
