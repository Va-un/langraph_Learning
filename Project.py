from langgraph.graph import StateGraph, END, START
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, SystemMessage, HumanMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
import os
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from prompts import coder_prompt ,Update_shower_prompt, Update_llm_prompt, saving_prompt
import re

os.environ["GOOGLE_API_KEY"] = "AIzaSyDxvHhOHjLhVkeK0z5tj96KYio2MZDrzpA"

class AgentState(TypedDict):
    messages : Annotated[Sequence[BaseMessage],add_messages]



@tool
def Code_runner(code):
    "Your a code runner you job is to Always  run the code and check if its working or not"
    
    
    try:
        if '```python' in code:
            code = re.search(r'```python\n(.*?)\n```', code, re.DOTALL).group(1)
        output = {}
        exec(code,output)
        
        return f"executed"
    except Exception as e:
        print("aag lagi")
        return f"error{e,code}"

@tool
def file_saver(file_name,code):
    "Your a file saver your work is to save the file ,you are called we agent want to save the file"
    with open(file_name, 'w') as file:
        file.write(code) 
    print(f"Code successfully saved to {file_name}")
    return "Done"

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20").bind_tools([Code_runner,file_saver])

def Input_question(state:AgentState):
    """
    Its and input block"""
    input_message = state["messages"][-1]
    if input_message.content == "filler":
        prommy = input("Ai: What would you like me to do today?\nUser:")
    else :
        prommy = input("User:")
    state["messages"] = list(state["messages"]) + [HumanMessage(content=prommy)]
    return state

def Coder_llm(state:AgentState):
    """
    Main coder job is to write, correct and update the given code
    """
    prompt = coder_prompt
    system_prompt = SystemMessage(content =prompt)
    result = model.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [result]}

def update_shower(state: AgentState):
    prompt =  Update_shower_prompt

    system_prompt = SystemMessage(content =prompt)
    result = model.invoke([system_prompt] + list(state["messages"][-4:]))
    print(result.content) #Asking if updates are required
    prommy = input("User:")
    state["messages"] = list(state["messages"]) + [HumanMessage(content=prommy)]
    return state

def update_llm(state: AgentState):
    prompt = Update_llm_prompt
    
    system_prompt = SystemMessage(content=prompt)
    result = model.invoke([system_prompt] + list(state["messages"][-4:]))
    
    return {"messages": [result]}

def saving_file(state:AgentState):

    prompt = saving_prompt
    system_prompt = SystemMessage(content =prompt)
    print("Ai:Do you want to save the file?")
    prommy = input("User:")
    state["messages"] = list(state["messages"]) + [HumanMessage(content=prommy)]
    result = model.invoke([system_prompt] + list(state["messages"]))
    return {"messages": [result]}

def init_checker(state: AgentState):
    """
    Job is to check if input is code or not if yes to execute else provide it back for input
    """
    last_message = state["messages"][-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "to_tool" 
    else:
        return "to_init"

def code_checker(state: AgentState):
    """
    Job is to check whether the code is executed or not if yes move to updater else move to llm to update and provide and executable code."""
    last_message = state["messages"][-1]
    if last_message.content.startswith("error"):
        return "to_llm"
    if last_message.content.startswith("executed"):
        return "to_updater_Shower"
    return "to_llm"  

def update_checker(state):
    """
    Checks the update_llm response to determine next action
    """
    last_message = state['messages'][-1]
    response = last_message.content.strip()
    

    
    if response == "SAVE_FILE":
        return "to_saving"
    else:
        return "to_coder"

def save_checker(state: AgentState):
    last_message = state["messages"][-1]

    if hasattr(last_message,'tool_calls') and last_message.tool_calls:
        print("last_message.tool_calls")
        return "SAVED"
    if last_message == "COMPLETED":
        return "COMPLETED"
    else:
        return "SAVED"
    



app = StateGraph(AgentState)
app.add_node("coder_llm",Coder_llm)
app.add_node("Input_question",Input_question)
app.add_node("update_shower",update_shower)
app.add_node("update_llm",update_llm)
app.add_node("saving_file",saving_file)

tool_node = ToolNode(tools=[Code_runner])
app.add_node("init_coder", tool_node)

save_node = ToolNode(tools=[file_saver])
app.add_node("File_saved", save_node)


app.add_edge(START ,'Input_question')
app.add_edge('Input_question','coder_llm')
app.add_conditional_edges('coder_llm',init_checker ,{
    'to_tool' : "init_coder",
    'to_init' : "Input_question",

} )
app.add_conditional_edges('init_coder',code_checker ,{
    'to_llm' : "coder_llm",
    'to_updater_Shower' : "update_shower"
} )
app.add_edge("update_shower",'update_llm')
app.add_conditional_edges('update_llm',update_checker,{
    'to_saving' : "saving_file",
    'to_coder' : "coder_llm"
})
app.add_conditional_edges('saving_file',save_checker,{
    'SAVED' : "File_saved",
    'COMPLETED' : END
})
app.add_edge("saving_file","File_saved")
app.add_edge("File_saved",END)


app =app.compile()


from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))
#result = app.invoke({'messages': "filler"})

    