
from google.cloud import firestore
from langchain_google_firestore import FirestoreChatMessageHistory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

print(llm.invoke("testing").content)