# ComicCraft — AI Comic Story Creator

This is a complete FastAPI/Jinja2 implementation of the supplied ComicCraft specification: 5-panel outline → narration/dialogue → one illustration per panel → preview → PDF export. The supplied document specifies Gemini Flash/Pro and Stable Diffusion; provider model names are configurable because model availability changes over time.

## Windows / VS Code
1. Install Python 3.10+ and VS Code.
2. Open this folder in VS Code.
3. Terminal → New Terminal:
   `python -m venv .venv`
   `.venv\Scripts\activate`
   `python -m pip install --upgrade pip`
   `pip install -r requirements.txt`
4. Copy `.env.example` to `.env`.
5. Add `GEMINI_API_KEY` and `HF_API_KEY`.
6. Run `uvicorn app.main:app --reload`
7. Open `http://127.0.0.1:8000`.
8. API docs: `http://127.0.0.1:8000/docs`.

## API test
POST `/generate-comic/json`:
`{"story_prompt":"A brave fox exploring an enchanted forest","character_name":"Ravi","setting":"Enchanted forest","tone":"Dramatic","art_style":"Comic book"}`

GET `/health` checks whether keys are configured.
