from langgraph.graph import StateGraph, START, END
from .state import TeamState
from .nodes.supervisor import supervisor_node
from .nodes.researcher import researcher_node
from .nodes.coder import coder_node

# 1. Initialize the global graph using our robust TypedDict
builder = StateGraph(TeamState)

# 2. Add all autonomous members
builder.add_node("Supervisor", supervisor_node)
builder.add_node("Researcher", researcher_node)
builder.add_node("Coder", coder_node)

# 3. Define the deterministic return edges
# No matter which worker executes, they must ALWAYS hand control back to the manager
for member in ["Researcher", "Coder"]:
    builder.add_edge(member, "Supervisor")

# 4. Define the dynamic routing logic
# The supervisor outputs a dict with the `next` key
builder.add_conditional_edges(
    "Supervisor",
    lambda state: state["next"],
    {
        "Researcher": "Researcher",
        "Coder": "Coder",
        "FINISH": END
    }
)

# 5. Define the entrypoint
builder.add_edge(START, "Supervisor")

# Compile the team
agent_team = builder.compile()
