from agent_app.llm.models import retriever, retrieve_check_llm


def retrieve(state):
    """
    Retrieve documents

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): New key added to state, documents, that contains retrieved documents
    """
    print("---RETRIEVE---")
    question = state["messages"][-1].content

    if retriever is None:
        return {"documents": []}

    documents = retriever.invoke(question)
    return {"documents": [d.page_content for d in documents]}


def check_retrieve(state):
    """
    Classify whether the question requires retrieval.
    Returns:
        state with key: "retrieve" = "retrieve" | "no retrieve"
    """
    question = state["messages"][-1].content

    decision = retrieve_check_llm.invoke({"question": question})

    return {
        "documents": decision
    }

def decide_to_retrieve(state):
    """
    Decide whether to retrieve based on human question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---DECIDE TO RETRIEVE---")
    decide = state["documents"]

    if decide == "retrieve":
        print("Decision: NEED RETRIEVAL")
        return "retrieve"
    else:
        print("Decision: NO RETRIEVAL NEEDED")
        return "generate"
