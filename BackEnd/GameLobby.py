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

timeout=10
class GameState(Persistent):
    def __init__(self, lobbyName, boardState, player_name):
        self.board = boardState
        self.lobbyName = lobbyName
        self.ready = False
        self.player_name = player_name
        self.moveLog = boardState.moveLog


class GameLobby():
    def __init__(self, client, boardState, *, white_player):
        
        
        self.white_player = white_player
        self.move_log = []
        self.last_processed_move = 0
        self.client = client
        self.running = True
        self.gameState = boardState
        self.gameOver = False
        self.boardState = boardState
        
        
    def start(self):
        print("waiting for the opponent...")
        while self.running and not self.gameState.ready:
            self.gameState = self.client.send(msg="get_game", data=self.gameState.lobbyName, return_response=True)
            time.sleep(0.5)
        print("Opponent found, Get Ready!.")
        if (self.white_player):
            self.my_turn=True
        else:
            self.my_turn=False
        
    def checkTurn(self):
        start_time = time.time()
        if self.my_turn:
            return True
        else:
            if time.time() - start_time > timeout:
                print("timeout")
                return False
            time.sleep(0.5)
            
    def checkIfGameActive(self):
       return not self.gameOver
        
    def update_MyGameState(self):
        if self.gameState.board != self.boardState.board:
            self.boardState.board = self.gameState.board
        
    def get_GameState(self):
        self.boardState = self.client.send(msg="get_game", data=self.gameState.lobbyName, return_response=True)
    
    def get_boardState(self):
        return self.boardState
    
    def make_Move(self,move):
        self.move_log.append(move)

        
    