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

    @staticmethod
    def pluralize(singular_word, number):
        if number == 1:
            return singular_word
        else:
            if singular_word == 'person':
                return 'people'
            elif singular_word == 'comment':
                return 'comments'
            else:
                assert "Unknown word to pluralize"


class EnterRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = EnterRenderer._format_date(event.date)
        return "{0}: {1} enters the room".format(formatted_date, event.actor)

    @staticmethod
    def multiple_render(events):
        num_actors = len({event.actor for event in events})
        pluralizable_word = EnterRenderer.pluralize("person", num_actors)
        return "{0} {1} entered".format(num_actors, pluralizable_word)


class LeaveRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = LeaveRenderer._format_date(event.date)
        return "{0}: {1} leaves the room".format(formatted_date, event.actor)

    @staticmethod
    def multiple_render(events):
        num_actors = len({event.actor for event in events})
        pluralizable_word = LeaveRenderer.pluralize("person", num_actors)
        return "{0} {1} left".format(num_actors, pluralizable_word)


class CommentRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = CommentRenderer._format_date(event.date)
        return '{0}: {1} comments: "{2}"'.format(formatted_date, event.actor, event.comment)

    @staticmethod
    def multiple_render(events):
        num_comments = len(events)
        pluralizable_word = CommentRenderer.pluralize("comment", num_comments)
        return "{0} {1}".format(num_comments, pluralizable_word)


class HighFiveRenderer(Renderer):
    @staticmethod
    def single_render(event):
        formatted_date = HighFiveRenderer._format_date(event.date)
        return "{0}: {1} high-fives {2}".format(formatted_date, event.actor, event.actee)

    @staticmethod
    def multiple_render(events):
        num_actors = len({event.actor for event in events})
        pluralizable_actors = HighFiveRenderer.pluralize("person", num_actors)
        num_actees = len({event.actee for event in events})
        pluralizable_actees = HighFiveRenderer.pluralize("person", num_actees)
        return "{0} {1} high fived {2} {3}".format(
            num_actors, pluralizable_actors, num_actees, pluralizable_actees)
