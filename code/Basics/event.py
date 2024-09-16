from Basics.window import Window
import pygame


class Event(Window):
    """
    The event modules
    contains Some useful elenents
    """

    def __repr__(self) -> str:
        return "<Event Object>"

    def get(eventType: str) -> list:
        """
        TO GET ALL THE EVENTS,event type should be None
        """
        return pygame.event.get(eventType)

    def get_pos() -> list:
        return pygame.mouse.get_pos()

    def detect(Quit: bool = False, feedback: bool = True) -> None:
        """
        This is the module used to detect quit
        so that you don't have to write if agsin
        """
        event = None
        event_list = Event.get(None)
        for event in Event.get(None):
            match event.type:
                case pygame.QUIT:
                    pygame.quit()
                    quit()
                case pygame.VIDEOEXPOSE:
                    return "expose", event
                case pygame.VIDEORESIZE:
                    return "resize", event
                case pygame.MOUSEBUTTONDOWN:
                    if feedback:
                        return "MOUSEDOWN", event
                case pygame.MOUSEBUTTONUP:
                    if feedback:
                        return "MOUSEUP", event
                case pygame.KEYDOWN:
                    if feedback:
                        return "KEYDOWN", event
                case pygame.MOUSEMOTION:
                    if feedback:
                        return "MOUSEMOTION", event
        return "", event_list
