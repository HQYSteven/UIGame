from typing import Any
from Basics.window import Window
import random
import pygame


class Text(Window):
    """
    The text Modules
    """

    def __init__(
        self,
        master: Window,
        x: int = 0,
        y: int = 0,
        text: str = "HELLO!",
        text_color: str = "black",
        border: int = 0,
        font_size: int = 12,
        theme: str = "light",
    ) -> None:
        Window.__init__(self)
        self.ANIMATING: bool = True
        self.font_size = font_size
        self.text_color = text_color
        self.master: Window = master  # the super class
        self.font: pygame.font.Font = pygame.font.Font(
            self.master.config_dict["font_path"], font_size
        )  # load the font
        self.text = self.font.render(text, 1, text_color)
        self.transparent: int = 0
        _, _, w, h = self.text.get_rect()
        w += master.DEFAULT_PADDING * 2
        h += master.DEFAULT_PADDING * 2
        self.surface: pygame.Surface = pygame.Surface((w, h))
        self.surface.fill(self.master.background_color)
        self.surface.blit(
            self.text, (self.master.DEFAULT_PADDING, self.master.DEFAULT_PADDING)
        )
        # self.surface.set_alpha(self.transparent)
        self.screen = master.screen  # get the screen(maybe it is useless but i did it just because i don't want to rewrite all the code regarding to it)
        self.master = master  # store the master class
        self.border = border  # init border
        self.x = x  # init x-axis pos
        self.theme_color = master.THEME_COLOR  # get the theme color of the window
        self.text = text  # set the text
        self.y = y  # init y-axis pos
        self.width = w
        self.x_border = self.x + self.width
        self.height = h
        self.y_border = self.y + self.height
        self.size: int = font_size  # init th font
        self.color = (
            text_color if text_color != self.AUTO else self.theme_color
        )  # decide if 'black' is suitable to the present theme,if not,use 'white'
        self.THEME = theme
        self.run: bool = True
        self.FOCUSED: bool = False
        self.DARK_MODE: bool = False
        self.TYPE: str = master.TEXT  # tell the refresher this element's type
        self.register_element()  # register the element
        return None

    def register_element(self) -> None:
        """
        Register The Text Object
        """
        self.index = len(self.master.element_list)
        self.master.register(self)

    async def listen(self, event) -> None:
        if self.run:
            await self.detect()

    async def dark_mode(self, master):
        self.master = master
        text = self.text
        self.DARK_MODE = False if self.DARK_MODE else True
        self.font: pygame.font.Font = pygame.font.Font(
            self.master.config_dict["font_path"], self.font_size
        )  # load the font
        self.text_color = await Window.reverse_color(self.text_color)
        self.text = self.font.render(self.text, 1, self.text_color)
        _, _, w, h = self.text.get_rect()
        w += self.master.DEFAULT_PADDING * 2
        h += self.master.DEFAULT_PADDING * 2
        self.surface: pygame.Surface = pygame.Surface((w, h))
        self.surface.set_alpha(300)
        self.surface.fill(master.background_color)
        self.surface.blit(
            self.text, (self.master.DEFAULT_PADDING, self.master.DEFAULT_PADDING)
        )
        self.width = w
        self.height = h
        self.text = text

    # Apparently th efollowing fucs are system method

    def __iadd__(self, __other) -> None:
        self.y += int(__other)
        return None

    def __isub__(self, __other) -> None:
        self.y -= int(__other)
        return None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return Text.refresh(self)

    def __eq__(self, __value: object) -> bool:
        return self is __value

    def __hash__(self) -> int:
        return hash(
            (self.x, self.y, self.text, self.color, self.size, self.font, self.border)
        )

    def __ilshift__(self, __scalar) -> None:
        self.x -= int(__scalar)
        return None

    def __irshift__(self, __scalar) -> None:
        self.x += int(__scalar)
        return None

    def __repr__(self) -> str:
        return f"{self.text}"

    # The Iteration fucs(That returns a iteration of the texts of the button)
    def __iter__(self):
        for char in self.text:
            yield char

    def __next__(self, index):
        try:
            yield self.text[index + 1]
        except IndexError:
            raise StopIteration

    # The end of system method

    def set_theme(self, theme: str = "light") -> None:
        """
        @ theme: The theme of the element
        """
        self.THEME = theme
        return None

    def set_color(self, color: list) -> None:
        """
        It sets the text you want's color
        """
        # set color, if random then create one randomly
        if color == "RANDOM":
            self.color = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
            return None
        self.color = color
        return None

    def set_coordinate(self, x, y) -> None:
        """
        Set The coodinate of the text object
        """
        self.x = x
        self.y = y

    def set_size(self, size: int) -> None:
        """
        It sets the text you want's size
        """
        self.size = size
        return None

    def set_text(self, text: str) -> None:
        """
        set the text of the text object
        """
        if self.text != text:
            self.text = text
            self.font: pygame.font.Font = pygame.font.Font(
                self.master.config_dict["font_path"], self.font_size
            )  # load the font
            self.text = self.font.render(text, 1, self.text_color)
            _, _, w, h = self.text.get_rect()
            w += self.master.DEFAULT_PADDING * 2
            h += self.master.DEFAULT_PADDING * 2
            self.surface: pygame.Surface = pygame.Surface((w, h))
            self.surface.fill(self.master.background_color)
            self.surface.blit(
                self.text, (self.master.DEFAULT_PADDING, self.master.DEFAULT_PADDING)
            )
            self.width = w
            self.height = h
            self.text = text
        return None

    async def detect(self):
        mousex, mousey = pygame.mouse.get_pos()
        if (
            mousex >= self.x
            and mousex <= self.x_border
            and mousey >= self.y
            and mousey <= self.y_border
        ):
            self.FOCUSED = True
        else:
            self.FOCUSED = False
            pygame.draw.rect(
                self.surface,
                self.master.background_color,
                [0, 0, self.width, self.height],
                1,
                self.master.SMALL_CORNER,
            )

    def mouse_detect(self):
        return self.x, self.y, self.width, self.height, self.master.SMALL_CORNER

    async def refresh(self) -> None:
        """
        Refresh the text object
        """
        if self.run:
            if self.ANIMATING:
                self.surface.set_alpha(self.transparent)
                if self.transparent == 200:
                    self.ANIMATING = False
                self.transparent += int((200 - self.transparent) / 10) + 1
            if self.FOCUSED:
                pygame.draw.rect(
                    self.surface,
                    self.master.THEME_COLOR,
                    [0, 0, self.width, self.height],
                    1,
                    self.master.SMALL_CORNER,
                )
            self.screen.blit(
                self.surface,
                (self.x, self.y),
            )
