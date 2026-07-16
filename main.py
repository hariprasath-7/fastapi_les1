from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return { "status": "success", "message": "My FastAPI app is working!"}
