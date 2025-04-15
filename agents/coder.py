from crewai import Agent
from tools.code_executor import CodeExecutor

executor = CodeExecutor()

CoderAgent = Agent(
    role="Coder",
    goal="Generate and refine code based on the project's requirements and research findings",
    backstory="You're an expert Python developer who turns ideas into code, debugging and optimizing on the go and also you are a skilled coder who can write and test Python code in a sandbox.",
    verbose=True,
    tools=[lambda code, deps=None: executor.execute_python_code(code, dependencies=deps)]  # Pass dependencies
)

def generate_code(prompt):
    return f"# Code generated based on: {prompt}\nprint('Hello from the Coder Agent!')"
