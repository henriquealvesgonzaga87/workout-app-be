from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Poetry e venv manual funcionando!"}
