import datetime
import discord
from config import config
from cogs.Events import Event
eventResponses = ['Will be there','Will not be there','Will be there but late','Will maybe be there']
class eventList:
    def __init__(self):
        self.events = []
    def jsonEnc(self):
        return {'events': self.events}

    def findEvent(self,**kwargs):
        for event in self.events:
            if kwargs["name"] == event.name:
                return event
        return None

    def addEvent(self,**kwargs):
        if kwargs.get("name",None) == None:
            returnstr = "An event name must be provided."
            return returnstr
        if not self.findEvent(name=kwargs["name"]):
            event = Event.event(kwargs)
            self.events.append(event)
            returnstr = "A new event is happening in Newlore: {name}".format(name=event.name)
            return returnstr
        else:
            returnstr = "{event} has already been added".format(event=kwargs["name"])
            return returnstr

    def removeEvent(self,**kwargs):
        event= self.findEvent(name=kwargs["name"])
        if event:
            returnstr = "{name} have been removed from the event list.".format(name=kwargs["name"])
            self.events.remove(event)
            return returnstr
        else:
            returnstr = "Event named {name} can not be found.".format(name=kwargs["name"])
            return returnstr

    def addResponseToEvent(self,**kwargs):
        event = self.findEvent(name=kwargs["name"])
        if event:
            event.addResponse(discordname=kwargs['discordname'],response=kwargs['response'])
        else:
            returnstr = "Could not find event with name {event}".format(event=kwargs["name"])
            return returnstr

    def removeResponseFromEvent(self,**kwargs):
        event = self.findEvent(name=kwargs["name"])
        if event:
            event.removeResponse(discordname=kwargs['discordname'], response=kwargs['response'])
        else:
            returnstr = "Could not find event with name {event}".format(event=kwargs["name"])
            return returnstr

    def listEvents(self,**kwargs):
        returnstr = "Current events on the Newlore server are:\n"
        i = 1
        for event in self.events:
            returnstr = "{prev}{int}. {eventname}\n".format(prev=returnstr,int=i,eventname=event.name)
            i = i + 1
        return returnstr

    def eventInfo(self,**kwargs):
        event = self.findEvent(name=kwargs["name"])
        if event:
            time = event.datetime.strftime("%I:%M%p on %B %d %Y")
            responseList = "\n\t\t"
            for response in event.responses:
                responseList = "{prev}-{name}: {response}\n\t\t".format(prev=responseList,name=response.discordname,response=response.response)
            returnstr = "{name}\n\tDescription: {description}\n\tLocation: {location}\n\tWhen: {datetime}\n\tResponses: {responseList}".format(
                name=event.name,description=event.description,location=event.location,datetime=time,responseList=responseList
            )
            return returnstr
        else:
            returnstr = "Could not find event with name: {eventname}".formate(eventname=kwargs["name"])
            return returnstr
    def eventEmbed(self,**kwargs):
        event = self.findEvent(name=kwargs["name"])
        embed = event.eventEmbed()
        return embed