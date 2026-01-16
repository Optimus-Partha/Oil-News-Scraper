from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import uvicorn
import os
from scraper import extract_oil_gas_news
from summarizer import summarize_news

app = FastAPI(title="AI News Summarizer")

# Use absolute path for templates directory
template_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=template_dir)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/summary")
async def get_summary():
    try:
        news, links = await extract_oil_gas_news()
        if not news:
            return JSONResponse(
                status_code=400,
                content={"error": "No news data retrieved"}
            )
        summary = await summarize_news(news)
        return JSONResponse({"summary": summary})
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )