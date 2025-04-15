import docker
import os
from typing import Tuple, List

class CodeExecutor:
    def __init__(self, container_name: str = "rd-assistant-code-server"):
        self.client = docker.from_client()
        self.container_name = container_name
        try:
            self.container = self.client.containers.get(container_name)
        except docker.errors.NotFound:
            raise Exception(f"Container {container_name} not found. Ensure Code Server is running.")

    def install_dependencies(self, libraries: List[str]) -> str:
        """
        Dynamically install Python libraries inside the container.
        Args:
            libraries: List of library names (e.g., ["numpy", "pandas"])
        Returns:
            Result message (success or error).
        """
        if not libraries:
            return "No dependencies to install."

        try:
            # Construct pip install command
            lib_string = " ".join(libraries)
            install_cmd = f"pip3 install {lib_string}"
            
            # Run the pip install command in the container
            install_result = self.container.exec_run(
                install_cmd,
                user="coder",
                stdout=True,
                stderr=True
            )
            
            if install_result.exit_code == 0:
                return f"Successfully installed: {lib_string}"
            else:
                error = install_result.output.decode("utf-8") if install_result.output else "Unknown error"
                return f"Failed to install dependencies: {error}"
        except Exception as e:
            return f"Error installing dependencies: {str(e)}"

    def execute_python_code(self, code: str, filename: str = "temp_script.py", dependencies: List[str] = None) -> Tuple[str, str]:
        """
        Execute Python code in the Code Server container after installing dependencies.
        Args:
            code: The Python code to execute.
            filename: Temporary file name for the code.
            dependencies: List of required libraries (e.g., ["numpy", "pandas"]).
        Returns:
            (stdout, stderr).
        """
        try:
            # Install dependencies if specified
            if dependencies:
                install_result = self.install_dependencies(dependencies)
                if "Failed" in install_result or "Error" in install_result:
                    return "", install_result

            # Write the code to a file in the container's project directory
            sandbox_path = f"/home/coder/project/{filename}"
            # Escape single quotes in the code to prevent shell injection
            escaped_code = code.replace("'", "'\\''")
            write_cmd = f"echo '{escaped_code}' > {sandbox_path}"
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
import numpy as np
array = np.array([1, 2, 3])
print("Array:", array)
    """
    stdout, stderr = executor.execute_python_code(sample_code, dependencies=["numpy"])
    print("Output:", stdout)
    print("Error (if any):", stderr)