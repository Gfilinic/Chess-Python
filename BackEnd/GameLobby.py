from ZODB import FileStorage, DB
from persistent import Persistent
from ZEO import ClientStorage
from persistent.list import PersistentList
from ZODB.POSException import ConflictError
from BTrees import OOBTree
import socket
import transaction
import threading
import sys, time

class GameState(Persistent):
    def __init__(self, lobbyName, boardState, player_name):
        self.board = boardState
        self.lobbyName = lobbyName
        self.ready = False
        self.player_name = player_name


class GameLobby():
    def __init__(self, client, gameState, boardState, white_player):
        
        self.boardState = boardState  
        self.white_player = white_player
        self.move_log = []
        self.last_processed_move = 0
        self.client = client
        self.running = True
        self.gameState = gameState
        
    def start(self):
        print("Čekam protivnika...")
        while self.running and not self.gameState.ready:
            self.game = self.client.send(msg="get_ready", data=self.gameState.lobbyName, return_response=True)
            if self.game == True:
                self.gameState.ready = True
            time.sleep(0.5)
        print("Pronađen je protivnik, igra može započeti.")
        