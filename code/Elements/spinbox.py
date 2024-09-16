from typing import Any
from Basics.window import Window
import pygame


class Spinbox(Window):
    """
    The Spinbox class (experimental)
    """

    def __repr__(self) -> str:
        return f"SpinBox object \nx:{self.x} y:{self.y} Secondaries:{self.element}"

    def __init__(
        self,
        master: Window,
        x: int = 0,
        y: int = 0,
        text: str = "",
        border: int = 0,
        height: int = 22,
        width: int = 80,
        body_color: list = [220, 220, 220],
        scale_color: list = [50, 50, 200],
        element: list = ["1", "2", "3"],
        theme: str = "light",
        radius: int = 2,
    ) -> None:
        """
        @ x: The x-coordinate of the Spinbox
        @ y: The y-coordinate of the Spinbox
        @ text: The Text which display on the spinbox when it is activated
        @ border: The border of the SpinBox
        @ height: The height of the spinbox
        @ width: The width of the spinbox
        @ body_color: The color of the body of the spinbox
        @ scale_color: The color of the scale
        @ element: The list of the elements of the spinbox
        @ theme: The theme of the spinbox
        @ radius: The border_radius of the spinbox
        """
        Window.__key_words__(self)
        self.master: Window = master
        self.screen = master.screen
        self.FOCUSED: bool = False
        self.screenHeight = master.screenHeight
        self.screenWidth = master.screenWidth
        self.x: int = x
        self.text_limit: int = int(width / 9)
        index = 0
        for text in element:
            if len(text) > self.text_limit:
                text = text[0 : self.text_limit]
                element[index] = text
            index += 1
        self.radius: int = radius
        self.THEME: str = theme
        self.add: int = 0
        self.y: int = y
        self.color_body: list[int] = body_color
        self.color_scale: list[int] = scale_color
        self.fore_background: list[int] = [
            scale_color[0] + 50,
            scale_color[1] + 50,
            scale_color[2] + 50,
        ]
        self.scale_x: int = x + width - 2 - int(width * 0.2)
        self.scale_y: int = y + 2
        self.element_present_index: int = 0
        self.scale_width: int = height - 4
        self.theme_color = master.THEME_COLOR
        self.font = pygame.font.Font(self.config_dict["font_path"], 15)
        self.element: list = element
        self.TEXT_COLOR: str = "black"
        self.ANIMATING: bool = False
        self.TYPE: str = master.SPINBOX
        self.height_final = len(self.element) * 15 + 5
        self.height_present: int = height
        self.default_text: list = text
        self.element_y: list = []
        self.border: list = border
        self.activate_status: list = []
        self.active: bool = False
        self.height: list = height
        self.width: list = width
        index = 0
        self.x_border: int = x + width
        self.y_border: int = y + height
        self.DARK_MODE: bool = False
        self.force_reload()
        self.register_element()

    def force_reload(self):
        length = len(self.element)
        y_append = self.y
        index = 0
        while index <= length:
            self.element_y.append(y_append)
            y_append += 15
            index += 1
        self.scale_height = int(self.height * 0.2)
        self.main_container = pygame.Surface((self.width, self.height))
        self.main_container.fill(self.master.background_color)
        pygame.draw.rect(
            self.main_container,
            self.color_body,
            [self.x, self.y, self.width, self.height],
            self.border,
            self.radius,
        )
        pygame.draw.rect(
            self.screen,
            self.color_scale,
            [self.scale_x, self.scale_y, self.scale_width, self.scale_height],
            0,
            self.radius,
        )
        self.text_list: list = []
        self.scale_height: int = int(self.width * 0.2)
        for t in self.element:
            text_surface = pygame.Surface((self.width, self.scale_height))
            text_display = self.font.render(t, True, "black")
            text_surface.fill(self.master.background_color)
            pygame.draw.rect(
                text_surface, self.color_body, [0, 0, self.width, self.scale_height]
            )
            text_surface.blit(text_display, (0, 0))
            self.text_list.append(text_surface)
        self.screen.blit(self.main_container, (self.x, self.y))

    async def dark_mode(self, master):
        self.master = master
        self.DARK_MODE = False if self.DARK_MODE else True
        self.color_body = await Window.reverse_color(self.color_body)
        self.color_scale = await Window.reverse_color(self.color_body)
        self.force_reload()

    def set_coordinate(self, x, y):
        x_former = self.x
        y_former = self.y
        self.x = x
        self.y = y
        x_add = self.x - x_former
        y_add = self.y - y_former
        self.scale_x += x_add
        self.scale_y += y_add
        self.x_border += x_add
        self.y_border += y_add
        index = 0
        length = len(self.element)
        y_append = y
        while index <= length:
            self.element_y[index] += y_add
            y_append += 15
            index += 1
        return None

    def register_element(self) -> Window:
        self.index = len(self.master.element_list)
        self.master.register(self)

    async def detect(self):
        """
        Detect if the element have been focused
        """
        x, y = pygame.mouse.get_pos()
        if self.x <= x and self.x_border >= x and self.y <= y and self.y_border >= y:
            self.FOCUSED = True
        else:
            self.FOCUSED = False

    def __hash__(self):
        return hash((self.x, self.y))

    def __iadd__(self, __other) -> None:
        self.y += int(__other)
        return None

    def __isub__(self, __other) -> None:
        self.y -= int(__other)
        return None

    def __iter__(self):
        for element in self.element:
            yield element

    def __next__(self, index) -> str:
        try:
            return self.element[index + 1]
        except IndexError:
            raise StopIteration

    def __ilshift__(self, __scalar) -> None:
        self.x -= int(__scalar)
        return None

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return Spinbox.refresh(self)

    def __irshift__(self, __scalar) -> None:
        self.x += int(__scalar)
        return None

    def __imul__(self, __other):
        self.x *= __other
        self.y *= __other

    def __idiv__(self, __other):
        self.x //= __other
        self.y //= __other

    def get_color(self) -> list:
        """
        It returns the color of the spinbox
        """
        return self.color_body

    def get_coordinate(self) -> tuple:
        """
        @ index: The index of the spinbox
        It returns the pos of the spinbox
        """
        return (self.x, self.y)

    def set_color(self, color: list = [0, 0, 0]) -> None:
        """
        @ color: The color you want to set
        @ index: The index of the spinbox
        It sets the color of the spinbox
        """
        self.color_body = color
        return None

    async def refresh(self) -> int:
        """
        It refreshes the userface of the spinbox
        """
        font = pygame.font.Font(self.master.config_dict["font_path"], 12)
        text = pygame.font.Font.render(
            font, self.default_text, True, self.TEXT_COLOR, None
        )
        pygame.draw.rect(
            self.screen,
            self.color_body,
            [self.x, self.y, self.width, self.height],
            self.border,
            self.radius,
        )
        if self.color_scale == self.AUTO:
            pygame.draw.rect(
                self.screen,
                self.theme_color,
                [self.scale_x, self.scale_y, self.scale_width, self.scale_height],
                0,
                self.radius,
            )
        pygame.draw.rect(
            self.screen,
            self.color_scale,
            [self.scale_x, self.scale_y, self.scale_width, self.scale_height],
            0,
            self.radius,
        )
        self.screen.blit(
            text,
            (self.x + 2, self.y + 2),
        )
        if self.FOCUSED:
            pygame.draw.rect(
                self.screen,
                self.theme_color,
                [self.x, self.y, self.width, self.height],
                1,
                2,
            )
        return await Spinbox.Refresh_element(self)

    def listen(self, event) -> None:
        """
        @ event: element from ```pygame.event.get()->list```
        Detect keyboard scroll event
        """
        self.detect()
        if self.FOCUSED:
            if not self.active:
                pygame.draw.rect(
                    self.main_container,
                    self.theme_color,
                    [self.x, self.y, self.width, self.height],
                    1,
                    self.radius,
                )
            if event.type == pygame.MOUSEBUTTONUP:
                self.active = False if self.active else True
                self.ANIMATING = True
            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_UP:
                        self.element_present_index -= (
                            1 if self.element_present_index else 0
                        )
                    case pygame.K_DOWN:
                        self.element_present_index += (
                            1 if self.element_present_index < self.length - 1 else 0
                        )

    async def refresh_texts(self, mousePos, font) -> None:
        i = 0
        for txt in self.element:
            if (
                mousePos[0] > self.x + 2
                and mousePos[0] <= self.x + self.width
                and mousePos[1] >= self.element_y[i]
                and mousePos[1] <= self.element_y[i] + 15
            ):
                pygame.draw.rect(
                    self.text_list[i],
                    self.fore_background,
                    [0, 0, self.width - 4, 15],
                    0,
                    3,
                )
                self.element_present_index = i
            else:
                pygame.draw.rect(
                    self.text_list[i],
                    self.color_body,
                    [0, 0, self.width - 4, 15],
                    0,
                    3,
                )
            text = pygame.font.Font.render(font, txt, True, self.TEXT_COLOR, None)
            self.text_list[i].blit(
                text,
                (2, 0),
            )
            self.screen.blit(self.text_list[i], [self.x + 2, self.element_y[i]])
            i += 1

    async def Refresh_element(self) -> None:
        """
        It refreshes the spinBoxes' secondaries
        """
        font = pygame.font.Font(self.master.config_dict["font_path"], 12)
        mousePos = pygame.mouse.get_pos()
        if not self.active and self.ANIMATING:
            self.height_present -= abs((self.height_present - self.height) / 10) + 1
            pygame.draw.rect(
                self.screen,
                self.color_body,
                [self.x, self.y, self.width, self.height_present],
                0,
                5,
            )
            if self.add <= 0:
                self.ANIMATING = False
                self.add = 0
        if self.active:
            if self.ANIMATING:
                self.height_present += (
                    abs((self.height_final - self.height_present) / 10) + 1
                )
                pygame.draw.rect(
                    self.screen,
                    self.color_body,
                    [self.x, self.y, self.width, self.height_present],
                    0,
                    5,
                )
                if self.height_present >= self.height_final:
                    self.ANIMATING = False

            else:
                pygame.draw.rect(
                    self.screen,
                    self.color_body,
                    [self.x, self.y, self.width, self.height_final],
                    0,
                    5,
                )
                await self.refresh_texts(mousePos, font)
        return None

    def mouse_detect(self) -> list[int, int, int, int]:
        if not self.active:
            return self.x, self.y, self.width, self.height, self.radius
        else:
            return (
                self.x + 2,
                self.element_y[self.element_present_index],
                self.width - 4,
                15,
                self.radius,
            )

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.main_container.set_alpha(alpha)
