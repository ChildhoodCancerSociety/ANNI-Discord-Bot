<h1 align="center">
  Childhood Cancer Society Discord Bot
</h1>

"ANNI" is a Discord bot created for the Childhood Cancer Society non-profit organization to help manage team members in the Childhood Cancer Society Discord Server.

[Gitbook](https://wiki.childhoodcancersociety.dev/)

## ⚙ Features

* Gather progress reports
* Answer common questions from organization members
* Send meeting links at designated times

## 🏛️ Project Structure:
```md
📂 ANNI-Discord-Bot
┃ ┣ 📂 cache            # Local data saved by the bot
┃ ┃ ┣ 📂 GoogleAPI         # API tokens and credentials for Google services (may be removed)
┃ ┃ ┣ 📂 Links             # YAML files for the "link" COG that store meeting link URLs
┃ ┃ ┗ 📂 MemberData        # Server and member data file(s) (created by view COG)
┃ ┣ 📂 config           # Configuration files for COGs
┃ ┣ 📂 cogs             # COG files, which are loaded on startup
┃ ┣ 📂 doc              # Command documentation files. Used by the "help" COG
┃ ┣ 📂 utils            # Python helper scripts for use by COGs
┃ ┃ ┗ 📙 helpers.py        # Main helper file with functions used by COGs
┃ ┣ 📄 requirements.txt # Project dependencies
┗ ┗ 📙 main.py          # Setup file that starts and configures the bot
```

## 📝 Prerequisites:
* Requires `python 3.11`
* Project dependencies are specified in the `requirements.txt` file. 
* This project currently uses YAML to save data to files.

## ✨ Getting Started:
1. Clone the repository:
   - `git clone https://github.com/ChildhoodCancerSociety/ANNI-Discord-Bot`
2. Create a Python virtual environment in the root of the project directory (BASH/UNIX):
   - `python -m venv .venv`
3. Activate the virtual environment (BASH/UNIX):
   - `. .venv/bin/activate`
4. Install any missing dependencies from the requirements.txt file (BASH/UNIX):
   - `.venv/bin/pip install -r requirements.txt`
5. Go to the [Discord Developer Portal](https://discord.com/developers/applications) and create a bot
6. Select the "OAuth2" category and under the "OAuth2 URL Generator" select "Bot", then "Administrator" in the menu that appears underneath
7. Copy the generated URL and paste it into a browser, and select a server to add the bot to
8. In the "Bot" category in the Discord Developer Portal, select "Reset Token" and copy the token
9. Create a `.env` in the root directory and add your bot token using the following format:
   - `token=YOUR_BOT_TOKEN`
10. Start the bot inside of the Python virtual environment:
   - `.venv/bin/python main.py`

## 🪛 General Usage:
The command prefix for this bot is `!`.  
With the bot installed and active, use the `!how` command to list all available commands alongside brief descriptions of their functionality. Instructions can also be found in the `doc` directory.