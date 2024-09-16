import random
from typing import Any
from Basics.window import Window
import pygame

coding = "utf8"


class Button(Window):
    """
    This class contains Button Objects
    """

    FULLSCREEN: str = "fullscreen"
    NORMAL: str = "normal"

    def __repr__(self) -> str:
        return f"<Button Object>:text:{self.text},color:{self.TEXT_COLOR}"

    def __ilshift__(self, __scalar) -> None:
        self.x -= int(__scalar)
        return None

    def __irshift__(self, __scalar) -> None:
        self.x += int(__scalar)
        return None

    def __init__(
        self,
        master: Window,
        x: int = 0,
        y: int = 0,
        color: list[int, int, int] | tuple[int, int, int] = [220, 220, 220],
        height: int = 100,
        width: int = 80,
        font_path: str | None = None,
        font_size: int = 15,
        border: int = 0,
        text: str = "",
        radius: int = 5,
        theme: str = "light",
        mode: str = "normal",
        func=None,
        func_options: list = [],
        depth: int = 8,
    ) -> None:
        """
        @ x: The x-axis pos
        @ y: The y-axis pos
        @ color: rgb color list/tuple
        @ height: The height of the element
        @ width: The width of the element
        @ font_path: The path of the font(ttf?) file
        @ font_size: The size of the text
        @ border: The border of the button
        @ text: The text you want to display on the button
        @ radius: the border radius of the button(-1/0 for straight corner)
        @ callback: decide if you need its call back.\n
        This fuc will create a Button Object\n
        You will need to call the refresh method to display it later.
        """
        # record the master class
        self.master: Window = master
        # GET THE SCREEN
        self.screen = master.screen
        # get the text
        self.height: int = height
        self.text: str = text
        self.mode: str = mode
        self.width: int = width
        self.FULL = False
        self.width_present = self.width
        self.height_present = self.height
        self.run: bool = True
        # init x,y
        self.x: int = x
        self.y: int = y
        self.x_border: int = x + width
        self.y_border: int = y + height
        # graphic init
        self.surface = pygame.Surface((width, height))
        self.surface.fill(self.master.background_color)
        # get the border of the button
        self.border: int = border
        # get the color of the button
        self.color: list[int, int, int] = color
        # get the height of the button
        self.THEME: str = theme
        # register the button
        self.ANIMATING: bool = False
        self.TYPE: str = master.BUTTON
        self.height_present: int = height
        self.width_present: int = width
        self.EXPAND: bool = False
        self.depth: int = depth
        self.x_present: int = 0
        self.x_add = 0
        self.y_add = 0
        self.y_present: int = 0
        self.TEXT_COLOR: str = "black"
        self.FOCUSED: bool = False
        self.func_callback = func
        self.func_result: None | Any = None
        self.func_options: list = func_options
        # if there isn't any font get in ,then use default in window.json
        if font_path is None:
            self.font = pygame.font.Font(self.master.config_dict["font_path"], 15)
        else:
            self.font = pygame.font.Font(font_path, font_size)
        # set the radius
        self.border_radius: int = radius
        self.background_color: list[int, int, int] = self.master.background_color
        self.activate_color: list[int, int, int] = color
        self.DARK_MODE: bool = False
        self.theme_color: list[int, int, int] = master.THEME_COLOR
        self.force_reload()
        self.register_element()
        return None

    def force_reload(self) -> None:
        self.master.judge_debug("[DEBUG]: Button reloaded")
        self.background_color: list[int, int, int] = self.master.background_color
        self.surface.fill(self.background_color)
        self.font = pygame.font.Font(self.master.config_dict["font_path"], 15)
        text = pygame.font.Font.render(
            self.font, self.text, True, self.TEXT_COLOR, None
        )
        pygame.draw.rect(
            self.surface,
            self.activate_color,
            [self.x_present, self.y_present, self.width_present, self.height_present],
            border_radius=self.border_radius,
        )

        _, _, w, h = text.get_rect()
        self.surface.blit(
            text,
            (int((self.width - w) / 2), int((self.height - h) / 2)),
        )
        self.screen.blit(self.surface, (self.x, self.y))

    async def dark_mode(self, master: Window) -> None:
        self.master.judge_debug(
            "[DEBUG]: Button Module turn to {}".format(
                "dark mode" if self.master.DARK_MODE else "light mode"
            )
        )
        self.master = master
        self.DARK_MODE = not self.DARK_MODE
        self.activate_color = await Window.reverse_color(self.activate_color)
        self.TEXT_COLOR = await Window.reverse_color(self.TEXT_COLOR)
        self.force_reload()

    def register_element(self) -> Window:
        """
        register the button compunent
        """
        self.index = len(self.master.element_list)
        self.master.register(self)

    def refresh_theme_color(self) -> None:
        """
        refresh the theme color
        """
        self.theme_color: list[int, int, int] = self.master.THEME_COLOR
        return None

    # Obviously ,the following fucs are system fucs

    def __iter__(self):
        for char in self.text:
            yield char

    def __next__(self, index):
        try:
            yield self.text[index + 1]
        except IndexError:
            raise StopIteration

    def callback(self) -> None | Any:
        if self.func_callback is not None:
            return self.func_callback(self.func_options)
        return None

    def set_color(self, color: list) -> None:
        if color == "RANDOM":
            self.color = [random.randint(0, 255) for _ in range(3)]
            return None
        self.color = color
        return None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return Button.refresh(self)

    def __len__(self) -> int:
        return len(self.text)

    def __bool__(self) -> bool:
        return True if self.text != "" else False

    # The following are some simple plugins

    def set_border(self, border: int) -> None:
        self.border = border
        return None

    def set_height(self, height: int) -> None:
        self.height = height
        self.x_border: int = self.x + self.width
        self.y_border: int = self.y + height
        # graphic init
        self.surface = pygame.Surface((self.width, height))
        self.surface.fill(self.master.background_color)
        self.font = pygame.font.Font(self.master.config_dict["font_path"], 15)
        text = pygame.font.Font.render(
            self.font, self.text, True, self.TEXT_COLOR, None
        )
        pygame.draw.rect(
            self.surface,
            self.activate_color,
            [self.x_present, self.y_present, self.width_present, self.height_present],
            border_radius=self.border_radius,
        )

        _, _, w, h = text.get_rect()
        self.surface.blit(
            text,
            (int((self.width - w) / 2), int((self.height - h) / 2)),
        )
        return None

    def set_width(self, width: int) -> None:
        self.width = width
        self.x_border: int = self.x + self.width
        self.y_border: int = self.y + self.height
        # graphic init
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.master.background_color)
        self.font = pygame.font.Font(self.master.config_dict["font_path"], 15)
        text = pygame.font.Font.render(
            self.font, self.text, True, self.TEXT_COLOR, None
        )
        pygame.draw.rect(
            self.surface,
            self.activate_color,
            [self.x_present, self.y_present, self.width_present, self.height_present],
            border_radius=self.border_radius,
        )

        _, _, w, h = text.get_rect()
        self.surface.blit(
            text,
            (int((self.width - w) / 2), int((self.height - h) / 2)),
        )
        return None

    def set_radius(self, radius: int) -> None:
        self.border_radius = radius
        return None

    async def detect(self):
        """
        Detect whether it has been clicked
        """
        # Get the coordinate of the mouse
        x, y = pygame.mouse.get_pos()
        # Make it faster,or it will write evey time it runs
        if self.x <= x and self.x_border >= x and self.y <= y and self.y_border >= y:
            self.FOCUSED = True
        else:
            self.FOCUSED = False
            pygame.draw.rect(
                self.surface,
                self.background_color,
                [
                    self.x_present,
                    self.y_present,
                    self.width_present,
                    self.height_present,
                ],
                1,
                self.border_radius,
            )

    async def listen(self, event) -> None:
        """
        This fuc is used to deal with mouse input
        """
        if self.run:
            await self.detect()
            if event.type == pygame.MOUSEBUTTONUP and self.FOCUSED:
                self.ANIMATING = True
                self.EXPAND = True
                self.clicked = False
                self.master.judge_debug("[DEBUG]: Button Module has been clicked")
            if event.type == pygame.MOUSEBUTTONDOWN and self.FOCUSED:
                self.clicked = True
                self.ANIMATING = True
                self.EXPAND = False
                self.func_result = self.callback()

    def mouse_detect(self) -> list[int, int, int, int]:
        return [
            self.x + self.x_present,
            self.y + self.y_present,
            self.width_present,
            self.height_present,
            self.border_radius,
        ]

    async def refresh(self):
        """
        this fuc is used to refresh the button object
        """
        if self.run:
            # inti the font and text

            if not self.ANIMATING:
                # init the surface

                if self.FOCUSED:
                    pygame.draw.rect(
                        self.surface,
                        self.theme_color,
                        [
                            self.x_present,
                            self.y_present,
                            self.width_present,
                            self.height_present,
                        ],
                        1,
                        self.border_radius,
                    )
                self.screen.blit(self.surface, (self.x, self.y))
            else:
                self.surface.fill(self.master.background_color)
                if not self.EXPAND:  # or fill the button with active color
                    if self.x_present < self.depth:
                        self.x_add = int((self.depth - self.x_add) / 5) + 1
                        self.x_present += self.x_add
                        self.width_present -= self.x_add * 2
                    if self.y_present < self.depth:
                        self.y_add = int((self.depth - self.y_add) / 5) + 1
                        self.y_present += self.y_add
                        self.height_present -= self.y_add * 2
                    if self.x_present >= self.depth and self.y_present >= self.depth:
                        self.x_present = self.depth
                        self.y_present = self.depth
                        self.y_add, self.x_add = 0, 0
                        self.width_present = self.width - self.depth * 2
                        self.height_present = self.height - self.depth * 2
                        self.ANIMATING = False
                        self.EXPAND = True

                    # blit the main surface on the screen (In This way, the text problem will be solved)
                else:
                    if self.x_present > 0:
                        self.x_add = int((self.depth - self.x_add) / 5) + 1
                        self.x_present -= self.x_add
                        self.width_present += self.x_add * 2
                    if self.y_present > 0:
                        self.y_add = int((self.depth - self.y_add) / 5) + 1
                        self.y_present -= self.y_add
                        self.height_present += self.y_add * 2
                    if self.x_present <= 0 and self.y_present <= 0:
                        self.x_present = 0
                        self.y_present = 0
                        self.y_add, self.x_add = 0, 0
                        self.height_present = self.height
                        self.width_present = self.width
                        self.ANIMATING = False
                        self.EXPAND = False

                pygame.draw.rect(
                    self.surface,
                    self.activate_color,
                    [
                        self.x_present,
                        self.y_present,
                        self.width_present,
                        self.height_present,
                    ],
                    border_radius=self.border_radius,
                )
                pygame.draw.rect(
                    self.surface,
                    self.theme_color,
                    [
                        self.x_present,
                        self.y_present,
                        self.width_present,
                        self.height_present,
                    ],
                    1,
                    self.border_radius,
                )
                self.font = pygame.font.Font(self.master.config_dict["font_path"], 15)
                text = pygame.font.Font.render(
                    self.font, self.text, True, self.TEXT_COLOR, None
                )
                _, _, w, h = text.get_rect()
                self.surface.blit(
                    text,
                    (int((self.width - w) / 2), int((self.height - h) / 2)),
                )
                self.screen.blit(self.surface, (self.x, self.y))

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.surface.set_alpha(alpha)
        print("[DEBUG]: Button Module alpha set to {}".format(alpha))
