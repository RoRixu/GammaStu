from cogs.Users import userlist
from cogs.Games import gamelist
from cogs.Events import eventlist
from cogs.Lobby import lobbyList

TOKEN =  "token"
APP_ID = 0
GUILD = 0
GAMENIGHTCHANNEL = 0

listofUsers = userlist.userlist()
listofGames = gamelist.gameList()
listofEvents = eventlist.eventList()
listofLobbies = lobbyList.lobbyList()

TIMETILLHALFHOUR = 30
EVENTUPDATEHOUR = 12
DAYOFWEEKTORUNGAMENIGHTPREP = 3

USERFILE='users.json'
GAMEFILE='games.json'
EVENTFILE='events.json'

EVENTEMBEDCOLOR = 0xFFAA00
EVENTOPTIONS = ['Will be there','Will not be there','Will be there but late','Will maybe be there']
POLLGRAPHLENGTH = 20
POLLEMBEDCOLOR = 0x07DE40
POLLICONS = ["\U0001F7E5","\U0001F7E7","\U0001F7E8","\U0001F7E9","\U0001F7E6","\U0001F7EA","\U00002B1B","\U0001F7EB","\U00002B1C","\U0001F49F"]
YESNO = ["\U0001F44D","\U0001F44E"]
NOYES = ["\U0001F44E","\U0001F44D"]

INTRESTROLES =["MTG","League"]

USEREMBEDCOLOR = 0x123D3A
PICTUREPATH = r'C:\Users\short\PycharmProjects\GammaStu-Beta\images/'
GOOGLEMAPSURL = "https://maps.google.com/maps?q="

GAMEEMBEDCOLOR = 0x5E0303
DEFAULTGAMEICON = "https://icon-library.com/images/file-icon-size/file-icon-size-19.jpg"
PLATFORMLIST = ["Steam","Epic Games","Ubisoft Connect","Origin","Riot","Web"]

TEAMCOLORS = [0xba0d0d,0x1b0dba,0xf5ee20,0x0fb80f,0xf536d8,0x000000,0x381a02,0x180238,0xd1d17d]