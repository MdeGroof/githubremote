import os
import subprocess
from github import Github

def run_command(cmd):
    subprocess.run(cmd, check=True)

def main():
    # Ask for info
    token = input("Enter your GitHub Personal Access Token: ").strip()
    repo_name = input("Enter new remote GitHub repository name: ").strip()
    
    # Authenticate with GitHub API
    gh = Github(token)
    user = gh.get_user()

    # Create remote repository
    print(f"Creating remote repository '{repo_name}' …")
    repo = user.create_repo(repo_name)  # Creates repo under your GitHub account
    print(f"Remote repo created: {repo.clone_url}")

    # Initialize local git repo, add files, commit
    print("Initializing local Git repo …")
    run_command(["git", "init"])
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-m", "Initial commit"])

    # Set default branch name to main
    run_command(["git", "branch", "-M", "main"])

    # Add remote and push, inserting the token into the URL
    url_with_token = f"https://{token}@github.com/{user.login}/{repo_name}.git"
    run_command(["git", "remote", "add", "origin", url_with_token])

    print("Pushing code to GitHub …")
    run_command(["git", "push", "-u", "origin", "main"])

    print("Done! 🎉")

if __name__ == "__main__":
    main()
