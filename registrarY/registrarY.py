from json import dump,load
from os import name as os_name
from os import get_terminal_size
from subprocess import run as sub_run
from tabulate import tabulate
__lazy_modules__ = ["openpyxl","subprocess","os"]
try:
    screen_size=get_terminal_size().columns
except OSError:
    screen_size=80
def create_default_database():                                                #soon to be removed
    while True:
        try:
            num_entry=int(input("Enter the number of entries you want to add: "))
            if num_entry > 0:
                break
            print("Enter a positive number.")
        except Exception as e:
            print("Enter a positive number")       
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    database = {}
    if num_entry > len(alphabet) * 1000:
        print("A maximum of 26000 records can be created with the current roll-number format.")
        return
    else:
        for i in range(num_entry):
            name = input("Enter the name: ")
            dob=input("Enter the date of birth (DD-MM-YYYY): ")
            fname=input("Enter the father's name: ")
            mname=input("Enter the mother's name: ")
            detail_set= {"Name":name,"date_of_birth": dob,"father_name": fname,"mother_name": mname}

            letter_index = i // 1000
            number = (i % 1000) + 1
            roll_no = alphabet[letter_index] + f"{number:04d}"
            data={}
            data[roll_no]=detail_set

            print(roll_no)
            database.update(data)

    print(database)
    python_file_content =database
    with open(f"{database_name}.eL", "w") as file:
        dump(python_file_content,file)

def dump_database(database):
    with open(f"{database_name}.eL", "w") as file:
        dump(database,file)

def load_database():
    try:
        with open(f"{database_name}.eL", "r") as file:
            data = load(file)
            if data is None:
                return {}
            if not isinstance(data, dict):
                print("Database file has an invalid format.")
                return {}
            return data
    except FileNotFoundError:
        return {}
    except (ValueError, OSError) as e:
        print(f"Unable to load database: {e}")
        return {}


def load_custom_schema():
    try:
        with open(f"custom_schema-{database_name}.eLs", "r") as file:
            content = load(file)
            if content is None:
                return {}
            if not isinstance(content, dict):
                print("Schema file has an invalid format.")
                return {}
            return content
    except FileNotFoundError:
        return {}
    except (ValueError, OSError) as e:
        print(f"Unable to load custom schema: {e}")
        return {}


def table_loader(database,num,primary_key):
    schema=load_custom_schema()
    headers=[]
    rows=[]
    primary_key_name = next(iter(schema), "Primary Key")
    field_names=[]
    for record in database.values():
        if isinstance(record, dict):
            for field_name in record:
                if field_name not in field_names:
                    field_names.append(field_name)

    schema_fields=list(schema.get(primary_key_name, {}).keys())
    # Use the saved schema only when it matches the records in this database.
    # This also lets the predefined student database work if an old custom
    # schema file is present.
    if schema_fields and any(field in field_names for field in schema_fields):
        headers=[primary_key_name] + schema_fields
    else:
        headers=["Primary Key"] + field_names

    if num=="all":
        for record_key, record in database.items():
            record = record if isinstance(record, dict) else {}
            rows.append([record_key] + [record.get(field, "") for field in headers[1:]])
        return headers,rows
    elif num=="single":
        if primary_key in database:
            record=database[primary_key]
            record = record if isinstance(record, dict) else {}
            rows=[[primary_key] + [record.get(field, "") for field in headers[1:]]]
        return headers,rows
    return headers,rows


def clear_screen():
    if os_name=="nt":
        sub_run(["cmd", "/c", "cls"], check=False)
    else:
        sub_run(["clear"], check=False)
    print(registrarY_text)

def custom_schema():
    primary_key=input("Enter unique primary key field:").strip()
    if not primary_key:
        print("Primary key field cannot be empty.")
        return
    fields=input("enter fields with data type(example name;str,age;int,gender;str):").strip()
    schema={}
    schema[primary_key] = {}
    try:
        for item in fields.split(","):
            field_name, data_type = item.split(";",1)
            field_name=field_name.strip()
            data_type=data_type.strip().lower()
            if not field_name or field_name == primary_key:
                raise ValueError("Field names must be non-empty and cannot match the primary key.")
            if data_type not in ("str", "int", "float"):
                raise ValueError(f"Unsupported data type: {data_type}")
            if field_name in schema[primary_key]:
                raise ValueError(f"Duplicate field name: {field_name}")
            schema[primary_key][field_name] = data_type
        if not schema[primary_key]:
            raise ValueError("At least one field is required.")
    except ValueError as e:
        print(f"Invalid schema: {e}")
        return
    print("Custom schema created:",schema)
    with open(f"custom_schema-{database_name}.eLs", "w") as file:
        dump(schema,file,indent=4)


def add_custom_data():
    try:
        schema=load_custom_schema()
        if not schema:
            print("Custom schema not found. Create a custom schema first.")
            return
        primary_key_name=next(iter(schema))
        fields=schema[primary_key_name]
        num_entry=int(input("Enter the number of entries you want to add: "))
        if num_entry <= 0:
            print("Please enter a positive number of entries.")
            return
        database=load_database()
        for i in range(num_entry):
            primary_key = input(f"Enter {primary_key_name} for entry number{i + 1}: ").strip()
            if not primary_key:
                print("Primary key cannot be empty.")
                continue
            if primary_key in database:
                print("Primary key already exists; you cannot add it.")
                continue
            record={}
            valid_record=True
            for field_name, data_type in fields.items():
                while True:
                    raw_value=input(f"Enter {field_name} ({data_type}): ")
                    try:
                        if data_type == "str":
                            value=raw_value
                        elif data_type == "int":
                            value=int(raw_value)
                        elif data_type == "float":
                            value=float(raw_value)
                        else:
                            print(f"Unsupported data type: {data_type}")
                            valid_record=False
                            break
                        record[field_name]=value
                        break
                    except ValueError:
                        print(f"Invalid value! Expected data type: {data_type}")
                if not valid_record:
                    break
            if valid_record:
                database[primary_key]=record
        dump_database(database)
    except ValueError:
        print("Please enter a valid number and values matching the assigned data types.")
    except OSError as e:
        print(f"{e} has occurred. Check file permissions and antivirus settings.")
    except Exception as e:
        print(f"Error occurred: {e}")


def view_all():
    database = load_database()
    if not database:
        print("The database is empty.")
        return
    headers,rows=table_loader(database,"all","")
    max_col_width = max(10, screen_size // max(1, len(headers)))
    print(tabulate(rows,headers,tablefmt="rounded_grid",maxcolwidths=max_col_width))


def search_database(primary_key):
    database=load_database()
    if primary_key in database:
        headers,table_list=table_loader(database,"single",primary_key)
        if headers and table_list:
            max_col_width = max(10, screen_size // max(1, len(headers)))
            print(tabulate(table_list,headers,tablefmt="rounded_grid",maxcolwidths=max_col_width))
        else:
            print("The selected record has an invalid format.")
    else:
        print("primary key",primary_key,"not found in the database")


def update_database():
    database=load_database()
    if not database:
        print("The database is empty.")
        return
    primary_key = input("Enter primary key to search: ").strip()
    if primary_key in database:
        if not isinstance(database[primary_key], dict):
            print("The selected record has an invalid format and cannot be updated.")
            return
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
    primary_key=input("enter the primary key of the desired to delete:").strip()
    if primary_key in database:
        search_database(primary_key)
        yn=input(f"do you want to delete {primary_key} y/n:").strip()
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
        if not database_name or database_name in (".", "..") or any(char in database_name for char in '/\\\\:*?"<>|') or any(ord(char) < 32 for char in database_name):
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

    [9, "Help",
     "Display this navigation guide, including menu options, feature "
     "descriptions, and supported commands for managing the database."],

    [10, "Exit",
     "Terminate the registrarY session. Database modifications are saved by their respective operations before exiting."]
]
        headers = ["Option", "Action", "Description"]
        max_col_width = max(10, screen_size // max(1, len(headers)))
        print(tabulate(help_data,headers,tablefmt="rounded_grid",maxcolwidths=max_col_width))
    elif option.lower()=="exit" or option=="10":
        clear_screen()
        print("""Kicking you out of the program......
DONE.""")
        break
    elif option.lower()=="menu" or option=="":
        clear_screen()
        headers=["Option","Cammand"]
        max_col_width = max(10, screen_size // max(1, len(headers)))
        print(tabulate(menu,headers,tablefmt="rounded_grid",maxcolwidths=max_col_width))
    else:
        clear_screen()
        headers=["Option","Cammand"]
        max_col_width = max(10, screen_size // max(1, len(headers)))
        print(tabulate(menu,["Option","Cammand"],tablefmt="rounded_grid",maxcolwidths=max_col_width))
        print("input valid option create/search")
    print("#" * 100)
