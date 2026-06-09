from langchain_community.document_loaders import PyPDFLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS

# -----------------------------
# LOAD PDF
# -----------------------------
loader = PyPDFLoader(
    "knowledge_base/pdfs/company_info.pdf"
)

documents = loader.load()

print(f"\nLoaded {len(documents)} pages")

# -----------------------------
# SPLIT TEXT
# -----------------------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

docs = text_splitter.split_documents(documents)

print(f"\nCreated {len(docs)} chunks")

# -----------------------------
# CREATE EMBEDDINGS
# -----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# -----------------------------
# CREATE VECTOR DATABASE
# -----------------------------
vectorstore = FAISS.from_documents(
    docs,
    embeddings
)

# -----------------------------
# SAVE DATABASE
# -----------------------------
vectorstore.save_local("faiss_index")

print("\nRAG database created successfully!")