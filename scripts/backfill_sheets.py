"""One-time script: backfill Google Sheets with all historical archive data.

Run via GitHub Actions or locally with credentials:
  GOOGLE_SHEETS_CREDENTIALS='...' GOOGLE_SHEETS_ID='...' python scripts/backfill_sheets.py
"""
from __future__ import annotations

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipeline.admin.sheets import SHEET_HEADERS, _get_worksheet, format_row
from pipeline.models import dict_to_briefing_node


def main():
    creds = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
    sheet_id = os.environ.get("GOOGLE_SHEETS_ID")
    if not creds or not sheet_id:
        print("ERROR: GOOGLE_SHEETS_CREDENTIALS and GOOGLE_SHEETS_ID required")
        sys.exit(1)

    worksheet = _get_worksheet(creds, sheet_id)

    # Clear and write headers
    worksheet.clear()
    worksheet.append_row(SHEET_HEADERS)

    # Load all daily JSON files
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output", "data", "daily")
    rows = []
    for path in sorted(glob.glob(os.path.join(data_dir, "*.json"))):
        with open(path, encoding="utf-8") as f:
            nodes_data = json.load(f)
        for node_data in nodes_data:
            node = dict_to_briefing_node(node_data)
            rows.append(format_row(node))

    if rows:
        # Batch append in chunks of 50 to avoid API limits
        for i in range(0, len(rows), 50):
            chunk = rows[i:i + 50]
            worksheet.append_rows(chunk)
            print(f"  Appended rows {i + 1}-{i + len(chunk)}")

    print(f"Backfilled {len(rows)} rows to Google Sheets")


if __name__ == "__main__":
    main()
