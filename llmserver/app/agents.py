from dotenv import load_dotenv

import re
from pathlib import Path
from typing import Callable, Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_openai import ChatOpenAI
from langchain.memory import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory, Runnable

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field

from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory

from typing import List

from langchain.prompts import PromptTemplate, load_prompt
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv() # NOTE: OPENAI_API_KEY of .env is on Paolo's machine


### AGENT OUTPUT PARSE FORMATS ###

class ConvenerRecommendation(BaseModel):
    agent1: str = Field(description="Top 1 priority agent to recommend")
    agent1_reason: str = Field(description="Why you want to recommend agent 1")
    agent2: str = Field(description="Top 2 priority agent to recommend")
    agent2_reason: str = Field(description="Why you want to recommend agent 2")
    agent3: str = Field(description="Top 2 priority agent to recommend")
    agent3_reason: str = Field(description="Why you want to recommend agent 2")


### AGENT FUNCTIONS ###
    
def _is_valid_identifier(value: str) -> bool:
    """Check if the session ID is in a valid format."""
    # Use a regular expression to match the allowed characters
    valid_characters = re.compile(r"^[a-zA-Z0-9-_]+$")
    return bool(valid_characters.match(value))

def create_session_factory(
    agent: Union[str],
) -> Callable[[str], BaseChatMessageHistory]:
    """Create a session ID factory that creates session IDs from a base dir.

    Args:
        base_dir: Base directory to use for storing the chat histories.

    Returns:
        A session ID factory that creates session IDs from a base path.
    """

    def get_chat_history(session_id: str) -> FileChatMessageHistory:
        """Get a chat history from a session ID."""
        if not _is_valid_identifier(session_id):
            raise HTTPException(
                status_code=400,
                detail=f"Session ID `{session_id}` is not in a valid format. "
                "Session ID must only contain alphanumeric characters, "
                "hyphens, and underscores.",
            )
        chat_history = FirestoreChatMessageHistory(
            session_id=session_id, collection="sessions"
        )
        db = firestore.Client(project="geometric-sled-417002") # Needs fixing
        doc_ref = db.collection("sessions").document(session_id)
        doc_ref.update(
            {"agent": agent}
        )

        return chat_history

    return get_chat_history


### CONVENER CHAIN ###

def create_convener_chain() -> Runnable:
    parser = JsonOutputParser(pydantic_object=ConvenerRecommendation)

    prompt = load_prompt("app/prompts/convener.json")
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())

    chain = prompt | ChatOpenAI(model='gpt-3.5-turbo') | parser

    return chain

if __name__ == '__main__':
    create_convener_chain()