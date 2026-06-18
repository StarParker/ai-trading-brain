from fastapi import FastAPI

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