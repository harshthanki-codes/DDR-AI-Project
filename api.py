from fastapi import FastAPI
from src.pipeline import run_pipeline
import threading

app = FastAPI()


@app.get("/")
def root():
    return {"message": "DDR AI System is running"}


@app.get("/generate")
def generate_report():
    def run():
        run_pipeline()

    # run in background (non-blocking)
    threading.Thread(target=run).start()

    return {
        "status": "Processing started",
        "output": "output/final_ddr.pdf"
    }