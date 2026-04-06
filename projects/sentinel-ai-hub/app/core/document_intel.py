import os
import logging
from typing import Optional
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest, DocumentContentFormat

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentIntelManager:
    def __init__(self, endpoint: Optional[str] = None, key: Optional[str] = None):
        load_dotenv()
        self.endpoint = endpoint or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT")
        self.key = key or os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY")

        if not self.endpoint or not self.key:
            raise ValueError("Azure Document Intelligence credentials missing.")

        self.client = DocumentIntelligenceClient(
            endpoint=self.endpoint, 
            credential=AzureKeyCredential(self.key)
        )

    def extract_markdown(self, file_path: str) -> str:
        """
        Extracts Markdown from a document using the prebuilt-layout model.
        This preserves structural elements like tables and headers.
        """
        logger.info(f"Extracting markdown from {file_path}...")
        
        with open(file_path, "rb") as f:
            poller = self.client.begin_analyze_document(
                "prebuilt-layout",
                AnalyzeDocumentRequest(bytes_source=f.read()),
                output_content_format=DocumentContentFormat.MARKDOWN
            )
            
        result = poller.result()
        logger.info(f"Extraction complete for {file_path}.")
        return result.content

if __name__ == "__main__":
    # Quick test
    try:
        manager = DocumentIntelManager()
        print("Document Intelligence Manager initialized.")
    except Exception as e:
        print(f"Error: {e}")
