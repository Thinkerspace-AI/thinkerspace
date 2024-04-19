# Template lifted from langchain examples
# https://github.com/langchain-ai/langserve/blob/main/examples/chat_with_persistence/server.py

from dotenv import load_dotenv

import re
import uuid
from pathlib import Path
from typing import Callable, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field

from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory

from pydantic import BaseModel

import app.agents as agents

class SessionCreation(BaseModel):
    agent: str
    userid: str
    root: str | None = None
    parent: str | None = None

class AgentSelection(BaseModel):
    agents: list
    session_id: str

class AgentsRequest(BaseModel):
    session_id: str

class SaveCompletion(BaseModel):
    session_id: str
    prompt: str
    completion: str

# load_dotenv() # NOTE: OPENAI_API_KEY of .env is on Paolo's machine

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/ping")
async def ping():
    return {"message": "Pong!"}

add_routes(
    app,
    agents.create_convener_chain(),
    path="/convene"
)

add_routes(
    app,
    agents.create_configurable_chain(),
    path="/agent",
)

@app.post("/create", status_code=201)
async def create_session(request: SessionCreation):
    session_id = str(uuid.uuid4())
    db = firestore.Client(project="geometric-sled-417002")
    if request.parent and request.root:
        new_ref = db.collection("sessions").document(request.root).collection("children").document(session_id)
        par_ref = db.collection("sessions").document(request.root).collection("children").document(request.parent)
        par_ref.update(
            {
                "children": firestore.ArrayUnion([session_id]) # Update the array of children IDs
            }
        )
    else:
        new_ref = db.collection("sessions").document(session_id)

    new_ref.set(
        {
            "agent": request.agent,
            "userid": request.userid,
            "root": request.root,
            "parent": request.parent,
        },
    )
    
    return {"id": session_id}

@app.post("/select")
async def select_agents(selection: AgentSelection):
    db = firestore.Client(project="geometric-sled-417002")
    ref = db.collection("sessions").document(selection.session_id)
    ref.set(
        {
            "agents": firestore.ArrayUnion(selection.agents)
        }
    )

@app.post("/getagents")
async def get_agents(selection: AgentsRequest):
    db = firestore.Client(project="geometric-sled-417002")
    ref = db.collection("sessions").document(selection.session_id)
    session_doc = await ref.get()
    try:
        return {"agents": session_doc.to_dict().agents}
    except:
        return HTTPException(status_code=404)

@app.post("/save")
async def save_completion(request: SaveCompletion):
    chat_history = FirestoreChatMessageHistory(
        session_id=request.session_id, collection="SessionHistories"
    )

    await chat_history.add_user_message(request.prompt)
    await chat_history.add_user_message(request.completion)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)