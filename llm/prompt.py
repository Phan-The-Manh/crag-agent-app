from langchain_core.prompts import ChatPromptTemplate


grade_system = """You are a grader assessing relevance of a retrieved document to a user question. \n 
    If the document contains keyword(s) or semantic meaning related to the question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."""
grade_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", grade_system),
        ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
    ]
)

llm_prompt = ChatPromptTemplate.from_template(
"""You are a helpful RAG assistant. Answer the user's question using the provided context.

## Context (use this as your primary source)

{context}

## Conversation history (for follow-ups and references)

{history}

## User question

{question}

## Instructions

- Base your answer on the context above. Quote or paraphrase from it when possible.
- If the context clearly contains the answer, give a direct, concise response.
- If the context is related but does not contain the answer, say: "The context doesn't contain enough information to answer that."
- Do not invent facts or add information not in the context.

## Answer

""")

rewrite_system = """You a question re-writer that converts an input question to a better version that is optimized \n 
     for web search. Look at the conversational history and input and try to reason about the underlying semantic intent / meaning."""
rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rewrite_system),
        (
            "human",
            "Here is the initial question: \n\n {question} \n Formulate an improved question.",
        ),
    ]
)

retrieve_prompt = ChatPromptTemplate.from_template(
    """
You are a precision router for a retrieval-augmented generation system.

### Task:
Analyze the user's question and determine if it requires external document retrieval.

### Routing Rules:
- Output "retrieve" if the question:
- Requires specific facts, internal data, or technical documentation.
- Asks about product features, company policies, or detailed "how-to" instructions.
- Mentions names, specific entities, or complex data points that require accuracy over intuition.

- Output "no retrieve" if the question:
- Is a greeting, farewell, or social pleasantry (e.g., "Hello", "Thanks").
- Is a meta-comment about the conversation (e.g., "Can you speak louder?", "Who are you?").

### Constraints:
- Your response must be EXACTLY one of these two strings: "retrieve" or "no retrieve".
- Do not provide any explanation, punctuation, or additional text.
- If you cannot determine the answer, default to "retrieve".

Question:
{question}

Answer:
"""
)

general_prompt = ChatPromptTemplate.from_template(
            """
You are a helpful and concise assistant.

Use the conversation history to understand references.
Answer the question using general knowledge.

Conversation History:
{history}

Question:
{question}

Answer:
"""
)