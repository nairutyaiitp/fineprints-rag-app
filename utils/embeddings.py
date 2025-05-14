from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import os
import numpy as np

class DocumentProcessor:
    def __init__(self, data_dir="./data"):
        self.data_dir = data_dir
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents = []
        self.chunks = []
        self.embeddings = None
        self.index = None
        
    def load_documents(self):
        """Load PDF documents from data directory."""
        self.documents = []
        for filename in os.listdir(self.data_dir):
            if filename.endswith('.pdf'):
                file_path = os.path.join(self.data_dir, filename)
                loader = PyPDFLoader(file_path)
                self.documents.extend(loader.load())
        return self.documents
    
    def split_documents(self):
        """Split documents into chunks."""
        self.chunks = self.text_splitter.split_documents(self.documents)
        return self.chunks
    
    def create_embeddings(self):
        """Create embeddings for text chunks."""
        texts = [chunk.page_content for chunk in self.chunks]
        self.embeddings = self.model.encode(texts)
        return self.embeddings
    
    def create_faiss_index(self):
        """Create FAISS index from embeddings."""
        dimension = self.embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(self.embeddings).astype('float32'))
        return self.index
    
    def process_documents(self):
        """Process documents end to end."""
        self.load_documents()
        self.split_documents()
        self.create_embeddings()
        self.create_faiss_index()
        return self.index, self.chunks