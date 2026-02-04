from langchain_core.documents import Document
from langchain_community.tools import DuckDuckGoSearchRun

web_search_tool = DuckDuckGoSearchRun()


def web_search(state):
    """
    Web search based on the latest human question.

    Returns:
        dict: Updated documents list with appended web result.
    """
    print("---WEB SEARCH---")

    question = state["web_search"]
    documents = state.get("documents", [])

    raw_text = web_search_tool.invoke(question)

    new_doc = Document(
        page_content=raw_text,
        metadata={"source": "duckduckgo", "type": "web"}
    )
    return {
        "documents": documents + [new_doc]
    }
