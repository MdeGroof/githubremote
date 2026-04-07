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
    # --- Step 1: Prompt for KeePass master password ---
    kp_path = os.getenv("KEEPASS_DEV_DB_PATH") #input("Enter path to your KeePass database (.kdbx): ").strip()
    print(kp_path)
    master_password = getpass("Enter your KeePass master password: ")

    # Open KeePass database
    try:
        kp = PyKeePass(kp_path, password=master_password)
    except Exception as e:
        print(f"Failed to open KeePass database: {e}")
        return

    # --- Step 2: Retrieve GitHub PAT ---
    entry = kp.find_entries(title=os.getenv("KEEPASS_ENTRY_TITLE"), first=True) #'GitHub-PAT-token-MdeGRoof', first=True)
    if not entry:
        print("GitHub PAT not found in KeePass!")
        return
    github_token = entry.password
    print("GitHub PAT retrieved successfully.")

    # --- Step 3: Prompt for repository info ---
    repo_name = input("Enter new GitHub repository name: ").strip()
    repo_description = input("Enter repository description (optional): ").strip()
    is_private = input("Private repository? (y/n): ").strip().lower() == "y"

    # --- Step 4: Authenticate with GitHub ---
    gh = Github(github_token)
    user = gh.get_user()

    # --- Step 5: Create remote repository ---
    print(f"Creating remote repository '{repo_name}' …")
    repo = user.create_repo(
        name=repo_name,
        description=repo_description,
        private=is_private
    )
    print(f"Remote repo created: {repo.clone_url}")

    # --- Step 6: Initialize local Git repo, add files, commit ---
    print("Initializing local Git repository …")
    run_command(["git", "init"])
    run_command(["git", "add", "."])
    run_command(["git", "commit", "-m", "Initial commit"])
    run_command(["git", "branch", "-M", "main"])

    # --- Step 7: Add remote with token in URL and push ---
    url_with_token = f"https://{github_token}@github.com/{user.login}/{repo_name}.git"
    run_command(["git", "remote", "add", "origin", url_with_token])
    print("Pushing code to GitHub …")
    run_command(["git", "push", "-u", "origin", "main"])

    print("\nAll done! Your code is on GitHub. 🎉")

if __name__ == "__main__":
    main()
