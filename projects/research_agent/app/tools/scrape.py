import requests
from bs4 import BeautifulSoup
from langchain_core.tools import BaseTool, tool
from app.tools.base import BaseAgentTool

@tool
def scrape_webpage(url: str) -> str:
    """
    Scrapes the text content of a given webpage URL.
    Use this to read the details of a link you found during a search.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Use BeautifulSoup to easily extract text and ignore scripts/styles
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        # Return only the first 10000 characters to avoid massive context window blowouts
        return text[:10000]
    except Exception as e:
        return f"Failed to scrape {url}. Error: {str(e)}"

class ScrapeTool(BaseAgentTool):
    """
    A concrete implementation of a web scraping tool to read URLs.
    """
    def get_tool(self) -> BaseTool:
        return scrape_webpage
