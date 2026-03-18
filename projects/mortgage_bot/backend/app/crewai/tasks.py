def create_mortgage_triage_tasks(agents: dict, query: str, context_bundle: dict):
    from crewai import Task

    intake_task = Task(
        description=(
            "Review the mortgage support question below and produce a short intake summary.\n\n"
            f"User question:\n{query}\n\n"
            "Summarize the issue, identify the likely support category, and note whether a loan identifier is present."
        ),
        expected_output="A concise intake summary with issue type, urgency clues, and whether a loan ID is present.",
        agent=agents["intake_analyst"],
    )

    loan_ops_task = Task(
        description=(
            "Analyze the operational mortgage context below and identify likely blockers.\n\n"
            f"Loan context:\n{context_bundle.get('loan_details')}\n\n"
            f"Open conditions:\n{context_bundle.get('loan_conditions')}\n\n"
            f"Milestone history:\n{context_bundle.get('milestone_history')}\n\n"
            "Explain what appears to be blocking the file and what should happen next operationally."
        ),
        expected_output="An operations-focused explanation of the likely blocker and the next operational step.",
        agent=agents["loan_ops_specialist"],
    )

    guideline_task = Task(
        description=(
            "Review the supporting knowledge context below and identify the most relevant guidance.\n\n"
            f"Knowledge context:\n{context_bundle.get('knowledge_context')}\n\n"
            "Summarize the most useful guidance that supports resolving the issue."
        ),
        expected_output="A concise knowledge summary tied to the issue and likely next action.",
        agent=agents["guideline_researcher"],
    )

    resolution_task = Task(
        description=(
            "Combine the prior agent work into a final mortgage support triage response.\n\n"
            f"Original question:\n{query}\n\n"
            "Write a final summary with:\n"
            "- issue summary\n"
            "- likely blocker\n"
            "- recommended next action\n"
            "- whether a support ticket should stay open or can be resolved"
        ),
        expected_output="A final triage response suitable for support operations review.",
        agent=agents["resolution_writer"],
        context=[intake_task, loan_ops_task, guideline_task],
    )

    return [intake_task, loan_ops_task, guideline_task, resolution_task]
