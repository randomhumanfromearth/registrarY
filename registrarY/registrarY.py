
    
  

    schema = active_schema(database)
    if not schema:
        print("No schema is available; cannot safely update this record.")
        return
    primary_key_name, fields = next(iter(schema.items()))

    search_database(primary_key)
    print("Enter new values, or press ENTER to keep the current value.")
    record = database[primary_key]
    for field_name, data_type in fields.items():
        current = record.get(field_name, "")
        while True:
            new_value = input(f"{field_name} (current: {current}): ")
            if new_value == "":
                break
            try:
                kind = str(data_type).lower()
                if kind in ("str", "string"):
                    record[field_name] = new_value
                elif kind == "int":
                    record[field_name] = int(new_value)
                elif kind == "float":
                    record[field_name] = float(new_value)
                else:
                    print(f"Unsupported data type: {data_type}")
                    break
                break
            except ValueError:
                print(f"Invalid value. Expected {data_type}. Please try again.")

    database[primary_key] = record
    dump_database(database)
    print("Database updated.")
    search_database(primary_key)


def delete_data_database():
    database = load_database()
    primary_key = input("Enter the primary key of the record to delete: ").strip()
    if primary_key not in database:
        print("Primary key not found.")
        return

    search_database(primary_key)
    answer = input(f"Do you want to delete '{primary_key}'? (y/n): ").strip().lower()
    if answer in ("y", "yes"):
        del database[primary_key]
        dump_database(database)
        print("Deletion done.")
    else:
        print("Deletion cancelled.")


def export_file_as_excel(database):
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ImportError:
        print("Excel export requires openpyxl. Install it with: pip install openpyxl")
        return

    headers, rows = table_loader(database)
    if not headers:
        print("Nothing to export: no schema or records found.")
        return

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = database_name[:31] or "Database"
    sheet.append(headers)
    for row in rows:
        sheet.append(row)
    for cell in sheet[1]:
        cell.font = Font(bold=True)

    output = Path(f"{database_name}.xlsx")
    try:
        workbook.save(output)
        print(f"Excel file saved: {output}")
    except OSError as exc:
        print(f"Could not save Excel file: {exc}")


def database_name_taker():
    while True:
        name = input("Enter the name of the database to use: ").strip()
        if not name:
            print("Database name cannot be empty.")
            continue
        # Keep the database files in the current folder; reject path separators.
        if Path(name).name != name or name in (".", ".."):
            print("Please enter a simple database name, not a path.")
            continue

        global database_name
        database_name = name
        if database_path().exists():
            return name

        print(f"Database '{name}' does not exist yet.")
        answer = input("Create a new database? (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            dump_database({})
            return name


def show_help():
    help_data = [
        [1, "Create Default", "Create student records with predefined fields and generated roll numbers."],
        [2, "Create Custom Schema", "Define a primary key and fields using str, int, or float."],
        [3, "Add Data", "Add records matching the active custom schema."],
        [4, "View All", "Display all records."],
        [5, "Search", "Find a record by its primary key."],
        [6, "Update", "Update fields; press ENTER to retain existing values."],
        [7, "Delete", "Delete a record after confirmation."],
        [8, "Export", "Export records to an Excel .xlsx file (requires openpyxl)."],
        [9, "Help", "Display this help."],
        [10, "Exit", "Close registrarY."],
    ]
    print_table(help_data, ["Option", "Command", "Description"])


def main():
    global database_name
    print(registrarY_text, "\n")
    database_name = database_name_taker()
    menu = [
        ["1", "Create default"],
        ["2", "Create custom schema"],
        ["3", "Add data"],
        ["4", "View all"],
        ["5", "Search"],
        ["6", "Update"],
        ["7", "Delete"],
        ["8", "Export"],
        ["9", "Help"],
        ["10", "Exit"],
    ]

    while True:
        print("\nWhat do you want to do? Type 'menu' to show the menu.")
        print_table(menu, ["Option", "Command"])
        option = input("Enter your option/command >>> ").strip().lower()

        try:
            if option in ("create default", "1"):
                create_default_database()
            elif option in ("create custom schema", "2"):
                custom_schema()
            elif option in ("add data", "3"):
                add_custom_data()
            elif option in ("view all", "4"):
                view_all()
            elif option in ("search", "5"):
                search_database(input("Enter primary key to search: ").strip())
            elif option in ("update", "6"):
                update_database()
            elif option in ("del", "delete", "7"):
                delete_data_database()
            elif option in ("export", "8"):
                export_file_as_excel(load_database())
            elif option in ("help", "9"):
                show_help()
            elif option in ("exit", "10"):
                print("Kicking you out of the program...\nDONE.")
                break
            elif option == "menu":
                continue
            else:
                print("Invalid option. Enter a menu number or command.")
        except (OSError, ValueError) as exc:
            print(f"Operation failed: {exc}")
        print("#" * 80)


if __name__ == "__main__":
    main()

