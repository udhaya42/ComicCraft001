import os
from pathlib import Path
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf

BASE_DIR=Path(__file__).resolve().parent.parent
templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))
router=APIRouter()

@router.get("/",response_class=HTMLResponse)
async def home(request:Request): return templates.TemplateResponse("index.html",{"request":request})

async def create_comic(data):
    outline=generate_outline(data.story_prompt,data.character_name,data.setting,data.tone,data.art_style)
    story=generate_story(outline,data.character_name,data.tone)
    images=[generate_image(p["image_prompt"],p["panel_number"]) for p in outline]
    layout=build_comic_layout(outline,story,images)
    return layout,save_pdf(layout)

@router.post("/generate",response_class=HTMLResponse)
async def generate(request:Request,story_prompt:str=Form(...),character_name:str=Form(...),setting:str=Form(...),tone:str=Form(...),art_style:str=Form(...)):
    try:
        data=PromptRequest(story_prompt=story_prompt,character_name=character_name,setting=setting,tone=tone,art_style=art_style)
        layout,pdf_path=await create_comic(data)
        return templates.TemplateResponse("comic_preview.html",{"request":request,"layout":layout,"pdf_path":pdf_path})
    except Exception as e: return templates.TemplateResponse("error.html",{"request":request,"error":str(e)},status_code=500)

@router.post("/generate-comic/json")
async def generate_json(data:PromptRequest):
    try:
        layout,pdf_path=await create_comic(data); return {"success":True,"layout":layout,"pdf_path":pdf_path}
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))

@router.get("/export-success",response_class=HTMLResponse)
async def export_success(request:Request): return templates.TemplateResponse("export_success.html",{"request":request})

@router.post("/test-image")
async def test_image(prompt:str=Form(...)):
    try: return {"success":True,"image_path":generate_image(prompt,0)}
    except Exception as e: raise HTTPException(status_code=500,detail=str(e))

@router.get("/health")
async def health(): return {"status":"ok","gemini_configured":bool(os.getenv("GEMINI_API_KEY")),"huggingface_configured":bool(os.getenv("HF_API_KEY"))}
