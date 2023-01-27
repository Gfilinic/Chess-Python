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



class GameLobby(Persistent):
    def __init__(self, name, boardState, player, client):
        self.name = name
        self.boardState = boardState  
        self.players = []
        self.players.append(player)
        self.move_log = []
        self.last_processed_move = 0
        self.ready = False
        self.client = client
        self.running = True
        
    def start(self):
        print("Čekam protivnika...")
        while self.running and not self.ready:
            self.game = self.client.send(msg="get_game", data=self.name, return_response=True)
            time.sleep(0.5)
        print("Pronađen je protivnik, igra može započeti.")
        