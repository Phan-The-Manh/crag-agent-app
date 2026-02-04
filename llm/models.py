from pathlib import Path

from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser
from agent_app.llm.prompt import llm_prompt, grade_prompt, rewrite_prompt, general_prompt, retrieve_prompt
from pydantic import BaseModel, Field
# from dotenv import load_dotenv

# load_dotenv()

# -----------------------------------------------------------------------------
# Vector Store (path relative to package root)
# -----------------------------------------------------------------------------
_agent_root = Path(__file__).resolve().parent.parent
_vector_store_path = str(_agent_root / "vector_store" / "faiss")

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
db = None
retriever = None

if _vector_store_path and Path(_vector_store_path).exists():
    try:
        db = FAISS.load_local(
            _vector_store_path,
            embeddings,
            allow_dangerous_deserialization=True,
        )
        retriever = db.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 2},
        )
    except Exception:
        db = None
        retriever = None


def reload_retriever():
    """Reload the vector store and retriever (e.g. after adding new PDFs)."""
    global db, retriever
    if Path(_vector_store_path).exists():
        try:
            db = FAISS.load_local(
                _vector_store_path,
                embeddings,
                allow_dangerous_deserialization=True,
            )
            retriever = db.as_retriever(
                search_type="similarity",
                search_kwargs={"k": 2},
            )
        except Exception:
            pass


# -----------------------------------------------------------------------------
# LLM and Chains
# -----------------------------------------------------------------------------
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)


class GradeDocuments(BaseModel):
    """Binary score for relevance check on retrieved documents."""

    binary_score: str = Field(
        description="Documents are relevant to the question, 'yes' or 'no'"
    )


structured_llm_grader = llm.with_structured_output(GradeDocuments)
retrieval_grader = grade_prompt | structured_llm_grader

rag_chain = llm_prompt | llm | StrOutputParser()
question_rewriter = rewrite_prompt | llm | StrOutputParser()
general_chain = general_prompt | llm | StrOutputParser()
retrieve_check_llm = retrieve_prompt | llm | StrOutputParser()
