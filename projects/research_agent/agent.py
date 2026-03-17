
def run(topic: str) -> str:
    """
    Kicks off the autonomous multi-step research agent.
    
    Args:
        topic: The broad subject you want the agent to search and report on.
        
    Returns:
        The final markdown research report as a string.
    """
    # Delay import until execution so module-level dependencies are ready
    from app.agent.graph import create_research_graph
    
    workflow = create_research_graph()
    
    # Initialize the LangGraph State dictionary
    initial_state = {
        "topic": topic,
        "messages": [],
        "loop_count": 0,
        "final_report": ""
    }
    
    # Run the graph until END is reached
    print(f"Starting autonomous research on: {topic}")
    result = workflow.invoke(initial_state)
    
    return result.get("final_report", "Research failed to produce a final report.")
