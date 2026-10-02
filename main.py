import logging

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from qna import answer_question
from summary_module import summarize_text
from learning_path import get_learning_recommendations
from quiz_module import generate_quiz
from explanation_module import explain_topic

# ── Logging ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-8s │ %(name)s │ %(message)s",
)
logger = logging.getLogger(__name__)

# ── App ─────────────────────────────────────────────────────────────
app = FastAPI(title="EduGenie")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Request model ───────────────────────────────────────────────────
class QuestionRequest(BaseModel):
    question: str


# ── Global error handler ────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )


# ── Routes ──────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={},
    )


@app.post("/qa")
def qa(request: QuestionRequest):
    answer = answer_question(request.question)
    return {"question": request.question, "answer": answer}


@app.post("/explain")
def explain(request: QuestionRequest):
    explanation = explain_topic(request.question)
    return {"topic": request.question, "explanation": explanation}


@app.post("/quiz")
def quiz(request: QuestionRequest):
    quiz_data = generate_quiz(request.question)
    return {"quiz": quiz_data}


@app.post("/summarize")
def summarize(request: QuestionRequest):
    summary = summarize_text(request.question)
    return {"text": request.question, "summary": summary}


@app.post("/learn/recommendations")
def learning_recommendations(request: QuestionRequest):
    recommendations = get_learning_recommendations(request.question)
    return {"topic": request.question, "recommendations": recommendations}