import collections
import datetime

import render

class Event:
    all_events = []
    hourly_buckets = collections.OrderedDict()
    daily_buckets = collections.OrderedDict()

    def __init__(self, date, actor):
        def _set_bucket(buckets, floored_date):
            """ Buckets are dictionaries of dictionaries, with top-level keys as dates rounded 
                to the last hour, day, etc.  The second level dictionaries map classes to event
                instances.  This function adds the just built event to the buckets """
            if not floored_date in buckets:
                buckets[floored_date] = {}
            if not self.__class__ in buckets[floored_date]:
                buckets[floored_date][self.__class__] = []
            event_list = buckets[floored_date].get(self.__class__, []) + [self]
            buckets[floored_date][self.__class__] = event_list
            
        self.date = date
        self.actor = actor
        self.all_events.append(self)

        """ Get the 'hourly floor' of each date e.g. 7:53:23.1234 pm -> 7:00 pm.  These are used
            as keys for the buckets """
        hourly_floored_date = self.date - datetime.timedelta(
                            minutes=self.date.minute, seconds=self.date.second, microseconds=self.date.microsecond)
        _set_bucket(self.hourly_buckets, hourly_floored_date)
        """ Get the 'daily floor' of each date e.g. March 4 7:53:23.1234 pm -> March 4 12:00 am.  These are used
            as keys for the buckets """
        daily_floored_date = self.date - datetime.timedelta(hours = self.date.hour,
                            minutes=self.date.minute, seconds=self.date.second, microseconds=self.date.microsecond)
        _set_bucket(self.daily_buckets, daily_floored_date)


class EnterEvent(Event):
    renderer = render.EnterRenderer

    @staticmethod
    def count_events(event_list):
        """ Given a list of events, return a proper count of the event, in this case 
            filtering out all repeated actors """
        actor_set = {event.actor for event in event_list}
        return len(actor_set)


class LeaveEvent(Event):
    renderer = render.LeaveRenderer

    @staticmethod
    def count_events(event_list):
        """ Given a list of events, return a proper count of the event, in this case 
            filtering out all repeated actors """
        actor_set = {event.actor for event in event_list}
        return len(actor_set)


class CommentEvent(Event):
    def __init__(self, date, actor, comment):
        self.comment = comment
        Event.__init__(self, date, actor)

    renderer = render.CommentRenderer


class HighFiveEvent(Event):
    def __init__(self, date, actor, actee):
        self.actee = actee
        Event.__init__(self, date, actor)

    renderer = render.HighFiveRenderer
