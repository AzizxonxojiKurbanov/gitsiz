from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import uvicorn

app = FastAPI()

# CORS – frontdan kelayotgan so‘rovlar uchun ruxsat
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # yoki ["https://www.apteka03.uz"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
async def search(q: str):
    try:
        with open("apteka-web/drug.json", encoding="utf-8") as f:
            drugs = json.load(f)
    except FileNotFoundError:
        return {"error": "Ma'lumotlar fayli topilmadi"}

    q = q.strip().lower()
    results = [
        d for d in drugs if q in d.get("Наименование", "").lower()
    ][:20]  # Faqat 20 ta birinchi mos natija

    return results

if __name__ == "__main__":
    uvicorn.run("search_api:app", host="0.0.0.0", port=8000, reload=True)
