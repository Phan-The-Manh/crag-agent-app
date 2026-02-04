from typing import List
from typing_extensions import Annotated 
from langchain.messages import AnyMessage
import operator

from typing_extensions import TypedDict


class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        messages: list of messages
        web_search: whether to add search
        documents: list of documents
    """

    messages : Annotated[List[AnyMessage], operator.add]
    web_search: str
    documents: List[str]