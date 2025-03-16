from langchain_groq import ChatGroq
from langchain.output_parsers import DatetimeOutputParser
from langchain_core.prompts import PromptTemplate
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env
llm = ChatGroq(model="llama3-8b-8192")
parser_dateTime = DatetimeOutputParser()

prompt_dateTime = PromptTemplate.from_template(
    template = "Answer the question.\n{format_instructions}\n{question}",
    partial_variables = {"format_instructions": parser_dateTime.get_format_instructions()},
)

prompt_value = prompt_dateTime.invoke({"question": "When was the first iPhone released"})
response = llm.invoke(prompt_value)
print(response.content)

returned_object = parser_dateTime.parse(response.content)
print(type(returned_object))