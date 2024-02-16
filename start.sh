#!/bin/bash

# Find the Repo (if name is changed this will need to be updated)
REPO=$(find / -name "Website-teams-code" 2>/dev/null)

# Change to the Repo
cd $REPO

# Activate the virtual environment
source .venv/bin/activate

# Begin running the application
python main.py
