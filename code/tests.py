import collections
import datetime
import unittest

import events
import render
import main

class TestSingleEventRenders(unittest.TestCase):
    def test_enter(self):
        test_date = datetime.datetime(year=2012, month=3, day=14, hour=5, minute=0)
        event = events.EnterEvent(test_date, "Bob")
        output = event.renderer.single_render(event)
        self.assertEqual(output, "5:00am: Bob enters the room") 

    def test_leave(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=23, minute=59)
        event = events.LeaveEvent(test_date, "Kate")
        output = event.renderer.single_render(event)
        self.assertEqual(output, "11:59pm: Kate leaves the room")
        
    def test_comment(self):
        test_date = datetime.datetime(year=1999, month=11, day=29, hour=13, minute=30)
        event = events.CommentEvent(test_date, "Charlie", "How's it going?")
        output = event.renderer.single_render(event)
        self.assertEqual(output, '1:30pm: Charlie comments: "How\'s it going?"')

    def test_high_five(self):
        test_date = datetime.datetime(year=2008, month=7, day=31, hour=1, minute=1)
        event = events.HighFiveEvent(test_date, "Ashley", "Simon")
        output = event.renderer.single_render(event)
        self.assertEqual(output, "1:01am: Ashley high-fives Simon")


class TestHourlyRender(unittest.TestCase):
    def tearDown(self):
        events.Event.hourly_bucket = collections.OrderedDict()
        events.Event.daily_bucket = collections.OrderedDict()

    def test_no_events(self):
        output = main.render_hourly()
        self.assertEqual(output, "")

    def test_one_enter(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=23, minute=59)
        event = events.EnterEvent(test_date, "Kate")
        output = main.render_hourly()
        self.assertEqual(output.strip(), "11pm:\t1 person(s) entered")

    def test_one_leave_one_later_comment(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=59)
        event = events.LeaveEvent(test_date, "Kate")
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=3, minute=59)
        event = events.CommentEvent(test_date, "Kate", "was here")
        output = main.render_hourly()
        self.assertEqual(output.strip(), "2am:\t1 person(s) left\n\t\n3am:\t1 comment(s)")

    def test_multiple_enters_one_person(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=50)
        event = events.EnterEvent(test_date, "Kate")
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=55)
        event = events.EnterEvent(test_date, "Kate")
        output = main.render_hourly()
        self.assertEqual(output.strip(), "2am:\t1 person(s) entered")

    def test_one_high_five(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=50)
        event = events.HighFiveEvent(test_date, "Kate", "John")
        output = main.render_hourly()
        self.assertEqual(output.strip(), "2am:\t1 person(s) high fived 1 person(s)")

    def test_two_high_fives(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=50)
        event = events.HighFiveEvent(test_date, "Kate", "John")
        output = main.render_hourly()
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=55)
        event = events.HighFiveEvent(test_date, "Kate", "Lewis")
        output = main.render_hourly()
        self.assertEqual(output.strip(), "2am:\t1 person(s) high fived 2 person(s)")

    def test_two_high_fivers(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=50)
        event = events.HighFiveEvent(test_date, "Kate", "John")
        output = main.render_hourly()
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=55)
        event = events.HighFiveEvent(test_date, "Lewis", "John")
        output = main.render_hourly()
        self.assertEqual(output.strip(), "2am:\t2 person(s) high fived 1 person(s)")


class TestDailyRender(unittest.TestCase):
    def tearDown(self):
        events.Event.hourly_bucket = collections.OrderedDict()
        events.Event.daily_bucket = collections.OrderedDict()

    def test_two_days(self):
        test_date = datetime.datetime(year=2010, month=2, day=10, hour=2, minute=59)
        event = events.LeaveEvent(test_date, "Kate")
        test_date = datetime.datetime(year=2010, month=2, day=11, hour=2, minute=59)
        event = events.CommentEvent(test_date, "Kate", "was here")
        output = main.render_daily()
        self.assertEqual(output.strip(), "2-10:\t1 person(s) left\n\t\n2-11:\t1 comment(s)")


if __name__ == '__main__':
    unittest.main()
