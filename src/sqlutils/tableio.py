
class BaseTable:
    """
    Just call the super init with a table name!
    """
    def __init__(self, table_name):
        self.rowid = -1
        self._table_name = table_name
        print("BASE INIT")

    def save(self, cursor):
        save_table(self, cursor)


def format_values_for_insert(values):
    return [format_value_for_sql(v) for v in values]


def format_value_for_sql(v):
    if isinstance(v, str):
        return v
    return v


def write_sql_sets(field_names):
    return [f"{k} = ?" for k in field_names]


def save_table(tbl, cursor):
    chk_tbl(tbl)
    vals = format_values_for_insert(collect_field_values(tbl))

    if tbl.rowid == -1:
        sql = write_insert_statement(tbl)
    else:
        sql = write_update_statement(tbl)
        vals.append(tbl.rowid)
    vals = tuple(vals)
    cursor.execute(sql, vals)


def chk_tbl(tbl):
    if not isinstance(tbl, BaseTable):
        raise ValueError("Input must be a BaseTable")


def collect_field_dict(tbl, include_rowid):
    field_dict = {k:v for k,v in vars(tbl).items() if not k.startswith("_")}
    if not include_rowid:
        field_dict.pop("rowid")
    return field_dict

def collect_field_values(tbl):
    """
    Returns all fields, except rowid, ordered alphabetically by field name
    """
    field_dict = collect_field_dict(tbl, False)
    return [field_dict[k] for k in sorted(field_dict.keys())]

def collect_columns(tbl, include_rowid=False):
    return [k for k in sorted(collect_field_dict(tbl, include_rowid))]

def write_insert_statement(tbl):
    table = tbl._table_name
    cols = ",".join(collect_columns(tbl))
    bindings = ",".join(["?" for x in collect_field_values(tbl)])
    return f"INSERT INTO {table} ({cols}) VALUES ({bindings});"

def write_update_statement(tbl):
    table = tbl._table_name
    cols = collect_columns(tbl)
    sets = ",".join(write_sql_sets(cols))
    return f"UPDATE {table} SET {sets} WHERE rowid = ?;"