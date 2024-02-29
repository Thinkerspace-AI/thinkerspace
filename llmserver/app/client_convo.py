import uuid
from langserve import RemoteRunnable

chat = RemoteRunnable("http://localhost:8000/openai")
session_id = str(uuid.uuid4())

while True:
    print("Agent: " + chat.invoke({"human_input": input("User: ")}, \
            {'configurable': { 'session_id': session_id}}).content)

