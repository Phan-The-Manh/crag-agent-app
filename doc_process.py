from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def load_pdf_safely(pdf_path: Path):
    """
    Load PDF using text extraction first, OCR only if needed.
    """
    # Try text-based extraction
    docs = PyPDFLoader(str(pdf_path)).load()

    if any(d.page_content.strip() for d in docs):
        print("📘 Detected text-based PDF (PyPDFLoader)")
        return docs

    # Fallback to OCR
    print("🖼️ No text found — falling back to OCR")
    return UnstructuredPDFLoader(
        str(pdf_path),
        strategy="ocr_only",
        mode="elements"
    ).load()


def store_pdf_to_faiss(
    pdf_path: str,
    vector_store_path: str,
    chunk_size: int = 800,
    chunk_overlap: int = 200,
    embedding_model: str = "text-embedding-3-small"
):
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    # 1️⃣ Load PDF (SYSTEMATIC STEP)
    documents = load_pdf_safely(pdf_path)
    print(f"📄 Loaded {len(documents)} document elements")

    if not documents:
        raise ValueError("PDF loaded but produced no documents")

    # 2️⃣ Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    chunks = splitter.split_documents(documents)

    # OCR hygiene
    chunks = [
        c for c in chunks
        if c.page_content.strip() and len(c.page_content) > 50
    ]

    print(f"✂️ Created {len(chunks)} text chunks")

    if not chunks:
        raise ValueError("No valid text chunks created")

    # 3️⃣ Embeddings
    embeddings = OpenAIEmbeddings(model=embedding_model)

    # 4️⃣ FAISS: delete old index, create new one from current PDF only
    vector_store_dir = Path(vector_store_path).resolve()
    for f in ("index.faiss", "index.pkl"):
        old_file = vector_store_dir / f
        if old_file.exists():
            old_file.unlink()
            print(f"🗑️ Removed old {f}")

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(str(vector_store_dir))

    print(f"✅ Stored new FAISS index at '{vector_store_path}'")
    return db

