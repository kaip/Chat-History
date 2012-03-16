import collections
import datetime

import render

class Event:
    all_events = []
    hourly_bucket = collections.OrderedDict()
    daily_bucket = collections.OrderedDict()

    def __init__(self, date, actor):
        def _set_bucket(bucket, rounded_date):
            if not rounded_date in bucket:
                bucket[rounded_date] = {}
            if not self.__class__ in bucket[rounded_date]:
                bucket[rounded_date][self.__class__] = []
            event_list = bucket[rounded_date].get(self.__class__, []) + [self]
            bucket[rounded_date][self.__class__] = event_list
            
        self.date = date
        self.actor = actor
        self.all_events.append(self)

        rounded_date = self.date - datetime.timedelta(
                            minutes=self.date.minute, seconds=self.date.second, microseconds=self.date.microsecond)
        _set_bucket(self.hourly_bucket, rounded_date)
        rounded_date = self.date - datetime.timedelta(hours = self.date.hour,
                            minutes=self.date.minute, seconds=self.date.second, microseconds=self.date.microsecond)
        _set_bucket(self.daily_bucket, rounded_date)


class EnterEvent(Event):
    renderer = render.EnterRenderer

    @staticmethod
    def count_events(event_list):
        actor_set = {event.actor for event in event_list}
        return len(actor_set)


class LeaveEvent(Event):
    renderer = render.LeaveRenderer

    @staticmethod
    def count_events(event_list):
        actor_set = {event.actor for event in event_list}
        return len(actor_set)


class CommentEvent(Event):
    def __init__(self, date, actor, comment):
        self.comment = comment
        Event.__init__(self, date, actor)

    renderer = render.CommentRenderer

    count_events = len


class HighFiveEvent(Event):
    def __init__(self, date, actor, actee):
        self.actee = actee
        Event.__init__(self, date, actor)

    @staticmethod
    def count_events(event_list):
        actor_set = {event.actor for event in event_list}
        actee_set = {event.actee for event in event_list}
        return len(actor_set),len(actee_set)

    renderer = render.HighFiveRenderer
