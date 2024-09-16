"""
Chart module
"""

from Basics.draw import Draw
from Basics.window import Window
import pygame


class Chart(Draw):
    STRING: str = "string"
    RECT: str = "RECT"

    def __init__(
        self,
        master: Window,
        x: int = 0,
        y: int = 0,
        datas: list[int] = [70, 20, 50, 47, 15, 60, 70, 80, 20],
        color: list[int, int, int] = [100, 100, 180],
        scale: int = 1,
        wid: int = 10,
        background: list[int, int, int] = [200, 200, 250],
        mode: str = "string",
        interval: int = 5,
    ) -> None:
        """
        @ master: The main Window
        @ x: The x-axis pos
        @ y:The y-axis pos
        @ datas: The datas of the Chart
        @ color: The color of the strings(rgb)
        @ scale: The scale of the chart
        @ wid: The width of the strings
        @ background: the background of the charts
        @ mode: The mode of the cgart(string, or rect)\n
        The Chart Module
        """
        self.datas: list[int] = datas
        datas.append(0)
        maxdata = sorted(datas)[-1]
        self.max_index = datas.index(maxdata)
        self.master = master
        self.x: int = x
        self.TYPE: int = master.CHART
        self.y: int = y
        self.height: int = int(maxdata / scale) + 20
        self.width: int = (len(datas) - 2) * (wid + interval) + 20
        self.rect_width: int = wid
        self.interval: int = interval - 3
        self.Surface: pygame.Surface = pygame.Surface((self.width, self.height))
        self.mode: str = mode
        self.background: list[int] = background
        self.scale: int = scale
        self.color: list[int] = color
        self.height_lists: list[int] = []
        self.height_add_lists: list[int] = []
        self.height_present_lists: list[int] = []
        self.FOCUSED: bool = False
        self.ANIMATING: bool = True
        self.run: bool = True
        self.sum: int = 0
        self.focused_data: int = 0
        self.DARK_MODE: bool = False
        for data in datas:
            self.height_lists.append(int(data / scale))
            self.height_add_lists.append(0)
            self.height_present_lists.append(0)
        self.register_element()

    def register_element(self):
        self.index = len(self.master.element_list)
        self.master.register(self)

    def add_figure(self, figure: int = 0, index: int = 0) -> None:
        """
        @ figure: The figure you want to add in the list
        @ index: The index you want to add at
        ADD FIGIRE
        """
        self.master.judge_debug("[DEBUG]: Figure {} added to the {} item of the chart".format(figure,index))
        self.element_list.insert(index, figure)
        maxdata = sorted(self.datas)[-1]
        self.max_index = self.datas.index(maxdata) + 1
        self.height: int = int(maxdata / self.scale) + 20
        self.width: int = (len(self.datas) - 2) * (self.rect_width + self.interval) + 20
        self.height_lists.insert(index, int(figure / self.scale))
        self.height_add_lists.insert(index, 0)
        self.height_present_lists.insert(index, int(figure / self.scale))
        self.Surface: pygame.Surface = pygame.Surface((self.width, self.height))

    def remove_figure(self, index: int = 0) -> None:
        """
        @ index: The index you want to delete at
        delete FIGIRE
        """
        self.master.judge_debug("[DEBUG]: Figure removed from the {} item of the chart".format(index))
        del self.element_list[index]
        maxdata = sorted(self.datas)[-1]
        self.max_index = self.datas.index(maxdata) + 1
        self.height: int = int(maxdata / self.scale) + 20
        self.width: int = (len(self.datas) - 2) * (self.rect_width + self.interval) + 20
        del self.height_lists[index]
        del self.height_add_lists[index]
        del self.height_present_lists[index]
        self.Surface: pygame.Surface = pygame.Surface((self.width, self.height))

    def force_reload(self) -> None:
        self.background_color = self.master.background_color
        self.refresh()

    async def dark_mode(self, master):
        self.DARK_MODE = False if self.DARK_MODE else True
        self.master = master
        self.background = await Window.reverse_color(self.background)
        self.color = await Window.reverse_color(self.color)


    async def refresh(self) -> None:
        """
        The refresh module of the chart
        """
        if self.run:
            mousex, mousey = pygame.mouse.get_pos()
            if not self.ANIMATING:
                self.Surface.fill(self.master.background_color)
                x_start = 10
                y_start = self.height - 10
                pos_before = (10, y_start - self.height_lists[0])
                pos_next = (10, y_start - self.height_lists[0])
                pygame.draw.rect(
                    self.Surface,
                    self.background,
                    [0, 0, self.width, self.height],
                    0,
                    self.master.SMALL_CORNER,
                )
                index = 0
                for height in self.height_lists:
                    if self.mode == self.RECT:
                        pygame.draw.rect(
                            self.Surface,
                            self.color,
                            [x_start, y_start - height, self.rect_width, height],
                            0,
                            self.master.SMALL_CORNER,
                        )
                        if (
                            mousex >= self.x + x_start
                            and mousex <= self.x + x_start + self.rect_width
                            and mousey >= self.y + y_start - height
                            and mousey <= self.y + y_start
                        ):
                            self.focused_data = index
                            pygame.draw.rect(
                                self.Surface,
                                self.master.THEME_COLOR,
                                [x_start, y_start - height, self.rect_width, height],
                                1,
                                self.master.SMALL_CORNER,
                            )
                    if self.mode == self.STRING:
                        pygame.draw.line(
                            self.Surface,
                            self.color,
                            pos_before,
                            pos_next,
                            self.rect_width,
                        )
                        if index + 1 < len(self.height_lists):
                            pos_before = pos_next
                            pos_next = (
                                x_start + 10,
                                y_start - self.height_lists[index + 1],
                            )
                        x_start += int(self.rect_width / 2)
                    index += 1
                    x_start += self.rect_width + self.interval
            else:
                self.Surface.fill(self.master.background_color)
                if self.mode == self.STRING:
                    self.ANIMATING = False
                if self.mode == self.RECT:
                    x_start = 10
                    self.sum = 0
                    y_start = self.height - 10
                    pos_before = (10, y_start - self.height_lists[0])
                    pos_next = (10, y_start - self.height_lists[0])
                    pygame.draw.rect(
                        self.Surface,
                        self.background,
                        [0, 0, self.width, self.height],
                        0,
                        self.master.SMALL_CORNER,
                    )
                    index = 0
                    if (
                        self.height_lists[self.max_index]
                        <= self.height_present_lists[self.max_index]
                    ):
                        self.ANIMATING = False
                    for height in self.height_lists:
                        self.height_add_lists[index] = int(
                            (height - self.height_present_lists[index]) / 10
                        )
                        if self.height_add_lists[index] <= 0:
                            self.height_add_lists[index] = 0
                            self.sum += 1
                        self.height_present_lists[index] += self.height_add_lists[index]
                        pygame.draw.rect(
                            self.Surface,
                            self.color,
                            [
                                x_start,
                                y_start - self.height_present_lists[index],
                                self.rect_width,
                                self.height_present_lists[index],
                            ],
                            0,
                            self.master.LARGE_CORNER,
                        )

                        index += 1
                        x_start += self.rect_width + self.interval
                    if self.sum == len(self.height_present_lists) - 1:
                        self.ANIMATING = False
            self.master.screen.blit(self.Surface, (self.x, self.y))

    async def listen(self, event) -> None:
        """
        Detect the events
        """
        if self.run:
            mousex, mousey = pygame.mouse.get_pos()
            if (
                self.x <= mousex
                and self.x + self.width >= mousex
                and mousey >= self.y
                and mousey <= self.y + self.height
            ):
                self.master.judge_debug("[DEBUG]: Chart got focused")
                self.FOCUSED = True
            else:
                self.FOCUSED = False

    def mouse_detect(self) -> list[int]:
        if self.mode == self.RECT:
            return (
                self.x + 10 + (self.interval + self.rect_width) * self.focused_data,
                self.y + self.height - 10 - self.height_lists[self.focused_data],
                self.rect_width,
                self.height_lists[self.focused_data],
                self.master.SMALL_CORNER,
            )
        else:
            return self.x, self.y, self.width, self.height, self.master.SMALL_CORNER
        
    def __iter__(self):
        for figure in self.element_list:
            yield figure

    def __next__(self,index):
        try:
            yield self.element_list[index + 1]
        except IndexError:
            raise StopIteration

    def __iadd__(self,__figure):
        self.add_figure(__figure,0)

    def __add__(self,__figure):
        self.element_list.insert(0,__figure)
        return self

    def __repr__(self) -> str:
        return "[Chart Object]"
