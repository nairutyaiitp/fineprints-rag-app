import google.generativeai as genai
import numpy as np
from sentence_transformers import SentenceTransformer
import os

class RAGSystem:
    def __init__(self, document_processor, api_key=None):
        self.document_processor = document_processor
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        if api_key:
            genai.configure(api_key=api_key)
        else:
            genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        
        # Configure the generative model
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }
        
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        
        self.gen_model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )
    
    def retrieve(self, query, k=5):
        """Retrieve relevant chunks for a query."""
        # Create query embedding
        query_embedding = self.model.encode([query])[0].reshape(1, -1)
        
        # Search in FAISS index
        distances, indices = self.document_processor.index.search(
            np.array(query_embedding).astype('float32'), k
        )
        
        # Get the relevant chunks
        retrieved_chunks = [self.document_processor.chunks[i] for i in indices[0]]
        return retrieved_chunks
    
    def generate(self, query, retrieved_chunks):
        """Generate response based on query and retrieved chunks."""
        context = "\n\n".join([chunk.page_content for chunk in retrieved_chunks])
        
        prompt = f"""
        You are a proposal assistant designed to help users understand and respond to government-issued procurement documents, including Invitations for Bid (IFB) and Invitations for Price Quote (IFPQ). 

        Use the provided context extracted from these official documents to answer user questions accurately and help them draft compliant project proposals.

        If the answer to the user's question cannot be found in the context, respond clearly that the information is not available.

        Context:
        {context}

        User Question: {query}
        """

        
        response = self.gen_model.generate_content(prompt)
        return response.text
    
    def query(self, user_query):
        """End-to-end RAG pipeline."""
        # Check if documents are processed
        if not hasattr(self.document_processor, 'index') or self.document_processor.index is None:
            self.document_processor.process_documents()
        
        # Retrieve relevant chunks
        retrieved_chunks = self.retrieve(user_query)
        
        # Generate response
        response = self.generate(user_query, retrieved_chunks)
        
        return response