from fastapi import FastAPI

app = FastAPI(title="Link Saver")


@app.get("/health")
def health_check():
    return {"status": "ok"}