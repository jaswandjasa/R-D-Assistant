from crewai import Crew, Task
from agents.researcher import ResearcherAgent
from agents.coder import CoderAgent
from agents.manager import ManagerAgent

class AssistantCrew:
    def __init__(self):
        # Initialize conversation history
        self.conversation_history = []

        self.task = Task(
            description="Understand the user's request and guide the coder to build the project. Use the conversation history for context: {history}",
            agent=ManagerAgent
        )

        self.crew = Crew(
            agents=[ManagerAgent, ResearcherAgent, CoderAgent],
            tasks=[self.task],
            verbose=True
        )

    def run(self, prompt):
        # Add the user's prompt to the history
        self.conversation_history.append({"role": "user", "content": prompt})

        # Format the history for the task
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])

        # Update the task description with the history
        self.task.description = self.task.description.format(history=history_str)

        # Run the crew
        result = self.crew.kickoff(user_input=prompt)

        # Add the assistant's response to the history
        self.conversation_history.append({"role": "assistant", "content": result})

        return result

    def get_history(self):
        return self.conversation_history