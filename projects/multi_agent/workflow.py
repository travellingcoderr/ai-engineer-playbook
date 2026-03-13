
def planner(goal):
    return ["research", "write"]

def run(goal):
    tasks = planner(goal)
    return f"Workflow completed for {goal}: {tasks}"
