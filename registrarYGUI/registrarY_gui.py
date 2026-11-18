"""Modern Tkinter GUI for the original registrarY CLI application.

This GUI deliberately reuses the original registrarY.py persistence, schema,
record-layout, and Excel-export functions without importing its CLI loop.
The original registrarY.py file remains unchanged.
"""
from __future__ import annotations

import ast
import json
import os
import string
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Any

APP_TITLE = "registrarY"
BG = "#0B1220"
SIDEBAR = "#101A2D"
PANEL = "#142238"
PANEL_ALT = "#192B45"
BORDER = "#263A58"
TEXT = "#E8EEF8"
MUTED = "#91A3BC"
ACCENT = "#6697FF"
ACCENT_HOVER = "#80A9FF"
GREEN = "#37C995"
RED = "#FF6B7D"
YELLOW = "#F4C46B"
FONT = ("Inter", 10)
FONT_BOLD = ("Inter", 10, "bold")
FONT_TITLE = ("Inter", 22, "bold")
FONT_SUBTITLE = ("Inter", 11)

DEFAULT_FIELDS = [
    ("Name", "str"),
    ("date_of_birth", "str"),
    ("father_name", "str"),
    ("mother_name", "str"),
]


def load_original_backend(source_path: Path) -> dict[str, Any]:
    """Load selected real functions from registrarY.py without running its CLI.

    The original script executes its interactive menu at module import time.
    Parsing its AST and executing only the reusable function definitions avoids
    that side effect while preserving the project's existing file handling.
    """
    if not source_path.is_file():
        raise FileNotFoundError(
            f"Cannot find {source_path.name}. Keep registrarY_gui.py beside "
            "the original registrarY.py file."
        )
    source = source_path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(source_path))
    wanted = {
        "dump_database",
        "load_database",
        "load_custom_schema",
        "table_loader",
        "export_file_as_excel",
    }
    selected = [
        node for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        and node.name in wanted
    ]
    found = {node.name for node in selected}
    missing = wanted - found
    if missing:
        raise RuntimeError(
            "The original registrarY.py is missing expected functions: "
            + ", ".join(sorted(missing))
        )
    namespace: dict[str, Any] = {
        "dump": json.dump,
        "load": json.load,
        "database_name": "",
    }
    module = ast.Module(body=selected, type_ignores=[])
    exec(compile(module, str(source_path), "exec"), namespace)
    return namespace


class RegistrarYApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("registrarY | Records Workspace")
        self.geometry("1280x790")
        self.minsize(1050, 680)
        self.configure(bg=BG)

        self.data_dir = Path.cwd()
        self.database_name: str | None = None
        self.backend: dict[str, Any] = {}
        self.current_page = "Dashboard"
        self.search_var = tk.StringVar()
        self.db_label_var = tk.StringVar(value="No database selected")
        self.location_var = tk.StringVar(value=str(self.data_dir))
        self.status_var = tk.StringVar(value="Ready")
        self.field_rows: list[tuple[ttk.Entry, ttk.Combobox]] = []
        self._style()
        self._build_shell()
        self.show_page("Dashboard")
        self.refresh_database_badge()

    # ---------- styling / shell ----------
    def _style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TFrame", background=BG)
        style.configure("Panel.TFrame", background=PANEL)
        style.configure("TLabel", background=BG, foreground=TEXT, font=FONT)
        style.configure("Muted.TLabel", background=BG, foreground=MUTED, font=FONT)
        style.configure("Panel.TLabel", background=PANEL, foreground=TEXT, font=FONT)
        style.configure("PanelMuted.TLabel", background=PANEL, foreground=MUTED, font=FONT)
        style.configure("Title.TLabel", background=BG, foreground=TEXT, font=FONT_TITLE)
        style.configure("Subtitle.TLabel", background=BG, foreground=MUTED, font=FONT_SUBTITLE)
        style.configure("CardValue.TLabel", background=PANEL, foreground=TEXT, font=("Inter", 24, "bold"))
        style.configure("CardLabel.TLabel", background=PANEL, foreground=MUTED, font=("Inter", 9, "bold"))
        style.configure("TButton", font=FONT_BOLD, padding=(12, 9), background=PANEL_ALT, foreground=TEXT, borderwidth=0)
        style.map("TButton", background=[("active", BORDER), ("disabled", PANEL)], foreground=[("disabled", MUTED)])
        style.configure("Accent.TButton", background=ACCENT, foreground="#081323", padding=(14, 10))
        style.map("Accent.TButton", background=[("active", ACCENT_HOVER)])
        style.configure("Danger.TButton", background="#542638", foreground="#FFDDE2")
        style.map("Danger.TButton", background=[("active", "#713044")])
        style.configure("Nav.TButton", anchor="w", background=SIDEBAR, foreground=MUTED, padding=(16, 12), font=FONT_BOLD)
        style.map("Nav.TButton", background=[("active", PANEL_ALT)], foreground=[("active", TEXT)])
        style.configure("Treeview", background=PANEL, fieldbackground=PANEL, foreground=TEXT, borderwidth=0, rowheight=34, font=FONT)
        style.configure("Treeview.Heading", background=PANEL_ALT, foreground=MUTED, relief="flat", font=("Inter", 9, "bold"), padding=(10, 10))
        style.map("Treeview", background=[("selected", "#29456F")], foreground=[("selected", "#FFFFFF")])
        style.configure("TEntry", padding=9, fieldbackground="#0E1A2C", foreground=TEXT, insertcolor=TEXT)
        style.configure("TCombobox", padding=8, fieldbackground="#0E1A2C", foreground=TEXT)
        style.configure("Vertical.TScrollbar", background=PANEL_ALT, troughcolor=BG, bordercolor=BG, arrowcolor=MUTED)

    def _build_shell(self) -> None:
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=238, highlightthickness=1, highlightbackground=BORDER)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(25, 28))
        mark = tk.Canvas(brand, width=42, height=42, bg=SIDEBAR, highlightthickness=0)
        mark.pack(side="left")
        mark.create_rectangle(3, 3, 39, 39, fill=ACCENT, outline="")
        mark.create_text(21, 21, text="rY", fill="#081323", font=("Inter", 15, "bold"))
        title_box = tk.Frame(brand, bg=SIDEBAR)
        title_box.pack(side="left", padx=11)
        tk.Label(title_box, text="registrarY", bg=SIDEBAR, fg=TEXT, font=("Inter", 17, "bold")).pack(anchor="w")
        tk.Label(title_box, text="RECORDS WORKSPACE", bg=SIDEBAR, fg=MUTED, font=("Inter", 7, "bold")).pack(anchor="w", pady=(2, 0))

        tk.Label(self.sidebar, text="WORKSPACE", bg=SIDEBAR, fg="#607591", font=("Inter", 8, "bold")).pack(anchor="w", padx=23, pady=(4, 9))
        self.nav_buttons: dict[str, ttk.Button] = {}
        for name, glyph in [("Dashboard", "◫"), ("Records", "▤"), ("Add record", "+"), ("Schema", "⌘"), ("Help", "?")]:
            btn = ttk.Button(self.sidebar, text=f"  {glyph}     {name}", style="Nav.TButton", command=lambda p=name: self.show_page(p))
            btn.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = btn

        divider = tk.Frame(self.sidebar, bg=BORDER, height=1)
        divider.pack(fill="x", padx=22, pady=(22, 18))
        tk.Label(self.sidebar, text="DATABASE", bg=SIDEBAR, fg="#607591", font=("Inter", 8, "bold")).pack(anchor="w", padx=23, pady=(0, 8))
        ttk.Button(self.sidebar, text="＋   New database", style="Accent.TButton", command=self.new_database).pack(fill="x", padx=17, pady=4)
        ttk.Button(self.sidebar, text="↗   Open database", style="Nav.TButton", command=self.open_database).pack(fill="x", padx=12, pady=4)
        ttk.Button(self.sidebar, text="▣   Change folder", style="Nav.TButton", command=self.change_folder).pack(fill="x", padx=12, pady=4)

        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=20, pady=20)
        tk.Frame(bottom, bg=BORDER, height=1).pack(fill="x", pady=(0, 12))
        tk.Label(bottom, text="LOCAL JSON STORAGE", bg=SIDEBAR, fg="#607591", font=("Inter", 8, "bold")).pack(anchor="w")
        tk.Label(bottom, text="Your data stays on this device.", bg=SIDEBAR, fg=MUTED, font=("Inter", 8)).pack(anchor="w", pady=(5, 0))

        self.main = tk.Frame(self, bg=BG)
        self.main.grid(row=0, column=1, sticky="nsew")
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(1, weight=1)
        header = tk.Frame(self.main, bg=BG)
        header.grid(row=0, column=0, sticky="ew", padx=34, pady=(25, 16))
        header.grid_columnconfigure(0, weight=1)
        self.page_title = tk.Label(header, text="Dashboard", bg=BG, fg=TEXT, font=FONT_TITLE)
        self.page_title.grid(row=0, column=0, sticky="w")
        self.page_subtitle = tk.Label(header, text="A clear view of your active records.", bg=BG, fg=MUTED, font=FONT_SUBTITLE)
        self.page_subtitle.grid(row=1, column=0, sticky="w", pady=(5, 0))
        dbbox = tk.Frame(header, bg=PANEL, highlightthickness=1, highlightbackground=BORDER, padx=13, pady=9)
        dbbox.grid(row=0, column=1, rowspan=2, sticky="e")
        tk.Label(dbbox, text="ACTIVE DATABASE", bg=PANEL, fg=MUTED, font=("Inter", 7, "bold")).pack(anchor="w")
        self.db_badge = tk.Label(dbbox, textvariable=self.db_label_var, bg=PANEL, fg=TEXT, font=FONT_BOLD)
        self.db_badge.pack(anchor="w", pady=(3, 0))

        self.content = tk.Frame(self.main, bg=BG)
        self.content.grid(row=1, column=0, sticky="nsew", padx=34, pady=(0, 18))
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(0, weight=1)

        footer = tk.Frame(self.main, bg=BG)
        footer.grid(row=2, column=0, sticky="ew", padx=34, pady=(0, 15))
        tk.Frame(footer, bg=BORDER, height=1).pack(fill="x", pady=(0, 10))
        tk.Label(footer, textvariable=self.location_var, bg=BG, fg="#71839D", font=("Inter", 8)).pack(side="left")
        tk.Label(footer, textvariable=self.status_var, bg=BG, fg=GREEN, font=("Inter", 8, "bold")).pack(side="right")

    # ---------- database / backend ----------
    def _load_backend(self) -> None:
        source = Path(__file__).with_name("registrarY.py")
        self.backend = load_original_backend(source)
        self._sync_backend_globals()

    def _sync_backend_globals(self) -> None:
        self.backend["database_name"] = self.database_name or ""

    def require_database(self) -> bool:
        if not self.database_name:
            messagebox.showinfo("Choose a database", "Create a new database or open an existing .eL file first.", parent=self)
            return False
        return True

    def refresh_database_badge(self) -> None:
        self.db_label_var.set(self.database_name or "No database selected")
        self.location_var.set(str(self.data_dir))

    def _db_path(self) -> Path:
        assert self.database_name
        return self.data_dir / f"{self.database_name}.eL"

    def load_db(self) -> dict[str, Any]:
        self._sync_backend_globals()
        return self.backend["load_database"]()

    def save_db(self, data: dict[str, Any]) -> None:
        self._sync_backend_globals()
        self.backend["dump_database"](data)

    def load_schema(self) -> dict[str, Any]:
        if not self.database_name:
            return {}
        self._sync_backend_globals()
        return self.backend["load_custom_schema"]()

    def _get_fields(self, db: dict[str, Any] | None = None) -> tuple[str, list[tuple[str, str]]]:
        schema = self.load_schema()
        if schema:
            key = next(iter(schema))
            return key, [(name, dtype) for name, dtype in schema[key].items()]
        data = db if db is not None else (self.load_db() if self.database_name else {})
        fields: list[str] = []
        for record in data.values():
            if isinstance(record, dict):
                for name in record:
                    if name not in fields:
                        fields.append(name)
        if not fields:
            fields = [name for name, _ in DEFAULT_FIELDS]
        inferred: list[tuple[str, str]] = []
        sample = next((r for r in data.values() if isinstance(r, dict)), {})
        for name in fields:
            value = sample.get(name, "")
            dtype = "int" if isinstance(value, int) and not isinstance(value, bool) else "float" if isinstance(value, float) else "str"
            inferred.append((name, dtype))
        return "Roll Number", inferred

    def _records_for_table(self, data: dict[str, Any]) -> tuple[list[str], list[list[Any]]]:
        self._sync_backend_globals()
        return self.backend["table_loader"](data, "all", "")

    # ---------- page routing ----------
    def clear_content(self) -> None:
        for child in self.content.winfo_children():
            child.destroy()

    def show_page(self, page: str) -> None:
        self.current_page = page
        self.clear_content()
        self.page_title.configure(text=page)
        subtitles = {
            "Dashboard": "A clear view of your active records.",
            "Records": "Browse, search, update and remove entries.",
            "Add record": "Add a new entry using the active database structure.",
            "Schema": "Define the fields and data types for a custom database.",
            "Help": "A quick guide to the registrarY workspace.",
        }
        self.page_subtitle.configure(text=subtitles.get(page, "Manage your records."))
        for name, btn in self.nav_buttons.items():
            btn.configure(style="Accent.TButton" if name == page else "Nav.TButton")
        if page == "Dashboard":
            self._dashboard_page()
        elif page == "Records":
            self._records_page()
        elif page == "Add record":
            self._add_page()
        elif page == "Schema":
            self._schema_page()
        else:
            self._help_page()

    def _panel(self, parent: tk.Widget, **kwargs: Any) -> tk.Frame:
        return tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=BORDER, **kwargs)

    def _empty_state(self, parent: tk.Widget, title: str, detail: str) -> None:
        box = self._panel(parent, padx=28, pady=34)
        box.pack(fill="both", expand=True)
        tk.Label(box, text="▤", bg=PANEL, fg=ACCENT, font=("Inter", 34)).pack(pady=(0, 12))
        tk.Label(box, text=title, bg=PANEL, fg=TEXT, font=("Inter", 16, "bold")).pack()
        tk.Label(box, text=detail, bg=PANEL, fg=MUTED, font=FONT, justify="center", wraplength=570).pack(pady=(8, 20))
        actions = tk.Frame(box, bg=PANEL)
        actions.pack()
        ttk.Button(actions, text="＋  Create database", style="Accent.TButton", command=self.new_database).pack(side="left", padx=5)
        ttk.Button(actions, text="Open existing", command=self.open_database).pack(side="left", padx=5)

    def _dashboard_page(self) -> None:
        if not self.database_name:
            self._empty_state(self.content, "Welcome to registrarY", "Create a database or open an existing .eL file to start managing records. The GUI uses the same JSON storage and schema files as the original CLI.")
            return
        db = self.load_db()
        key, fields = self._get_fields(db)
        top = tk.Frame(self.content, bg=BG)
        top.pack(fill="x", pady=(0, 18))
        cards = [("TOTAL RECORDS", f"{len(db):,}", "Saved entries"), ("DATA FIELDS", str(len(fields)), "Active columns"), ("DATABASE TYPE", "CUSTOM" if self.load_schema() else "STANDARD", "Current structure")]
        for i, (label, value, note) in enumerate(cards):
            card = self._panel(top, padx=20, pady=17)
            card.pack(side="left", fill="both", expand=True, padx=(0 if i == 0 else 10, 0))
            tk.Label(card, text=label, bg=PANEL, fg=MUTED, font=("Inter", 8, "bold")).pack(anchor="w")
            tk.Label(card, text=value, bg=PANEL, fg=TEXT, font=("Inter", 25, "bold")).pack(anchor="w", pady=(7, 2))
            tk.Label(card, text=note, bg=PANEL, fg="#7287A4", font=("Inter", 8)).pack(anchor="w")

        row = tk.Frame(self.content, bg=BG)
        row.pack(fill="both", expand=True)
        heading = tk.Frame(row, bg=BG)
        heading.pack(fill="x", pady=(0, 10))
        tk.Label(heading, text="Recent records", bg=BG, fg=TEXT, font=("Inter", 14, "bold")).pack(side="left")
        ttk.Button(heading, text="Export Excel", command=self.export_excel).pack(side="right")
        ttk.Button(heading, text="Create default students", command=self.create_default_wizard).pack(side="right", padx=7)
        ttk.Button(heading, text="View all records  →", command=lambda: self.show_page("Records")).pack(side="right", padx=7)
        self._build_table(row, db, height=10)

    def _build_table(self, parent: tk.Widget, db: dict[str, Any], height: int = 13) -> ttk.Treeview:
        wrap = self._panel(parent, padx=1, pady=1)
        wrap.pack(fill="both", expand=True)
        headers, rows = self._records_for_table(db)
        if not headers:
            headers = ["Primary Key"]
        tree = ttk.Treeview(wrap, columns=headers, show="headings", height=height)
        for col in headers:
            tree.heading(col, text=col)
            tree.column(col, width=max(120, min(240, 950 // max(1, len(headers)))), minwidth=90, stretch=True)
        tree.pack(side="left", fill="both", expand=True, padx=(8, 0), pady=8)
        scrollbar = ttk.Scrollbar(wrap, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 7), pady=8)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.tag_configure("odd", background="#172841")
        tree.tag_configure("even", background=PANEL)
        for index, row in enumerate(rows):
            tree.insert("", "end", iid=str(index), values=[self._display_value(v) for v in row], tags=("odd" if index % 2 else "even",))
        return tree

    @staticmethod
    def _display_value(value: Any) -> str:
        text = str(value)
        return text if len(text) <= 110 else text[:107] + "..."

    def _records_page(self) -> None:
        if not self.require_database():
            self._empty_state(self.content, "No database open", "Open a database to view its records.")
            return
        bar = tk.Frame(self.content, bg=BG)
        bar.pack(fill="x", pady=(0, 12))
        search = ttk.Entry(bar, textvariable=self.search_var, width=34)
        search.pack(side="left", ipady=3)
        search.insert(0, "")
        search.bind("<Return>", lambda _e: self.refresh_records())
        ttk.Button(bar, text="Search", style="Accent.TButton", command=self.refresh_records).pack(side="left", padx=7)
        ttk.Button(bar, text="Clear", command=self.clear_search).pack(side="left")
        ttk.Button(bar, text="＋ Add record", command=lambda: self.show_page("Add record")).pack(side="right")
        ttk.Button(bar, text="Delete selected", style="Danger.TButton", command=self.delete_selected).pack(side="right", padx=7)
        ttk.Button(bar, text="Edit selected", command=self.edit_selected).pack(side="right", padx=7)
        self.records_host = tk.Frame(self.content, bg=BG)
        self.records_host.pack(fill="both", expand=True)
        self.refresh_records()

    def refresh_records(self) -> None:
        if not hasattr(self, "records_host") or not self.records_host.winfo_exists():
            return
        for child in self.records_host.winfo_children():
            child.destroy()
        db = self.load_db()
        query = self.search_var.get().strip().lower()
        if query:
            db = {k: v for k, v in db.items() if query in str(k).lower() or (isinstance(v, dict) and any(query in str(x).lower() for x in v.values()))}
        if not db:
            self._empty_state(self.records_host, "No matching records", "Try a different search, or add a new record.")
            return
        self.records_tree = self._build_table(self.records_host, db, height=15)
        self._visible_keys = list(db.keys())
        self.records_tree.bind("<Double-1>", lambda _e: self.edit_selected())

    def clear_search(self) -> None:
        self.search_var.set("")
        self.refresh_records()

    def _selected_key(self) -> str | None:
        tree = getattr(self, "records_tree", None)
        if tree is None or not tree.winfo_exists():
            return None
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Select a record", "Select a record in the table first.", parent=self)
            return None
        index = int(selected[0])
        if index >= len(getattr(self, "_visible_keys", [])):
            return None
        return self._visible_keys[index]

    # ---------- CRUD ----------
    @staticmethod
    def _coerce(raw: str, dtype: str) -> Any:
        if dtype == "int":
            return int(raw)
        if dtype == "float":
            return float(raw)
        return raw

    def _next_roll_number(self, existing: dict[str, Any]) -> str:
        for i in range(26 * 1000):
            idx = i
            candidate = string.ascii_uppercase[idx // 1000] + f"{(idx % 1000) + 1:04d}"
            if candidate not in existing:
                return candidate
        raise ValueError("The existing roll-number format supports at most 26,000 records.")

    def _add_form_fields(self, parent: tk.Widget, fields: list[tuple[str, str]], initial: dict[str, Any] | None = None) -> dict[str, ttk.Entry]:
        entries: dict[str, ttk.Entry] = {}
        for i, (field, dtype) in enumerate(fields):
            line = tk.Frame(parent, bg=PANEL)
            line.pack(fill="x", pady=7)
            tk.Label(line, text=field, bg=PANEL, fg=TEXT, font=FONT_BOLD, width=22, anchor="w").pack(side="left")
            entry = ttk.Entry(line)
            entry.pack(side="left", fill="x", expand=True, ipady=3)
            if initial is not None and field in initial:
                entry.insert(0, str(initial[field]))
            entry._registrary_dtype = dtype  # type: ignore[attr-defined]
            entries[field] = entry
        return entries

    def _add_page(self) -> None:
        if not self.require_database():
            self._empty_state(self.content, "No database open", "Create or open a database before adding records.")
            return
        db = self.load_db()
        primary_key_name, fields = self._get_fields(db)
        is_default = not bool(self.load_schema())
        outer = self._panel(self.content, padx=24, pady=22)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="New record", bg=PANEL, fg=TEXT, font=("Inter", 16, "bold")).pack(anchor="w")
        description = "The roll number is generated automatically using registrarY's A0001 format." if is_default else f"Enter a unique value for {primary_key_name}, then complete the schema fields."
        tk.Label(outer, text=description, bg=PANEL, fg=MUTED, font=FONT).pack(anchor="w", pady=(5, 18))
        key_entry: ttk.Entry | None = None
        if not is_default:
            line = tk.Frame(outer, bg=PANEL)
            line.pack(fill="x", pady=(0, 8))
            tk.Label(line, text=primary_key_name, bg=PANEL, fg=TEXT, font=FONT_BOLD, width=22, anchor="w").pack(side="left")
            key_entry = ttk.Entry(line)
            key_entry.pack(side="left", fill="x", expand=True, ipady=3)
        entries = self._add_form_fields(outer, fields)

        def save() -> None:
            try:
                data = self.load_db()
                if is_default:
                    key = self._next_roll_number(data)
                else:
                    assert key_entry is not None
                    key = key_entry.get().strip()
                    if not key:
                        raise ValueError(f"{primary_key_name} cannot be empty.")
                if key in data:
                    raise ValueError(f"Record {key} already exists.")
                record: dict[str, Any] = {}
                for field, entry in entries.items():
                    value = self._coerce(entry.get().strip(), getattr(entry, "_registrary_dtype", "str"))
                    record[field] = value
                data[key] = record
                self.save_db(data)
                self.status_var.set(f"Saved record {key}")
                messagebox.showinfo("Record saved", f"Record {key} was saved successfully.", parent=self)
                self.show_page("Records")
            except ValueError as exc:
                messagebox.showerror("Check the form", str(exc), parent=self)
            except Exception as exc:
                messagebox.showerror("Unable to save", str(exc), parent=self)

        actions = tk.Frame(outer, bg=PANEL)
        actions.pack(fill="x", pady=(22, 0))
        ttk.Button(actions, text="Save record", style="Accent.TButton", command=save).pack(side="left")
        ttk.Button(actions, text="Cancel", command=lambda: self.show_page("Records")).pack(side="left", padx=8)

    def edit_selected(self) -> None:
        key = self._selected_key()
        if key is None:
            return
        data = self.load_db()
        record = data.get(key)
        if not isinstance(record, dict):
            messagebox.showerror("Invalid record", "This record does not contain a valid object and cannot be edited.", parent=self)
            return
        schema = self.load_schema()
        schema_key = next(iter(schema), None)
        fields = []
        for name, value in record.items():
            dtype = schema.get(schema_key, {}).get(name) if schema_key else None
            if dtype is None:
                dtype = "int" if isinstance(value, int) and not isinstance(value, bool) else "float" if isinstance(value, float) else "str"
            fields.append((name, dtype))
        dialog = tk.Toplevel(self)
        dialog.title(f"Edit record · {key}")
        dialog.configure(bg=BG)
        dialog.geometry("560x520")
        dialog.transient(self)
        dialog.grab_set()
        body = tk.Frame(dialog, bg=PANEL, padx=24, pady=22, highlightthickness=1, highlightbackground=BORDER)
        body.pack(fill="both", expand=True, padx=18, pady=18)
        tk.Label(body, text=f"Edit record  {key}", bg=PANEL, fg=TEXT, font=("Inter", 16, "bold")).pack(anchor="w", pady=(0, 6))
        tk.Label(body, text="Update the values below. The primary key stays unchanged.", bg=PANEL, fg=MUTED, font=FONT).pack(anchor="w", pady=(0, 16))
        entries = self._add_form_fields(body, fields, record)

        def save() -> None:
            try:
                updated = dict(record)
                for field, entry in entries.items():
                    updated[field] = self._coerce(entry.get().strip(), getattr(entry, "_registrary_dtype", "str"))
                latest = self.load_db()
                if key not in latest:
                    raise ValueError("This record was removed by another action.")
                latest[key] = updated
                self.save_db(latest)
                dialog.destroy()
                self.status_var.set(f"Updated record {key}")
                self.refresh_records()
            except ValueError as exc:
                messagebox.showerror("Invalid value", str(exc), parent=dialog)

        ttk.Button(body, text="Save changes", style="Accent.TButton", command=save).pack(anchor="w", pady=(18, 0))

    def delete_selected(self) -> None:
        key = self._selected_key()
        if key is None:
            return
        if not messagebox.askyesno("Delete record", f"Permanently delete record {key}?", icon="warning", parent=self):
            return
        data = self.load_db()
        if key in data:
            del data[key]
            self.save_db(data)
            self.status_var.set(f"Deleted record {key}")
            self.refresh_records()

    # ---------- schema / database management ----------
    def _schema_page(self) -> None:
        if not self.require_database():
            self._empty_state(self.content, "No database open", "Open or create a database to define its custom schema.")
            return
        existing = self.load_schema()
        outer = self._panel(self.content, padx=24, pady=22)
        outer.pack(fill="both", expand=True)
        tk.Label(outer, text="Custom schema designer", bg=PANEL, fg=TEXT, font=("Inter", 16, "bold")).pack(anchor="w")
        tk.Label(outer, text="Fields are saved in the original custom_schema-<database>.eLs format.", bg=PANEL, fg=MUTED, font=FONT).pack(anchor="w", pady=(5, 17))
        keyline = tk.Frame(outer, bg=PANEL)
        keyline.pack(fill="x", pady=(0, 14))
        tk.Label(keyline, text="Primary key", bg=PANEL, fg=TEXT, font=FONT_BOLD, width=18, anchor="w").pack(side="left")
        key_entry = ttk.Entry(keyline)
        key_entry.pack(side="left", fill="x", expand=True, ipady=3)
        if existing:
            key_entry.insert(0, next(iter(existing)))
        tk.Frame(outer, bg=BORDER, height=1).pack(fill="x", pady=(2, 12))
        tk.Label(outer, text="FIELDS", bg=PANEL, fg=MUTED, font=("Inter", 8, "bold")).pack(anchor="w", pady=(0, 6))
        rows_host = tk.Frame(outer, bg=PANEL)
        rows_host.pack(fill="x")
        self.field_rows = []

        def add_field(name: str = "", dtype: str = "str") -> None:
            row = tk.Frame(rows_host, bg=PANEL)
            row.pack(fill="x", pady=4)
            entry = ttk.Entry(row)
            entry.pack(side="left", fill="x", expand=True, ipady=3)
            entry.insert(0, name)
            combo = ttk.Combobox(row, values=("str", "int", "float"), state="readonly", width=10)
            combo.set(dtype if dtype in ("str", "int", "float") else "str")
            combo.pack(side="left", padx=(9, 9))
            ttk.Button(row, text="Remove", command=lambda: remove_field(row, entry, combo)).pack(side="left")
            self.field_rows.append((entry, combo))

        def remove_field(row: tk.Widget, entry: ttk.Entry, combo: ttk.Combobox) -> None:
            self.field_rows = [(e, c) for e, c in self.field_rows if e is not entry]
            row.destroy()

        if existing:
            k = next(iter(existing))
            for name, dtype in existing[k].items():
                add_field(name, dtype)
        else:
            add_field("name", "str")
            add_field("age", "int")
        tools = tk.Frame(outer, bg=PANEL)
        tools.pack(fill="x", pady=(12, 0))
        ttk.Button(tools, text="＋ Add field", command=add_field).pack(side="left")

        def save_schema() -> None:
            key = key_entry.get().strip()
            schema: dict[str, dict[str, str]] = {key: {}}
            if not key:
                messagebox.showerror("Invalid schema", "Primary key name cannot be empty.", parent=self)
                return
            try:
                for entry, combo in self.field_rows:
                    name, dtype = entry.get().strip(), combo.get()
                    if not name or name == key:
                        raise ValueError("Field names must be non-empty and cannot match the primary key.")
                    if name in schema[key]:
                        raise ValueError(f"Duplicate field name: {name}")
                    if dtype not in ("str", "int", "float"):
                        raise ValueError(f"Unsupported data type: {dtype}")
                    schema[key][name] = dtype
                if not schema[key]:
                    raise ValueError("Add at least one field.")
                path = self.data_dir / f"custom_schema-{self.database_name}.eLs"
                path.write_text(json.dumps(schema, indent=4), encoding="utf-8")
                self.status_var.set("Custom schema saved")
                messagebox.showinfo("Schema saved", f"Saved {path.name}.", parent=self)
                self.show_page("Dashboard")
            except ValueError as exc:
                messagebox.showerror("Invalid schema", str(exc), parent=self)

        ttk.Button(tools, text="Save schema", style="Accent.TButton", command=save_schema).pack(side="right")
        if existing:
            tk.Label(outer, text="Saving a new schema changes how future records are entered. Existing records are not rewritten.", bg=PANEL, fg=YELLOW, font=("Inter", 8)).pack(anchor="w", pady=(16, 0))

    def new_database(self) -> None:
        name = simpledialog.askstring("New database", "Enter a database name (without .eL):", parent=self)
        if name is None:
            return
        name = name.strip()
        invalid = not name or name in (".", "..") or any(char in name for char in '/\\:*?"<>|') or any(ord(char) < 32 for char in name)
        if invalid:
            messagebox.showerror("Invalid name", "Use a simple database name without path separators or special characters.", parent=self)
            return
        path = self.data_dir / f"{name}.eL"
        if path.exists():
            if not messagebox.askyesno("Database exists", f"{path.name} already exists. Open it?", parent=self):
                return
        else:
            path.write_text("{}", encoding="utf-8")
        os.chdir(self.data_dir)
        self.database_name = name
        self._load_backend()
        self.refresh_database_badge()
        self.status_var.set(f"Opened {name}")
        self.show_page("Dashboard")

    def open_database(self) -> None:
        path = filedialog.askopenfilename(
            parent=self,
            title="Open registrarY database",
            initialdir=str(self.data_dir),
            filetypes=[("registrarY databases", "*.eL"), ("All files", "*.*")],
        )
        if not path:
            return
        selected = Path(path)
        try:
            payload = json.loads(selected.read_text(encoding="utf-8"))
            if payload is None:
                payload = {}
            if not isinstance(payload, dict):
                raise ValueError("The selected file does not contain a JSON object.")
        except Exception as exc:
            messagebox.showerror("Cannot open database", str(exc), parent=self)
            return
        self.data_dir = selected.parent
        os.chdir(self.data_dir)
        self.database_name = selected.stem
        self._load_backend()
        self.refresh_database_badge()
        self.status_var.set(f"Opened {selected.name}")
        self.show_page("Dashboard")

    def change_folder(self) -> None:
        folder = filedialog.askdirectory(parent=self, title="Choose the folder containing .eL databases", initialdir=str(self.data_dir))
        if not folder:
            return
        self.data_dir = Path(folder)
        os.chdir(self.data_dir)
        self.database_name = None
        self.backend = {}
        self.refresh_database_badge()
        self.status_var.set("Database folder changed")
        self.show_page("Dashboard")

    def create_default_wizard(self) -> None:
        if not self.require_database():
            return
        if self.load_schema():
            messagebox.showwarning("Custom schema is active", "This database has a custom schema. Create default student records in a separate database without a custom schema.", parent=self)
            return
        count = simpledialog.askinteger("Create default student records", "How many student records should be created?", minvalue=1, maxvalue=26000, parent=self)
        if count is None:
            return
        dialog = tk.Toplevel(self)
        dialog.title("Default student records")
        dialog.configure(bg=BG)
        dialog.geometry("570x510")
        dialog.transient(self)
        dialog.grab_set()
        panel = tk.Frame(dialog, bg=PANEL, padx=24, pady=22, highlightthickness=1, highlightbackground=BORDER)
        panel.pack(fill="both", expand=True, padx=16, pady=16)
        state = {"index": 0, "records": []}
        progress = tk.Label(panel, text=f"Student 1 of {count}", bg=PANEL, fg=ACCENT, font=FONT_BOLD)
        progress.pack(anchor="w")
        tk.Label(panel, text="Create default student database", bg=PANEL, fg=TEXT, font=("Inter", 16, "bold")).pack(anchor="w", pady=(8, 5))
        tk.Label(panel, text="Each student receives the same sequential roll-number format as the original CLI.", bg=PANEL, fg=MUTED, font=FONT, wraplength=480).pack(anchor="w", pady=(0, 16))
        entries = self._add_form_fields(panel, DEFAULT_FIELDS)
        action = tk.Frame(panel, bg=PANEL)
        action.pack(fill="x", pady=(20, 0))

        def next_student() -> None:
            try:
                record = {name: self._coerce(entry.get().strip(), "str") for name, entry in entries.items()}
                if any(not str(value).strip() for value in record.values()):
                    raise ValueError("Complete all four student fields before continuing.")
                state["records"].append(record)
                state["index"] += 1
                if state["index"] >= count:
                    database = self.load_db()
                    for record in state["records"]:
                        key = self._next_roll_number(database)
                        database[key] = record
                    self.save_db(database)
                    dialog.destroy()
                    self.status_var.set(f"Created {count} student record(s)")
                    messagebox.showinfo("Default records created", f"Saved {count} student record(s) to {self.database_name}.eL.", parent=self)
                    self.show_page("Dashboard")
                    return
                progress.configure(text=f"Student {state['index'] + 1} of {count}")
                for entry in entries.values():
                    entry.delete(0, "end")
            except ValueError as exc:
                messagebox.showerror("Check the form", str(exc), parent=dialog)

        ttk.Button(action, text="Save student & continue", style="Accent.TButton", command=next_student).pack(side="left")
        ttk.Button(action, text="Cancel", command=dialog.destroy).pack(side="left", padx=8)

    def export_excel(self) -> None:
        if not self.require_database():
            return
        try:
            self._sync_backend_globals()
            self.backend["export_file_as_excel"](self.load_db())
            output = self.data_dir / f"{self.database_name}.xlsx"
            self.status_var.set(f"Exported {output.name}")
            messagebox.showinfo("Export complete", f"Excel file saved to:\n{output}", parent=self)
        except ImportError:
            messagebox.showerror("openpyxl is required", "Install it with: python -m pip install openpyxl", parent=self)
        except Exception as exc:
            messagebox.showerror("Export failed", str(exc), parent=self)

    def _help_page(self) -> None:
        panel = self._panel(self.content, padx=25, pady=23)
        panel.pack(fill="both", expand=True)
        tk.Label(panel, text="Built around your original registrarY backend", bg=PANEL, fg=TEXT, font=("Inter", 16, "bold")).pack(anchor="w")
        tk.Label(panel, text="The GUI reads and writes the exact same file types as the CLI. It does not create a second database format.", bg=PANEL, fg=MUTED, font=FONT, wraplength=750, justify="left").pack(anchor="w", pady=(7, 19))
        items = [
            ("Database files", "<name>.eL — JSON object containing the records."),
            ("Custom schema", "custom_schema-<name>.eLs — primary key and field data types."),
            ("Default records", "Name, date_of_birth, father_name and mother_name with generated A0001-style keys."),
            ("Supported types", "str, int and float for custom schema fields."),
            ("Excel export", "Exports the active database to <name>.xlsx using openpyxl."),
            ("CLI compatibility", "The original registrarY.py is kept unchanged; the GUI loads its reusable functions without starting the CLI menu."),
        ]
        for title, detail in items:
            row = tk.Frame(panel, bg=PANEL_ALT, padx=15, pady=12)
            row.pack(fill="x", pady=5)
            tk.Label(row, text=title, bg=PANEL_ALT, fg=ACCENT_HOVER, font=FONT_BOLD).pack(anchor="w")
            tk.Label(row, text=detail, bg=PANEL_ALT, fg=TEXT, font=FONT, justify="left", wraplength=760).pack(anchor="w", pady=(4, 0))
        actions = tk.Frame(panel, bg=PANEL)
        actions.pack(fill="x", pady=(18, 0))
        ttk.Button(actions, text="Export current database", style="Accent.TButton", command=self.export_excel).pack(side="left")
        ttk.Button(actions, text="Create default student records", command=self.create_default_wizard).pack(side="left", padx=8)


def main() -> None:
    try:
        app = RegistrarYApp()
    except Exception as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("registrarY could not start", str(exc), parent=root)
        root.destroy()
        raise
    app.mainloop()


if __name__ == "__main__":
    main()
