from agent_app.llm.models import question_rewriter

def transform_query(state):
    """
    Transform the query to produce a better question.

    Args:
        state (dict): The current graph state

    Returns:
        state (dict): Updates question key with a re-phrased question
    """

    print("---TRANSFORM QUERY---")
    question = state["messages"][-1].content

    # Re-write question
    better_question = question_rewriter.invoke({"question": question})
    return {"web_search": better_question}