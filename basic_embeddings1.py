from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from uuid import uuid4
import logging
import json
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vector_store = InMemoryVectorStore(embeddings)

#create some documents
document_1 = Document(
    page_content="I had chocolate chip pancakes and scrambled eggs for breakfast this morning.",
    metadata={"source": "tweet"}
)

#try embedding a json
weather_data = {
    "forecast": "cloudy",
    "max-temperature" : 62
}
document_2 = Document(
    # page_content="The weather forecast for tomorrow is cloudy and overcast, with a high of 62 degrees.",
    page_content = json.dumps(weather_data),
    metadata={"source": "news"}
)

document_3 = Document(
    page_content="Building an exciting new project with LangChain - come check it out!",
    metadata={"source": "tweet"}
)

documents = [document_1, document_2, document_3]

#generate unique uuids that needs to be associated with documents
uuids = [str(uuid4()) for _ in range(len(documents))]

logging.info("adding documents to vector store...")
vector_store.add_documents(documents=documents, ids=uuids)

query = "What's the weather going to be like tomorrow?"
results = vector_store.similarity_search(query, k=1)  # e.g., top 1 match

logging.info(f"results={results[0].page_content}")


