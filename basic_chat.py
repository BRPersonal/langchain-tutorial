from langchain_groq import ChatGroq
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env
llm = ChatGroq(model="llama-3.3-70b-versatile")

system_message ={"role": "system", "content": "You are a helpful assistant."}
user_message = {"role": "user", "content": "Hi, my name is Krishna."}
messages=[system_message,user_message]

response = llm.invoke(messages)
print(response.content)

