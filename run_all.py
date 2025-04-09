import os
import subprocess
import sys

# Directory of this script / repo
REPO_DIR = os.path.dirname(__file__)

def git_pull():
    print("Pulling latest code from GitHub…")
    subprocess.run(["git", "-C", REPO_DIR, "pull"], check=True)

def install_deps():
    print("Installing dependencies…")
    req = os.path.join(REPO_DIR, "requirements.txt")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", req], check=True)

def optimize():
    print("Running AI‑driven optimization…")
    subprocess.run([sys.executable, os.path.join(REPO_DIR, "optimize.py")], check=True)

def git_commit_and_push():
    print("Committing & pushing updated parameters…")
    subprocess.run(["git", "-C", REPO_DIR, "add", "params.json"], check=True)
    subprocess.run([
        "git", "-C", REPO_DIR, "commit", "-m",
        "chore: auto‑update best strategy parameters"
    ], check=True)
    subprocess.run(["git", "-C", REPO_DIR, "push"], check=True)

if __name__ == "__main__":
    git_pull()
    install_deps()
    optimize()
    git_commit_and_push()
    print("All done! Your strategy and parameters are up to date.")
