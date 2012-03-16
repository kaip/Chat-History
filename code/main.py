import datetime
import random

import events

def render_multiple(buckets, datetime_format):
    """ Given a particular "bucket" set (hourly, daily, etc) and a datetime_format for strftime
        build a string for containing the chat history with the bucket's granularity.  This
        is done by iterating over each bucket, getting a count of all items within, and rendering
        each count"""
    return_string = ""
    for date, event_dict in buckets.iteritems():
        return_string += date.strftime(datetime_format).lstrip("0").lower() + ":\t"
        for event_type, event_list in event_dict.iteritems():
            return_string += event_type.renderer.multiple_render(event_list) + "\n\t"
        return_string += "\n"
    return return_string


def render_minute_to_minute():
    all_events = (event.renderer.single_render(event) for event in events.Event.all_events)
    return '\n'.join(all_events)


def render_hourly():
    return render_multiple(events.Event.hourly_buckets, "%I%p")


def render_daily():
    return render_multiple(events.Event.daily_buckets, "%m-%d")


def build_random_events():
    """ Build a sample set of events over the course of a few days """
    event_list = (events.CommentEvent, events.LeaveEvent, events.EnterEvent, events.HighFiveEvent)
    name_list = ['Andy', 'Tom', 'Jacob', 'Jim']
    date = datetime.datetime.now() - datetime.timedelta(days=4)
    while date < datetime.datetime.now():
        date += datetime.timedelta(minutes=random.randint(0,61))

        event_type = random.choice(event_list)
        name = random.choice(name_list)
        if(event_type == events.EnterEvent or event_type == events.LeaveEvent):
            event_type(date, name) 
            print event_type, date, name
        elif(event_type == events.CommentEvent):
            event_type(date, name, "Random comment!") 
            print event_type, date, name
        elif(event_type == events.HighFiveEvent):
            second_name_list = [other_name for other_name in name_list if other_name != name]
            second_name = random.choice(second_name_list)
            event_type(date, name, second_name)
            print event_type, date, name, second_name
        else:
            assert("Something is very wrong")
        


if __name__ == '__main__':
    build_random_events()
    granularity = input('Granularity (1 for minute-to-minute, 2 for hourly, 3 for daily)? ')
    if granularity == 1:
        print render_minute_to_minute()
    elif granularity == 2:
        print render_hourly()
    elif granularity == 3:
        print render_daily()
