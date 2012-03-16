class Renderer:
    @staticmethod
    def _format_date(date):
        """ Format date to "5:00am" format """
        return date.strftime("%I:%M%p").lstrip("0").lower()
        
    @staticmethod
    def single_render(event):
        """ Return a string representing a single event """
        raise NotImplementedError()

    @staticmethod
    def multiple_render(events):
        """ Return a string representing multiple events """
        raise NotImplementedError()


class EnterRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = EnterRenderer._format_date(event.date)
        return "{0}: {1} enters the room".format(formatted_date, event.actor)

    @staticmethod
    def multiple_render(events):
        actor_set = {event.actor for event in events}
        return "{0} person(s) entered".format(len(actor_set))


class LeaveRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = LeaveRenderer._format_date(event.date)
        return "{0}: {1} leaves the room".format(formatted_date, event.actor)

    @staticmethod
    def multiple_render(events):
        actor_set = {event.actor for event in events}
        return "{0} person(s) left".format(len(actor_set))


class CommentRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = CommentRenderer._format_date(event.date)
        return '{0}: {1} comments: "{2}"'.format(formatted_date, event.actor, event.comment)

    @staticmethod
    def multiple_render(events):
        return "{0} comment(s)".format(len(events))


class HighFiveRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = HighFiveRenderer._format_date(event.date)
        return "{0}: {1} high-fives {2}".format(formatted_date, event.actor, event.actee)

    @staticmethod
    def multiple_render(events):
        actor_set = {event.actor for event in events}
        actee_set = {event.actee for event in events}
        return "{0} person(s) high fived {1} person(s)".format(len(actor_set), len(actee_set))
