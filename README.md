# AURA Connector Documentation Hub

A static local website containing the AURA connector landing page and 30 local board briefings. All prioritized connectors now have a local HTML briefing.

## Project structure

```text
AURA-Connector-Documentation-Hub/
├── index.html
├── run-local.bat
├── README.md
└── briefings/
    └── 30 standalone connector briefing files
```

## Run from the F: drive

1. Extract the project ZIP.
2. Move the extracted folder to:

   ```text
   F:\AURA-Connector-Documentation-Hub
   ```

3. Double-click `run-local.bat`.
4. The website will open at:

   ```text
   http://localhost:8080
   ```

5. To stop the local server, return to the command window and press `Ctrl+C`.

Python must be installed for `run-local.bat`. The script supports both the `py` and `python` commands.

## Run without a local server

You can also double-click `index.html`. Search, filters, and briefing links work directly from the folder. Internet access is only required for external source and Google Drive links.

## Upload to GitHub

Create an empty repository on GitHub, then run these commands in Command Prompt:

```bat
F:
cd F:\AURA-Connector-Documentation-Hub
git init
git add .
git commit -m "Initial AURA connector documentation hub"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub details.

## Enable GitHub Pages

1. Open the repository on GitHub.
2. Go to **Settings → Pages**.
3. Under **Build and deployment**, select **Deploy from a branch**.
4. Select the `main` branch and `/ (root)` folder.
5. Save and wait for GitHub to provide the website URL.

No build command, package installation, or framework is required.
