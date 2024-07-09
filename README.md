# ArcadeAutomation
This was created to automate the commit process for Arcade and automatically commits code to GitHub and runs slack commands for users every hour.
To commit, I use the command line and the following commands:
    git init
    (for each file less than 100MB) git add <filename>
    git commit -m "<user message>"
    git branch -M main
    git remote add origin <origin>
    git push -u origin main

Program assumes you have pip/pip3 to install all libraries. Also, /. makes program ignore that path.