from git import Repo
import os

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
        origin = repo.create_remote('origin', remote_url)
    except Exception:
        origin = repo.remotes.origin
    origin.push(refspec='master:master')
    return "Pushed to GitHub."
