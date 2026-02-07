from langchain_core.messages import AIMessage, HumanMessage
from agent_app.llm.models import rag_chain, general_chain


def _format_history(messages):
    """Convert message list to readable string for the prompt."""
    lines = []
    for m in messages:
        role = "Human" if isinstance(m, HumanMessage) else "Assistant"
        lines.append(f"{role}: {m.content}")
    return "\n".join(lines) if lines else "None"


def generate(state):
    """
    Generate answer based on whether context documents are available.

    Args:
        state (dict): The current graph state.

    Returns:
        dict: Updated state with new AI message appended to messages.
    """
    print("---GENERATE---")

    messages = state["messages"]
    question = messages[-1].content
    raw_docs = state.get("documents")
    # Only use list of docs for RAG; check_retrieve stores decision string
    documents = raw_docs if isinstance(raw_docs, list) and raw_docs else None

    # Format history and context as readable strings for the LLM
    history_str = _format_history(messages[:-1])

    if documents:
        context_str = "\n\n---\n\n".join(documents)
        generation = rag_chain.invoke({
            "history": history_str,
            "context": context_str,
            "question": question
        })
    else:
        generation = general_chain.invoke({
            "history": history_str,
            "question": question
        })

    # 🔑 Append AI response to messages
    new_messages = messages + [AIMessage(content=generation)]

    return {
        "messages": new_messages
    }


def decide_to_generate(state):
    """
    Determines whether to generate an answer, or re-generate a question.

    Args:
        state (dict): The current graph state

    Returns:
        str: Binary decision for next node to call
    """

    print("---ASSESS GRADED DOCUMENTS---")
    web_search = state["web_search"]

    if web_search == "Yes":
        # All documents have been filtered check_relevance
        # We will re-generate a new query
        print(
            "---DECISION: ALL DOCUMENTS ARE NOT RELEVANT TO QUESTION, TRANSFORM QUERY---"
        )
        return "transform_query"
    else:
        # We have relevant documents, so generate answer
        print("---DECISION: GENERATE---")
        return "generate"