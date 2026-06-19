# import lines
from fastapi import FastAPI
from diary.diary_model import DiaryEntry, load_entries, save_entries

app = FastAPI()


@app.get("/")
def root():
    return {"status": "AI Trading Brain Online"}


@app.get("/health")
def health():
    return {
        "status": "ok",
        "components": {
            "api": "online"
        }
    }


@app.post("/diary")
def create_diary_entry(entry: DiaryEntry):
    entries = load_entries()
    entries.append(entry.model_dump())
    save_entries(entries)
    return {"message": "Diary entry saved!"}


@app.get("/diary")
def get_diary_entries():
    return load_entries()