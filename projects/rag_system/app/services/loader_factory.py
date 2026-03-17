import os
from langchain_core.document_loaders import BaseLoader

from packages.core.enums import LoaderStrategy

class LoaderFactory:
    """
    Factory to instantiate the correct document loader based on file type or strategy.
    """

    @staticmethod
    def create_loader(file_path: str, strategy: LoaderStrategy = LoaderStrategy.AUTO) -> BaseLoader:
        """
        Creates and returns a LangChain BaseLoader instance.
        
        Args:
            file_path: The path or URL to the document to be loaded.
            strategy: 'auto' (guess by extension), 'pdf', 'markdown', or 'text'.
        """
        if strategy == LoaderStrategy.AUTO:
            _, ext = os.path.splitext(file_path.lower())
            if ext == ".pdf":
                strategy = LoaderStrategy.PDF
            elif ext in [".md", ".markdown"]:
                strategy = LoaderStrategy.MARKDOWN
            else:
                strategy = LoaderStrategy.TEXT

        if strategy == LoaderStrategy.PDF:
            try:
                from langchain_community.document_loaders import PyPDFLoader
                return PyPDFLoader(file_path)
            except ImportError:
                raise ImportError("Please install pypdf to use the PDF loader.")

        elif strategy == LoaderStrategy.MARKDOWN:
            try:
                from langchain_community.document_loaders import UnstructuredMarkdownLoader
                return UnstructuredMarkdownLoader(file_path)
            except ImportError:
                raise ImportError("Please install unstructured to use the Markdown loader.")

        elif strategy == LoaderStrategy.TEXT:
            try:
                from langchain_community.document_loaders import TextLoader
                return TextLoader(file_path)
            except ImportError:
                raise ImportError("TextLoader is missing.")

        else:
             raise ValueError(f"Unsupported Loader strategy: {strategy}")
