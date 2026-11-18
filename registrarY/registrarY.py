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

