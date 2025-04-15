from crewai import Agent

CoderAgent = Agent(
    role="Coder",
    goal="Generate and refine code based on the project's requirements and research findings",
    backstory="You're an expert Python developer who turns ideas into code, debugging and optimizing on the go.",
    verbose=True
)

def generate_code(prompt):
    return f"# Code generated based on: {prompt}\nprint('Hello from the Coder Agent!')"
