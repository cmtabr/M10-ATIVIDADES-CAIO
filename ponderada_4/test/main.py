from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.post("/home", tags=["Test"])
async def login():
    return {"Response": "Hello World"}