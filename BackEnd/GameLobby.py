from ZODB import FileStorage, DB
from persistent import Persistent
from ZEO.ClientStorage import ClientStorage
from persistent.list import PersistentList
from BTrees import OOBTree
import Main
import transaction
import threading

class GameLobby(Persistent):
    def __init__(self, name, boardState, player, adress, port):
        self.name = name
        self.boardState = boardState  
        self.players = []
        self.player.append(player) 
        
        self.storage = ClientStorage.ClientStorage( ( adress, port ) )
        self.bp = DB( self.storage )
        self.connection = self.bp.open()
        
        self.lobby = self.openSession()
        self.uthread = threading.Thread( target=self.checkUpdates )
        self.uthread.start()
        
    def openSession(self, lobby):
        root = self.connection.root()
        if not 'session' in root.keys():
            print( 'Making Dictionary for sessions' )
            root[ 'session' ] = OOBTree.OOBTree()
            transaction.commit()
		
        session = root[ 'session' ]
		
        if not lobby in session.keys():
            print( 'Creating new lobby:', lobby )
            session[ lobby ] = self
            transaction.commit()
        session = session[ lobby ]
        return session

    def checkUpdates( self ):
        self.active = True
        while self.active:
            self.connection.sync()
            #boardstate



