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

import agents

load_dotenv() # NOTE: OPENAI_API_KEY of .env is on Paolo's machine

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

@app.get("/create")
async def create_session(
    agent: str, 
    user: str | None = "test",
    root: str | None = None, 
    parent: str | None = None
):
    session_id = uuid.uuid4()
    db = firestore.Client(project="geometric-sled-417002")
    if parent and root:
        new_ref = db.collection("sessions").document(root).collection("children").document(session_id)
        par_ref = db.collection("sessions").document(root).collection("children").document(parent)
        par_ref.update(
            {
                "children": # Update the array of children IDs
            }
        )
    else:
        new_ref = db.collection("sessions").document(session_id)

    new_ref.set(
        {
            "agent": agent,
            "user": user,
            "root": parent,
            "parent": None,
        },
    )


    return {"id": session_id}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)