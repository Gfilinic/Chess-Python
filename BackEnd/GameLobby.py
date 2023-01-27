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
            self.gameState = self.client.send(msg="get_game", data=self.gameState.lobbyName, return_response=True)
            time.sleep(0.5)
        print("Pronađen je protivnik, igra može započeti.")
        if (self.white_player):
            self.my_turn=True
        else:
            self.my_turn=False
        
    def checkTurn(self):
        while self.running and self.gameState.ready:
            if self.my_turn:
                return True
            else:
                return False
            
    def checkIfGameActive(self):
       return (self.running and self.gameState.ready)
        
    def update_MyGameState(self):
        self.gameState = self.client.send(msg="get_game", data=self.gameState.lobbyName, return_response=True)
        self.my_turn = not self.my_turn
        
    def get_GameState(self):
        self.gameState = self.client.send(msg="get_game", data=self.gameState.lobbyName, return_response=True)
        
        
    