class Renderer:
    @staticmethod
    def _format_date(date):
        # Format date to "5:00am" format
        return date.strftime("%I:%M%p").lstrip("0").lower()
        
    @staticmethod
    def single_render(event):
        raise NotImplementedError()


class EnterRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = EnterRenderer._format_date(event.date)
        return "{0}: {1} enters the room".format(formatted_date, event.actor)

    @staticmethod
    def multiple_render(num_events):
        return "{0} person(s) entered".format(num_events)


class LeaveRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = LeaveRenderer._format_date(event.date)
        return "{0}: {1} leaves the room".format(formatted_date, event.actor)

    @staticmethod
    def multiple_render(num_events):
        return "{0} person(s) left".format(num_events)


class CommentRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = CommentRenderer._format_date(event.date)
        return '{0}: {1} comments: "{2}"'.format(formatted_date, event.actor, event.comment)

    @staticmethod
    def multiple_render(num_events):
        return "{0} comment(s)".format(num_events)


class HighFiveRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = HighFiveRenderer._format_date(event.date)
        return "{0}: {1} high-fives {2}".format(formatted_date, event.actor, event.actee)
    @staticmethod
    def multiple_render(event_tuple):
        num_high_fivers = event_tuple[0]
        num_high_fivees = event_tuple[1]
        return "{0} person(s) high fived {1} person(s)".format(num_high_fivers, num_high_fivees)
