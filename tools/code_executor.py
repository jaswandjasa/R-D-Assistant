import docker
import os
from typing import Tuple

class CodeExecutor:
    def __init__(self, container_name: str = "rd-assistant-code-server"):
        self.client = docker.from_client()
        self.container_name = container_name
        try:
            self.container = self.client.containers.get(container_name)
        except docker.errors.NotFound:
            raise Exception(f"Container {container_name} not found. Ensure Code Server is running.")

    def execute_python_code(self, code: str, filename: str = "temp_script.py") -> Tuple[str, str]:
        """
        Execute Python code in the Code Server container.
        Returns (stdout, stderr).
        """
        try:
            # Write the code to a file in the container's project directory
            sandbox_path = f"/home/coder/project/{filename}"
            write_cmd = f"echo '{code}' > {sandbox_path}"
            self.container.exec_run(f"sh -c \"{write_cmd}\"", user="coder")

            # Execute the file with Python
            exec_cmd = f"python3 {sandbox_path}"
            exec_result = self.container.exec_run(
                exec_cmd,
                user="coder",
                stdout=True,
                stderr=True
            )

            stdout = exec_result.output.decode("utf-8") if exec_result.output else ""
            stderr = stdout if exec_result.exit_code != 0 else ""

            # Clean up the temporary file
            self.container.exec_run(f"rm {sandbox_path}", user="coder")

            return stdout, stderr
        except Exception as e:
            return "", f"Execution failed: {str(e)}"

# Example usage
if __name__ == "__main__":
    executor = CodeExecutor()
    sample_code = """
print("Hello from the sandbox!")
x = 5 + 3
print(f"Result: {x}")
    """
    stdout, stderr = executor.execute_python_code(sample_code)
    print("Output:", stdout)
    print("Error (if any):", stderr)