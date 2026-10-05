import shutil
import tempfile
import unittest
import json
from pathlib import Path
from unittest.mock import patch

import server


def make_rows():
    headers = list(server.FIELD_HEADERS.values()) + list(server.ENTERPRISE_HEADERS.values())
    values = [
        1,
        "Example Connector",
        "Enterprise",
        "1 - Build",
        85,
        "Build eligible",
        "Example use case",
        "Example rationale",
        "BYO",
        5,
        4,
        "Yes",
        "Read",
        92,
        "1 Build now",
        "L1",
        "Example enterprise rationale",
    ]
    return {
        1: {index: {"value": value, "formula": False, "reference": f"C{index}"} for index, value in enumerate(headers, 1)},
        2: {index: {"value": value, "formula": index in {4, 5}, "reference": f"C{index}"} for index, value in enumerate(values, 1)},
    }


def make_journey_rows():
    headers = list(server.JOURNEY_HEADERS.values())
    rows = {
        4: {
            index: {"value": value, "formula": False, "reference": f"C{index}"}
            for index, value in enumerate(headers, 1)
        }
    }
    for offset in range(6):
        journey_id = f"J{offset + 1}"
        values = [
            journey_id,
            f"Journey {offset + 1}",
            "example-connector",
            "Example Connector",
            "L1" if offset < 4 else "L2",
            "Read" if offset < 4 else "Handoff, then Read",
            "Shared foundation",
            "Validated" if offset < 2 else "Gate open",
            f"Resolve gate {offset + 1}",
            "example-connector",
            "No transactional writes",
            "Test source note",
        ]
        rows[5 + offset] = {
            index: {"value": value, "formula": False, "reference": f"C{index}"}
            for index, value in enumerate(values, 1)
        }
    return rows


class WorkbookReaderTests(unittest.TestCase):
    def test_current_workbook_matches_expected_register(self):
        payload = server.read_connectors()
        records = payload["connectors"]
        self.assertEqual(30, len(records))
        self.assertEqual("Microsoft 365 / Microsoft Graph + Entra", records[0]["name"])
        self.assertEqual(100, records[0]["score"])
        self.assertEqual("1 - Build", records[0]["wave"])
        self.assertEqual(
            "briefings/AURA_Microsoft_365_Employee_Digital_Hub_FINAL_EN.html",
            records[0]["url"],
        )
        self.assertEqual(
            [
                "Microsoft 365 / Microsoft Graph + Entra",
                "SAP SuccessFactors",
                "SPL National Address",
                "Qiwa",
                "Muqeem",
                "GOSI",
                "Mudad",
            ],
            [record["name"] for record in records[:7]],
        )
        self.assertTrue(all(record["wave"] == "1 - Build" for record in records[:7]))
        self.assertEqual(
            [100, 98, 97, 96, 95, 94, 93],
            [record["score"] for record in records[:7]],
        )
        self.assertEqual("Kidana", records[-1]["name"])
        self.assertEqual(30, sum(bool(record["url"]) for record in records))
        self.assertEqual(92, records[0]["enterpriseLaunch"]["priorityIndex"])
        self.assertEqual("L1", records[0]["enterpriseLaunch"]["wave"])
        self.assertEqual(6, len(payload["phaseOne"]["journeys"]))
        self.assertEqual(4, len(payload["phaseOne"]["stages"][0]["journeyIds"]))
        self.assertEqual(2, len(payload["phaseOne"]["stages"][1]["journeyIds"]))

    def test_static_snapshot_matches_current_workbook(self):
        snapshot_path = server.ROOT / "data" / "connectors.json"
        snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
        current = server.read_connectors()
        self.assertEqual(current["connectors"], snapshot["connectors"])
        self.assertEqual(current["phaseOne"], snapshot["phaseOne"])
        self.assertEqual("staticSnapshot", snapshot["source"]["deliveryMode"])

    def test_published_site_uses_static_snapshot_only(self):
        index = (server.ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('fetch("data/connectors.json"', index)
        self.assertNotIn('fetch("/api/connectors"', index)
        self.assertNotIn('["/api/connectors", "data/connectors.json"]', index)

    def test_missing_required_header_is_rejected(self):
        rows = make_rows()
        summary_column = list(server.FIELD_HEADERS.values()).index("AURA value rationale") + 1
        del rows[1][summary_column]
        with self.assertRaisesRegex(server.WorkbookError, "Missing required header"):
            server._records_from_rows(rows, server.ROOT)

    def test_duplicate_connector_is_rejected(self):
        rows = make_rows()
        rows[3] = {key: dict(value) for key, value in rows[2].items()}
        rows[3][1]["value"] = 2
        with self.assertRaisesRegex(server.WorkbookError, "Duplicate connector"):
            server._records_from_rows(rows, server.ROOT)

    def test_missing_enterprise_header_is_rejected(self):
        rows = make_rows()
        model_column = list(server.FIELD_HEADERS.values()).__len__() + 1
        del rows[1][model_column]
        with self.assertRaisesRegex(server.WorkbookError, "Missing required header"):
            server._records_from_rows(rows, server.ROOT)

    def test_duplicate_rank_is_rejected(self):
        rows = make_rows()
        rows[3] = {key: dict(value) for key, value in rows[2].items()}
        rows[3][2]["value"] = "Second Connector"
        with self.assertRaisesRegex(server.WorkbookError, "Duplicate Rank"):
            server._records_from_rows(rows, server.ROOT)

    def test_invalid_score_is_rejected(self):
        rows = make_rows()
        rows[2][5]["value"] = 101
        with self.assertRaisesRegex(server.WorkbookError, "outside 0–100"):
            server._records_from_rows(rows, server.ROOT)

    def test_blank_cached_score_is_rejected_with_save_guidance(self):
        rows = make_rows()
        rows[2][5]["value"] = None
        with self.assertRaisesRegex(server.WorkbookError, "recalculate it, and save it"):
            server._records_from_rows(rows, server.ROOT)

    def test_invalid_enterprise_index_is_rejected(self):
        rows = make_rows()
        headers = list(server.FIELD_HEADERS.values()) + list(server.ENTERPRISE_HEADERS.values())
        column = headers.index(server.ENTERPRISE_HEADERS["priorityIndex"]) + 1
        rows[2][column]["value"] = 101
        with self.assertRaisesRegex(server.WorkbookError, "index outside 0–100"):
            server._records_from_rows(rows, server.ROOT)

    def test_invalid_enterprise_wave_is_rejected(self):
        rows = make_rows()
        headers = list(server.FIELD_HEADERS.values()) + list(server.ENTERPRISE_HEADERS.values())
        column = headers.index(server.ENTERPRISE_HEADERS["launchWave"]) + 1
        rows[2][column]["value"] = "Wave One"
        with self.assertRaisesRegex(server.WorkbookError, "invalid Enterprise wave"):
            server._records_from_rows(rows, server.ROOT)

    def test_journey_referential_integrity_and_stage_counts(self):
        records = server._records_from_rows(make_rows(), server.ROOT)
        phase_one = server._journeys_from_rows(make_journey_rows(), records)
        self.assertEqual(6, len(phase_one["journeys"]))
        self.assertEqual("example-connector", phase_one["journeys"][0]["primaryConnectorKey"])

    def test_duplicate_journey_id_is_rejected(self):
        records = server._records_from_rows(make_rows(), server.ROOT)
        rows = make_journey_rows()
        rows[6][1]["value"] = "J1"
        with self.assertRaisesRegex(server.WorkbookError, "Duplicate Journey ID"):
            server._journeys_from_rows(rows, records)

    def test_invalid_journey_depth_is_rejected(self):
        records = server._records_from_rows(make_rows(), server.ROOT)
        rows = make_journey_rows()
        depth_column = list(server.JOURNEY_HEADERS.values()).index("Depth at launch") + 1
        rows[5][depth_column]["value"] = "Write"
        with self.assertRaisesRegex(server.WorkbookError, "invalid journey depth"):
            server._journeys_from_rows(rows, records)

    def test_unresolved_journey_connector_key_is_rejected(self):
        records = server._records_from_rows(make_rows(), server.ROOT)
        rows = make_journey_rows()
        keys_column = list(server.JOURNEY_HEADERS.values()).index("Connector keys") + 1
        rows[5][keys_column]["value"] = "missing-connector"
        with self.assertRaisesRegex(server.WorkbookError, "unresolved connector key"):
            server._journeys_from_rows(rows, records)

    def test_missing_workbook_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            missing = Path(temp_dir) / server.WORKBOOK_FILENAME
            with self.assertRaisesRegex(server.WorkbookError, "was not found"):
                server.read_connectors(missing, Path(temp_dir))

    def test_malformed_workbook_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            malformed = Path(temp_dir) / server.WORKBOOK_FILENAME
            malformed.write_bytes(b"not an xlsx file")
            with self.assertRaisesRegex(server.WorkbookError, "not a valid .xlsx"):
                server.read_connectors(malformed, Path(temp_dir))

    def test_cache_returns_stale_copy_after_later_failure(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            workbook = root / server.WORKBOOK_FILENAME
            shutil.copy2(server.WORKBOOK_PATH, workbook)
            cache = server.ConnectorCache(workbook, server.ROOT)
            first = cache.load()
            workbook.write_bytes(b"broken")
            second = cache.load()
            self.assertFalse(first["source"]["stale"])
            self.assertTrue(second["source"]["stale"])
            self.assertEqual(30, len(second["connectors"]))
            self.assertIn("not a valid .xlsx", second["source"]["warning"])

    def test_cache_retries_temporary_file_error(self):
        payload = {"source": {"stale": False}, "connectors": []}
        cache = server.ConnectorCache()
        with patch("server.read_connectors", side_effect=[PermissionError("locked"), payload]) as reader:
            self.assertIs(payload, cache.load())
            self.assertEqual(2, reader.call_count)


if __name__ == "__main__":
    unittest.main()
