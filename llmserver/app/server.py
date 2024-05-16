# Template lifted from langchain examples
# https://github.com/langchain-ai/langserve/blob/main/examples/chat_with_persistence/server.py

from dotenv import load_dotenv

import re
import uuid
from pathlib import Path
from typing import Callable, Union

from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field

from langchain_core.messages.human import HumanMessage
from langchain_core.messages.ai import AIMessage
from langchain_openai import ChatOpenAI

from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory

from pydantic import BaseModel

import app.agents as agents

class SessionCreation(BaseModel):
    agent: str
    user_id: str
    root: str | None = None
    parent: str | None = None

class AgentSelection(BaseModel):
    agents: list
    user_id: str
    session_id: str

class AgentsRequest(BaseModel):
    user_id: str
    session_id: str

class SaveCompletion(BaseModel):
    user_id: str
    session_id: str
    prompt: str
    completion_agent: str
    completion_message: str # agent: str; message: str
    not_picked_1_agent: str
    not_picked_1_message: str
    not_picked_2_agent: str
    not_picked_2_message: str

class HistoryRequest(BaseModel):
    user_id: str
    session_id: str

class RegisterRequest(BaseModel):
    email: str
    pw_hash: str
    user_id: str | None = None

class LoginRequest(BaseModel):
    email: str
    pw_hash: str

class SessionsRequest(BaseModel):
    user_id: str

# load_dotenv() # NOTE: OPENAI_API_KEY of .env is on Paolo's machine

def _is_session_owner(user_id: str, session_id: str):
    db = firestore.Client(project="geometric-sled-417002")
    sessions = db.collection("users").document(user_id).collection('sessions').stream()
    for session in sessions:
        session: firestore.DocumentSnapshot
        if session_id == session.get('id'):
            return True
        
    return False

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces"
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
    path="/convene",
)

add_routes(
    app,
    agents.create_configurable_chain(),
    path="/agent",
)

@app.post("/create", status_code=201)
async def create_session(request: SessionCreation):
    db = firestore.Client(project="geometric-sled-417002")
    #if not db.collection("users").document(request.user_id).get().exists:
    #    raise HTTPException(404, detail="User not registered")
    
    session_id = str(uuid.uuid4())
    
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
            "user_id": request.user_id,
            "root": request.root,
            "parent": request.parent,
        },
    )

    user_ref = db.collection("users").document(request.user_id).collection("sessions")
    user_ref.add({
        "id": session_id,
        "timestamp": firestore.SERVER_TIMESTAMP 
    })
    
    return {"id": session_id}

@app.post("/select")
async def select_agents(selection: AgentSelection):
    if not _is_session_owner(selection.user_id, selection.session_id):
        raise HTTPException(
            status_code=403,
            detail="User does not own this session"
        )
    db = firestore.Client(project="geometric-sled-417002")
    ref = db.collection("sessions").document(selection.session_id)
    ref.set(
        {
            "agents": firestore.ArrayUnion(selection.agents)
        }
    )

@app.post("/getagents")
async def get_agents(selection: AgentsRequest):
    if not _is_session_owner(selection.user_id, selection.session_id):
        raise HTTPException(
            status_code=403,
            detail="User does not own this session"
        )
    db = firestore.Client(project="geometric-sled-417002")
    ref = db.collection("sessions").document(selection.session_id)
    session_doc = ref.get()
    try:
        return {"agents": session_doc.get('agents')}
    except:
        raise HTTPException(status_code=404)

@app.post("/save")
async def save_completion(request: SaveCompletion):
    if not _is_session_owner(request.user_id, request.session_id):
        raise HTTPException(
            status_code=403,
            detail="User does not own this session"
        )
    chat_history = FirestoreChatMessageHistory(
        session_id=request.session_id, collection="SessionHistories"
    )

    chat_history.add_user_message(request.prompt)
    chat_history.add_ai_message(request.completion_message)

    prompt_entry = {
        'message': request.prompt, 
        'agent': 'user',
        "picked": True,
        "timestamp": firestore.SERVER_TIMESTAMP 
    }
    completion_entry = {
        "agent": request.completion_agent,
        "message": request.completion_message,
        "picked": True,
        'timestamp': firestore.SERVER_TIMESTAMP,
    }

    not_picked_1_entry = {
        "agent": request.not_picked_1_agent,
        "message": request.not_picked_1_message,
        "picked": False,
        'timestamp': firestore.SERVER_TIMESTAMP,
    }

    not_picked_2_entry = {
        "agent": request.not_picked_2_agent,
        "message": request.not_picked_2_message,
        "picked": False,
        'timestamp': firestore.SERVER_TIMESTAMP
    }

    db = firestore.Client(project="geometric-sled-417002")
    complete_history = db.collection("CompleteHistories").document(request.session_id).collection("Messages")

    for entry in [prompt_entry, completion_entry, not_picked_1_entry, not_picked_2_entry]:
        complete_history.add(entry)
    
    # Generate a session title
    llm = ChatOpenAI()
    messages = (
        db.collection("CompleteHistories")
        .document(request.session_id)
        .collection("Messages")
        .order_by('timestamp', direction=firestore.Query.ASCENDING)
        .stream()
    )
    history = " ".join([message.get('message') for message in messages])
    title = llm.invoke(f"Generate a title for this topic: {history}").content

    # Add session title to CompleteHistories
    complete_history = db.collection("CompleteHistories").document(request.session_id)

    complete_history.set(
        {
            "title": title
        },
        merge=True
    )

@app.post("/history")
async def history(request: HistoryRequest):
    if not _is_session_owner(request.user_id, request.session_id):
        raise HTTPException(
            status_code=403,
            detail="User does not own this session"
        )
    db = firestore.Client(project="geometric-sled-417002")

    title = db.collection("CompleteHistories").document(request.session_id).get().get('title')
    entries = []
    messages = (
        db.collection("CompleteHistories")
        .document(request.session_id)
        .collection("Messages")
        .order_by('timestamp', direction=firestore.Query.ASCENDING)
        .stream()
    )
    for message in messages:
        message: firestore.DocumentSnapshot
        entry = {
            'agent': message.get('agent'),
            'message': message.get('message'),
            'picked': message.get('picked')
        }
        entries.append(entry)
    try:
        return {'title': title, 'messages': entries}
    except:
        raise HTTPException(status_code=404)
    
@app.post("/register")
async def register(request: RegisterRequest):
    db = firestore.Client(project="geometric-sled-417002")
    ref = db.collection("users").document(request.email)

    if ref.get().exists:
        raise HTTPException(status_code=403, detail="User is already registered")
    
    if request.user_id == None:
        user_id = str(uuid.uuid4())
    else:
        user_id = request.user_id

    ref.set({
        'user_id': user_id,
        'pw_hash': request.pw_hash
    })

    return {'user_id': user_id}

@app.post("/login")
async def login(request: LoginRequest):
    db = firestore.Client(project="geometric-sled-417002")
    ref = db.collection("users").document(request.email)

    if not ref.get().exists:
        raise HTTPException(status_code=403, detail="User is not registered")
    
    if not request.pw_hash == ref.get().get('pw_hash'):
        raise HTTPException(status_code=401, detail="Wrong password")

    return {'user_id': ref.get().get('user_id')}

@app.post("/getsessions")
async def get_sessions(request: SessionsRequest):
    db = firestore.Client(project="geometric-sled-417002")

    sessions = []
    sessions_ref = (
        db.collection("users")
        .document(request.user_id)
        .collection("sessions")
        .order_by('timestamp', direction=firestore.Query.DESCENDING)
        .stream()
    )
    for session in sessions_ref:
        session: firestore.DocumentSnapshot
        session_id = session.get('id')

        messages = (
            db.collection("CompleteHistories")
            .document(session_id)
            .collection("Messages")
            .where('picked', '==', True)
            .order_by('timestamp', direction=firestore.Query.DESCENDING)
            .limit(1)
            .stream()
        )
        
        title = db.collection("CompleteHistories").document(session_id).get().get('title')
        for message in messages:
            last_message = message

        entry = {
            'session_id': session_id,
            'title': title,
            'last_message': last_message.get('message'),
            'timestamp': last_message.get('timestamp')
        }
        sessions.append(entry)
    try:
        return sessions
    except:
        raise HTTPException(status_code=404)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)