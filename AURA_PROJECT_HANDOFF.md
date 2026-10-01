# Aura Connectors project handoff

Prepared on 1 October 2026 for continuing the project in GPT Desktop.

## Start here

The project researches and prioritizes enterprise and Saudi integrations for **Aura, a digital employee hub**, and presents the findings through concise executive HTML briefings and a searchable documentation landing page.

The latest direction is a **local Windows project on the F: drive**. The user will upload it to GitHub themselves. **Do not upload, push, publish, or deploy this project on the user's behalf.**

The existing local project has been recovered and inspected for this handoff. It contains **30 connector cards, 16 local HTML briefings, and 14 cards marked as planned**. All 16 local briefing links in `index.html` resolve to included files. This confirms documentation coverage, not production integration readiness. Windows execution, provider connectivity, and browser interaction were not tested during this handoff.

## What to give the next assistant

Upload `AURA_PROJECT_HANDOFF.md` and paste `RESUME_PROMPT.txt`. Provide the local project folder or the full handoff ZIP when file editing is needed. The package contains:

| Item | Purpose |
|---|---|
| `AURA_PROJECT_HANDOFF.md` | Project context, requirements, status, next steps, and links |
| `RESUME_PROMPT.txt` | Ready-to-paste instructions for the next assistant |
| `AURA-Connector-Documentation-Hub/` | Existing local website, preserved unchanged |
| `sources/original/` | The 14 supplied DOCX developer guides and the roadmap HTML |
| `sources/text/` | Text extracted from the DOCX guides for easier reading |
| `references/AURA_Connector_Prioritization_2026-09-29.xlsx` | Original saved workbook snapshot; compare with current Drive version before changing priorities |
| `references/AURA_Connector_Documentation_Hub.html` | Recovered standalone landing-page artifact |
| `references/AURA-Connector-Documentation-Hub.zip` | Original delivered local project ZIP |
| `CONNECTOR_SNAPSHOT.json` | The 30 connector records extracted from the packaged local landing page |
| `MANIFEST.json` | File inventory, sizes, and SHA-256 hashes |

The source texts are reading aids. Preserve the original DOCX files as the authoritative supplied versions, including their tables and payload structure. Earlier conversations, connected Google Drive access, and temporary sandbox paths are not guaranteed to be available in the next session; use the packaged files and recorded links.

## Project scope

Analyze how each connector supports an employee hub, whether the company can actually obtain access, how it would integrate, what blocks delivery, and what commercial terms need confirmation. Do not equate public documentation with production entitlement.

**Enterprise connectors:** SAP S/4HANA; SAP SuccessFactors; Microsoft 365 / Microsoft Graph + Entra; Oracle Fusion ERP / HCM; ServiceNow; Dynamics 365 / Dataverse.

**Saudi and sector connectors:** ZATCA Integration Service; PayTabs; SADAD; NIC; MOI; Ministry of Commerce; MOFA; Tasheer Connect; Nusuk Imtithal / Sahab; CRS; SAR through Masar Integration Gateway; Kidana; Atlas; IATA; SPL National Address; Etimad APIs; Nafath; Qiwa; GOSI; Yaqeen; Muqeem; Mudad; Ajeer; Absher.

This is a **documentation and prioritization project**. The recovered website is static HTML/CSS/JavaScript. The included developer guides describe integrations; their presence does not prove working adapters have been deployed.

## Decisions and requirements to preserve

### Executive briefings

- Clear English for nontechnical executives; simple, short, and to the point.
- Explain what the provider/service is and its value for Aura in the Saudi market.
- Show the workbook score, rank, priority/wave, and relevant access conditions.
- Explain how integration would work, using a small mind map and an integration flow.
- Include official evidence and links, prerequisites, and cost information.
- Distinguish documented capability, internal assumptions, unverified access, and decisions still needed.
- Use the existing design as the reference. The requested visual direction was inspired by [NTGapps](https://ntgapps.com/).
- Do not invent prices, credentials, API access, production approvals, or delivery commitments. Where commercial terms are unavailable, state that a provider quotation or contract confirmation is required.
- The user prefers that images/photos are generated only after asking and receiving explicit agreement. Existing HTML/CSS and diagram content can be maintained without generating imagery.

### Workbook

The master is named `AURA_Connector_Prioritization_2026-09-29`. Earlier work recorded one Priority Score and connector-specific bullet explanations, especially for:

- Use case
- Provider onboarding / commercial
- Prerequisites / blockers
- Recommended integration / data flow
- Access model
- Difficulty drivers

Earlier detailed documents were linked into the workbook. Before editing it, read the current file, preserve its columns/formulas and existing links, and check that the source version is current. The packaged workbook is the saved 29 September snapshot and may predate later Drive edits.

### Local documentation hub

- Keep one landing page connecting all available local HTML briefings.
- Preserve search, filters, connector cards, availability indicators, and source links.
- Use relative local briefing paths such as `briefings/spl-national-address.html`.
- Mark missing HTML briefings as planned, with no misleading active button.
- Keep links to the source workbook and Detailed Documents folder.
- Keep the project suitable for local use and a later GitHub upload by the user.

## Completed work and evidence level

| Work | Status at handoff |
|---|---|
| 30-connector prioritization workbook | Created in earlier work; a saved original snapshot is packaged. Later Drive edits were reported in conversation and need comparison with the current Drive file. |
| Detailed documents for Microsoft Graph + Entra, SAP S/4HANA, and SPL | Creation and workbook linking were recorded in earlier conversation. Exact Microsoft/SAP document links are not available here; find them in the current workbook or Drive folder if needed. |
| 16 HTML executive briefings | Verified as actual files in the recovered local project. |
| Documentation landing page | Verified: 30 connector records, 16 briefing URLs, 14 empty briefing URLs. |
| Windows local project ZIP | Recovered and inspected; includes `index.html`, `briefings/`, `run-local.bat`, and `README.md`. |
| Installation under F: | Requested by user; no evidence in this session that extraction or Windows execution has happened. |
| GitHub upload | Reserved for the user; no upload performed in this handoff. |
| Provider access and live integrations | Not established by this handoff. |

Microsoft Graph and SAP S/4HANA remain **planned HTML cards**, despite earlier detailed documents existing in another format. Do not treat those earlier documents as already packaged HTML briefings.

## Connector coverage and priority snapshot

The following table is copied from the recovered local landing page. It is a project snapshot, not a new scoring exercise or independent validation of the current Drive workbook. Rank is the hub/workbook ordering; scores alone do not explain the ordering because access readiness affects sequencing.

| Rank | Connector | Score | Wave | Local HTML briefing |
|---:|---|---:|---|---|
| 1 | Microsoft 365 / Microsoft Graph + Entra | 85 | 1 - Build | Planned |
| 2 | SAP S/4HANA | 84 | 1 - Build | Planned |
| 3 | SAP SuccessFactors | 84 | 1 - Build | [Available](AURA-Connector-Documentation-Hub/briefings/sap-successfactors.html) |
| 4 | ServiceNow | 82 | 1 - Build | [Available](AURA-Connector-Documentation-Hub/briefings/servicenow.html) |
| 5 | SPL National Address | 75 | 2 - Conditional | [Available](AURA-Connector-Documentation-Hub/briefings/spl-national-address.html) |
| 6 | Oracle Fusion ERP / HCM | 72 | 2 - Conditional | [Available](AURA-Connector-Documentation-Hub/briefings/oracle-fusion-erp-hcm.html) |
| 7 | Dynamics 365 / Dataverse | 70 | 2 - Conditional | [Available](AURA-Connector-Documentation-Hub/briefings/dynamics-365-dataverse.html) |
| 8 | PayTabs | 63 | 2 - Conditional | [Available](AURA-Connector-Documentation-Hub/briefings/paytabs.html) |
| 9 | IATA | 45 | 3 - Demand led | [Available](AURA-Connector-Documentation-Hub/briefings/iata.html) |
| 10 | Nafath | 68 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/nafath.html) |
| 11 | Qiwa | 65 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/qiwa.html) |
| 12 | Etimad APIs | 64 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/etimad-apis.html) |
| 13 | Absher | 56 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/absher.html) |
| 14 | GOSI | 56 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/gosi.html) |
| 15 | Muqeem | 53 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/muqeem.html) |
| 16 | Yaqeen | 53 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/yaqeen.html) |
| 17 | ZATCA Integration Service | 49 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/zatca-integration-service.html) |
| 18 | NIC | 46 | D - Discovery | [Available](AURA-Connector-Documentation-Hub/briefings/nic.html) |
| 19 | Ministry of Commerce | 44 | D - Discovery | Planned |
| 20 | Mudad | 44 | D - Discovery | Planned |
| 21 | SADAD | 44 | D - Discovery | Planned |
| 22 | Ajeer | 41 | D - Discovery | Planned |
| 23 | CRS | 37 | D - Discovery | Planned |
| 24 | SAR through Masar Integration Gateway | 37 | D - Discovery | Planned |
| 25 | MOFA | 34 | D - Discovery | Planned |
| 26 | MOI | 34 | D - Discovery | Planned |
| 27 | Nusuk Imtithal / Sahab | 34 | D - Discovery | Planned |
| 28 | Tasheer Connect | 34 | D - Discovery | Planned |
| 29 | Atlas | 29 | D - Discovery | Planned |
| 30 | Kidana | 29 | D - Discovery | Planned |

## Keep roadmap order separate from workbook rank

The supplied `AURA_Component_Roadmap_Interactive_v2.html` contains an Enterprise & Saudi Connectors section. The original analysis request was to read that section first, then the remaining sources and official documentation.

The roadmap says **SAP S/4HANA is first in enterprise execution**, driven by commercial pipeline. The hub snapshot instead has **Microsoft Graph + Entra at overall rank 1** and **SAP S/4HANA at overall rank 2**. These are different prioritization views; label both clearly rather than silently replacing one with the other.

The roadmap puts **SPL National Address first in Saudi execution**, while the hub gives SPL overall rank 5, score 75, Wave 2 Conditional. Preserve that distinction too.

The roadmap also contains an internal claim that S/4HANA is **35% complete**, an **8–12 week** estimate for its first reusable production-ready pack, and estimates for other tracks. These are source assertions; validate them with the project owner before presenting them as current delivery facts.

The roadmap proposes parallel enterprise build, Saudi open-API, Saudi access/partnership, and connector-platform tracks. This describes the project's delivery model, not an instruction to have the assistant spawn agents.

## Supplied technical sources

Fourteen supplied DOCX files are Java Developer Guides with a stated contract baseline of **28 September 2026**. They describe prerequisites, HTTP contracts, credentials/placeholders, payloads, transport code, and example operations. They refer to owner-provided gateways and approved access, so preserve the distinction between an internal/intermediary contract and a provider's publicly documented API.

| Original filename | Subject |
|---|---|
| `01-zatca.docx` | ZATCA Integration Service |
| `02-paytabs.docx` | PayTabs |
| `03-sadad.docx` | SADAD through ePayment |
| `04-nic.docx` | NIC |
| `05-moi.docx` | MOI Umrah Agent Integration |
| `06-ministry-of-commerce.docx` | Ministry of Commerce |
| `07-mofa.docx` | MOFA External Agent Registration |
| `08-tasheer-connect.docx` | Tasheer Connect |
| `09-nusuk-imtithal-sahab.docx` | Nusuk Imtithal and Sahab |
| `10-crs.docx` | CRS Hotel Search and Reservation |
| `11-sar-masar-gateway.docx` | SAR through Masar Gateway |
| `12-kidana.docx` | Kidana Handover Files |
| `13-atlas.docx` | Atlas Nationalities and Hotels |
| `14-iata.docx` | IATA Agency Code Verification |
| `AURA_Component_Roadmap_Interactive_v2.html` | Roadmap; begin with Enterprise & Saudi Connectors |

Important interpretation points for future research:

- Keep **ZATCA Integration Service via an intermediary** separate from a claim of direct ZATCA Fatoora integration.
- Keep **SAR through Masar Gateway** separate from an assumed direct SAR API.
- Keep the supplied NIC and MOI operations tied to their specific pilgrimage/agent/permit workflows; do not generalize them into unrestricted national services.
- Resolve ambiguous provider identities such as CRS and Atlas before claiming public API availability.
- For Dynamics 365 / Dataverse, confirm the customer's actual product and environment; do not assume every Dynamics product uses the same API or permissions.
- Recheck official provider documentation and commercial access before new technical or pricing claims. This handoff preserves existing research; it does not refresh all official sources.

## Key reference links

- [Detailed Documents folder](https://drive.google.com/drive/folders/1Yc6D6niwYnjmWIzRFgLP1OfVVcR03-OZ)
- [Prioritization workbook on Drive](https://drive.google.com/file/d/1-e-GRxaLLD3P52Wz7h3Hgk3ZQEXOGCOh/view)
- [SPL National Address API catalogue](https://nationaladdressapis.developer.azure-api.net/apis)
- [NTGapps design reference](https://ntgapps.com/)

The following briefing URLs were supplied in the project context. They are recorded for navigation; the Drive contents and sharing permissions were not reread in this handoff. The local files packaged here provide the transferable versions. HTML opened through Drive preview may show source/preview behavior rather than run as a normal website; use the local HTML pages to read the briefings.

- [ZATCA Integration Service briefing](https://drive.google.com/file/d/1ui2E1Gyo-K4fsijSxvWrws19tGT76pp-/view)
- [PayTabs briefing](https://drive.google.com/file/d/1XKayVBDJXiZI8OLNimyj4RJvV2U6X8P0/view)
- [NIC briefing](https://drive.google.com/file/d/15NFfIWYR3sGt75NAeEkruCNtgRnEsffy/view)
- [IATA CheckACode briefing](https://drive.google.com/file/d/1reeiJAFeq3zlUNOO46vYET7uzQVUk3xk/view)
- [SPL National Address briefing](https://drive.google.com/file/d/17Y7vdCCpSnlP8JczJJjIt3JFHPvKe-sT/view)
- [Etimad APIs briefing](https://drive.google.com/file/d/1tbFCNpsYlUWDRgc-LL8J7wkmeQblDPkm/view)
- [Nafath briefing](https://drive.google.com/file/d/1Wr0bjVeNLa-MYhPB_GzKoRtBLFwmWV08/view)
- [Qiwa briefing](https://drive.google.com/file/d/1EI6jSbAIl8fn6hMzzsoHl7xffcADgbC0/view)
- [GOSI briefing](https://drive.google.com/file/d/1Yuo71YlHHdnLJNnolJnoOWdsnKPfvDzv/view)
- [Yaqeen briefing](https://drive.google.com/file/d/1RYfpUQtr3JFeNaF_w8YkHj_YXlbVkoOV/view)
- [Muqeem briefing](https://drive.google.com/file/d/1QjGFM55WRC73Tl9wSK42te4w9dus1kY6/view)
- [Absher briefing](https://drive.google.com/file/d/1VUYSnFNSFztAia0C3_B3tUfkXWnHd7Zh/view)
- [SAP SuccessFactors briefing](https://drive.google.com/file/d/1vKg-Buf4UOtstiKmbvNGIAr8VO8q6YDF/view)
- [Oracle Fusion ERP / HCM briefing](https://drive.google.com/file/d/1NnBRndkoO7A7RAqhD_PDa97bx8TDuiiE/view)
- [ServiceNow briefing](https://drive.google.com/file/d/1TSOMj03QhS8yMVIagU4Oxp0DkMOE8vC3/view)

The Dynamics 365 / Dataverse HTML is included locally as `briefings/dynamics-365-dataverse.html`; an exact standalone Drive URL was not provided. Official evidence links are embedded in the briefing pages.

## Run the existing project on Windows

Use the existing project at:

```text
F:\AURA-Connector-Documentation-Hub
```

If the user extracts this whole handoff to another folder, copy its `AURA-Connector-Documentation-Hub` subfolder to that location, or run it where extracted. No installation path is hardcoded in the launcher.

1. Double-click `run-local.bat` in the project folder.
2. The supplied script looks for `py` or `python` and serves the folder at `http://localhost:8080`.
3. Press `Ctrl+C` in its command window to stop it.
4. The supplied README also supports opening `index.html` directly. Internet is still required for external sources and Drive links.

There is no npm build or framework requirement. Python is required only for the batch-file server. Check port availability and Python installation if local startup fails. This handoff verifies the files and local link targets; it does not certify the launcher on the user's Windows machine.

## Recommended continuation

The latest active task was moving the documentation hub to a local project. Resume that task before starting a new research cycle.

1. Read this handoff and inspect the actual local files. Preserve any newer user edits.
2. Establish whether the user has already extracted and run the project on F:. If the next environment cannot access F:, work with the provided project copy and describe the exact changed files.
3. Check the landing page and local briefing navigation in a browser: opening a briefing should render its HTML page rather than send the reader to Drive preview.
4. Exercise search, category/wave/availability filters, narrow-screen layout, and empty results. Record any failures before changing the project.
5. Compare current workbook values with `CONNECTOR_SNAPSHOT.json` before changing score/rank/wave labels. Keep roadmap execution order separate.
6. If the user continues documentation authoring, use the current workbook/earlier detailed documents to create Microsoft Graph + Entra and SAP S/4HANA HTML briefings in the existing style, then update their local card paths. This is a proposed next task, not already completed work.
7. Complete remaining connector briefings when requested, using the source guides and official evidence. Update availability only when the corresponding file exists.
8. Keep GitHub upload with the user. Update the README if changes affect local execution.

### Completion checks for future website edits

- All 30 unique connectors remain present.
- Each available button resolves to a local briefing file.
- Planned cards do not point at nonexistent HTML pages.
- Counts reflect actual available/planned records.
- Search and filters still work.
- Scores and waves match the chosen current source, with unresolved differences explained.
- External evidence links remain identifiable and local relative links work from the project folder.
- No provider secrets are added to the static website.
- No GitHub push, website publication, or deployment is performed on behalf of the user.

## Open items

- User-side extraction and execution under F: are unconfirmed.
- Current Drive workbook changes and exact links to the earlier Microsoft/SAP detailed documents need retrieval if those files become relevant.
- Fourteen HTML cards remain planned, including Microsoft Graph + Entra and SAP S/4HANA.
- Customer scope, sandbox access, permissions, production entitlement, quotas, provider quotations, and contracts remain connector-specific prerequisites to confirm.
- The roadmap's progress and timing claims require owner validation.

Handoff boundary: this transfer preserves existing artifacts and context. It does not change connector research, overwrite the website, or publish anything.
