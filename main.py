import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
import tracing
from team import run_team

app = FastAPI()
run_lock = threading.Lock()

class Topic(BaseModel):
    topic: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/app")
def frontend():
    return FileResponse("static/index.html")

@app.post("/run")
def run(t: Topic):
    with run_lock:
        report = run_team(t.topic)
        return {"report": report, "trace": list(tracing.events)}