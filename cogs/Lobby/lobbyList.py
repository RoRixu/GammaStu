from cogs.Lobby import Lobby
class lobbyList:
    def __init__(self):
        self.lobbies = []
    def findLobby(self,**kwargs):
        for lobby in self.lobbies:
            if lobby.name == kwargs['name']:
                return lobby
        return None
    def addLobby(self,**kwargs):
        if not self.findLobby(name=kwargs['name']):
            lobby = Lobby.lobby(**kwargs)
            self.lobbies.append(lobby)
            return lobby
        return None
    def removeLobby(self,**kwargs):
        lobby = self.findLobby(**kwargs)
        self.lobbies.remove(lobby)
        return
    def clearLobbies(self):
        self.lobbies = []
