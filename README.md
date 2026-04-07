Githubremote

A script to create a remote repository automatically
Uses environment variables and a PAT token stored in a local keepaass database.

Define "KEEPASS_DEV_DB_PATH" as an environment variable for the location where the keppass database is stored.
Define "KEEPASS_ENTRY_TITLE" as an anvironment variabel for the entry where the PAT is stored in KeePass.

The script will ask for KeePass database password and check if it can find the PAT.

After confirming the database and PAT are found the script will check if a remote repository already exists, if not one will be created. The code will be committed and pushed to the remote repository.
