from typing import Any
from Basics.window import Window
import pygame

coding = "utf8"


class Popup(Window):
    """
    This is a class providing a widget to achieve the feature of the pop up menu
    """

    def __init__(
        self,
        master: Window,
        pos: str = "bottom",
        height: int = 100,
        background=[220, 220, 0],
        handle_color: list[int] = [100, 100, 200],
        title: str = "Hello!",
        text: list[str] = ["This is a message box  Hi There!"],
    ) -> None:
        Window.__key_words__(self)
        self.master: Window = master
        self.screen = master.screen
        self.add: int = 0
        self.x = 0
        self.y = 0
        self.screenHeight: int = master.screenHeight
        self.height: int = height
        self.background: list[int] = background
        self.titles: str = title
        self.secondary: list = text
        self.FOCUSED: bool = False
        self.ANIMATING: bool = False
        self.TYPE: str = master.POPUP
        self.position: str = pos
        self.font = pygame.font.Font(master.config_dict["font_path"], 15)
        self.width = master.screenWidth
        self.screenWidth = master.screenWidth
        self.handle_color: list[int] = handle_color
        self.title_pos = [20, self.screenHeight - height + 20]
        if pos == "left":
            self.handle_width: int = 10
            self.handle_height: int = 20
            self.statusbar_height: int = master.screenHeight
            self.statusbar_width: int = 50
            self.y_present: int = 0
            self.x_present: int = 0
            self.handle_pos: list[int] = [
                self.screenWidth - 20,
                int(self.screenHeight / 2 - 10),
            ]

            self.pos: list[int] = [self.screenWidth - 40, 0]
        if pos == "bottom":
            self.handle_width: int = 20
            self.handle_height: int = 10
            self.statusbar_height: int = 50
            self.statusbar_width: int = master.screenWidth
            self.y_present: int = master.screenHeight
            self.x_present: int = 0
            self.handle_pos: list[int] = [
                int(self.screenWidth / 2 - 10),
                self.screenHeight - 20,
            ]

            self.pos: list[int] = [0, self.screenHeight - 40]
        if pos == "right":
            self.handle_width: int = 10
            self.handle_height: int = 20
            self.statusbar_height: int = master.screenHeight
            self.statusbar_width: int = 50
            self.y_present: int = 0
            self.x_present: int = self.screenWidth
            self.handle_pos: list[int] = [20, int(self.screenHeight / 2 - 10)]
            self.pos.append([0, 0])
        self.x_border: int = 0
        self.Y_border: int = 0
        self.DARK_MODE: bool = False
        self.register_element(master)
        return None

    async def listen(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.ANIMATING = True
            await self.detect()

    async def dark_mode(self, master: Window) -> None:
        self.master = master
        self.DARK_MODE = False if self.DARK_MODE else True
        self.handle_color = await Window.reverse_color(self.handle_color)
        self.background = await Window.reverse_color(self.background)

    def register_element(self, master: Window) -> Window:
        self.index = len(self.master.element_list)
        master.register(self)
        return master

    def __repr__(self) -> str:
        return "Popup Object!!!"

    def __iter__(self):
        for t in self.secondary:
            yield t

    def __next__(self,__index):
        try:
            yield self.secondary[__index+1]
        except IndexError:
            raise StopIteration
        
    def __iadd__(self,__other):
        self.secondary.append(__other)

    def set_text(self, text: str = "") -> None:
        """
        It sets a popup's text
        """
        self.secondary = text
        return None

    async def refresh(self):
        # refresh the secondaries first or the following statements cannot display
        await Popup.refresh_secondary(self)
        pygame.draw.rect(
            self.screen,
            self.background,
            [self.pos[0], self.pos[1], self.statusbar_width, self.statusbar_height],
            0,
            5,
        )
        pygame.draw.rect(
            self.screen,
            self.handle_color,
            [
                self.handle_pos[0],
                self.handle_pos[1],
                self.handle_width,
                self.handle_height,
            ],
            0,
            3,
        )

    def __len__(self):
        return len(self.secondary)

    def __getitem__(self, __index) -> str:
        return self.secondary[__index]

    def __setitem__(self, __index, __other) -> None:
        self.secondary[__index] = __other
        return None

    async def detect(self):
        """
        It detects if mouse has clicked some elements
        """
        pos = pygame.mouse.get_pos()
        if (
            pos[0] >= self.pos[0]
            and pos[0] <= self.pos[0] + self.statusbar_width
            and pos[1] > self.pos[1]
            and pos[1] <= self.pos[1] + self.statusbar_height
        ):
            self.FOCUSED = True
        else:
            self.FOCUSED = False

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return Popup.refresh(self)

    async def refresh_secondary(self):
        if not self.ANIMATING:
            font = pygame.font.Font(self.config_dict["font_path"], 20)
            if self.FOCUSED:
                pygame.draw.rect(
                    self.screen,
                    self.background,
                    [0, self.screenHeight - self.height, self.screenWidth, self.height],
                    0,
                    10,
                )
                text = pygame.font.Font.render(font, self.titles, True, [0, 0, 0], None)
                self.screen.blit(
                    text,
                    self.title_pos,
                )
                font = pygame.font.Font(self.master.config_dict["font_path"], 12)
                for txt in self.secondary:
                    text = pygame.font.Font.render(font, txt, True, [0, 0, 0], None)
                    self.screen.blit(
                        text,
                        [self.title_pos[0], self.title_pos[1] + 50],
                    )
        else:
            if self.FOCUSED:
                self.y_present -= int((self.y_present - self.y) / 10) + 1
                if self.y_present <= self.screenHeight - self.height:
                    self.add = 0
                    self.y_present = self.screenHeight - self.height
                    self.ANIMATING = False
            else:
                self.y_present += (
                    int((self.master.screenHeight - self.y_present) / 10) + 1
                )
                if self.y_present >= self.master.screenHeight:
                    self.ANIMATING = False
                    self.y_present = self.master.screenHeight
            pygame.draw.rect(
                self.screen,
                self.background,
                [0, self.y_present, self.screenWidth, self.height],
                0,
                10,
            )
        return None

    def mouse_detect(self) -> list[int, int, int, int]:
        return self.x, self.y_present, self.width, self.height, 10
