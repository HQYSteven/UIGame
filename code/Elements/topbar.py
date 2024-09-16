from typing import Any
from Basics.window import Window
import pygame


class Topbar(Window):
    """
    The topbar fuc
    """

    def __init__(
        self, master: Window, y: int = 0, height: int = 50, element_width: int = 80
    ) -> None:
        Window.__init__(self)
        self.master: Window = master
        self.add = 0
        self.x: int = 0
        self.y: int = y
        self.height: int = height
        self.screenHeight: int = master.screenHeight
        self.screenWidth: int = master.screenWidth
        self.element_width: int = element_width
        self.active_color: list = (
            self.master.THEME_COLOR
        )  # the color when it is activated
        self.bar_text_list: list[str] = []  # the text of each content
        self.element_text_y_list: list[list] = []  # the y coordinate of the secondaries
        self.bar_height_list: list[int] = []  # the height of each content
        self.bar_elements_text_list: list[list[str]] = []  # The content of the topbar
        self.bar_surfaces_list: list[list[pygame.Surface]] = []
        self.bar_text_x_lists: list[list[int]] = []
        self.bar_text_y_lists: list[list[int]]
        self.y_present: int = self.y
        self.color: list = self.master.element_background
        self.theme_color: list[int, int, int] = master.THEME_COLOR

        self.top_container = pygame.Surface((self.screenWidth, self.height))
        self.top_container.fill(self.master.element_background)
        self.FOCUSED: bool = False
        self.ANIMATING: bool = False
        self.run: bool = True

        self.TYPE: str = master.TOPBAR
        self.TEXT_COLOR = "black"
        self.register_element(self.master)
        return None

    def register_element(self, master: Window) -> Window:
        self.index = len(self.master.element_list)
        master.register(self)
        return master

    def force_reload(self) -> None:
        """
        Reload the topbar's elements
        """
        self.top_container.fill(self.master.element_background)
        index = 0
        for element in self.bar_text_list:
            y = self.y + self.height + self.master.DEFAULT_PADDING
            for bar_text in element:
                txt = self.font.render(bar_text, True, "black")
                _, _, w, h = txt.get_rect()
                x = (self.element_width - w) // 2
                self.bar_text_x_lists[index].append(x)
                self.bar_text_y_lists[index].append(y)
                surface = pygame.Surface(
                    (self.element_width, h + self.master.DEFAULT_PADDING)
                )
                surface.fill(self.master.element_background)
                surface.blit(txt, (x, y))
                self.bar_surfaces_list[index].append(surface)
                y += h + self.master.DEFAULT_PADDING
            index += 1

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return Topbar.refresh(self)

    def __repr__(self) -> str:
        return f"Topbar Object:{len(self.text)} in total"

    def create(
        self, text: str, element: list = [], color: list = [200, 200, 200]
    ) -> int:
        """
        @ text: The txet you want to display on
        It creates a topbar
        """
        self.bar_elements_text_list.append(text)
        self.active_color.append([color[0] + 30, color[1] + 30, color[2]])
        self.element_text_y_list.append([])
        container = pygame.Surface((self.height, len(element) * 40 + 4))
        container.fill(self.master.background_color)
        self.bar_surfaces_list.append(container)
        index = 0
        y_append = 0
        length = len(element)
        while index < length:
            self.element_y[-1].append(y_append)
            y_append += 17
            index += 1
        return len(self.text) - 1

    # This is pretty conplex so a decide to rewrite it
    # As a result, the  whole Topbar Module is not available
    # Due to the visitors,i may finish this part several days later.
    # Now i decide to have fun first.
    # By the way ,Good luck to myself,my score will be announced today
    # Hop i can get into the senior high school

    def add_element(self, index: int, text: str) -> int:
        """
        @ text: The txet you want to display on
        It creates a topbar element object
        """
        self.element[index].append(text)
        return len(self.element) - 1

    def __iter__(self):
        for element in self.element:
            yield element

    def __next__(self, index) -> str:
        try:
            return self.element[index + 1]
        except IndexError:
            raise StopIteration

    def detect_topbar_click(self, mousePos: list) -> int:
        """
        A fuc used to detect if the object of the topbar has been clicked.
        """
        x, y = mousePos
        index = 0
        x_detect = 0
        y_detect = 10
        for text in self.text:
            if (
                x >= x_detect
                and x <= x_detect + 60
                and y > y_detect
                and y <= y_detect + 50
            ):
                self.status[index] = True if self.status[index] is not True else False
                return index, text

            x_detect += 60
            index += 1

    def set_color(self, color) -> None:
        self.color = color

    def listen(self, event):
        if self.run:
            _, y = pygame.mouse.get_pos()
            if (
                event.type == pygame.MOUSEBUTTONUP
                and y >= self.y
                and y <= self.height + self.y
            ):
                self.ANIMATING = True
                self.FOCUSED = True
                self.detect_topbar_click(pygame.mouse.get_pos())
            else:
                self.FOCUSED = False

    def refresh(self) -> None:
        """
        This fuc refreshes The topbars on the screen.
        """
        if self.run:
            self.top_container.fill(self.master.background_color)
            pygame.draw.rect(
                self.top_container, self.color, [0, 0, self.screenWidth, 30], 0, 5
            )
            index = 0
            for text in self.text:
                self.top_container.blit(
                    pygame.font.Font.render(
                        self.font, text, True, self.TEXT_COLOR, None
                    ),
                    (10 + (60 * index), 5),
                )
                index += 1
            self.screen.blit(self.top_container, (0, 0))
            # return Topbar.refresh_element(self)

    def refresh_element(self) -> None:
        """
        Refresh The topbar element By loop
        """
        if self.run:
            if not self.ANIMATING:
                pass
            else:
                pass
        return None

    def set_transparent(self, index, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.bar_surfaces_list[index].set_alpha(alpha)
        self.top_container.set_alpha(alpha)
