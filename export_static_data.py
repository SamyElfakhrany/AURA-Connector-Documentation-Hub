"""Export the validated workbook payload for static hosts such as GitHub Pages."""

from __future__ import annotations

import json
from datetime import datetime, timezone

import server


def main() -> None:
    payload = server.read_connectors()
    payload["source"]["deliveryMode"] = "staticSnapshot"
    payload["source"]["generatedAt"] = datetime.now(timezone.utc).isoformat()

    output_path = server.ROOT / "data" / "connectors.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Exported {len(payload['connectors'])} connectors and "
        f"{len(payload['phaseOne']['journeys'])} journeys to {output_path}."
    )


if __name__ == "__main__":
    main()
