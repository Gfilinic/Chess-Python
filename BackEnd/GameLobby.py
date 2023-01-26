from ZODB import FileStorage, DB
from persistent import Persistent
from ZEO import ClientStorage
from persistent.list import PersistentList
from ZODB.POSException import ConflictError
from BTrees import OOBTree
import socket
#import Main
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
        
        self.session = self.openSession(name)
        self.lobby = zeoClient(name)
        
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
            session[ lobby ] = zeoClient(lobby)
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
            
    
    def checkUpdates( self ):
        self.active = True
        while self.active:
            self.connection.sync()
            moves = self.lobby.newTurns()
            for move in moves:
                self.move_log.append(move)
                print("Dodan move: ",str(move))		
        time.sleep( 1 )
        
    def sendMoveToServer(self,move, event=None):
        self.lobby.sendMove(move)


T = 1          
class zeoClient:
    def __init__(self,  lobbyName):
        self.moveLog=OOBTree.OOBTree()
        self.lobbyName = lobbyName

        
    def sendMove(self, move):
        while True:
            try:
                t = transaction.get()
                self.moveLog[T] = move
                t.commit()
            except ConflictError or ValueError:
                    t.abort()
                    time.sleep(1)
                    pass
            else:
                break
    
    def newTurns(self):
        global T
        moves = []
        for T2, move in self.moveLog.items():
            if T2 > T:
                moves.append( move )
                T = T2
        return moves
        

        
    

