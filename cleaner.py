
import csv
import json
from pathlib import Path

INPUT_FILE = Path("input.csv")
OUTPUT_FILE = Path("cleaned_data.json")
REJECTED_FILE = Path("rejected_rows.json")

REQUIRED_COLUMNS = {"name", "age", "city"}


def clean_record(row):
    cleaned_row = {
        key.strip().lower(): (value or "").strip()
        for key, value in row.items()
        if key is not None
    }

    missing_columns = REQUIRED_COLUMNS - cleaned_row.keys()

    if missing_columns:
        raise ValueError(
            f"Missing columns: {', '.join(sorted(missing_columns))}"
        )

    name = cleaned_row["name"]
    age_text = cleaned_row["age"]
    city = cleaned_row["city"]

    if not name or not age_text or not city:
        raise ValueError("Name, age, and city are required")

    try:
        age = int(age_text)
    except ValueError:
        raise ValueError("Age must be a whole number") from None

    if age < 0:
        raise ValueError("Age cannot be negative")

    return {
        "name": name,
        "age": age,
        "city": city
    }


def clean_csv():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}"
        )

    cleaned_records = []
    rejected_records = []

    with INPUT_FILE.open(
        "r", newline="", encoding="utf-8-sig"
    ) as csv_file:
        reader = csv.DictReader(csv_file)

        if not reader.fieldnames:
            raise ValueError("The CSV file has no header row")

        normalized_headers = [
            header.strip().lower()
            for header in reader.fieldnames
            if header is not None
        ]

        if len(normalized_headers) != len(set(normalized_headers)):
            raise ValueError("The CSV contains duplicate column names")

        missing_columns = REQUIRED_COLUMNS - set(normalized_headers)

        if missing_columns:
            raise ValueError(
                f"Required columns missing: "
                f"{', '.join(sorted(missing_columns))}"
            )

        for row_number, row in enumerate(reader, start=2):
            try:
                cleaned_records.append(clean_record(row))
            except ValueError as error:
                rejected_records.append({
                    "row_number": row_number,
                    "reason": str(error),
                    "data": row
                })

    with OUTPUT_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(cleaned_records, json_file, indent=2, ensure_ascii=False)

    with REJECTED_FILE.open("w", encoding="utf-8") as json_file:
        json.dump(rejected_records, json_file, indent=2, ensure_ascii=False)

    print("Data cleaning completed!")
    print(f"Total rows processed: {len(cleaned_records) + len(rejected_records)}")
    print(f"Accepted rows: {len(cleaned_records)}")
    print(f"Rejected rows: {len(rejected_records)}")
    print(f"Cleaned output: {OUTPUT_FILE}")
    print(f"Rejected output: {REJECTED_FILE}")


if __name__ == "__main__":
    try:
        clean_csv()
    except (OSError, csv.Error, ValueError) as error:
        print(f"Error: {error}")
