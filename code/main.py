import datetime
import random

import events

def render_multiple(bucket, datetime_format):
    return_string = ""
    for date, event_dict in bucket.iteritems():
        return_string += date.strftime(datetime_format).lstrip("0").lower() + ":\t"
        for event_type, event_list in event_dict.iteritems():
            return_string += event_type.renderer.multiple_render(event_type.count_events(event_list)) + "\n\t"
        return_string += "\n"
    return return_string


def render_hourly():
    return render_multiple(events.Event.hourly_bucket, "%I%p")


def render_daily():
    return render_multiple(events.Event.daily_bucket, "%m-%d")


def random_datetime():
    days_ago = random.randint(0,4)
    hour = random.randint(0,23)
    minute = random.randint(0,60)
    date = datetime.datetime.now()
    date = date - datetime.timedelta(days=days_ago)
    date.hour = hour
    date.minute = minute

    return date

def build_random_events():
    event_list = (events.CommentEvent, events.LeaveEvent, events.EnterEvent, events.HighFiveEvent)
    name_list = ('Andy', 'Tom', 'Jacob', 'Jim')
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
            second_name = random.choice(name_list)
            event_type(date, name, random.choice(name_list))
            print event_type, date, name, second_name
        else:
            assert("Something is very wrong")
        


if __name__ == '__main__':
    build_random_events()
    granularity = input('Granularity (1 for minute-to-minute, 2 for hourly, 3 for daily)?')
    if granularity == 1:
        for event in events.Event.all_events:
            print event.renderer.single_render(event)
    elif granularity == 2:
        print render_hourly()
    elif granularity == 3:
        print render_daily()
