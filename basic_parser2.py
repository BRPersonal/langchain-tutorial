from langchain_groq import ChatGroq
from langchain.output_parsers import CommaSeparatedListOutputParser
from langchain_core.prompts import PromptTemplate
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env
llm = ChatGroq(model="llama3-8b-8192")

parser_list = CommaSeparatedListOutputParser()
prompt_list = PromptTemplate.from_template(
    template = "Answer the question.\n{format_instructions}\n{question}",
    partial_variables = {"format_instructions": parser_list.get_format_instructions()},
)

prompt_value = prompt_list.invoke({"question": "List 4 chocolate brands"})
response = llm.invoke(prompt_value)
print(response.content)

returned_object = parser_list.parse(response.content)
print(type(returned_object))
