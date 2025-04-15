from crewai import Agent

ManagerAgent = Agent(
    role="Project Manager",
    goal="Understand user intent, coordinate with other agents, and ensure deliverables meet goals",
    backstory="You oversee the R&D process, breaking down requests into steps and assigning tasks to agents.",
    verbose=True
)
