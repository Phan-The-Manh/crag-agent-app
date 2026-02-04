from langgraph.graph import StateGraph, START, END
from agent_app.graph.graph_state import GraphState
from langgraph.checkpoint.memory import InMemorySaver  
from agent_app.nodes.retrieve import retrieve, check_retrieve, decide_to_retrieve
from agent_app.nodes.grade import grade_documents
from agent_app.nodes.generate import generate, decide_to_generate
from agent_app.nodes.rewrite_question import transform_query
from agent_app.nodes.web_search import web_search

workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("check_retrieve", check_retrieve)  # check retrieve
workflow.add_node("retrieve", retrieve)  # retrieve
workflow.add_node("grade_documents", grade_documents)  # grade documents
workflow.add_node("generate", generate)  # generate
workflow.add_node("transform_query", transform_query)  # transform_query
workflow.add_node("web_search_node", web_search)  # web search

# Build graph
workflow.add_edge(START, "check_retrieve")
# workflow.add_edge(START, "retrieve")
workflow.add_conditional_edges(
    "check_retrieve",
    decide_to_retrieve,
    {
        "retrieve": "retrieve",
        "generate": "generate",
    }
)
workflow.add_edge("retrieve", "grade_documents")
workflow.add_conditional_edges(
    "grade_documents",
    decide_to_generate,
    {
        "transform_query": "transform_query",
        "generate": "generate",
    }
)
workflow.add_edge("transform_query", "web_search_node")
workflow.add_edge("web_search_node", "generate")
workflow.add_edge("generate", END)

# Compile
checkpointer = InMemorySaver()  
app = workflow.compile(checkpointer=checkpointer)

from pprint import pprint
from langchain_core.messages import HumanMessage


inputs ={"messages": [HumanMessage(content="Automatic Prompt Design")]}
config = {
    "configurable": {
        "thread_id": "user-1"   # any stable ID (user id, session id, etc.)
    }
}


if __name__ == "__main__":
    from pprint import pprint
    from langchain_core.messages import HumanMessage

    inputs = {"messages": [HumanMessage(content="Hello, can you help me with AI?")]}
    config = {"configurable": {"thread_id": "user-1"}}

    for output in app.stream(inputs, config=config):
        for key, value in output.items():
            pprint(f"Node '{key}':")
        pprint("\n---\n")

    pprint(value["messages"][-1].content)
