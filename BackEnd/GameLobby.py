from ZODB import FileStorage, DB
from persistent import Persistent
from ZEO import ClientStorage
from persistent.list import PersistentList
from ZODB.POSException import ConflictError
from BTrees import OOBTree
import Main
import transaction
import threading
import sys, time
T = 0 # globalna varijabla

class GameLobby(Persistent):
    def __init__(self, name, boardState, player, adress, port):
        self.name = name
        self.boardState = boardState  
        self.players = []
        self.players.append(player)
        self.moveLog = [] 
        
        self.storage = ClientStorage.ClientStorage( ( adress, port ) )
        self.bp = DB( self.storage )
        self.connection = self.bp.open()
        
        self.lobby = self.openSession(name)
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
            session[ lobby ] = lobby
            transaction.commit()
        session = session[ lobby ]
        return session

    def checkUpdates( self ):
        self.active = True
        while self.active:
            self.connection.sync()
            global T
            if self.moveLog != []:
                for T2, move in self.moveLog.items():
                    if T2 > T:
                        self.moveLog.append( move )
                        T = T2
            return self.moveLog
            
    def sendMove(self, move):
        while True:
            try:    
                t = transaction.get()
                now = time.time()
                self.moveLog[ now ] = move
                t.commit()
            except ConflictError or ValueError:
                t.abort()
                time.sleep( 1 )
                pass
            else:
                break



