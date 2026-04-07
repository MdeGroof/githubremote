import os
import subprocess
from getpass import getpass
from pykeepass import PyKeePass
from github import Github

def run_command(cmd):
    """Run shell command and print errors if any."""
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}\n{e}")
        exit(1)

def main():
    kp_path = os.getenv("KEEPASS_DEV_DB_PATH")
    print(kp_path)
    master_password = getpass("Enter your KeePass master password: ")

    try:
        kp = PyKeePass(kp_path, password=master_password)
    except Exception as e:
        print(f"Failed to open KeePass database: {e}")
        return

    entry = kp.find_entries(title=os.getenv("KEEPASS_ENTRY_TITLE"), first=True)
    if not entry:
        print("GitHub PAT not found in KeePass!")
        return
    github_token = entry.password
    print("GitHub PAT retrieved successfully.")

    repo_name = input("Enter new GitHub repository name: ").strip()
    repo_description = input("Enter repository description (optional): ").strip()
    is_private = input("Private repository? (y/n): ").strip().lower() == "y"

    gh = Github(github_token)
    user = gh.get_user()

    print(f"Creating remote repository '{repo_name}' …")
    repo = user.create_repo(
        name=repo_name,
        description=repo_description,
        private=is_private
    )
    print(f"Remote repo created: {repo.clone_url}")

    print("Initializing local Git repository …")
    run_command(["git", "init"])
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-m", "Initial commit"])
    run_command(["git", "branch", "-M", "main"])

    url_with_token = f"https://{github_token}@github.com/{user.login}/{repo_name}.git"
    run_command(["git", "remote", "add", "origin", url_with_token])
    print("Pushing code to GitHub …")
    run_command(["git", "push", "-u", "origin", "main"])

    print("\nAll done! Your code is on GitHub. 🎉")

if __name__ == "__main__":
    main()
