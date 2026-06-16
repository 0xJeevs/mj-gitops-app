from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World from MJ's GitOps App!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
