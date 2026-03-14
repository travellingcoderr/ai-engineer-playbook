from langchain_text_splitters import TextSplitter

class SplitterFactory:
    """
    Factory class to instantiate the correct document text splitter/chunker.
    """
    
    @staticmethod
    def create_splitter(strategy: str, chunk_size: int, chunk_overlap: int) -> TextSplitter:
        """
        Creates and returns a LangChain TextSplitter instance.
        
        Args:
            strategy: 'recursive_character', 'markdown', etc.
            chunk_size: The target max size for every chunk.
            chunk_overlap: Shared characters between consecutive chunks.
        """
        strategy = strategy.lower().strip()
        
        if strategy == "recursive_character":
            try:
                from langchain_text_splitters import RecursiveCharacterTextSplitter
                return RecursiveCharacterTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                    length_function=len
                )
            except ImportError:
                 raise ImportError("Please ensure langchain-text-splitters is installed.")
                 
        elif strategy == "markdown":
            try:
                from langchain_text_splitters import MarkdownTextSplitter
                return MarkdownTextSplitter(
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
            except ImportError:
                 raise ImportError("Please ensure langchain-text-splitters is installed.")
                 
        else:
            raise ValueError(f"Unsupported Splitter strategy: {strategy}")
