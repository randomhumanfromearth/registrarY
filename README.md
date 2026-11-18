# registrarY

**A lightweight Python-based record management system with CLI, Lite, and GUI editions.**

registrarY helps you create and manage structured databases locally using Python. It supports student records, custom schemas, record management, searching, and Excel export.

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-AGPL--3.0-blue.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?style=flat&logo=github&logoColor=white)](https://github.com/randomhumanfromearth/registrarY)

> **Fork notice:** This repository is an independently maintained fork of [lyashwith/registrarY](https://github.com/lyashwith/registrarY). It builds upon the original project while introducing additional versions and modifications. Development in this repository is independent of the upstream project.

---

## Editions

registrarY provides three editions to suit different preferences.

| Edition | Interface | Description |
|---|---|---|
| **registrarY CLI** | Terminal | The original command-line application for managing databases through an interactive menu. |
| **registrarY Lite** | Lightweight | A streamlined edition intended to provide a lightweight way to use registrarY. |
| **registrarY GUI** | Desktop GUI | A graphical desktop interface for managing records without using terminal menus. |

### 1. registrarY CLI

The original terminal-based application.

Features include:
- Create student databases.
- Define custom database schemas.
- Add, view, search, update, and delete records.
- Export records to Excel.
- Store databases locally in JSON-based files.

Run:

```bash
python3 registrarY/registrarY.py
```

### 2. registrarY Lite

A lightweight edition maintained separately from the main application.

It provides an alternative for users who prefer a smaller, streamlined version of registrarY.

The Lite edition is maintained in:

```text
registrarY-lite/
```

Navigate to that directory and run its main Python entry point.

### 3. registrarY GUI

A desktop graphical interface designed to make database management easier and more accessible.

Instead of navigating terminal menus, users can interact with records through a graphical application.

Planned interface capabilities include:
- Dashboard with database statistics.
- Add and edit records through forms.
- Search and browse database records.
- Delete records with confirmation.
- Manage custom schemas.
- Export records to Excel.
- Open and create database files.

The GUI edition is maintained separately in:

```text
registrarYGUI/
```

It uses Python's Tkinter interface and can be launched independently of the CLI.

---

## Features

- **Student database:** Create and manage student records.
- **Custom schemas:** Define your own primary keys, fields, and data types.
- **Record management:** Add, view, search, update, and delete records.
- **Excel export:** Export database records to `.xlsx` workbooks.
- **Local storage:** Keep database information in local JSON-based files.
- **Multiple editions:** Choose between CLI, Lite, and GUI interfaces.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/randomhumanfromearth/registrarY.git
cd registrarY
```

### CLI edition

Install the required packages:

```bash
python3 -m pip install tabulate openpyxl
```

Run:

```bash
python3 registrarY/registrarY.py
```

### Lite edition

Navigate to the Lite directory:

```bash
cd registrarY-lite
```

Install the dependencies specified for that edition, then run its main Python entry point.

### GUI edition

Install Tkinter on Ubuntu/Debian:

```bash
sudo apt install python3-tk
```

Install the GUI dependencies:

```bash
python3 -m pip install -r registrarYGUI/requirements-gui.txt
```

Launch the GUI from the repository root:

```bash
python3 registrarYGUI/registrarY_gui.py
```

---

## Custom schemas

registrarY supports custom database structures.

For example, a database can use the following schema:

```json
{
    "id": {
        "name": "str",
        "age": "int",
        "percentage": "float"
    }
}
```

Supported data types:

| Type | Description |
|---|---|
| `str` | Text |
| `int` | Integer |
| `float` | Decimal number |

The primary key uniquely identifies each record.

---

## Default student database

The default student database includes:

| Field | Description |
|---|---|
| `Name` | Student's name |
| `date_of_birth` | Date of birth |
| `father_name` | Father's name |
| `mother_name` | Mother's name |

Student roll numbers are automatically generated in this format:

```text
A0001
A0002
A0003
```

---

## Storage

The original CLI edition uses JSON-based local storage.

| File | Purpose |
|---|---|
| `<database_name>.eL` | Database records |
| `custom_schema-<database_name>.eLs` | Custom schema |
| `<database_name>.xlsx` | Excel export |

The file extensions are specific to registrarY; the database and schema contents are JSON.

Keep backups of important database files.

---

## Project structure

```text
registrarY/
│
├── registrarY/
│   └── registrarY.py
│
├── registrarY-lite/
│   └── ...
│
├── registrarYGUI/
│   ├── registrarY_gui.py
│   └── requirements-gui.txt
│
├── Documents/
│   └── screenshots
│
├── LICENSE
└── README.md
```

---

## Original project and attribution

This repository is a separate, independently maintained fork of:

**[lyashwith/registrarY](https://github.com/lyashwith/registrarY)**

The original project is the foundation of this repository. Credit for the original work belongs to its original author.

This fork maintains its own development direction, modifications, and additional editions.

---

## License

Distributed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.

See [LICENSE](LICENSE) for the complete license terms.

---

## Repository

[GitHub – randomhumanfromearth/registrarY](https://github.com/randomhumanfromearth/registrarY)

If you find this project useful, consider giving it a ⭐.
