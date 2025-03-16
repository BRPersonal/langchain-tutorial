from typing_extensions import TypedDict
import random
from typing import Literal
from langgraph.graph import StateGraph
from langgraph.graph import START, END


#ensure that a dictionary has specific keys and holds value of
#specific type
class State(TypedDict):
    graph_state: str

#nodes are just python functions that take a state parameter, update it
#and return the modified state. Here we are only returning a dictionary
#that adheres to State typed dictionary

#define node 1
def node_1(state):
    print("---Node 1---")
    return {"graph_state": state['graph_state'] + " AGI"}

#define node 2
def node_2(state):
    print("---Node 2---")
    return {"graph_state": state['graph_state'] + " Achieved!"}

#define node 3
def node_3(state):
    print("---Node 3---")
    return {"graph_state": state['graph_state'] + " Not Achieved :("}


#Note how we specify that this method is going to return
#fixed string literals
def decide_next_node(state) -> Literal["node_2", "node_3"]:
    # Often, we use the state to decide the next node
    user_input = state['graph_state']

    # Here, we randomly split between Node 2 and Node 3
    if random.random() < 0.5:
        # 50% of the time, we return Node 2
        return "node_2"

    # Otherwise, we return Node 3
    return "node_3"

#create a graph
builder = StateGraph(State)

#add nodes to graph
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)

#mark starting node. This will always run first
builder.add_edge(START, "node_1")

#add the conditional edge to connect node_1 to either node_2 or node_3,
# based on the logic we defined in the decide_next_node function.
builder.add_conditional_edges("node_1", decide_next_node)

#mark node2 and node3 as terminal nodes, signalling no further action is required
builder.add_edge("node_2", END)
builder.add_edge("node_3", END)

#compile the graph, to ensure every node is connected correctly, so that there are no orphaned nodes
graph = builder.compile()
print(graph.invoke({"graph_state" : "Has AGI been achieved?"}))





