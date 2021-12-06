
class LocationManager():
    def __init__(self, database):
        self.db = database

    def new_location(self, longitude, latitude, name):
        venue = Venue(longitude, latitude, name)
        venue.save(self.db)

    def retrieve_location(self, location_id):
        with self.db.read() as (conn, c):
            c.execute("SELECT longitude, latitude, name FROM Venue WHERE rowid = ?", (location_id,))
            r = c.fetchone()
            if r is not None:
                return Venue(r[0], r[1], r[2], rowid=location_id)
        return None

    def update_location(self, venue):
        venue.save(self.db)

    def get_venues_near(self, longitude, latitude, nearness=0.1):
        sql = """SELECT rowid, longitude, latitude, name 
            FROM Venue 
            WHERE Longitude BETWEEN ? AND ?
            AND Latitude BETWEEN ? AND ?
            """
        vals = (longitude-nearness, longitude+nearness, latitude-nearness, latitude+nearness)
        with self.db.read() as (conn, c):
            rs = c.execute(sql, vals)
            return [Venue(r[1], r[2], r[3], rowid=r[0]) for r in rs]


class Venue:
    def __init__(self, longitude, latitude, name, rowid=-1):
        self.rowid = rowid
        self.longitude = longitude
        self.latitude = latitude
        self.name = name

    def save(self, db):
        if self.rowid == -1:
            sql = "INSERT INTO Venue VALUES (?, ?, ?)"
            vals = (self.longitude, self.latitude, self.name)
        else:
            sql = "UPDATE Venue SET longitude = ?, latitude = ?, name = ? WHERE rowid = ?"
            vals = (self.longitude, self.latitude, self.name, self.rowid)

        with db.write() as (conn, c):
            c.execute(sql, vals)

