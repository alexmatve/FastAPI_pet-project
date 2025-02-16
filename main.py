from fastapi import FastAPI, Request, status
from router import router as vac_router

# uvicorn main:app --reload
# fastapi dev main.py
app = FastAPI()
app.include_router(vac_router)
