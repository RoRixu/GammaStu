from cogs.Users import userlist
from cogs.Games import gamelist
from cogs.Events import eventlist

#TOKEN =  "TOKEN"
#APP_ID = "APPID"
#GUILD = "GUILDID"
#GAMENIGHTCHANNEL = "GAMENIGHTCHANNELID"

listofUsers = userlist.userlist()
listofGames = gamelist.gameList()
listofEvents = eventlist.eventList()

TIMETILLHALFHOUR = 30
EVENTUPDATEHOUR = 12
DAYOFWEEKTORUNGAMENIGHTPREP = 3

USERFILE='users.json'
GAMEFILE='games.json'
EVENTFILE='events.json'

EVENTEMBEDCOLOR = 0xFFAA00
EVENTOPTIONS = ['Will be there','Will not be there','Will be there but late','Will maybe be there']
POLLEMBEDCOLOR = 0x07DE40
POLLICONS = ["\U0001F7E5","\U0001F7E7","\U0001F7E8","\U0001F7E9","\U0001F7E6","\U0001F7EA","\U00002B1B","\U0001F7EB","\U00002B1C","\U0001F49F"]
YESNO = ["\U0001F44D","\U0001F44E"]
NOYES = ["\U0001F44E","\U0001F44D"]

INTRESTROLES =["MTG","League"]