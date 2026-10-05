# AURA Connector Documentation Hub

A local website containing a code-native Employee Lifecycle Integration Map, the 30-connector portfolio, and 30 local board briefings. The lifecycle map connects AURA modules, Microsoft 365 services, the integration layer, and Saudi connectors from pre-join through exit or rehire. Portfolio rankings remain separate from the 60% enterprise value / 40% customer-obtainable access launch model.

## Project structure

```text
AURA-Connector-Documentation-Hub/
├── index.html
├── server.py
├── run-local.bat
├── README.md
├── outputs/
│   └── enterprise-phase-one-2026-10-05/
│       └── AURA_Connector_Prioritization_Enterprise_Phase_One_2026-10-05.xlsx
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

Python must be installed for `run-local.bat`. The script supports both the `py` and `python` commands and does not require additional packages.

## Update website data

1. Open `outputs/enterprise-phase-one-2026-10-05/AURA_Connector_Prioritization_Enterprise_Phase_One_2026-10-05.xlsx` in Excel.
2. Edit `Prioritized Connector Register` for connector data. The `Day-one Journeys` sheet remains available through the API for compatibility, but it no longer controls the lifecycle visualization.
3. Save the workbook so Excel stores all recalculated portfolio and enterprise-launch values.
4. Refresh the website in the browser.

The `/api/connectors` response preserves the existing connector fields and adds an `enterpriseLaunch` object to each connector plus a top-level `phaseOne` object. The server rejects missing fields, duplicate journey IDs, invalid launch stages/depths/scores, unresolved connector keys, and formulas without saved results. If a later workbook read fails, the last valid dataset is served with a stale-data warning.

Portfolio rank and score are not recalculated by the website. They remain independent from the enterprise launch index.

The Excel connection requires the local server. Opening `index.html` directly does not load workbook data.

## Publish workbook data to GitHub Pages

GitHub Pages cannot run the Python workbook service. Before publishing workbook changes, regenerate the validated static snapshot:

```bat
python export_static_data.py
```

The website first uses `/api/connectors` locally and automatically falls back to `data/connectors.json` on static hosting. Commit the generated snapshot together with the workbook and website changes.

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
