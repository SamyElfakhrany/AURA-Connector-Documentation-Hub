"""Local AURA documentation server backed by the saved Excel workbook."""

from __future__ import annotations

import argparse
import copy
import json
import posixpath
import re
import threading
import time
import zipfile
from datetime import datetime, timezone
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parent
WORKBOOK_FILENAME = "AURA_Connector_Prioritization_Enterprise_Phase_One_2026-10-05.xlsx"
WORKBOOK_RELATIVE_PATH = Path("outputs") / "enterprise-phase-one-2026-10-05" / WORKBOOK_FILENAME
WORKBOOK_PATH = ROOT / WORKBOOK_RELATIVE_PATH
SHEET_NAME = "Prioritized Connector Register"
JOURNEY_SHEET_NAME = "Day-one Journeys"

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PACKAGE_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
CELL_REFERENCE = re.compile(r"^([A-Z]+)(\d+)$")

FIELD_HEADERS = {
    "rank": "Rank",
    "name": "Connector",
    "category": "Category",
    "wave": "Wave",
    "score": "Priority Score /100",
    "access": "Access status",
    "useCase": "Use case",
    "summary": "AURA value rationale",
}

ENTERPRISE_HEADERS = {
    "model": "Launch model",
    "value": "Enterprise value 1–5",
    "accessScore": "Customer access 1–5",
    "critical": "Launch-critical",
    "depth": "Launch depth",
    "priorityIndex": "Enterprise priority index /100",
    "bucket": "Enterprise bucket",
    "launchWave": "Enterprise wave",
    "rationale": "Launch rationale",
}

JOURNEY_HEADERS = {
    "id": "Journey ID",
    "name": "Journey",
    "connectorKeys": "Connector keys",
    "connectors": "Connectors",
    "stage": "Launch stage",
    "depth": "Depth at launch",
    "dependsOn": "Depends on",
    "validationState": "Validation state",
    "nextGate": "Next gate",
    "primaryConnectorKey": "Primary connector key",
    "writeControl": "Write control",
    "sourceNote": "Source note",
}

ENTERPRISE_MODELS = {"BYO", "AURA-as-party", "Demand-gated"}
ENTERPRISE_DEPTHS = {"Read", "Handoff", "Handoff, then Read", "-"}
ENTERPRISE_WAVES = {"L1", "L2", "L3", "-"}
ENTERPRISE_BUCKETS = {
    "1 Build now",
    "2 Negotiate access",
    "3 Quick win (handoff)",
    "4 Park",
    "Parked: AURA-as-party",
    "Demand-gated",
}

BRIEFING_FILES = {
    "Microsoft 365 / Microsoft Graph + Entra": "briefings/microsoft-365-graph-entra.html",
    "SAP S/4HANA": "briefings/sap-s4hana.html",
    "SAP SuccessFactors": "briefings/sap-successfactors.html",
    "ServiceNow": "briefings/servicenow.html",
    "SPL National Address": "briefings/spl-national-address.html",
    "Oracle Fusion ERP / HCM": "briefings/oracle-fusion-erp-hcm.html",
    "Dynamics 365 / Dataverse": "briefings/dynamics-365-dataverse.html",
    "PayTabs": "briefings/paytabs.html",
    "IATA": "briefings/iata.html",
    "Nafath": "briefings/nafath.html",
    "Qiwa": "briefings/qiwa.html",
    "Etimad APIs": "briefings/etimad-apis.html",
    "Absher": "briefings/absher.html",
    "GOSI": "briefings/gosi.html",
    "Muqeem": "briefings/muqeem.html",
    "Yaqeen": "briefings/yaqeen.html",
    "ZATCA Integration Service": "briefings/zatca-integration-service.html",
    "NIC": "briefings/nic.html",
    "Ministry of Commerce": "briefings/ministry-of-commerce.html",
    "Mudad": "briefings/mudad.html",
    "SADAD": "briefings/sadad.html",
    "Ajeer": "briefings/ajeer.html",
    "CRS": "briefings/crs.html",
    "SAR through Masar Integration Gateway": "briefings/sar-masar-gateway.html",
    "MOFA": "briefings/mofa.html",
    "MOI": "briefings/moi-umrah-agent.html",
    "Nusuk Imtithal / Sahab": "briefings/nusuk-imtithal-sahab.html",
    "Tasheer Connect": "briefings/tasheer-connect.html",
    "Atlas": "briefings/atlas.html",
    "Kidana": "briefings/kidana-handover-files.html",
}

CONNECTOR_NAMES_BY_KEY = {
    Path(path).stem: name for name, path in BRIEFING_FILES.items()
}


class WorkbookError(Exception):
    """A safe, user-facing workbook read or validation error."""


def _main_tag(name: str) -> str:
    return f"{{{MAIN_NS}}}{name}"


def _column_number(reference: str) -> int:
    match = CELL_REFERENCE.match(reference)
    if not match:
        raise WorkbookError(f"Invalid Excel cell reference: {reference}")
    column = 0
    for character in match.group(1):
        column = column * 26 + ord(character) - ord("A") + 1
    return column


def _relationship_target(
    archive: zipfile.ZipFile, relationship_id: str, sheet_name: str
) -> str:
    try:
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
    except (KeyError, ET.ParseError) as error:
        raise WorkbookError("The workbook relationship data is missing or invalid.") from error

    relationship_tag = f"{{{PACKAGE_REL_NS}}}Relationship"
    for relationship in relationships.findall(relationship_tag):
        if relationship.get("Id") == relationship_id:
            target = relationship.get("Target")
            if not target:
                break
            if target.startswith("/"):
                return target.lstrip("/")
            return posixpath.normpath(posixpath.join("xl", target))
    raise WorkbookError(f"The worksheet relationship for '{sheet_name}' is missing.")


def _worksheet_path(archive: zipfile.ZipFile, sheet_name: str = SHEET_NAME) -> str:
    try:
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
    except (KeyError, ET.ParseError) as error:
        raise WorkbookError("The workbook definition is missing or invalid.") from error

    for sheet in workbook.findall(f"{_main_tag('sheets')}/{_main_tag('sheet')}"):
        if sheet.get("name") == sheet_name:
            relationship_id = sheet.get(f"{{{OFFICE_REL_NS}}}id")
            if relationship_id:
                return _relationship_target(archive, relationship_id, sheet_name)
    raise WorkbookError(f"Worksheet '{sheet_name}' was not found.")


def _shared_strings(archive: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    except ET.ParseError as error:
        raise WorkbookError("The workbook shared strings are invalid.") from error

    return [
        "".join(text.text or "" for text in item.iter(_main_tag("t")))
        for item in root.findall(_main_tag("si"))
    ]


def _cell_value(cell: ET.Element, shared_strings: list[str]):
    cell_type = cell.get("t")
    if cell_type == "inlineStr":
        inline = cell.find(_main_tag("is"))
        return "" if inline is None else "".join(
            text.text or "" for text in inline.iter(_main_tag("t"))
        )

    value_element = cell.find(_main_tag("v"))
    raw_value = None if value_element is None else value_element.text
    if raw_value is None:
        return None
    if cell_type == "s":
        try:
            return shared_strings[int(raw_value)]
        except (ValueError, IndexError) as error:
            raise WorkbookError("The workbook contains an invalid shared-string reference.") from error
    if cell_type in {"str", "e"}:
        return raw_value
    if cell_type == "b":
        return raw_value == "1"

    try:
        number = float(raw_value)
    except ValueError:
        return raw_value
    return int(number) if number.is_integer() else number


def _worksheet_rows(
    archive: zipfile.ZipFile, sheet_name: str = SHEET_NAME
) -> dict[int, dict[int, dict]]:
    worksheet_path = _worksheet_path(archive, sheet_name)
    shared_strings = _shared_strings(archive)
    try:
        worksheet = ET.fromstring(archive.read(worksheet_path))
    except (KeyError, ET.ParseError) as error:
        raise WorkbookError(f"Worksheet '{sheet_name}' is missing or invalid.") from error

    rows: dict[int, dict[int, dict]] = {}
    sheet_data = worksheet.find(_main_tag("sheetData"))
    if sheet_data is None:
        raise WorkbookError(f"Worksheet '{sheet_name}' has no cell data.")

    for row_element in sheet_data.findall(_main_tag("row")):
        row_number = int(row_element.get("r", "0"))
        row: dict[int, dict] = {}
        for cell in row_element.findall(_main_tag("c")):
            reference = cell.get("r")
            if not reference:
                continue
            row[_column_number(reference)] = {
                "value": _cell_value(cell, shared_strings),
                "formula": cell.find(_main_tag("f")) is not None,
                "reference": reference,
            }
        if row:
            rows[row_number] = row
    return rows


def _required_text(value, label: str, row_number: int) -> str:
    if value is None or not str(value).strip():
        raise WorkbookError(f"Row {row_number} is missing '{label}'.")
    return str(value).strip()


def _required_number(value, label: str, row_number: int) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WorkbookError(
            f"Row {row_number} has no saved numeric value for '{label}'. "
            "Open the workbook in Excel, recalculate it, and save it."
        )
    return float(value)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.casefold()).strip("-")


def _integer_in_range(value, label: str, row_number: int, minimum: int, maximum: int) -> int:
    number = _required_number(value, label, row_number)
    if not number.is_integer() or not minimum <= number <= maximum:
        raise WorkbookError(
            f"Row {row_number} has an invalid '{label}'; use a whole number from "
            f"{minimum} to {maximum}."
        )
    return int(number)


def _records_from_rows(rows: dict[int, dict[int, dict]], root: Path) -> list[dict]:
    header_row = rows.get(1)
    if not header_row:
        raise WorkbookError(f"Worksheet '{SHEET_NAME}' has no header row.")

    header_columns: dict[str, int] = {}
    duplicate_headers: set[str] = set()
    for column, cell in header_row.items():
        value = cell["value"]
        if value is None:
            continue
        header = str(value).strip()
        if header in header_columns:
            duplicate_headers.add(header)
        header_columns[header] = column
    if duplicate_headers:
        names = ", ".join(sorted(duplicate_headers))
        raise WorkbookError(f"Duplicate required header(s): {names}.")

    all_headers = {**FIELD_HEADERS, **ENTERPRISE_HEADERS}
    missing_headers = [header for header in all_headers.values() if header not in header_columns]
    if missing_headers:
        raise WorkbookError("Missing required header(s): " + ", ".join(missing_headers) + ".")

    records: list[dict] = []
    seen_names: set[str] = set()
    seen_ranks: set[int] = set()
    required_columns = {key: header_columns[header] for key, header in all_headers.items()}

    for row_number in sorted(number for number in rows if number > 1):
        row = rows[row_number]
        values = {
            key: row.get(column, {"value": None})["value"]
            for key, column in required_columns.items()
        }
        if all(value is None or str(value).strip() == "" for value in values.values()):
            continue

        name = _required_text(values["name"], FIELD_HEADERS["name"], row_number)
        normalized_name = name.casefold()
        if normalized_name in seen_names:
            raise WorkbookError(f"Duplicate connector '{name}' at row {row_number}.")
        seen_names.add(normalized_name)

        rank_number = _required_number(values["rank"], FIELD_HEADERS["rank"], row_number)
        if rank_number <= 0 or not rank_number.is_integer():
            raise WorkbookError(f"Row {row_number} has an invalid Rank; use a positive whole number.")
        rank = int(rank_number)
        if rank in seen_ranks:
            raise WorkbookError(f"Duplicate Rank {rank} at row {row_number}.")
        seen_ranks.add(rank)

        score_number = _required_number(values["score"], FIELD_HEADERS["score"], row_number)
        if not 0 <= score_number <= 100:
            raise WorkbookError(f"Row {row_number} has a Priority Score outside 0–100.")
        score = int(score_number) if score_number.is_integer() else score_number

        model = _required_text(values["model"], ENTERPRISE_HEADERS["model"], row_number)
        if model not in ENTERPRISE_MODELS:
            raise WorkbookError(f"Row {row_number} has an invalid Launch model: '{model}'.")
        value_score = _integer_in_range(
            values["value"], ENTERPRISE_HEADERS["value"], row_number, 1, 5
        )
        access_score = _integer_in_range(
            values["accessScore"], ENTERPRISE_HEADERS["accessScore"], row_number, 1, 5
        )
        critical_text = _required_text(
            values["critical"], ENTERPRISE_HEADERS["critical"], row_number
        )
        if critical_text not in {"Yes", "No"}:
            raise WorkbookError(
                f"Row {row_number} has an invalid Launch-critical value; use Yes or No."
            )
        depth = _required_text(values["depth"], ENTERPRISE_HEADERS["depth"], row_number)
        if depth not in ENTERPRISE_DEPTHS:
            raise WorkbookError(f"Row {row_number} has an invalid Launch depth: '{depth}'.")
        priority_number = _required_number(
            values["priorityIndex"], ENTERPRISE_HEADERS["priorityIndex"], row_number
        )
        if not 0 <= priority_number <= 100:
            raise WorkbookError(
                f"Row {row_number} has an Enterprise priority index outside 0–100."
            )
        priority_index = (
            int(priority_number) if priority_number.is_integer() else priority_number
        )
        bucket = _required_text(values["bucket"], ENTERPRISE_HEADERS["bucket"], row_number)
        if bucket not in ENTERPRISE_BUCKETS:
            raise WorkbookError(f"Row {row_number} has an invalid Enterprise bucket: '{bucket}'.")
        launch_wave = _required_text(
            values["launchWave"], ENTERPRISE_HEADERS["launchWave"], row_number
        )
        if launch_wave not in ENTERPRISE_WAVES:
            raise WorkbookError(f"Row {row_number} has an invalid Enterprise wave: '{launch_wave}'.")

        briefing_file = BRIEFING_FILES.get(name)
        briefing_url = briefing_file if briefing_file and (root / briefing_file).is_file() else None
        connector_key = Path(briefing_file).stem if briefing_file else _slug(name)
        records.append(
            {
                "key": connector_key,
                "rank": rank,
                "name": name,
                "category": _required_text(values["category"], FIELD_HEADERS["category"], row_number),
                "wave": _required_text(values["wave"], FIELD_HEADERS["wave"], row_number),
                "score": score,
                "access": _required_text(values["access"], FIELD_HEADERS["access"], row_number),
                "useCase": _required_text(values["useCase"], FIELD_HEADERS["useCase"], row_number),
                "summary": _required_text(values["summary"], FIELD_HEADERS["summary"], row_number),
                "url": briefing_url,
                "enterpriseLaunch": {
                    "model": model,
                    "value": value_score,
                    "accessScore": access_score,
                    "critical": critical_text == "Yes",
                    "depth": depth,
                    "priorityIndex": priority_index,
                    "bucket": bucket,
                    "wave": launch_wave,
                    "rationale": _required_text(
                        values["rationale"], ENTERPRISE_HEADERS["rationale"], row_number
                    ),
                },
            }
        )

    if not records:
        raise WorkbookError(f"Worksheet '{SHEET_NAME}' contains no valid connector rows.")
    return records


def _journeys_from_rows(rows: dict[int, dict[int, dict]], records: list[dict]) -> dict:
    header_row_number = None
    header_columns: dict[str, int] = {}
    for row_number in sorted(rows):
        candidate = {
            str(cell["value"]).strip(): column
            for column, cell in rows[row_number].items()
            if cell["value"] is not None
        }
        if all(header in candidate for header in JOURNEY_HEADERS.values()):
            header_row_number = row_number
            header_columns = candidate
            break
    if header_row_number is None:
        raise WorkbookError(
            f"Worksheet '{JOURNEY_SHEET_NAME}' is missing the required journey headers."
        )

    connector_by_key = {record["key"]: record for record in records}
    journeys: list[dict] = []
    seen_ids: set[str] = set()
    required_columns = {
        key: header_columns[header] for key, header in JOURNEY_HEADERS.items()
    }

    for row_number in sorted(number for number in rows if number > header_row_number):
        row = rows[row_number]
        values = {
            key: row.get(column, {"value": None})["value"]
            for key, column in required_columns.items()
        }
        if all(value is None or str(value).strip() == "" for value in values.values()):
            continue

        journey_id = _required_text(values["id"], JOURNEY_HEADERS["id"], row_number)
        if journey_id in seen_ids:
            raise WorkbookError(f"Duplicate Journey ID '{journey_id}' at row {row_number}.")
        seen_ids.add(journey_id)

        stage = _required_text(values["stage"], JOURNEY_HEADERS["stage"], row_number)
        if stage not in {"L1", "L2"}:
            raise WorkbookError(f"Row {row_number} has an invalid Launch stage: '{stage}'.")
        depth = _required_text(values["depth"], JOURNEY_HEADERS["depth"], row_number)
        if depth not in {"Read", "Handoff", "Handoff, then Read"}:
            raise WorkbookError(f"Row {row_number} has an invalid journey depth: '{depth}'.")

        connector_keys = [
            key.strip()
            for key in _required_text(
                values["connectorKeys"], JOURNEY_HEADERS["connectorKeys"], row_number
            ).split(";")
            if key.strip()
        ]
        if len(connector_keys) != len(set(connector_keys)):
            raise WorkbookError(f"Row {row_number} contains duplicate connector keys.")
        unresolved = [key for key in connector_keys if key not in connector_by_key]
        if unresolved:
            raise WorkbookError(
                f"Row {row_number} has unresolved connector key(s): {', '.join(unresolved)}."
            )
        primary_key = _required_text(
            values["primaryConnectorKey"],
            JOURNEY_HEADERS["primaryConnectorKey"],
            row_number,
        )
        if primary_key not in connector_keys:
            raise WorkbookError(
                f"Row {row_number} primary connector key must appear in Connector keys."
            )

        connector_refs = [
            {
                "key": key,
                "name": connector_by_key[key]["name"],
                "rank": connector_by_key[key]["rank"],
                "url": connector_by_key[key]["url"],
            }
            for key in connector_keys
        ]
        journeys.append(
            {
                "id": journey_id,
                "name": _required_text(values["name"], JOURNEY_HEADERS["name"], row_number),
                "connectorKeys": connector_keys,
                "connectors": _required_text(
                    values["connectors"], JOURNEY_HEADERS["connectors"], row_number
                ),
                "stage": stage,
                "depth": depth,
                "dependsOn": _required_text(
                    values["dependsOn"], JOURNEY_HEADERS["dependsOn"], row_number
                ),
                "validationState": _required_text(
                    values["validationState"],
                    JOURNEY_HEADERS["validationState"],
                    row_number,
                ),
                "nextGate": _required_text(
                    values["nextGate"], JOURNEY_HEADERS["nextGate"], row_number
                ),
                "primaryConnectorKey": primary_key,
                "writeControl": _required_text(
                    values["writeControl"], JOURNEY_HEADERS["writeControl"], row_number
                ),
                "sourceNote": _required_text(
                    values["sourceNote"], JOURNEY_HEADERS["sourceNote"], row_number
                ),
                "connectorRefs": connector_refs,
            }
        )

    if len(journeys) != 6:
        raise WorkbookError(
            f"Worksheet '{JOURNEY_SHEET_NAME}' must contain exactly six journeys; "
            f"found {len(journeys)}."
        )
    if sum(journey["stage"] == "L1" for journey in journeys) != 4:
        raise WorkbookError("Day-one Journeys must contain four L1 journeys.")
    if sum(journey["stage"] == "L2" for journey in journeys) != 2:
        raise WorkbookError("Day-one Journeys must contain two L2 journeys.")

    return {
        "title": "Enterprise Phase One",
        "scope": "Shared Saudi enterprise journey architecture for Elm, stc and Al Rajhi",
        "guardrail": "Read-only APIs and official handoffs; no transactional writes.",
        "foundation": {
            "title": "Shared enterprise foundation",
            "connectorKeys": ["microsoft-365-graph-entra", "sap-successfactors"],
            "gate": "Confirm each customer's Entra tenant and SuccessFactors test access.",
        },
        "stages": [
            {
                "id": "L1",
                "label": "Launch core",
                "journeyIds": [journey["id"] for journey in journeys if journey["stage"] == "L1"],
            },
            {
                "id": "L2",
                "label": "Access-enabled",
                "journeyIds": [journey["id"] for journey in journeys if journey["stage"] == "L2"],
            },
        ],
        "journeys": journeys,
        "gates": [
            {
                "journeyId": journey["id"],
                "state": journey["validationState"],
                "nextGate": journey["nextGate"],
            }
            for journey in journeys
        ],
    }


def read_connectors(workbook_path: Path = WORKBOOK_PATH, root: Path = ROOT) -> dict:
    if not workbook_path.is_file():
        raise WorkbookError(f"Workbook '{workbook_path.name}' was not found in the project folder.")
    try:
        with zipfile.ZipFile(workbook_path) as archive:
            records = _records_from_rows(_worksheet_rows(archive, SHEET_NAME), root)
            phase_one = _journeys_from_rows(
                _worksheet_rows(archive, JOURNEY_SHEET_NAME), records
            )
    except zipfile.BadZipFile as error:
        raise WorkbookError(f"Workbook '{workbook_path.name}' is not a valid .xlsx file.") from error

    modified_at = datetime.fromtimestamp(workbook_path.stat().st_mtime, timezone.utc).isoformat()
    return {
        "source": {
            "file": workbook_path.name,
            "href": (
                WORKBOOK_RELATIVE_PATH.as_posix()
                if workbook_path.resolve() == WORKBOOK_PATH.resolve()
                else workbook_path.name
            ),
            "sheet": SHEET_NAME,
            "journeySheet": JOURNEY_SHEET_NAME,
            "modifiedAt": modified_at,
            "stale": False,
        },
        "connectors": records,
        "phaseOne": phase_one,
    }


class ConnectorCache:
    def __init__(self, workbook_path: Path = WORKBOOK_PATH, root: Path = ROOT):
        self.workbook_path = workbook_path
        self.root = root
        self.last_good: dict | None = None
        self.lock = threading.Lock()

    def load(self) -> dict:
        with self.lock:
            last_error: Exception | None = None
            for attempt in range(3):
                try:
                    payload = read_connectors(self.workbook_path, self.root)
                    self.last_good = payload
                    return payload
                except (WorkbookError, OSError, ET.ParseError) as error:
                    last_error = error
                    if attempt < 2:
                        time.sleep(0.15 * (attempt + 1))

            message = str(last_error) if last_error else "The workbook could not be read."
            if self.last_good is not None:
                payload = copy.deepcopy(self.last_good)
                payload["source"]["stale"] = True
                payload["source"]["warning"] = message
                return payload
            raise WorkbookError(message)


CONNECTOR_CACHE = ConnectorCache()


class AURARequestHandler(SimpleHTTPRequestHandler):
    server_version = "AURALocal/1.0"

    def do_GET(self):
        if urlsplit(self.path).path == "/api/connectors":
            try:
                self._send_json(CONNECTOR_CACHE.load(), 200)
            except WorkbookError as error:
                self._send_json({"error": str(error)}, 503)
            return
        super().do_GET()

    def _send_json(self, payload: dict, status: int):
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)


def main():
    parser = argparse.ArgumentParser(description="Serve the AURA connector documentation hub.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()

    handler = partial(AURARequestHandler, directory=str(ROOT))
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"AURA Connector Documentation Hub: http://{args.host}:{args.port}")
    print("Save the Excel workbook, then refresh the browser to load the latest data.")
    print("Press Ctrl+C to stop the server.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
