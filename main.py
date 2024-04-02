from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from prodAI import process_prompt

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/process/")
async def process_content(request: PromptRequest):
    try:
        result = process_prompt(request.prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
