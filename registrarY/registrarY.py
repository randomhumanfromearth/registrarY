        headers,table_list=table_loader(database,"single",primary_key)
        if headers and table_list:
            max_col_width = max(10, screen_size // max(1, len(headers)))
            print(tabulate(table_list,headers,tablefmt="rounded_grid",maxcolwidths=max_col_width))
    else:
        print("primary key",primary_key,"not found in the database")


def update_database():
    database=load_database()
    if not database:
        print("The database is empty.")
        return
    primary_key = input("Enter primary key to search: ").strip()
    if primary_key in database:
        search_database(primary_key)
        print("Enter the new details to update the database or press ENTER KEY to keep the original values")
        schema=load_custom_schema()
        primary_key_name=next(iter(schema), None)
        for field_name, value in database[primary_key].items():
            datatype=schema.get(primary_key_name, {}).get(field_name) if primary_key_name else None
            if datatype is None:
                datatype = "int" if isinstance(value, int) and not isinstance(value, bool) else "float" if isinstance(value, float) else "str"
            while True:
                new_value = input(f"      {field_name} (current value: {value}): ")
                if new_value=="":
                    break
                try:
                    if datatype=="int":
                        database[primary_key][field_name] = int(new_value)
                    elif datatype=="float":
                        database[primary_key][field_name] = float(new_value)
                    else:
                        database[primary_key][field_name] = str(new_value)
                    break
                except ValueError:
                    print(f"Invalid value! Expected data type: {datatype}")
        dump_database(database)
        print("Database Updated\\nCurrent Table:")
        search_database(primary_key)
    else:
        print("Primary Key",primary_key,"not found in the database")


def delete_data_database():
    database=load_database()
    primary_key=str(input("enter the primary key of the desired to delete:"))
    if primary_key in database:
        search_database(primary_key)
        yn=input(f"do you want to delete {primary_key} y/n:")
        if yn.lower()=="y" or yn.lower()=="yes":
            del database[primary_key]
            dump_database(database)
            print("Deletion done")
        else:
            print("deletion abandoned")
    else:
        print("Primary key not found")
def export_file_as_excel(database):
    from openpyxl import Workbook as workbook       #lazy
    wbk=workbook()
    wak=wbk.active
    wak.title=f"{database_name}"[:31]
    headers,rows=table_loader(database,"all","")
    if headers:
        wak.append(headers)
    for i in rows:
        wak.append(i)
    from openpyxl.styles import Font
    for cell in wak[1]:
        cell.font = Font(bold=True)
    wbk.save(f"{database_name}.xlsx") 
def database_name_taker():
    while True:
        database_name=str(input("Enter the name of the database to do the operations:")).strip()
        if not database_name or database_name in (".", "..") or any(char in database_name for char in '/\\:*?"<>|\\x00'):
            print("Enter a valid database name (without path separators or special characters).")
            continue
        try:
            with open(f"{database_name}.eL", "r") as file:
                existing=load(file)
            if existing is not None and not isinstance(existing, dict):
                print("Database file has an invalid format.")
                continue
            if database_name!="" and database_name!=" ":
                return database_name
        except FileNotFoundError:
            print(f"You will have create a new database {database_name} as the file doesnt exist \nand later continue to do operations on it") 
            question1=str(input("do you want to create new database?y/n:"))
            if question1.lower()=="y" or question1.lower()=="yes":
                with open(f"{database_name}.eL", "w") as file:
                    dump({},file)
                clear_screen()
            else:
                clear_screen()
                continue
            return database_name
        except Exception as e:
            print(f"Error occured\nError name:{e}")


registrarY_text=r"""
                                 __             __                               _____ ___ 
    _______    ____      ____   |__|   ______ _/  |_  _______  _____    _______  \__  |   |
    \_  __ \ _/ __ \    / ___\  |  |  /  ___/ \   __\ \_  __ \ \__  \   \_  __ \  /   |   |
     |  | \/ \  ___/   / /_/  > |  |  \___ \   |  |    |  | \/  / __ \_  |  | \/  \____   |
     |__|     \___  >  \___  /  |__| /____  >  |__|    |__|    (____  /  |__|     / ______|
                  \/  /_____/             \/                        \/            \/       """



print(registrarY_text,"\n\n")
database_name=database_name_taker()
menu = [["(1)", "Create default"],["(2)", "Create custom Schema"],["(3)", "Add data"],["(4)", "View all"],["(5)", "Search"],["(6)", "Update"],["(7)", "Delete"],["(8)", "Export"],["(9)", "Help"],["(10)", "Exit"]]
number_for_check=0
while True:
    print("What do you want to do?\nType Menu for printing menu/Help for Help ")
    if number_for_check==0:
        headers=["Option","Cammand"]
        max_col_width = max(10, screen_size // max(1, len(headers)))
        print(tabulate(menu,headers,tablefmt="rounded_grid",maxcolwidths=max_col_width))
        number_for_check=1
    option=str(input("Enter your option/command >>>"))
    if option.lower()=="create default" or option=="1":
        clear_screen()
        create_default_database()
    elif option.lower()=="create custom schema" or option=="2":
        clear_screen()
        custom_schema()
    elif option.lower()=="add data" or option=="3":
        clear_screen()
        add_custom_data()
    elif option.lower()=="view all" or option=="4":
        clear_screen()
        view_all()
    elif option.lower()=="search" or option=="5":
        clear_screen()
        primary_key = input(f"Enter primary key to search: ")
        search_database(primary_key)
    elif option.lower()=="update" or option=="6":
        update_database()
    elif option.lower()=="del" or option.lower()=="delete" or option.lower()=="7":
        delete_data_database()
    elif option.lower()=="export" or option.lower()=="8":
        clear_screen()
        database=load_database()
        print("File save successfully")
        export_file_as_excel(database)
    elif option.lower()=="help" or option=="9":
        clear_screen()
        help_data = [
    [1, "Create Default\n",
     "Create a standard student database with predefined fields\n"
     "Name, Date of Birth, Father's Name, and Mother's Name. \n"
     "Automatically generate unique Roll Numbers (e.g., A0001) \n"
     "for each student record.\n"],

    [2, "Create Custom Schema\n",
     "Design a database structure by specifying a unique primary key \n"
     "and custom field names with their data types (str, int, float). \n"
     "The schema defines the fields available when adding and managing records.\n"],

    [3, "Add Data\n",
     "Insert new records into the active database using its defined schema. \n"
     "Enter a unique primary key and provide values matching the assigned \n"
     "data types. Existing primary keys cannot be reused.\n"],

    [4, "View All\n",
     "Display all records in the active database in a structured table. \n"
     "Column headers are generated from the schema, making records easier \n"
     "to read and compare.\n"],

    [5, "Search\n",
     "Retrieve a specific record by entering its unique primary key \n"
     "or Roll Number. Displays the matching record's primary key, \n"
     "field names, and stored values.\n"],

    [6, "Update\n",
     "Modify the field values of an existing record by entering its \n"
     "primary key. Press ENTER without typing a new value to retain \n"
     "the existing value. Changes are saved to the database file.\n"],

    [7, "Delete\n",
     "Remove a record from the active database using its primary key. \n"
     "The record is displayed before deletion, and confirmation is \n"
     "requested to help prevent accidental data loss.\n"],

    [8, "Export\n",
     "Export the active database records to an Excel (.xlsx) file. \n"
     "The first row contains column headers formatted in bold, followed \n"
     "by the database records. Requires the openpyxl package.\n"],

