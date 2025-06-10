import random
from typing import Dict, List, TypedDict
from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):
    name: str
    win_number: int
    us_number : int
    win_cond: str
    attempts : int

def greeting_node(state:AgentState):
    state["attempts"] = 0
    state["win_number"] = random.randint(0,10)
    print(state["win_number"])
    state["win_cond"] = "False"
    print(f"Welcome {state['name']} lets begin guess game")
    return state

def user_inp(state:AgentState):
    state["attempts"] += 1
    state["us_number"] = int(input(f"Whats your guess on  you {state['attempts']} attempt?"))
    if state["us_number"] == state["win_number"]:
        state["win_cond"] = "True"
    if state["us_number"] > state["win_number"]:
        print("guess lower")
        state["win_cond"] = "False"   
    if state["us_number"] < state["win_number"]:
        print("guess higher")
        state["win_cond"] = "False"
    return state

def Checker(state:AgentState):
    return state["win_cond"]

graph = StateGraph(AgentState)
graph.add_node("greeting_node",greeting_node)
graph.add_node('user_inp',user_inp)

graph.add_edge(START,'greeting_node')
graph.add_edge('greeting_node','user_inp')
graph.add_conditional_edges('user_inp',Checker,{
    "True": END,
    "False": "user_inp"
})
app = graph.compile()



# Correct initialization
ini = AgentState(
    name="Varun",
    win_number=0,
    us_number=0,
    win_cond="False",
    attempts=0
)

print(app.invoke(ini))