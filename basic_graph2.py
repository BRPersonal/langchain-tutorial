from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from utils.AppConfig import AppConfig

_ = AppConfig()  #we just have to load the env

#define a state schema that holds entire conversation
#we don't need any additional fields here.
#Then why do we need this class?
class MyMessagesState(MessagesState):
    # Inherits from MessagesState, which automatically handles adding messages
    pass

#we need an llm that can remember chat history. Hence we are going for this model
llm = ChatOpenAI(model="gpt-4o")

#define a tool
@tool
def multiply(a: int, b: int) -> int:
    """
    multiply two numbers

    Args:
        a (int): input number 1.
        b (int): input number 2.

    Returns:
        int: the result of multiplying two numbers
    """

    return a * b

@tool
def calculate_discount(price: float, discount_percentage: float) -> float:
    """
    Calculates the final price after applying a discount.

    Args:
        price (float): The original price of the item.
        discount_percentage (float): The discount percentage (e.g., 20 for 20%).

    Returns:
        float: The final price after the discount is applied.
    """
    if not (0 <= discount_percentage <= 100):
        raise ValueError("Discount percentage must be between 0 and 100")

    discount_amount = price * (discount_percentage / 100)
    final_price = price - discount_amount
    return final_price


#create a node that reads the entire conversation
#pass it to llm to generate a response , considering all past messges
#returns new message , so that is appended to the state
def invoke_llm(state: MyMessagesState):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MyMessagesState)
builder.add_node("tool_calling_llm", invoke_llm)
builder.add_edge(START, "tool_calling_llm")
builder.add_edge("tool_calling_llm", END)

# A ToolNode automatically handles executing any tool calls made by the LLM
# Note that node name has to be "tools" . Otherwise, we get exception
builder.add_node("tools", ToolNode([multiply,calculate_discount]))

# Add a conditional edge that uses 'tools_condition', which is pre-built node defined in langgraph
# If the LLM’s response indicates a tool call, it routes to the ToolNode
# Otherwise, it routes to END
# I believe there will be only one ToolNode in a graph that will hold all the tools
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)

builder.add_edge("tools", END)
graph = builder.compile()

print("-------conversation #1")
userInputs = [HumanMessage(content="Hello!")]
messages = graph.invoke({"messages": userInputs})
for m in messages['messages']:
    print(m.content)

print("-------conversation #2")
userInputs = [HumanMessage(content="Multiply 2 and 3")]
messages = graph.invoke({"messages": userInputs})
for m in messages['messages']:
  print(m.content)

print("-------conversation #3")
userInputs = [HumanMessage(content="What is the price of an item that costs $100 after a 20% discount?")]
messages = graph.invoke({"messages": userInputs})
for m in messages['messages']:
  print(m.content)


print("-------conversation #4")
userInputs = [HumanMessage(content="I have an item whose price is calculated as product of 50 and 2.What will be the price of the item after applying 20% discount?")]
messages = graph.invoke({"messages": userInputs})
for m in messages['messages']:
  print(m.content)
