from git import Repo
import os
from dotenv import load_dotenv

load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def init_git_repo(repo_path="repo"):
    if not os.path.exists(repo_path):
        os.makedirs(repo_path)
    repo = Repo.init(repo_path)
    return repo

def commit_changes(repo, message="Initial commit"):
    repo.git.add(all=True)
    repo.index.commit(message)
    return f"Committed with message: {message}"

def push_to_github(repo, remote_url):
    try:
        # Ensure the remote URL uses the token for authentication
        if not remote_url.startswith("https://"):
            raise ValueError("Remote URL must be an HTTPS URL (e.g., https://github.com/username/repo.git)")
        
        if not GITHUB_TOKEN:
            raise ValueError("GITHUB_TOKEN not found in .env file")

        # Inject the token into the URL: https://<token>@github.com/username/repo.git
        auth_url = remote_url.replace("https://", f"https://{GITHUB_TOKEN}@")

        try:
            origin = repo.create_remote('origin', auth_url)
        except Exception:
            origin = repo.remotes.origin
            origin.set_url(auth_url)

        origin.push(refspec='main:main')  # Use 'main' branch (GitHub default)
        return "Successfully pushed to GitHub."
    except Exception as e:
        return f"Failed to push to GitHub: {str(e)}"