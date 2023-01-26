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

class GameLobby(Persistent):
    def __init__(self, name, boardState, player, adress, port):
        self.name = name
        self.boardState = boardState  
        self.players = []
        self.players.append(player)
        self.move_log = []
        self.last_processed_move = 0
        
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
    
    def joinSession(self, lobby, player):
        root = self.connection.root()
        session = root['session']
        if len(self.players) < 2:
            self.players.append(player)
            transaction.commit()
        else:
            print("The lobby is full, please try again later.")
        if lobby in session.keys():
            self.lobby = session[lobby]
            self.players.append(player)
            transaction.commit()
            print(f"{player} has joined the lobby {lobby}")
        else:
            print(f"Error: {lobby} not found")
            
    
    def sendMove(self, move):
        while True:
            try:
                t = transaction.get()
                self.move_log.append(move)
                t.commit()
            except ConflictError or ValueError:
                    t.abort()
                    time.sleep(1)
                    pass
            else:
                break

    def checkUpdates( self ):
        self.active = True
        while self.active:
            self.connection.sync()
            if len(self.move_log) > self.last_processed_move:
                last_move = self.move_log[-1]
                self.playMoveOpponent(self.boardState, last_move)
                with open("Database\output.txt", "a") as file:
                    file.write(str(last_move) + ", ")
                self.last_processed_move = len(self.move_log)

    def playMoveOpponent(self, boardState, move):
        boardState.makeMove(move)
            
