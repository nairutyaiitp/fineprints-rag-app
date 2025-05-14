from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import os
from fastapi import Request
from fastapi.responses import JSONResponse

from utils.embeddings import DocumentProcessor
from utils.fine_prints import FinePrintsExtractor
from utils.rag import RAGSystem

app = FastAPI(title="Project Proposal Assistant")
templates = Jinja2Templates(directory="templates")

# Initialize components
document_processor = DocumentProcessor(data_dir="./data")
fine_prints_extractor = FinePrintsExtractor(document_processor)
rag_system = RAGSystem(document_processor)

@app.on_event("startup")
async def startup_event():
    document_processor.process_documents()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/select-mode", response_class=HTMLResponse)
async def select_mode(request: Request, mode: str):
    if mode == "summary":
        return templates.TemplateResponse("summary.html", {"request": request})
    elif mode == "chatbot":
        return templates.TemplateResponse("chatbot.html", {"request": request})
    else:
        raise HTTPException(status_code=400, detail="Invalid mode")

class ChatQuery(BaseModel):
    query: str

@app.get("/fine-prints")
async def get_fine_prints():
    try:
        fine_prints = fine_prints_extractor.extract_fine_prints()
        return {"fine_prints": fine_prints}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting fine-prints: {str(e)}")

# @app.post("/chat")
# async def chat(chat_query: ChatQuery):
#     try:
#         response = rag_system.query(chat_query.query)
#         return {"response": response}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

# @app.post("/chat")
# async def chat(request: Request):
#     try:
#         data = await request.json()
#         print("Request Data:", data)  # Debug print

#         user_message = data.get("message", "")
#         print("User Message:", user_message)  # Debug print

#         # Your chatbot logic here
#         #response = my_chatbot_function(user_message)  # Placeholder
#         response = rag_system.query(chat_query.query)
#         return {"response": response}
    
#     except Exception as e:
#         import traceback
#         traceback.print_exc()  # This will print full error in terminal
#         return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        print("Request Data:", data)  # Debug print

        user_message = data.get("query", "")
        print("User Message:", user_message)  # Debug print

        # Replace this:
        # response = rag_system.query(chat_query.query)

        # With this:
        response = rag_system.query(user_message)

        return {"response": response}
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JSONResponse(status_code=500, content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
