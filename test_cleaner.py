
import csv
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import cleaner


class TestCleanRecord(unittest.TestCase):

    def test_removes_whitespace_and_converts_age(self):
        row = {
            "name": " Gopal ",
            "age": "22",
            "city": " Hyderabad "
        }

        result = cleaner.clean_record(row)

        self.assertEqual(result, {
            "name": "Gopal",
            "age": 22,
            "city": "Hyderabad"
        })

    def test_rejects_missing_name(self):
        row = {"name": "", "age": "22", "city": "Hyderabad"}

        with self.assertRaisesRegex(ValueError, "required"):
            cleaner.clean_record(row)

    def test_rejects_invalid_age(self):
        row = {"name": "Anita", "age": "abc", "city": "Mumbai"}

        with self.assertRaisesRegex(ValueError, "whole number"):
            cleaner.clean_record(row)

    def test_rejects_negative_age(self):
        row = {"name": "Rahul", "age": "-1", "city": "Chennai"}

        with self.assertRaisesRegex(ValueError, "negative"):
            cleaner.clean_record(row)

    def test_rejects_missing_required_column(self):
        row = {"name": "Gopal", "age": "22"}

        with self.assertRaisesRegex(ValueError, "Missing columns"):
            cleaner.clean_record(row)


class TestCleanCsv(unittest.TestCase):

    def test_creates_cleaned_and_rejected_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            input_file = folder / "input.csv"
            output_file = folder / "cleaned_data.json"
            rejected_file = folder / "rejected_rows.json"

            with input_file.open(
                "w", newline="", encoding="utf-8"
            ) as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(["name", "age", "city"])
                writer.writerow([" Gopal ", "22", " Hyderabad "])
                writer.writerow(["Anita", "abc", "Mumbai"])

            with (
                patch.object(cleaner, "INPUT_FILE", input_file),
                patch.object(cleaner, "OUTPUT_FILE", output_file),
                patch.object(cleaner, "REJECTED_FILE", rejected_file),
            ):
                cleaner.clean_csv()

            with output_file.open(encoding="utf-8") as json_file:
                cleaned = json.load(json_file)

            with rejected_file.open(encoding="utf-8") as json_file:
                rejected = json.load(json_file)

            self.assertEqual(len(cleaned), 1)
            self.assertEqual(cleaned[0]["age"], 22)
            self.assertEqual(cleaned[0]["name"], "Gopal")
            self.assertEqual(len(rejected), 1)
            self.assertIn("whole number", rejected[0]["reason"])


if __name__ == "__main__":
    unittest.main()
