from packages.core.services.llm_factory import LLMFactory


def create_mortgage_triage_agents():
    from crewai import Agent

    intake_llm = LLMFactory.create_llm(
        instrument=True,
        component="crewai",
        operation="intake_analyst",
    )
    loan_ops_llm = LLMFactory.create_llm(
        instrument=True,
        component="crewai",
        operation="loan_ops_specialist",
    )
    guideline_llm = LLMFactory.create_llm(
        instrument=True,
        component="crewai",
        operation="guideline_researcher",
    )
    resolution_llm = LLMFactory.create_llm(
        instrument=True,
        component="crewai",
        operation="resolution_writer",
    )

    intake_analyst = Agent(
        role="Mortgage Intake Analyst",
        goal="Understand the borrower issue, extract the loan context, and frame the support problem clearly.",
        backstory=(
            "You specialize in mortgage support intake. You identify the actual issue, "
            "normalize the wording, and prepare the case for downstream specialists."
        ),
        llm=intake_llm,
        verbose=True,
    )

    loan_ops_specialist = Agent(
        role="Mortgage Loan Ops Specialist",
        goal="Analyze loan status, milestone progression, and open conditions to identify operational blockers.",
        backstory=(
            "You work in mortgage operations and understand loan milestones, conditions, "
            "underwriting blockers, and how to move files forward."
        ),
        llm=loan_ops_llm,
        verbose=True,
    )

    guideline_researcher = Agent(
        role="Mortgage Guidelines Researcher",
        goal="Use relevant knowledge and policy context to support the likely resolution path.",
        backstory=(
            "You are a mortgage knowledge specialist who can connect operational issues "
            "to the most relevant internal guidance and policy context."
        ),
        llm=guideline_llm,
        verbose=True,
    )

    resolution_writer = Agent(
        role="Mortgage Resolution Writer",
        goal="Produce a final triage summary with the issue, likely blocker, and recommended next action.",
        backstory=(
            "You write concise support responses that combine operational facts and guidance "
            "into something an internal support team can act on."
        ),
        llm=resolution_llm,
        verbose=True,
    )

    return {
        "intake_analyst": intake_analyst,
        "loan_ops_specialist": loan_ops_specialist,
        "guideline_researcher": guideline_researcher,
        "resolution_writer": resolution_writer,
    }
