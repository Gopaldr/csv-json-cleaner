# CSV-to-JSON Data Cleaner

## Overview

The CSV-to-JSON Data Cleaner is a Python command-line application that reads CSV files, validates and cleans records, and exports valid records to JSON. Invalid records are saved separately with their row numbers and rejection reasons.

## Features

- Reads CSV files using Python's built-in `csv` module.
- Removes unnecessary whitespace from column names and values.
- Validates required columns: `name`, `age`, and `city`.
- Converts valid ages into integers.
- Rejects records with missing fields, invalid ages, or negative ages.
- Exports valid records to `cleaned_data.json`.
- Exports rejected records and their reasons to `rejected_rows.json`.
- Handles missing input files and malformed or incomplete input.

## Requirements

- Python 3.10 or later recommended.
- No third-party Python packages are required.

## Project Structure

```text
csv-json-cleaner/
├── cleaner.py
├── input.csv
├── cleaned_data.json
├── rejected_rows.json
├── test_cleaner.py
└── README.md
```

The JSON output files are generated when the program runs.

## How to Run

1. Install Python 3 if it is not already installed.
2. Open a terminal in the project directory.
3. Run the program:

```bash
py cleaner.py
```

On systems where `py` is unavailable, use:

```bash
python cleaner.py
```

The program reads `input.csv` and creates the two JSON output files in the current directory.

## Sample Input

```csv
name,age,city
 Gopal ,22,Hyderabad
Priya,25,Bangalore
Rahul, ,Chennai
,30,Delhi
Anita,abc,Mumbai
Kiran,28, Pune
```

## Expected Result

For the sample input, the program processes six records:

- Accepted records: 3
- Rejected records: 3

Valid records are written to `cleaned_data.json`. Rejected records are written to `rejected_rows.json` with their original row numbers and reasons.

## Testing

The application should be tested with valid records, missing fields, invalid ages, negative ages, missing input files, and empty CSV files.

## Limitations

- The application expects the required columns to be named `name`, `age`, and `city`.
- The input and output filenames are configured in the Python source code.
- The program processes a single CSV file per execution.
- Data is validated according to the rules implemented in `cleaner.py`.

## Learning Outcomes

This project demonstrates Python fundamentals, file handling, CSV and JSON processing, functions, exception handling, input validation, and basic data-cleaning practices.
