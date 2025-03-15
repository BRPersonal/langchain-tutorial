from langchain_groq import ChatGroq
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env
llm = ChatGroq(model="llama3-8b-8192")

response = llm.invoke("What is the tallest building in the world?")
print(response.content)