
    
  

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

