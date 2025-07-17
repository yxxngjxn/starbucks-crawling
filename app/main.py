from fastapi import FastAPI
from app.merge import merge_beverage_data

app = FastAPI()

@app.get("/beverages")
def get_beverages():
    data = merge_beverage_data()
    return {"data": data}