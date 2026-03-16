from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from functools import lru_cache

# Import the shared base configuration from the global package
from packages.core.config import get_config as get_base_config, AppConfig as BaseAppConfig

class AgentConfiguration(BaseSettings):
    max_loops: int = Field(default=5, description="Maximum number of times the agent can loop/search before forcing a final answer")
    system_prompt: str = Field(default="You are an expert market intelligence researcher. You must run searches, read websites, and synthesize a comprehensive markdown report.", description="The core instruction for the agent")

class ToolConfiguration(BaseSettings):
    enabled_tools: List[str] = Field(default=["search", "scrape"], description="The tools the agent is permitted to use")
    search_provider: str = Field(default="tavily", description="The search engine provider to use (e.g., duckduckgo, tavily)")

class ResearchAgentConfig(BaseAppConfig):
    """
    Extends the base shared application configuration with parameters
    specific to the autonomous research agent project.
    """
    agent: AgentConfiguration = AgentConfiguration()
    tools: ToolConfiguration = ToolConfiguration()

@lru_cache()
def get_research_config() -> ResearchAgentConfig:
    """Returns a cached instance of the Research Agent configuration."""
    # First, let the global module load the env vars safely
    get_base_config()
    
    # Now instantiate our extended configuration
    config = ResearchAgentConfig()
    return config
