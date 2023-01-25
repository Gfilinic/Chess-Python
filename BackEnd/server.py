import Main
import transaction
from ZODB import FileStorage, DB
from persistent import Persistent
from ZEO.ClientStorage import ClientStorage

def open_cs(zhost, zport):
    storage = ClientStorage((zhost, zport))
    db = DB(storage)
    conn = db.open()
    return conn

    storage2 = FileStorage.FileStorage('/tmp/tbp.fs') 
    db2 = DB( storage2 ) 
    conn2 = db2.open() 
    root2 = conn2.root()

def refreshSrvBoard(c):
    transaction.begin()
    root = c.root()
    board = root['board']
    transaction.commit()
    return board

if __name__ == '__main__':
    try:
        c = open_cs('localhost, 2709')
        transaction.begin()
        root = c.root()
        root['board'] = PersistentList()
        root['board'] = board
        board = root['board']
        transaction.commit()
        print('*'*40)
        print("Game created successfully!")
        print('*'*40)
    except:
        print('*'*40)
        print("Game created successfully!")
        print('*'*40)