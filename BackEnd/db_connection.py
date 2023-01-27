from ZODB import DB
from ZEO.ClientStorage import ClientStorage

class DBConnection:
    def __init__(self, database_name='db.fs', address='localhost', port=2709):
        self.address = address
        self.port = port
        self.database_name = database_name

    def connect(self):
        conn = self._open_cs()
        return conn.root()

    def open_cs(self):
        st = ClientStorage((self.address, self.port))
        db = DB(st)
        conn = db.open()
        return conn

    def create_connection(self):
        db_connection = self.open_cs()
        root = db_connection.root()
        return db_connection, root
