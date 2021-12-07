from src import sqlutils


class Inventory:
    def __init__(self, db):
        self.db = db

    def new_beer(self, json_data):
        beer = Beer.from_json(json_data)
        with self.db.write() as (conn, c):
           return beer.save(c)

    def retrieve_beer(self, beer_id):
        with self.db.read() as (conn, c):
            return Beer.retrieve_for_id(c, beer_id)

    def update_beer(self, rowid, json_data):
        beer = Beer.from_json(json_data)
        beer.rowid = rowid
        with self.db.write() as (conn, c):
            return beer.save(c)


class Beer(sqlutils.BaseTable):
    def __init__(self):
        super().__init__("Beer")
        self.brewery = ""
        self.name = ""
        self.category = ""
        self.style = ""
        self.alcohol = 0.0
        self.notes = ""