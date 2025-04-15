import docker
import os
import pickle
from typing import Tuple, List, Dict, Any

class CodeExecutor:
    def __init__(self, container_name: str = "rd-assistant-code-server"):
        self.client = docker.from_client()
        self.container_name = container_name
        self.state_file = "/home/coder/project/executor_state.pkl"
        try:
            self.container = self.client.containers.get(container_name)
        except docker.errors.NotFound:
            raise Exception(f"Container {container_name} not found. Ensure Code Server is running.")

    def install_dependencies(self, libraries: List[str]) -> str:
        if not libraries:
            return "No dependencies to install."

        try:
            lib_string = " ".join(libraries)
            install_cmd = f"pip3 install {lib_string}"
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

    def save_state(self, state: Dict[str, Any]) -> str:
        """
        Save the state (variables) to a file in the container.
        """
        try:
            # Serialize the state to a local file
            with open("executor_state.pkl", "wb") as f:
                pickle.dump(state, f)

            # Copy the file to the container
            copy_cmd = f"cp executor_state.pkl {self.state_file}"
            os.system(f"docker cp executor_state.pkl {self.container_name}:{self.state_file}")

            # Clean up the local file
            os.remove("executor_state.pkl")
            return "State saved successfully."
        except Exception as e:
            return f"Failed to save state: {str(e)}"

    def load_state(self) -> Dict[str, Any]:
        """
        Load the state (variables) from the container.
        Returns an empty dict if no state exists.
        """
        try:
            # Copy the state file from the container to the host
            copy_cmd = f"docker cp {self.container_name}:{self.state_file} executor_state.pkl"
            os.system(copy_cmd)

            # Load the state
            with open("executor_state.pkl", "rb") as f:
                state = pickle.load(f)

            # Clean up the local file
            os.remove("executor_state.pkl")
            return state
        except Exception as e:
            # If the file doesn't exist or there's an error, return an empty dict
            return {}

    def execute_python_code(self, code: str, filename: str = "temp_script.py", dependencies: List[str] = None) -> Tuple[str, str]:
        try:
            # Install dependencies if specified
            if dependencies:
                install_result = self.install_dependencies(dependencies)
                if "Failed" in install_result or "Error" in install_result:
                    return "", install_result

            # Load the previous state
            state = self.load_state()

            # Write the state to a file so the script can load it
            state_code = "import pickle\n"
            state_code += f"with open('{self.state_file}', 'rb') as f:\n"
            state_code += "    state = pickle.load(f)\n"
            for var_name, var_value in state.items():
                state_code += f"{var_name} = state.get('{var_name}')\n"

            # Combine the state loading with the user's code
            full_code = state_code + "\n" + code

            # Add code to save the state at the end
            full_code += "\n\n# Save the state\n"
            full_code += "new_state = {}\n"
            full_code += "for var in dir():\n"
            full_code += "    if not var.startswith('__'):\n"
            full_code += "        new_state[var] = eval(var)\n"
            full_code += f"with open('{self.state_file}', 'wb') as f:\n"
            full_code += "    pickle.dump(new_state, f)\n"

            # Write the code to a file in the container's project directory
            sandbox_path = f"/home/coder/project/{filename}"
            escaped_code = full_code.replace("'", "'\\''")
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