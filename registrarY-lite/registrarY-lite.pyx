# cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False
"""
Cython-compiled helpers for registrarY.

These functions intentionally accept normal Python dictionaries/lists so the
existing .eL JSON database format and the CLI remain compatible.
"""

cpdef str make_roll_number(Py_ssize_t index):
    """Return the existing A0001..Z1000 roll-number format."""
    cdef Py_ssize_t letter_index
    cdef Py_ssize_t number

    if index < 0 or index >= 26000:
        raise ValueError("Roll-number index must be between 0 and 25999.")

    letter_index = index // 1000
    number = (index % 1000) + 1
    return chr(65 + letter_index) + f"{number:04d}"


cpdef tuple build_table(dict database, dict schema, str num, object primary_key):
    """
    Build table headers and rows using the same schema-selection rules as the
    original Python table_loader().
    """
    cdef list headers = []
    cdef list rows = []
    cdef list field_names = []
    cdef list schema_fields
    cdef object primary_key_name
    cdef object record_key
    cdef object record
    cdef object field_name
    cdef object field

    primary_key_name = next(iter(schema), "Primary Key")

    # Preserve first-seen field order across records.
    for record in database.values():
        if isinstance(record, dict):
            for field_name in record:
                if field_name not in field_names:
                    field_names.append(field_name)

    schema_fields = list(schema.get(primary_key_name, {}).keys())

    # Use the saved schema only if it overlaps with fields in this database.
    has_schema_field = False
    if schema_fields:
        for field in schema_fields:
            if field in field_names:
                has_schema_field = True
                break

    if has_schema_field:
        headers = [primary_key_name] + schema_fields
    else:
        headers = ["Primary Key"] + field_names

    if num == "all":
        for record_key, record in database.items():
            if not isinstance(record, dict):
                record = {}
            rows.append([record_key] + [record.get(field, "") for field in headers[1:]])
        return headers, rows

    if num == "single":
        if primary_key in database:
            record = database[primary_key]
            if not isinstance(record, dict):
                record = {}
            rows = [[primary_key] + [record.get(field, "") for field in headers[1:]]]
        return headers, rows

    return headers, rows
