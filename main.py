from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from prodAI import process_prompt

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/process/")
async def process_content(request: PromptRequest):
    try:
        result = process_prompt(request.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Use environment variable PORT if available, else default to 8000
    uvicorn.run(app, host="0.0.0.0", port=port)
