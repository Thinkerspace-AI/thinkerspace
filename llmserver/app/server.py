# Template lifted from langchain examples
# https://github.com/langchain-ai/langserve/blob/main/examples/chat_with_persistence/server.py

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
from langchain_core.runnables.history import RunnableWithMessageHistory

from langserve import add_routes
from langserve.pydantic_v1 import BaseModel, Field

from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory

from typing import List

from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv() # NOTE: OPENAI_API_KEY of .env is on Paolo's machine

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
        db = firestore.Client(project="geometric-sled-417002")
        doc_ref = db.collection("sessions").document(session_id)
        doc_ref.update(
            {"agent": agent}
        )

        return chat_history

    return get_chat_history


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
async def root():
    return {"message": "Pong!"}


class ConvenerRecommendation(BaseModel):
    agent1: str = Field(description="Top 1 priority agent to recommend")
    agent1_reason: str = Field(description="Why you want to recommend agent 1")
    agent2: str = Field(description="Top 2 priority agent to recommend")
    agent2_reason: str = Field(description="Why you want to recommend agent 2")
    agent3: str = Field(description="Top 2 priority agent to recommend")
    agent3_reason: str = Field(description="Why you want to recommend agent 2")

parser = JsonOutputParser(pydantic_object=ConvenerRecommendation)

# Declare a chain

prompt = PromptTemplate(
    template="""You are an agent tasked with recommending three experts to consult on validating a user’s business/startup idea using the Lean Canvas. You have information about each agent’s expertise. Provide your top three recommendations and explain why each agent is suitable for the task.

Agents:
Marketing Specialist: The marketing specialist will help you analyze your target audience, identify market trends, and assess the demand for your product or service. They’ll guide you in crafting effective messaging and positioning strategies to reach potential customers.
UI/UX Designer: The UI/UX designer will focus on enhancing the user experience of your product or app. They’ll ensure that your Lean Canvas translates into an engaging and user-friendly design, optimizing usability, navigation, and aesthetics.
Technical Engineer: The technical engineer will assess the feasibility of your startup idea from a technical standpoint. They’ll advise on the best technologies, scalability, and security measures. Their insights will be crucial for building a robust product.
Product Manager: The product manager plays a critical role in validating business ideas by ensuring alignment with customer needs, market demand, and feasibility. They guide the product development process and help you avoid building something that the market doesn’t need.
Financial Analyst: The financial analyst uses their expertise to validate business ideas, ensuring alignment with financial goals and market realities. Their insights are valuable for entrepreneurs seeking funding or planning strategic moves.

{format_instructions}

{history}

{human_input}""",
    input_variables=["human_input"],
    partial_variables={"format_instructions": parser.get_format_instructions()}
)

chain = prompt | ChatOpenAI(model='gpt-3.5-turbo') | parser


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    # The field extra defines a chat widget.
    # As of 2024-02-05, this chat widget is not fully supported.
    # It's included in documentation to show how it should be specified, but
    # will not work until the widget is fully supported for history persistence
    # on the backend.
    human_input: str = Field(
        ...,
        description="The human input to the chat system.",
        extra={"widget": {"type": "chat", "input": "human_input"}},
    )


chain_with_history = RunnableWithMessageHistory(
    chain,
    create_session_factory("convener"),
    input_messages_key="human_input",
    history_messages_key="history",
).with_types(input_type=InputChat)


add_routes(
    app,
    chain_with_history,
    path="/convene"
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)