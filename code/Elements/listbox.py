import pygame
from Basics.window import Window
from typing import Any

coding = "utf8"


class Listbox(Window):
    """
    listbox module(experimental)
    """

    def __init__(
        self,
        master: Window,
        background: list[int] = [100, 100, 100],
        foreground: list[int] = [150, 150, 205],
        height: int = 100,
        width: int = 100,
        elements: list[str] = [],
        x: int = 0,
        y: int = 0,
        border: int = 0,
        radius: int = 3,
        font_size: int = 12,
        func=None,
        func_options: list = [],
    ) -> None:
        Window.__init__(self)
        self.master: Window = master
        self.screen = master.screen
        self.theme_color = master.THEME_COLOR
        self.screenHeight = master.screenHeight
        self.element_present_index: int = 0
        self.screenWidth = master.screenWidth
        self.master = master
        self.run: bool = True
        self.background: list[int] = background  # the background of the listbox
        self.foreground: list[int] = foreground  # the foreground (button's color)
        self.height: int = height
        self.width: int = width
        self.maximum_displaying: int = (self.height - 10) // (
            font_size + 3
        ) - 1  # This have to min 1 because the index starts from 0
        # init theme
        self.THEME: str = "light"
        # get the elements
        self.elements: list[str] = elements
        self.x: int = x
        self.mouse_focus: bool = True
        self.TEXT_COLOR: str = "black"
        self.TYPE: str = master.LISTBOX
        self.ANIMATING: bool = False
        self.UP: bool = False
        self.DOWN: bool = False
        self.y: int = y
        self.font_size = font_size
        self.add: int = 0
        self.FOCUSED: bool = (
            False  # This boolean will tell the element whether it is focused
        )
        self.start = 0
        self.add: int = 0
        self.end = self.maximum_displaying
        self.border: int = border
        self.length: int = len(elements)
        self.radius: int = radius
        self.x_border: int = x + width
        self.y_border: int = y + height
        self.func_callback = func
        self.DARK_MODE: bool = False
        self.func_options: list = func_options
        self.func_results: None | Any = None
        # get the activate color from the foreground
        self.add_present: int = 0
        self.force_reload()
        self.register_element()
        return None

    def force_reload(self) -> None:
        """
        This function will reload the whole Listbox
        """
        if self.master.debug:
            print("[DEBUG]: Listbox reloaded")
        self.element_surfaces: list = []
        self.main_surface = pygame.Surface((self.width, self.height))
        self.main_surface.fill(self.master.background_color)
        index = 0
        for element in self.elements:
            element_surface = pygame.Surface((self.width - 6, self.font_size + 3))
            element_surface.fill(self.background)
            pygame.draw.rect(
                element_surface,
                self.foreground,
                [0, 0, self.width - 6, self.font_size + 6],
                0,
                self.radius,
            )
            text = self.font.render(element, True, "black")
            element_surface.blit(
                text,
                (
                    int((self.width - 6 - text.get_rect()[2]) / 2),
                    int((self.height - text.get_rect()[3]) / 2),
                ),
            )
            self.element_surfaces.append(element_surface)
            self.main_surface.blit(
                element_surface, (3, index * (self.font_size + 8) + 3)
            )
            index += 1
        self.active_color: list[int] = [
            self.foreground[0] + 50,
            self.foreground[1] + 50,
            self.foreground[2] + 50,
        ]
        self.element_surfaces_active: list = []
        for element in self.elements:
            element_surface = pygame.Surface((self.width - 6, self.font_size + 3))
            element_surface.fill(self.background)
            pygame.draw.rect(
                element_surface,
                self.active_color,
                [0, 0, self.width - 6, self.font_size + 6],
                0,
                self.radius,
            )
            text = self.font.render(element, True, "black")
            element_surface.blit(text, (5, int((self.height - text.get_rect()[3]) / 2)))
            self.element_surfaces_active.append(element_surface)
            self.main_surface.blit(
                element_surface, (3, index * (self.font_size + 8) + 3)
            )
            index += 1

    async def dark_mode(self, master: Window) -> None:
        if self.master.debug:
            print(
                "[DEBUG]: Listbox has been turned to dark mode"
                if self.DARK_MODE
                else "[DEBUG]: Listbox has been turned to light mode"
            )
        self.DARK_MODE = False if self.DARK_MODE else True
        self.master = master
        self.background = await Window.reverse_color(self.background)
        self.TEXT_COLOR = await Window.reverse_color(self.TEXT_COLOR)
        self.active_color = await Window.reverse_color(self.active_color)
        self.force_reload()

    def mouse_detect(self):
        return (
            self.x + 3,
            self.y + self.add + 3 + (self.font_size + 8) * self.element_present_index,
            self.width - 6,
            self.font_size + self.master.PADDING_SMALL,
            self.master.LARGE_CORNER,
        )

    def register_element(self) -> None:
        self.index = len(self.master.element_list)
        self.master.register(self)

    def __iter__(self):
        for element in self.elements:
            yield element
        raise StopIteration

    def __next__(self, index) -> str:
        try:
            return self.elements[index + 1]
        except IndexError:
            raise StopIteration

    def __iadd__(self, __other) -> None:
        self.y += int(__other)
        return None

    def __isub__(self, __other) -> None:
        self.y -= int(__other)
        return None

    def __getitem__(self, __index) -> str:
        return self.elements[__index]

    def __setitem__(self, __index, __other) -> None:
        self.elements[__index] = __other

    def __len__(self):
        return len(self.elements)

    def __ilshift__(self, __scalar) -> None:
        self.x -= int(__scalar)
        return None

    def __irshift__(self, __scalar) -> None:
        self.x += int(__scalar)
        return None

    def set_element(self, elements: list[str]):
        """
        @ elements: The list of choices(str only)
        """
        self.elements = elements
        return None

    def set_background(self, color: list[int]) -> None:
        """
        It will set the element's background
        """
        self.background = color
        return None

    def set_text(self, index: int = 0, text: str = "") -> None:
        """
        @ index: The index Of The element
        It will set the text of the element you sent in
        """
        self.elements[index] = text
        return None

    def set_active_color(self, color: list[int] = [100, 100, 100]) -> None:
        """
        @ color: The color when the choice is active
        This fuc will set the active color
        """
        self.active_color = color
        return None

    def set_pos(self, x: int = 0, y: int = 0) -> None:
        """
        @ x: The x-axis pos
        @ y: The y-axis pos
        This fuc will set the element's pos
        """
        self.x = x
        self.y = y
        return None

    def detect(self):
        if self.run:
            x, y = pygame.mouse.get_pos()
            if (
                x >= self.x
                and self.y <= y
                and self.y_border >= y
                and self.x_border >= x
            ):
                self.FOCUSED = True
                self.mouse_focus = True
            else:
                self.FOCUSED = False

    def callback(self) -> None | Any:
        """
        The callback of the compenent
        """
        if self.func_callback is not None:
            return self.func_callback(self.func_options)
        return None

    async def detect_mouse_wheel_direction(self, event):
        self.func_result = self.callback()
        if event.y > 0:
            self.UP = True
            self.start -= 1
            self.end -= 1
            if self.start <= 0:
                self.start = 0
                self.ANIMATING = False
                # debug need
                self.master.judge_debug("[DEBUG]:Animatation stopped")
            if self.end <= self.length:
                self.end = self.length
                self.ANIMATING = False
                # debug need
                self.master.judge_debug("[DEBUG]:Animatation stopped")
        elif event.y < 0:
            self.DOWN = True
            self.start += 1
            self.end += 1
            if self.end >= self.length:
                self.end = self.length
                self.ANIMATING = False
                # debug need
                self.master.judge_debug("[DEBUG]:Animatation stopped")
                self.start = self.length - self.maximum_displaying
            if self.start <= 0:
                self.start = 0
                self.ANIMATING = False
                # debug need
                self.master.judge_debug("[DEBUG]:Animatation stopped")
        self.ANIMATING = True

    async def detect_mouse_wheel_unfocused(self, event) -> None:
        self.func_result = self.callback()
        if event.y > 0:
            self.UP = True
            self.start -= 1
            self.end -= 1
            if self.start <= 0:
                self.start = 0
                self.ANIMATING = False
                # debug need
                self.master.judge_debug("[DEBUG]:Animatation stopped")
            if self.end <= self.length:
                self.end = self.length
                self.ANIMATING = False
                # debug need
                self.master.judge_debug("[DEBUG]:Animatation stopped")

    async def listen(self, event):
        """
        @ event: element from ```pygame.event.get()```
        Detect keyboard scroll event
        """
        if self.run:
            self.detect()
            if self.FOCUSED:
                await self.detect_mouse_wheel_direction(event)
                if event.type == pygame.MOUSEWHEEL:
                    await self.detect_mouse_wheel_unfocused(event)
                else:
                    self.UP = False
                    self.DOWN = False

    def draw_border(self):
        """
        Draw The border of the element focused
        """
        pygame.draw.rect(
            self.screen,
            self.theme_color,
            [
                self.x + 3,
                3 + (self.font_size + 8) * self.element_displaying,
                self.width - 6,
                self.font_size + 3,
            ],
            1,
            self.radius,
        )

    async def reinit(self):
        self.main_surface.fill(self.master.background_color)
        pygame.draw.rect(
            self.main_surface,
            self.background,
            [0, 0, self.width, self.height],
            self.border,
            self.radius,
        )

    async def refresh_items(self, index, element_x, mousex, mousey):
        # refresh the whole listbox if not animating
        element_y = 3
        # refresh the texts
        for element in self.element_surfaces[self.start : self.end]:
            color = self.foreground
            if (
                mousex >= self.x + element_x + self.add
                and mousex <= self.x_border + self.add
                and mousey >= element_y + self.y
                and mousey <= self.y + element_y + self.font_size + 3
                or index - self.start == self.element_present_index
            ):
                if self.mouse_focus:
                    self.element_present_index = index + self.start
                    color = self.active_color
            element.fill(self.background)
            pygame.draw.rect(
                element,
                color,
                [0, 0, self.width - 6, self.font_size + 3],
                0,
                self.radius,
            )
            if self.FOCUSED:
                pygame.draw.rect(
                    self.main_surface,
                    self.master.THEME_COLOR,
                    [0, 0, self.width, self.height],
                    1,
                    self.radius,
                )
            # get the width,height of the text
            text = self.font.render(self.elements[index], True, "black")
            _, _, w, h = text.get_rect()
            # blit the text to the surface
            element.blit(
                text,
                (
                    int((self.width - 6 - w) / 2),
                    int((self.font_size + 3 - h) / 2),
                ),
            )
            # blit the whole surface
            self.main_surface.blit(element, (element_x, element_y + self.add))
            element_y += self.font_size + 8
            index += 1
        self.screen.blit(self.main_surface, (self.x, self.y))

    async def match_directions(self):  # judge if the listbox is scrolling up or down
        if self.UP:
            self.add_present -= (self.font_size + 8 + self.add_present) / 10 + 1
            if (self.font_size + 8 + self.add_present) <= 0:
                self.add -= self.font_size + 8
                self.UP = False
                self.ANIMATING = False
                self.add_present = 0
                return None
        if self.DOWN:
            self.add_present += (self.font_size + 8 - self.add_present) / 10 + 1
            if (self.font_size + 8 - self.add_present) / 10 <= 0:
                self.add += self.font_size + 8
                self.ANIMATING = False
                self.DOWN = False
                self.add_present = 0
                return None

    async def refresh_items_when_animating(
        self, element_x, element_y, mousex, mousey, index
    ) -> None:
        for element in self.element_surfaces[self.start : self.end]:
            color = self.foreground
            if (
                mousex >= self.x + element_x
                and mousex <= self.x_border
                and mousey >= element_y + self.y + self.add + self.add_present
                and mousey
                <= self.y + element_y + self.font_size + 3 + self.add + self.add_present
                or index - self.start == self.element_present_index
            ):
                if self.mouse_focus:
                    self.element_present_index = index + self.start
                    color = self.active_color
            element.fill(self.background)
            pygame.draw.rect(
                element,
                color,
                [0, 0, self.width - 6, self.font_size + 3],
                0,
                self.radius,
            )
            if self.FOCUSED:
                pygame.draw.rect(
                    self.main_surface,
                    self.master.THEME_COLOR,
                    [0, 0, self.width, self.height],
                    1,
                    self.radius,
                )
            # get the size of the text object
            self.main_surface.blit(element, (element_x, element_y))
            text = self.font.render(self.elements[index], True, "black")
            _, _, w, h = text.get_rect()
            """
                    blit the text or the text won't show
                    """
            element.blit(
                text,
                (
                    int((self.width - 6 - w) / 2),
                    int((self.font_size + 3 - h) / 2),
                ),
            )
            self.main_surface.blit(
                element,
                (
                    3,
                    index * (self.font_size + 8) + 3 + self.add + self.add_present,
                ),
            )
            element_y += self.font_size + 8
            index += 1

    async def refresh(self):
        """
        This fuc will refresh the Listbox Object
        """
        if self.run:
            await self.reinit()
            element_x = 3
            index = 0
            mousex, mousey = pygame.mouse.get_pos()
            if not self.ANIMATING:
                await self.refresh_items(index, element_x, mousex, mousey)
            else:
                # if animating,then store the present pos
                element_y = self.add_present
                await self.match_directions()
                await self.refresh_items_when_animating(
                    element_x, element_y, mousex, mousey, index
                )
                # refresh the element of the listbox
            self.screen.blit(self.main_surface, (self.x, self.y))

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.main_surface.set_alpha(alpha)
