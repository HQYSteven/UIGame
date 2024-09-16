import pygame
from Basics.window import Window

"""
Progress bar module
"""


class ProgressBar(Window):
    """
    A module aims to offer a good experience in creating a progress bar
    """

    def __init__(
        self,
        master: Window,
        x: int = 0,
        y: int = 0,
        step: int = 1,
        width: int = 100,
        height: int = 10,
        from_: int = 0,
        border: int = 0,
        to: int = 100,
        mode: str = "light",
        bar_color: list[int, int, int] = [200, 200, 200],
        scale_color: list[int, int, int] = [100, 100, 200],
        border_radius: int = 5,
        loop: int = -1,
    ) -> None:
        if loop == -1:
            loop = 100000000
        self.master: Window = master
        self.border_radius: int = border_radius
        self.step: int = step
        self.ANIMATING: bool = False
        self.width: int = width
        self.screen = master.screen
        self.step_present: int = from_
        self.run: bool = True
        self.height: int = height
        self.border: int = border
        self.from_: int = from_
        self.to: int = to
        self.main_surface = pygame.Surface((self.width, self.height))
        self.main_surface.fill(self.master.background_color)
        self.mode: str = mode
        self.theme_color = master.THEME_COLOR
        self.color: list[int, int, int] = bar_color
        self.x: int = x
        self.y: int = y
        self.x_border: int = x + width
        self.y_border: int = y + height
        self.scale_color: list[int, int, int] = scale_color
        self.theme_color: list[int, int, int] = master.THEME_COLOR
        self.following_color: list[int, int, int] = [
            master.THEME_COLOR[0] + 20,
            master.THEME_COLOR[1] + 20,
            master.THEME_COLOR[2] + 20,
        ]
        self.scale_width: int = 20
        self.scale_height: int = self.height - 2
        self.loop: bool = loop
        self.color_present: list[int, int, int] = self.scale_color
        self.add_step: float = self.width / (to - from_)
        self.scale_x: int = int(self.from_ * self.add_step)
        self.START: bool = True
        self.TYPE: str = master.PROGRESSBAR
        self.FOCUSED: bool = False
        self.active_color: list[int, int, int] = [
            self.scale_color[0] + 10,
            self.scale_color[1] + 10,
            self.scale_color[2] + 10,
        ]
        self.container = pygame.Surface((width, height))
        self.container.fill(self.master.background_color)
        self.DARK_MODE: bool = False
        self.register_element()
        return None

    async def dark_mode(self, master: Window) -> None:
        self.DARK_MODE = False if self.DARK_MODE else True
        self.master = master
        self.active_color = await Window.reverse_color(self.active_color)
        self.color_present = await Window.reverse_color(self.color_present)
        self.following_color = await Window.reverse_color(self.following_color)
        self.scale_color = await Window.reverse_color(self.scale_color)
        self.theme_color = self.master.THEME_COLOR

    def register_element(
        self,
    ) -> Window:
        self.index = len(self.master.element_list)
        self.master.register(self)

    def __iter__(self):
        for index in range(self.step_present):
            yield index

    def __next__(self, index):
        while index < len(self.step_present) - 1:
            yield index + 1
        else:
            raise StopIteration

    def set_coordinate(self, x, y) -> None:
        self.x_border = x + self.width
        self.y_border = y + self.height
        self.x = x
        self.y = y

    def pause(self) -> None:
        """
        pause or start the progressbar
        """
        self.START = True if not self.START else False
        return None

    def reset(self) -> None:
        """
        reset the progress bar
        """
        self.step_present = self.from_
        self.scale_x = int(self.x + self.from_ * self.add_step)
        return None

    def set_scale(self, scale: int) -> None:
        """
        @ scale: The number you want to set in
        set the scales
        """
        self.step_present = scale % (self.to - self.from_)
        self.scale_x = int(self.from_ * self.add_step)
        return None

    def get(self) -> int:
        """
        Get the value present
        """
        return self.step_present

    async def listen(self, event) -> None:
        """
        Detect if it has ben focused
        """
        if self.run:
            x, y = pygame.mouse.get_pos()
            if (
                self.x <= x
                and self.y <= y
                and self.x_border >= x
                and self.y_border >= y
            ):
                self.FOCUSED = True
                pygame.draw.rect(
                    self.container,
                    self.theme_color,
                    [0, 0, self.width, self.height],
                    1,
                    self.border_radius,
                )
            else:
                self.FOCUSED = False
            await self.detect_click(event)

    async def refresh(self) -> None:
        """
        refresh the progressbar
        """
        if self.run:
            # 绘制progress bar
            self.container.fill(self.master.background_color)
            pygame.draw.rect(
                self.container,
                self.color,
                [0, 0, self.width, self.height],
                border_radius=self.border_radius,
            )
            # 增加现在的实时step
            if self.START:
                self.step_present += 1
                self.scale_x = int(self.step_present * self.add_step)
                if self.scale_x >= self.width and self.loop:
                    self.loop -= 1
                    self.scale_x = 0
                    self.step_present = 0
                if self.loop == 0:
                    self.START = False
            # 绘制进度条的浅色部分
            if self.scale_x <= self.scale_width:
                self.scale_x = self.scale_width
            pygame.draw.rect(
                self.container,
                self.active_color,
                [0, 0, self.scale_x, self.height],
                0,
                self.border_radius,
            )
            pygame.draw.rect(
                self.container,
                self.theme_color,
                [
                    self.scale_x - self.scale_width,
                    1,
                    self.scale_width,
                    self.scale_height,
                ],
                0,
                self.border_radius,
            )
            self.screen.blit(self.container, (self.x, self.y))

    async def detect_click(self, event) -> bool:
        """
        detect if the mouse have dragged the scale
        """
        if self.run:
            mousex, mousey = pygame.mouse.get_pos()
            mousex -= 20
            if event.type == pygame.MOUSEBUTTONUP and self.FOCUSED and self.loop:
                self.START = True
                # 当鼠标松开，复原scale,计算当前的step
                self.color_present = self.scale_color
                self.step_present = int(
                    ((mousex - self.x) / self.width) * (self.to - self.from_)
                )
                self.scale_x = int(self.from_ * self.add_step)

            if event.type == pygame.MOUSEBUTTONDOWN and self.FOCUSED:
                mousex, mousey = pygame.mouse.get_pos()
                # 当鼠标按下时，递增停止，scale位置为鼠标位置
                if (
                    mousex >= self.scale_x
                    and mousex <= self.scale_x + self.scale_width
                    and mousey >= self.y + 1
                    and mousey <= self.y + self.height
                ):
                    self.START = False
                    self.color_present = self.scale_color
                    self.scale_x = mousex - self.scale_width

            return False

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.container.set_alpha(alpha)

    def mouse_detect(self) -> list[int, int, int, int]:
        return (
            self.scale_x + self.x - self.scale_width,
            self.y + 1,
            self.scale_width,
            self.scale_height,
            self.border_radius,
        )
