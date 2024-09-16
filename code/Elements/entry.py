from Basics.window import Window
import pygame

coding = "utf8"
"""
This is a class aim to offer a inputbox module
"""


class Entry(Window):
    """
    InputBox Module
    """

    NORMAL = "normal"
    MIN = ("min",)
    PASSWORD: str = "passport"
    WHOLE: str = "whole"
    FRONT: str = "front"
    BACK: str = "back"

    def __init__(
        self,
        master: Window,
        x: int,
        y: int,
        default_str: str = "",
        height: int = 30,
        width: int = 150,
        background: list[int, int, int] | tuple[int, int, int] = [220, 220, 220],
        border: int = 0,
        border_radius: int = 5,
        text_color: list[int, int, int] = [0, 0, 0],
        font_size: int = 12,
    ) -> None:
        """
        @ x: The x-axis coordinate
        @ y: The y-axis coordinate
        @ default_str: The string which is in the entry at first(default)
        @ height: The height of the entry
        @ width: The width of the entry
        @ text_color: The color of the text(rgb list)[0,0,0] in default
        @ background: The background of the entry
        @ notice: The strings in the background
        \n This fuc will create an Entry object
        """
        self.master: Window = master
        self.screen = master.screen
        self.screenHeight = master.screenHeight
        self.theme_color = master.THEME_COLOR
        self.screenWidth = master.screenWidth
        self.font = pygame.font.Font(self.master.config_dict["font_path"], font_size)
        self.font_size = font_size
        self.default_str: str = default_str

        self.x: int = x
        self.y: int = y

        self.text_color = text_color
        self.x_border: int = x + width
        self.y_border: int = y + height

        self.width: int = width
        self.height: int = height

        self.width_present: int = self.width
        self.height_present: int = self.height

        self.width_min: int = 40
        self.height_min: int = 20

        self.text_x = 5
        self.text_y = int((self.height - self.font_size) / 2)

        self.border: int = border
        self.border_radius: int = border_radius
        self.background: list[int, int, int] | tuple[int, int, int] = background

        self.cursor_index: int = -1
        self.text_left_start: int = 0
        self.text_right_start: int = 0
        self.mode: str = self.NORMAL
        self.FOCUSED_PART: str = self.WHOLE

        self.TYPE: str = master.ENTRY
        self.text_left: str = self.default_str
        self.text_all: str = self.default_str
        self.text_right: str = ""
        self.ANIMATING: bool = False
        self.run: bool = True
        self.backspace: bool = False
        self.FOCUSED: bool = False
        self.FOCUSED: bool = False
        self.DARK_MODE: bool = False
        self.TEXT_COLOR: str = "black"
        self.force_reload()
        self.register_element(master)
        return None

    def force_reload(self):
        """
        Reload the entry
        """
        self.cursor_surface: pygame.Surface = self.font.render(
            "|", True, self.TEXT_COLOR
        )
        self.w_cursor, self.h_cursor, _, _ = self.cursor_surface.get_rect()
        self.text_front: pygame.Surface = self.font.render(
            self.default_str, True, self.text_color
        )
        self.w_front, _, _, _ = self.text_front.get_rect()
        self.text_back: pygame.Surface = self.font.render("", True, self.text_color)
        self.w_back, _, _, _ = self.text_back.get_rect()
        self.back_x = (
            self.master.DEFAULT_PADDING + self.w_cursor + self.master.PADDING_SMALL
        )
        self.front_x = self.master.DEFAULT_PADDING
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.master.background_color)
        pygame.draw.rect(
            self.surface,
            self.background,
            [0, 0, self.width, self.height],
            0,
            self.border_radius,
        )

    def mouse_detect(self) -> list[int, int, int, int]:
        match self.mode:
            case self.NORMAL:
                match self.FOCUSED_PART:
                    case self.WHOLE:
                        return (
                            self.x,
                            self.y,
                            self.width,
                            self.height,
                            self.border_radius,
                        )
                    case self.FRONT:
                        return (
                            self.x + self.front_x,
                            self.y + self.text_y,
                            self.w_front,
                            self.font_size,
                            self.border_radius,
                        )
                    case self.BACK:
                        return (
                            self.x + self.back_x,
                            self.y + self.text_y,
                            self.w_back,
                            self.font_size,
                            self.border_radius,
                        )
            case self.MIN:
                return (
                    self.x,
                    self.y,
                    self.width_min,
                    self.height_min,
                    self.master.SMALL_CORNER,
                )

    def min_mode(self):
        """
        Change mode to the minus mode
        """
        self.mode = self.MIN
        self.ANIMATING = True

    def max_mode(self):
        """
        Chane the mode to the maxium mode
        """
        self.mode = self.NORMAL
        self.ANIMATING = True

    def register_element(self, master: Window) -> Window:
        self.index = len(self.master.element_list)
        master.register(self)
        return master

    def set_coordinate(self, x, y) -> None:
        x_former = self.x
        y_former = self.y
        self.x = x
        self.y = y
        y_add = self.y - y_former
        x_add = self.x - x_former
        self.text_x += x_add
        self.text_y += y_add
        return None

    async def detect(self):
        """
        Detect if It has be focused
        """
        if self.run:
            x, y = pygame.mouse.get_pos()
            if (
                x >= self.x
                and self.y <= y
                and self.y_border >= y
                and self.x_border >= x
            ):
                self.FOCUSED = True
                self.FOCUSED_PART = self.WHOLE
                if (
                    x >= self.x + self.front_x
                    and self.y + self.text_y <= y
                    and self.y_border >= y
                    and self.x + self.front_x + self.w_front >= x
                ):
                    self.FOCUSED_PART = self.FRONT
                if (
                    x >= self.x + self.back_x
                    and self.y + self.text_y <= y
                    and self.y_border >= y
                    and self.x + self.back_x + self.w_back >= x
                ):
                    self.FOCUSED_PART = self.BACK
            else:
                self.FOCUSED = False

    async def dark_mode(self, master: Window) -> None:
        self.master.judge_debug(
                "[DEBUG]: Entry has been turned to {} mode".format(
                "dark" if self.DARK_MODE
                else "light"
            ))
        self.master = master
        self.DARK_MODE = False if self.DARK_MODE else True
        self.text_color = await Window.reverse_color(self.text_color)
        self.background = await Window.reverse_color(self.background)

    async def detect_front(self) -> None:
        if self.w_front >= self.width - 2 * self.master.DEFAULT_PADDING:
            self.text_left = self.text_left[1:]
            self.text_left_start += 1
            if self.cursor_index < len(self.text_all) - 1:
                self.text_right += self.text_all[self.cursor_index + 1]

    async def detect_key(self, event) -> None:
        match event.key:
            case pygame.K_LEFT:
                if self.text_left != "":
                    self.text_right = self.text_left[-1] + self.text_right
                if self.cursor_index > 0:
                    self.text_left = self.text_left[0:-2]

            case pygame.K_RIGHT:
                if self.text_right != "":
                    self.text_left = self.text_left + self.text_right[0]
                    self.text_right = self.text_right[1:-1]
            case pygame.K_BACKSPACE:
                self.text_all = (
                    self.text_all[0 : self.cursor_index - 1]
                    + self.text_all[self.cursor_index : -1]
                )
                self.cursor_index -= 1
                if self.text_left != "":
                    self.text_left = self.text_left[0:-2]
                if self.cursor_index > 0:
                    self.text_left += self.text_all[self.cursor_index - 1]
            case pygame.K_DELETE:
                self.text_all = (
                    self.text_all[0 : self.cursor_index]
                    + self.text_all[self.cursor_index + 1 : -1]
                )
                if self.text_right != "":
                    self.text_right = self.text_right[1:-1]
                if self.cursor_index < len(self.text_all) - 1:
                    self.text_right += self.text_all[self.cursor_index + 1]
            case _:
                self.text_left += event.unicode
                self.cursor_index += 1
                self.text_all = (
                    self.text_all[0 : self.cursor_index]
                    + event.unicode
                    + self.text_all[self.cursor_index : -1]
                )
                self.text_right_start += 1

    async def listen(self, event: list) -> None:
        """
        @ event: The event you get (use)`for event in pygame.event.get()` or `for event in Event.get()`.They are is equal.
        This fuc will listen the keyboard events
        """
        if self.run:
            match self.mode:
                case self.NORMAL:
                    await self.detect()
                    await self.detect_front()
                    if event.type == pygame.KEYDOWN and self.FOCUSED:
                        await self.detect_key(event)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed()[2]:
                            self.MIN = True
                            self.min_mode()
                case self.MIN:
                    await self.detect_min()
                    if (
                        event.type == pygame.MOUSEBUTTONDOWN
                        and self.FOCUSED
                        and pygame.mouse.get_pressed()[2]
                    ):
                        self.max_mode()
                        self.surface.fill(self.master.background_color)
            return None

    async def detect_min(self) -> None:
        """
        Detect whether the bar have been clicked or not
        """
        if self.run:
            x, y = pygame.mouse.get_pos()
            if (
                x >= self.x
                and self.y <= y
                and self.y + self.height_min >= y
                and self.x + self.width_min >= x
            ):
                self.FOCUSED = True
            else:
                self.FOCUSED = False

    async def reloead_figures(self) -> None:
        _, _, self.w_front, _ = self.text_front.get_rect()
        _, _, self.w_back, _ = self.text_back.get_rect()
        # get the figures of the back  surface
        self.back_x = (
            self.master.DEFAULT_PADDING + self.w_cursor + self.master.PADDING_SMALL
        )
        self.front_x = self.master.DEFAULT_PADDING

    async def reload_texts(self) -> None:
        self.text_front: pygame.Surface = self.font.render(
            self.text_left, True, self.text_color
        )
        # get the figures of the front surface
        self.text_back: pygame.Surface = self.font.render(
            self.text_right, True, self.text_color
        )

    async def reload_surface(self) -> None:
        pygame.draw.rect(
            self.surface,
            self.background,
            [0, 0, self.width, self.height],
            0,
            self.border_radius,
        )
        # blit the surfaces on the screen
        self.surface.blit(self.text_front, (self.front_x, self.text_y))
        self.surface.blit(self.text_back, (self.back_x, self.text_y))
        self.surface.blit(
            self.cursor_surface,
            (
                self.front_x + self.w_front + self.w_cursor + 2,
                self.text_y,
            ),
        )
        self.screen.blit(self.surface, (self.x, self.y))

    async def refresh(self) -> None:
        if self.run:
            match self.mode:
                case self.NORMAL:
                    self.surface.fill(self.master.background_color)
                    if self.FOCUSED:
                        pygame.draw.rect(
                            self.surface,
                            self.master.THEME_COLOR,
                            [0, 0, self.width, self.height],
                            1,
                            self.border_radius,
                        )
                    if not self.ANIMATING:
                        """
                        This Part of the programme should be rewritten
                        """
                        await self.reload_texts()
                        await self.reloead_figures()
                        await self.reload_surface()
                    else:
                        if self.width - self.width_present >= 0:
                            self.width_present += (
                                int((self.width - self.width_present) / 10) + 1
                            )
                        if self.height - self.height_present >= 0:
                            self.height_present += (
                                int((self.height - self.height_present) / 10) + 1
                            )
                        pygame.draw.rect(
                            self.screen,
                            self.background,
                            [self.x, self.y, self.width_present, self.height_present],
                            self.border,
                            self.border_radius,
                        )
                        if self.FOCUSED:
                            pygame.draw.rect(
                                self.surface,
                                self.theme_color,
                                [
                                    self.x,
                                    self.y,
                                    self.width_present,
                                    self.height_present,
                                ],
                                1,
                                self.border_radius,
                            )
                        if (
                            self.width <= self.width_present
                            and self.height <= self.height_present
                        ):
                            self.ANIMATING = False
                case self.MIN:
                    if not self.ANIMATING:
                        pygame.draw.rect(
                            self.master.screen,
                            self.background,
                            [self.x, self.y, self.width_min, self.height_min],
                            0,
                            self.border_radius,
                        )
                    else:
                        if self.width_present - self.width_min >= 0:
                            self.width_present -= (
                                int((self.width_present - self.width_min) / 10) + 1
                            )
                        if self.height_present - self.height_min >= 0:
                            self.height_present -= (
                                int((self.height_present - self.height_min) / 10) + 1
                            )
                        pygame.draw.rect(
                            self.screen,
                            self.background,
                            [self.x, self.y, self.width_present, self.height_present],
                            self.border,
                            self.border_radius,
                        )
                        if (
                            self.width_present <= self.width_min
                            and self.height_present <= self.height_min
                        ):
                            self.ANIMATING = False

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.surface.set_alpha(alpha)

    def __iadd__(self, __figure):
        self.text_all = (
            self.text_all[0 : self.cursor_index]
            + __figure
            + self.text_all[self.cursor_index : -1]
        )

    def __add__(self, __figure):
        self.text_all = (
            self.text_all[0 : self.cursor_index]
            + __figure
            + self.text_all[self.cursor_index : -1]
        )
        return self

    def __iter__(self):
        for char in self.text_all:
            yield char

    def __next__(self, index):
        try:
            yield self.text_all[index + 1]
        except IndexError:
            raise StopIteration

    def __repr__(self) -> str:
        return "[Entry Object]:{} in the chart,cursor is in {}".format(
            len(self.text_all), self.cursor_index
        )
