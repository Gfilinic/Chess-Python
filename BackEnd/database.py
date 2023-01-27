import transaction
from persistent.dict import PersistentDict
from persistent.list import PersistentList

from ZODB.POSException import ConflictError
import time
from db_connection import DBConnection

class Database:
    def __init__(self, database_name, address, port):
        db = DBConnection(database_name=database_name, address=address, port=port)
        self.db_connection, self.root = db.create_connection()

    def username_exists(self, username):
        try:
            exists = len([user for user in self.root['users'] if user.username == username]) > 0
            return exists
        except KeyError:
            self.root['users'] = PersistentList()
            return False

    def user_exists(self, login_user):
        try:
            user_exists = len([user for user in self.root['users'] if
                        user.username == login_user.username and user.password == login_user.password]) > 0
            return user_exists
        except KeyError:
            self.root['users'] = PersistentList()
            return False

    def register_user(self, user):
        transaction.begin()
        try:
            self.root['users'].extend([user])
        except KeyError:
            self.root['users'] = PersistentList()
            self.root['users'].extend([user])
        transaction.commit()

    def update_board(self, boardState):
        while True:
            try:
                transaction.begin()
                try:
                    self.root['lobbies'][boardState.game_name].board = boardState.board
                except Exception as e:
                    print("Error:", str(e))
                transaction.commit()
            except ConflictError or ValueError:
                transaction.abort()
                time.sleep(1)
                pass
            else:
                break

    def insert_new_game(self, gameLobby):
        transaction.begin()
        try:
            self.root['lobbies'][gameLobby] = gameLobby
        except KeyError:
            self.root['lobbies'] = PersistentDict()
            self.root['lobbies'][gameLobby] = gameLobby
        transaction.commit()

    def get_user(self, username):
        try:
            user = [user for user in self.root['users'] if user.username == username][0]
            return user
        except KeyError:
            return

    def get_game(self, lobbyName):
        self.db_connection.sync()
        try:
            return self.root['lobbies'][lobbyName]
        except KeyError:
            return

    def get_playing_games(self):
        self.db_connection.sync()
        try:
            return self.root['lobbies']
        except KeyError:
            transaction.begin()
            self.root['lobbies'] = PersistentDict()
            transaction.commit()

    def set_game_ready(self, lobbyName):
        transaction.begin()
        try:
            self.root['lobbies'][lobbyName].ready = True
        except Exception as e:
            print("Error:", str(e))
        transaction.commit()

    def remove_game(self, lobbyName):
        self.db_connection.sync()
        transaction.begin()
        try:
            del self.root['lobbies'][lobbyName]
        except KeyError:
            return
        transaction.commit()
    
    def get_ready(self, lobbyName):
        self.db_connection.sync()
        try:
            return self.root['lobbies'][lobbyName].ready
        except KeyError:
            return
        

    def set_winner(self, username):
        transaction.begin()
        user = self.get_user(username)
        user.games_won += 1
        try:
            for i, user in enumerate(self.root['users']):
                if user.username == username:
                    self.root['users'][i] = user
        except Exception as e:
            print("Error:", str(e))
        transaction.commit()

    def set_loser(self, username):
        transaction.begin()
        user = self.get_user(username)
        user.games_lost += 1
        try:
            for i, user in enumerate(self.root['users']):
                if user.username == username:
                    self.root['users'][i] = user
        except Exception as e:
            print("Error:", str(e))
        transaction.commit()
