from crewai import Crew, Task
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from agents.manager import ManagerAgent

class AssistantCrew:
    def __init__(self):
        self.task = Task(
            description="Understand the user's request and guide the coder to build the project.",
            agent=ManagerAgent
        )

        self.crew = Crew(
            agents=[ManagerAgent, ResearcherAgent, CoderAgent],
            tasks=[self.task],
            verbose=True
        )

    def run(self, prompt):
        return self.crew.kickoff(user_input=prompt)