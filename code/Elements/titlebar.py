from Basics.window import Window
import json
import pygame

"""
This file contains a titlebar class it will load the title,icon,and the close,minus,full-screen button
"""


class Titlebar(Window):
    """
    This is a title bar object
    WARNING!!!!   EXPERIMENTAL FEATURE
    """

    def __init__(self, master: Window, title: str = "Hi There!") -> None:
        """
        @ master: Window object
        @ title: The title of the window
        This method will create a titlebar object
        """
        self.master = master
        self.dict = json.loads(Window.read_file("./config/titlebar.json", 0, 100))
        self.radius: int = self.dict["button_radius"]
        self.height: int = self.dict["bar_height"]
        self.main_surface: pygame.Surface = pygame.Surface([master.screenWidth, self.height])
        # load the topbar icon(in ./icons)usually,you can change it by replace the file by your own,or change the path in ./config/window.json
        # Thanks,Harmony!
        self.cacnel: pygame.Surface = pygame.image.load(self.dict["window_close_icon"])
        # load the min and max icon(It's a str)
        self.minus = master.font.render(
            "-",
            0,
            [220, 220, 220] if master.THEME_MODE == master.DARK else [10, 10, 10],
        )
        self.full_screen = master.font.render(
            "+",
            0,
            [220, 220, 220] if master.THEME_MODE == master.DARK else [10, 10, 10],
        )
        self.screenWidth = master.screenWidth
        # load the title surface
        self.title_surface = master.font.render(title, 1, self.master.TITLE_COLOR)
        _, _, self.w, self.h = self.title_surface.get_rect()
        self.w += self.master.PADDING_SMALL * 2
        self.text = pygame.Surface((self.w, self.h))
        self.text.fill(self.master.element_background)
        self.text_pos: list[int, int] = (
            int((self.master.screenWidth - self.w - self.master.PADDING_SMALL) / 2),
            int((40 - self.h) / 2),
        )
        self.text.blit(self.title_surface, (self.master.PADDING_SMALL, 0))

        # Know if the window is resizable
        self.resizable = master.resizable
        # init all the pos of the icons
        self.cancel_pos: list[int] = [self.screenWidth - self.master.PADDING_LARGE, 20]
        self.full_screen_pos: list[int] = [
            self.screenWidth - self.master.PADDING_LARGE * 2,
            20,
        ]
        self.minus_pos: list[int] = [
            self.screenWidth - self.master.PADDING_LARGE * 3,
            20,
        ]
        self.icon_path = self.dict["window_icon"]
        # get the theme present
        self.theme = master.THEME_MODE
        # init title
        self.title: str = title
        self.TYPE: str = self.master.TITLEBAR
        self.FOCUSED: bool = False
        self.ANIMATING: bool = False
        self.focused_button: int = 0
        self.DARK_MODE:bool = False
        self.register_element()

    def register_element(self):
        self.index = len(self.master.element_list)
        self.master.register(self)

    async def dark_mode(self,master:Window):
        self.DARK_MODE = False if self.DARK_MODE else True
        self.master = master
        self.title_surface = master.font.render(self.title, 1, self.master.TITLE_COLOR)
        _, _, self.w, self.h = self.title_surface.get_rect()
        self.w += self.master.PADDING_SMALL * 2
        self.text = pygame.Surface((self.w, self.h))
        self.text.fill(self.master.element_background)
        self.text_pos: list[int, int] = (
            int((self.master.screenWidth - self.w - self.master.PADDING_SMALL) / 2),
            int((40 - self.h) / 2),
        )
        self.text.blit(self.title_surface, (self.master.PADDING_SMALL, 0))



    async def refresh(self) -> None:
        """
        Draw The titlebar
        """
        # init the main surface
        self.main_surface.fill(self.master.element_background)
        # blit the title
        self.title_surface.blit(self.main_surface, [80, 20])
        # I want to draw a title bar like the ons in MacOS
        pygame.draw.circle(
            self.main_surface,
            self.dict["close_button_color"],
            self.cancel_pos,
            self.radius,
        )
        pygame.draw.circle(
            self.main_surface,
            self.dict["full_screen_button_color"],
            self.full_screen_pos,
            self.radius,
        )
        pygame.draw.circle(
            self.main_surface,
            self.dict["minus_button_color"],
            self.minus_pos,
            self.radius,
        )
        # blit the main surface
        self.main_surface.blit(self.text, self.text_pos)
        self.master.screen.blit(self.main_surface, [0, 0])

    async def listen(self, event) -> None:
        """
        Detect if the button have been pressed
        """
        mousex, mousey = pygame.mouse.get_pos()
        if mousey <= self.height:
            self.FOCUSED = True
        else:
            self.FOCUSED = False
        if mousex >= self.text_pos[0] and mousex <= self.text_pos[0] + self.w:
            self.focused_button = 3
        if (
            mousex >= self.cancel_pos[0] - self.radius
            and mousex <= self.cancel_pos[0] + self.radius
        ):
            self.focused_button = 0
        if (
            mousex >= self.minus_pos[0] - self.radius
            and mousex <= self.minus_pos[0] + self.radius
        ):
            self.focused_button = 1
        if (
            mousex >= self.full_screen_pos[0] - self.radius
            and mousex <= self.full_screen_pos[0] + self.radius
        ):
            self.focused_button = 2
        if event.type == pygame.MOUSEBUTTONUP:
            # Get the pos user's mouse is at
            mousex, mousey = pygame.mouse.get_pos()
            # quit if the quit button is pressed
            if mousey <= self.height:
                if (
                    mousex >= self.cancel_pos[0] - self.radius
                    and mousex <= self.cancel_pos[0] + self.radius
                ):
                    # quit if the quit button have been pressed
                    quit()
                if (
                    mousex >= self.minus_pos[0] - self.radius
                    and mousex <= self.minus_pos[0] + self.radius
                ):
                    # use the prepared method the hide the screen
                    pygame.display.iconify()
                    self.master.EXPOSE = False
                if (
                    mousex >= self.full_screen_pos[0] - self.radius
                    and mousex <= self.full_screen_pos[0] + self.radius
                ):
                    # full screen if the user want to full screen
                    pygame.FULLSCREEN = True if not pygame.FULLSCREEN else False
                    self.full_screen = pygame.FULLSCREEN
            else:
                self.FOCUSED = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # display the isons if the mouse haven't been released
            mousex, mousey = pygame.mouse.get_pos()
            if mousey <= self.height:
                if (
                    mousex >= self.cancel_pos[0] - self.radius*2
                    and mousex <= self.cancel_pos[0] + self.radius*2
                ):
                    self.cacnel.blit(
                        self.main_surface,
                        [self.cancel_pos[0] - self.radius*2, self.cancel_pos[1] - self.radius*2],
                    )
                if (
                    mousex >= self.minus_pos[0] - self.radius*2
                    and mousex <= self.minus_pos[0] + self.radius*2
                ):
                    self.minus.blit(self.main_surface, [self.minus_pos[0] - self.radius*2, 20])
                if (
                    mousex >= self.full_screen_pos[0] - self.radius*2
                    and mousex <= self.full_screen_pos[0] + self.radius*2
                ):
                    self.full_screen.blit(
                        self.main_surface, [self.full_screen_pos[0] - self.radius*2, 15]
                    )
        return None

    def mouse_detect(self) -> list[int]:
        match self.focused_button:
            case 0:
                return (
                    self.cancel_pos[0] - self.radius,
                    self.cancel_pos[1] - self.radius,
                    self.radius * 2,
                    self.radius * 2,self.radius
                )
            case 1:
                return (
                    self.minus_pos[0] - self.radius,
                    self.minus_pos[1] - self.radius,
                    self.radius * 2,
                    self.radius * 2,self.radius
                )
            case 2:
                return (
                    self.full_screen_pos[0] - self.radius,
                    self.full_screen_pos[1] - self.radius,
                    self.radius * 2,
                    self.radius * 2,self.radius
                )
            case 3:
                return (
                    self.text_pos[0],
                    self.text_pos[1],
                    self.w,
                    self.h,self.radius
                )

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.main_surface.set_alpha(alpha)
