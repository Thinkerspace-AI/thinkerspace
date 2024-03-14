from dotenv import load_dotenv

import re
from pathlib import Path
from typing import Callable, Union

from fastapi import HTTPException
from langchain_openai import ChatOpenAI
from langchain.memory import FileChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory, Runnable

from langserve.pydantic_v1 import BaseModel, Field

from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory

from typing import List, Dict

from langchain.prompts import PromptTemplate, load_prompt
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

from agentutils import load_agent_options

load_dotenv() # NOTE: OPENAI_API_KEY of .env is on Paolo's machine


### AGENT OUTPUT PARSE FORMATS ###

class ConvenerRecommendation(BaseModel):
    agents: List[str] = Field(description="Top 3 agents you want to recommend")
    reasons: List[str] = Field(description="Reasons why you recommend each of them from 1 to 3")


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
            session_id=session_id, collection="SessionHistories"
        )

        return chat_history

    return get_chat_history


### CONVENER CHAIN ###

def create_convener_chain() -> RunnableWithMessageHistory:
    root_dir = Path(__file__).resolve().parent
    parser = JsonOutputParser(pydantic_object=ConvenerRecommendation)

    prompt = load_prompt(root_dir / "prompts/convener.json")
    prompt = prompt.partial(format_instructions=parser.get_format_instructions())

    chain = prompt | ChatOpenAI(model='gpt-3.5-turbo') | parser
    chain_with_history = RunnableWithMessageHistory(
        chain,
        create_session_factory("convener"),
        input_messages_key="human_input",
        output_messages_key="agents",
        history_messages_key="history",
    )
    return chain_with_history

def create_configurable_chain() -> RunnableWithMessageHistory:
    prompt = PromptTemplate(
        template="Evaluate the business idea.\n{history}\n{human_input}",
        input_variables=[
            "human_input",
            "history"
        ]
    ).configurable_fields(
        template=load_agent_options()
    )

    chain = prompt | ChatOpenAI(model='gpt-3.5-turbo')
    chain_with_history = RunnableWithMessageHistory(
        chain,
        create_session_factory("configurable"),
        input_messages_key="human_input",
        history_messages_key="history",
    )

    return chain_with_history

if __name__ == '__main__':
    create_configurable_chain()