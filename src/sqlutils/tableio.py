
class BaseTable:
    """
    Just call the super init with a table name!
    """
    def __init__(self, table_name):
        self.rowid = -1
        self._table_name = table_name

    def save(self, cursor):
        return save_table(self, cursor)

    @classmethod
    def retrieve_for_id(cls, cursor, rowid):
        instance = cls()
        instance.rowid = rowid
        return select_by_id(instance, cursor)

    @classmethod
    def from_json(cls, json_data):
        instance = cls()
        return create_from_json(instance, json_data)

    def new_instance(self):
        return type(self)()

    def write_json(self):
        return collect_field_dict(self, include_rowid=True)

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

    if tbl.rowid == -1:
        tbl.rowid = cursor.lastrowid
    return tbl.rowid


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


def select_by_id(tbl, cursor):
    chk_tbl(tbl)

    table = tbl._table_name
    fields = ",".join(collect_columns(tbl, include_rowid=True))
    sql = f"SELECT {fields} FROM {table} WHERE rowid = ? LIMIT 1"
    vals = (tbl.rowid,)

    cursor.execute(sql, vals)
    r = cursor.fetchone()
    if r is None: 
        return None
    return create_entity_from_row(tbl, r)


def create_entity_from_row(template, row):
    chk_tbl(template)

    instance = template.new_instance()
    for k in row.keys():
        v = row[k]
        setattr(instance, k, v)
    return instance


def create_from_json(template, json_data):
    chk_tbl(template)
    instance = template.new_instance()
    cols = collect_columns(instance, include_rowid=True)
    for c in cols:
        v = json_data.get(c)
        if v is None and c == "rowid":
            continue
        elif v is None:
            raise ValueError(f"No value for {c}")
        else:
            setattr(instance, c, v)
    return instance
