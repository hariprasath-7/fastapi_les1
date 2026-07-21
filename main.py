import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Fruit CRUD API")

# 1. CORS Configuration (Allows your React frontend to connect)
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",  # Create React App default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. In-Memory Database Structure
memory_db = {
    "fruits": []
}

# 3. Pydantic Models for Validation & Serialization
class Fruit(BaseModel):
    id: int
    name: str

class FruitsList(BaseModel):
    fruits: List[Fruit]


# --- CRUD ENDPOINTS FOR FRUITS ---

# CREATE
@app.post("/fruits", response_model=Fruit)
def create_fruit(fruit: Fruit):
    # Check if a fruit with this ID already exists
    if any(f.id == fruit.id for f in memory_db["fruits"]):
        raise HTTPException(status_code=400, detail="Fruit already exists")
    
    memory_db["fruits"].append(fruit)
    return fruit


# READ ALL
@app.get("/fruits", response_model=FruitsList)
def get_fruits():
    return {"fruits": memory_db["fruits"]}


# READ ONE
@app.get("/fruits/{fruit_id}", response_model=Fruit)
def get_fruit(fruit_id: int):
    fruit = next((f for f in memory_db["fruits"] if f.id == fruit_id), None)
    if not fruit:
        raise HTTPException(status_code=404, detail="Fruit not found")
    
    return fruit


# UPDATE
@app.put("/fruits/{fruit_id}", response_model=Fruit)
def update_fruit(fruit_id: int, updated_fruit: Fruit):
    for index, fruit in enumerate(memory_db["fruits"]):
        if fruit.id == fruit_id:
            memory_db["fruits"][index] = updated_fruit
            return updated_fruit
            
    raise HTTPException(status_code=404, detail="Fruit not found")


# DELETE
@app.delete("/fruits/{fruit_id}")
def delete_fruit(fruit_id: int):
    for index, fruit in enumerate(memory_db["fruits"]):
        if fruit.id == fruit_id:
            memory_db["fruits"].pop(index)
            return {"message": "Fruit deleted successfully"}
            
    raise HTTPException(status_code=404, detail="Fruit not found")


# 4. Program Entry Point Execution
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)