import pytest
from src import sqlutils, database
from src.sqlutils.tableio import save_table

class ExampleTable(sqlutils.BaseTable):

    def __init__(self):
        super().__init__("TestTable")
        self.StringColumn = ""
        self.IntColumn = -1
        self.AnotherInt = -1
        print("EXAMPLE INIT")


@pytest.fixture
def memory_db():
    return database.Provider(":memory:")

def test_write_sql(memory_db):
    
    entity = ExampleTable()
    entity.StringColumn = "Text Value"
    entity.IntColumn = 3
    entity.AnotherInt = 1

    with memory_db.write() as (conn, c):

        c.execute("CREATE TABLE TestTable ( StringColumn TEXT, IntColumn NUMBER, AnotherInt NUMBER);")
        conn.commit()

        entity.save(c)
        entity.rowid = c.lastrowid
        conn.commit()

        test_val = "different"
        entity.StringColumn = test_val
        entity.save(c)
        conn.commit()

        rs = c.execute("SELECT StringColumn, IntColumn, AnotherInt FROM TestTable;")
        string_vals = [r[0] for r in rs]
        assert(len(string_vals) == 1)
        assert(string_vals[0] == test_val)
        

def test_bad_object(memory_db):
    not_an_entity = "text"
    with memory_db.write() as (conn, c):
        with pytest.raises(ValueError) as ve:
            save_table(not_an_entity, c)




