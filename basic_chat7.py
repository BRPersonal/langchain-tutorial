from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from models.author import Author
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env

llm = ChatGroq(model="llama3-8b-8192")
author_parser = PydanticOutputParser(pydantic_object=Author)

prompt_list = PromptTemplate.from_template(
    template = "Answer the question.\n{format_instructions}\n{question}",
    partial_variables = {"format_instructions": author_parser.get_format_instructions()},
)

prompt_value = prompt_list.invoke({"question": "Give me the books written by Dan Brown"})
response = llm.invoke(prompt_value)

author_x = author_parser.parse(response.content)
print(f"{author_x.name} wrote {author_x.number} books.")
print(author_x.books)
