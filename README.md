# registrarY

A Python-based command-line application for creating and managing structured databases using JSON files. Create student databases, define custom schemas, manage records, search data, and export records to Excel.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github&logoColor=white)](https://github.com/randomhumanfromearth/registrarY)

> **Fork notice:** This repository is an independently maintained fork of [lyashwith/registrarY](https://github.com/lyashwith/registrarY). It builds upon the original project while maintaining its own changes and development history. Changes in this repository are not automatically submitted to the upstream project.

---

## Overview

registrarY is a lightweight record-management application written in Python. It stores records locally in JSON-based files and provides an interactive command-line menu for managing them.

The application supports both a predefined student database and user-defined database schemas. Records can be added, viewed, searched, updated, deleted, and exported to Excel.

## Features

- **Default student database** — Create student records with predefined fields and automatically generated roll numbers.
- **Custom schemas** — Define your own primary key, field names, and data types.
- **Add records** — Insert records while checking for duplicate primary keys.
- **View records** — Display database records in formatted tables.
- **Search records** — Find records using their primary keys.
- **Update records** — Modify existing records while retaining unchanged values.
- **Delete records** — Remove records with confirmation.
- **Excel export** — Export records into `.xlsx` workbooks.
- **Local storage** — Store database and schema information in JSON-based files.

## Preview

### Command-line interface

![registrarY Preview](https://raw.githubusercontent.com/randomhumanfromearth/registrarY/main/Documents/IMG-20261011-WA0001.jpg)

![registrarY Preview](https://raw.githubusercontent.com/randomhumanfromearth/registrarY/main/Documents/IMG-20261011-WA0002.jpg)

## Requirements

- Python 3
- `tabulate`
- `openpyxl` (required for Excel export)

The `json`, `os`, and `subprocess` modules are included with Python.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/randomhumanfromearth/registrarY.git
```

### 2. Enter the project directory

```bash
cd registrarY
```

### 3. Install dependencies

```bash
python3 -m pip install tabulate openpyxl
```

### 4. Run registrarY

```bash
python3 registrarY/registrarY.py
```

The application will ask you for a database name when it starts.

## Usage

### Starting the application

Run:

```bash
python3 registrarY/registrarY.py
```

Enter a database name when prompted:

```text
Enter the name of the database to do the operations: students
```

registrarY looks for a corresponding `students.eL` file in the current working directory. If it does not exist, the application offers to create a new database.

### Menu

The application provides the following operations:

| Option | Operation |
|:---:|---|
| 1 | Create default database |
| 2 | Create custom schema |
| 3 | Add data |
| 4 | View all records |
| 5 | Search |
| 6 | Update |
| 7 | Delete |
| 8 | Export to Excel |
| 9 | Help |
| 10 | Exit |

You can enter the option number or, where supported, the corresponding command.

## Default student database

Select **1 — Create default** to create a student database.

Each record contains:

| Field | Description |
|---|---|
| `Name` | Student's name |
| `date_of_birth` | Date of birth |
| `father_name` | Father's name |
| `mother_name` | Mother's name |

The application automatically generates roll numbers in this format:

```text
A0001
A0002
A0003
```

The date of birth is requested in `DD-MM-YYYY` format.

The current roll-number format supports a maximum of 26,000 records per generated database.

## Custom schemas

Select **2 — Create custom schema** to define your own record structure.

First, enter a primary key name. Then specify the fields and their data types.

Example:

```text
name;str,age;int,percentage;float
```

If the primary key is `id`, the resulting schema is:

```json
{
    "id": {
        "name": "str",
        "age": "int",
        "percentage": "float"
    }
}
```

### Supported data types

| Type | Description | Example |
|---|---|---|
| `str` | Text | `"Arun"` |
| `int` | Integer | `18` |
| `float` | Decimal number | `93.17` |

The primary key uniquely identifies each record. Duplicate primary keys are not accepted.

Create a custom schema before adding records that use it.

## Managing records

### Add records

Select **3 — Add data**.

Enter the number of records and provide a unique primary key followed by the values for the schema fields.

Example:

```text
Enter id for entry number1: 101
Enter name (str): Arun
Enter age (int): 18
Enter percentage (float): 93.17
```

Values are checked against the data types defined in the schema.

### View records

Select **4 — View all** to display all records in a formatted table.

### Search

Select **5 — Search** and enter the primary key of the record you want to find.

### Update

Select **6 — Update** and enter the primary key of the record.

Enter new values for the fields you want to change. Press **Enter** without entering a value to retain the existing value.

### Delete

Select **7 — Delete** and enter the primary key of the record.

The application displays the selected record and asks for confirmation before deleting it.

## Export to Excel

Select **8 — Export** to export the active database to an Excel workbook.

For a database named `students`, the output file is:

```text
students.xlsx
```

The workbook contains the record fields as column headers, followed by the stored records. The header row is formatted in bold.

Install `openpyxl` if it is not already installed:

```bash
python3 -m pip install openpyxl
```

## Storage format

registrarY uses Python's built-in JSON serialization for local storage. The file extensions are specific to this project; the contents are JSON.

| File | Purpose |
|---|---|
| `<database_name>.eL` | Stores database records |
| `custom_schema-<database_name>.eLs` | Stores the custom schema |
| `<database_name>.xlsx` | Excel export |

Example:

```text
students.eL
custom_schema-students.eLs
students.xlsx
```

Database and schema files are created in the application's current working directory.

## Project structure

```text
registrarY/
├── registrarY/
│   └── registrarY.py
├── Documents/
│   └── screenshots
├── LICENSE
└── README.md
```

Database files, schema files, and exported workbooks are generated when the application is used.

## Current limitations

- Database records are stored locally; cloud synchronization is not provided.
- The complete JSON database is loaded into memory for operations.
- The application does not provide user authentication or database encryption.
- Supported custom field types are `str`, `int`, and `float`.
- Database backups and automatic recovery are not built in.
- The application is intended for lightweight record management and experimentation, not as a replacement for a production database system.

Keep backups of important database files.

## License

This project is distributed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See the [LICENSE](LICENSE) file for the complete license terms.

## Original project

This repository is a separate fork of:

**[lyashwith/registrarY](https://github.com/lyashwith/registrarY)**

The original project and its author retain their respective attribution. This fork is maintained independently.

## Repository

[![GitHub Repository](https://img.shields.io/badge/GitHub-randomhumanfromearth%2FregistrarY-181717?style=flat&logo=github&logoColor=white)](https://github.com/randomhumanfromearth/registrarY)

If you find this project useful, consider giving it a ⭐.
