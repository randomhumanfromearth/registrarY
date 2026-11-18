<div align="center">

# registrarY

**A lightweight, JSON-backed command-line record manager written in Python.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)](#requirements)
[![Storage](https://img.shields.io/badge/Storage-JSON-informational)](#data-storage)
[![License](https://img.shields.io/badge/License-FUNSL%20v1.0-blue)](LICENCE)

*A personal fork of [registrarY](https://github.com/lyashwith/registrarY), maintained at [randomhumanfromearth/registrarY](https://github.com/randomhumanfromearth/registrarY).*

</div>

---

## About

**registrarY** is an interactive terminal application for creating and managing structured records. It can be used as a simple student-record manager or adapted to other kinds of data through custom schemas.

Records are stored locally in JSON format, while the application provides a menu for common database operations such as adding, viewing, searching, updating, deleting, and exporting records.

This repository is a fork of the original registrarY project. It retains attribution to the original author and uses the license included in this repository.

## Features

- **Named databases** — open an existing database or create a new one.
- **Default student records** — create student entries with predefined fields and generated roll numbers.
- **Custom schemas** — define a primary key and fields with supported data types.
- **Record management** — add, view, search, update, and delete records.
- **Duplicate-key protection** — prevent a record from being added with a primary key that already exists.
- **Input validation** — validate supported custom field types and numeric values.
- **Formatted terminal tables** — display records using `tabulate`.
- **Excel export** — export records to `.xlsx` workbooks using `openpyxl`.
- **Interactive menu and help** — access operations through numbered choices or command names.

## Menu

| Option | Operation |
|:---:|---|
| 1 | Create default student records |
| 2 | Create a custom schema |
| 3 | Add records using the custom schema |
| 4 | View all records |
| 5 | Search by primary key |
| 6 | Update a record |
| 7 | Delete a record |
| 8 | Export records to Excel |
| 9 | Display help |
| 10 | Exit |

Type `menu` at the prompt to display the menu again.

## Requirements

- Python 3
- `tabulate` — formatted terminal tables
- `openpyxl` — Excel export

The `json`, `os`, `pathlib`, and `subprocess` modules used by the application are included with Python.

## Installation

### 1. Clone this fork

```bash
git clone https://github.com/randomhumanfromearth/registrarY.git
cd registrarY
```

### 2. Install dependencies

```bash
python -m pip install tabulate openpyxl
```

On some Linux systems, use `python3` instead of `python`.

### 3. Run the application

```bash
python registrarY/registrarY.py
```

## Getting started

When the application starts, enter a database name. For example:

```text
Enter the name of the database to use: students
```

The application looks for a corresponding `students.eL` file. If it does not exist, you can choose to create a new database.

Use a simple database name rather than a filesystem path.

### Create a default student database

Choose **1 — Create default**, then enter the number of student records to create.

The default student record contains:

| Field | Description |
|---|---|
| `Name` | Student's name |
| `date_of_birth` | Date of birth (`DD-MM-YYYY`) |
| `father_name` | Father's name |
| `mother_name` | Mother's name |

Roll numbers are generated sequentially, for example:

```text
A0001
A0002
A0003
```

### Create a custom schema

Choose **2 — Create custom schema**.

First enter the primary-key field name. Then define the record fields as comma-separated `field;type` pairs.

Example:

```text
Primary key: id
Fields: name;str,age;int,percentage;float
```

This creates a schema equivalent to:

```json
{
  "id": {
    "name": "str",
    "age": "int",
    "percentage": "float"
  }
}
```

Supported field types:

| Type | Meaning | Example |
|---|---|---|
| `str` | Text | `"Asha"` |
| `int` | Whole number | `18` |
| `float` | Decimal number | `93.5` |

Create the schema before choosing **3 — Add data**.

### Add records

Choose **3 — Add data**. Enter the primary key and then provide a value for each field in the schema.

Each primary key must be unique in the selected database. A duplicate key is rejected.

### View and search records

- Choose **4 — View all** to display the stored records in a table.
- Choose **5 — Search** and enter a primary key to find one record.

### Update a record

Choose **6 — Update**, then enter the record's primary key.

The application displays the existing values and prompts for replacements. Press **Enter** without entering a value to keep the existing value.

### Delete a record

Choose **7 — Delete**, enter the primary key, and confirm the deletion when prompted.

### Export to Excel

Choose **8 — Export** to create an Excel workbook for the selected database.

For a database named `students`, the output file is:

```text
students.xlsx
```

Excel export requires `openpyxl`:

```bash
python -m pip install openpyxl
```

## Data storage

registrarY uses Python's built-in JSON serialization. The file extensions are project-specific; the contents are JSON.

| File | Purpose |
|---|---|
| `<database_name>.eL` | Stores records |
| `custom_schema-<database_name>.eLs` | Stores the custom schema |
| `<database_name>.xlsx` | Excel export |

For example:

```text
students.eL
custom_schema-students.eLs
students.xlsx
```

Database and schema files are stored locally in the application's working directory. They are not encrypted.

## Project layout

```text
registrarY/
├── Documents/                 # Project screenshots and supporting files
├── registrarY/
│   ├── registrarY.py          # Main Python application
│   ├── database.eL            # Sample/placeholder database
│   └── custom_schema-database.eLs
├── registrarY-lite/
│   └── registrarY-lite.pyx    # Lite/Cython source file
├── LICENCE
└── README.md
```

## Important notes

- This is a small local record-management project, not a full database server.
- The database is loaded into memory while operations are performed.
- There is no built-in authentication, encryption, cloud sync, or multi-user access control.
- Keep backups of `.eL` and `.eLs` files before making significant changes.
- Do not use the current application to store sensitive or confidential information.
- Review the source code before running it, especially when using code obtained from a public repository.

## Known repository note

The Python file currently present at `registrarY/registrarY.py` should be checked before running: the version inspected while preparing this README appeared to begin partway through a function rather than with the complete program. Make sure the complete, tested application source is committed to that path before treating the installation instructions above as ready to run.

## License and attribution

This fork includes the `LICENCE` file. Read that file for the complete **Free Use, No-Sale License (FUNSL) v1.0** terms.

The original project is by **Yashwith L**:

- Original repository: https://github.com/lyashwith/registrarY
- This fork: https://github.com/randomhumanfromearth/registrarY

This fork does not claim original authorship of the upstream project. Changes made in this fork should be distinguished from the original work.

---

<div align="center">

**registrarY — simple records, managed locally.**

</div>
