# backend/app/api/simple_test.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def simple_test():
    return {"message": "Simple test works!"}

@router.post("/echo")
def echo(data: dict):
    return {"received": data, "message": "Echo successful"}