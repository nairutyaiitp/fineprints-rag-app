import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()  

class FinePrintsExtractor:
    def __init__(self, document_processor, api_key=None):
        self.document_processor = document_processor
        genai.configure(api_key=api_key or os.environ.get("GEMINI_API_KEY"))

        # Configure the model
        generation_config = {
            "temperature": 0.4,
            "top_p": 0.9,
            "top_k": 50,
            #"max_output_tokens": 2048,
            "max_output_tokens": 4096,
        }

        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
            safety_settings=safety_settings
        )

    def extract_fine_prints(self):
        """Extract fine prints from documents."""
        if not self.document_processor.documents:
            self.document_processor.load_documents()

        all_text = "\n\n".join([doc.page_content for doc in self.document_processor.documents])

        prompt = f"""
        I have project documents that I need to analyze for drafting project proposals.

        Please extract the key details (fine-prints) from these documents that are critical for drafting project proposals.
        Focus on:
        1. Project requirements and specifications
        2. Deadlines and timelines
        3. Technical constraints
        4. Deliverables
        5. Assessment criteria

        Here are the documents:
        {all_text}

        Format your response as a structured list of key points, organized by category.
        """

        # prompt = f"""
        # I am analyzing project documents to prepare strong and compliant project proposals.

        # Please extract key fine-print details from the following documents that are essential for drafting accurate proposals. Focus specifically on the following categories:

        # 1. Project requirements and specifications  
        #  List any mandatory tasks, expected scope of work, service details, or compliance standards

        # 2. Deadlines and timelines  
        #  Include submission dates, project milestones, service start/end dates, or inspection schedules

        # 3. Technical constraints  
        #  Mention licensing, equipment requirements, workforce qualifications, environmental or operational limits

        # 4. Deliverables  
        #  Identify all expected outputs including services, documentation, reports, equipment, or training

        # 5. Assessment criteria  
        #  Describe how bids or proposals will be evaluated, including any scoring systems, preferences, or eligibility rules

        # Here are the project documents to analyze:
        # {all_text}

        # Return your response as a clean, structured list of categorized points. The summary should be clear and actionable for use by a proposal drafting team.
        # """


        response = self.model.generate_content(prompt)
        return response.text