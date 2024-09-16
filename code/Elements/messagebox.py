"""
This is a messagebox (inspired by iOS messagebox)
"""

import pygame
from Basics.window import Window
import json


class Messagebox(Window):
    """
    This is a messagebox inspired by iOS messagebox
    """

    NORMAL = "normal"
    OK_ONLY = "ok"
    YES_OR_ON = "yn"

    def __init__(
        self,
        master: Window,
        width: int,
        height: int,
        text: str = "",
        mode: str = "normal",
    ) -> None:
        """
        @ master The top screen
        @ width: The width of the messagebox
        @ height: THe height of the massagebox
        @ text: Text u want to show
        @ mode: The mode of the massagebox['normal','ok','yn']
        This is an message box class
        """
        # init some of the figures for the messagebox
        self.screen: pygame.Surface = master.screen
        self.width: int = width
        self.height: int = height
        self.screenWidth: int = master.screenWidth
        self.screenHeight: int = master.screenHeight
        self.x = int((self.screenWidth - self.width) / 2)
        self.x_border: int = self.x + self.width
        self.y = self.screenHeight - self.height - 50
        self.font_size = self.BODY_SMALL
        self.y_border: int = self.y + self.height
        self.focused_button: int = 0
        self.add: int = 0
        self.y_present = self.screenHeight
        self.step: int = 0
        self.master: Window = master
        self.mode: str = mode
        self.text_surface: list = []
        # cut the texts into lines
        text_list = []
        medium = ""
        for char in text:
            if char == "\n":
                text_list.append(medium)
                medium = ""
            medium += char
        text_list.append(medium)
        self.text: list[str] = text_list
        # load srcs from the dir
        self.font = pygame.font.Font(
            self.master.config_dict["font_path"], self.BODY_MEDIUM
        )
        self.message_dict = json.loads(
            Messagebox.read_file("./config/messagebox.json", 0, 100)
        )
        self.background: list[int] = self.message_dict["messagebox_background"]
        self.button_background: list[int] = self.message_dict[
            "messagebox_normal_button_color"
        ]
        self.button_background_active: list[int] = self.message_dict[
            "messagebox_normal_button_active"
        ]
        for text in self.text:
            self.text_surface.append(self.master.font.render(text, 1, "black"))
        self.surface = pygame.Surface((width, height))
        # init booleans need for the init
        self.result: str | None = None
        self.DARK_MODE: bool = False
        self.ANIMATING = False
        self.run = False
        self.FOCUSED: bool = False
        self.TYPE: str = self.master.MESSAGEBOX
        self.register_element()
        self.force_reload()
        # debug
        self.activate()
        return None

    async def dark_mode(self, master: Window) -> None:
        if self.run:
            self.master.judge_debug(
                    "[DEBUG]: Messagebox has been turned to dark mode"
                    if self.DARK_MODE
                    else "[DEBUG]: Messagebox has been turned to light mode"
                )
            self.DARK_MODE = False if self.DARK_MODE else True
            self.master = master
            self.background = await Window.reverse_color(self.background)
            self.button_background = await Window.reverse_color(self.button_background)
            self.button_background_active = await Window.reverse_color(
                self.button_background_active
            )
            self.force_reload()

    def force_reload(self):
        self.master.judge_debug("[DEBUG]: Listbox has been reloaded")
        self.surface.fill(self.master.background_color)
        self.button_list: list[pygame.Surface] = []
        match self.mode:
            case "normal":
                self.button_list.append("Copy That")
            case "ok":
                self.button_list.append("Okay")
            case "yn":
                self.button_list.append("Yes")
                self.button_list.append("No")
                self.button_list.append("Cancel")
        self.button_surface: list[pygame.Surface] = []
        self.default_width = self.width - self.BODY_MEDIUM
        for button_text in self.button_list:
            button = self.master.font.render(button_text, 1, "black")
            _, _, w, _ = button.get_rect()
            x = int((self.default_width - w) / 2)
            button_surface = pygame.Surface((self.default_width, 25))
            button_surface.fill(self.background)
            pygame.draw.rect(
                button_surface,
                self.button_background,
                [0, 0, self.default_width, 25],
                0,
                self.master.SMALL_CORNER,
            )
            button_surface.blit(button, (x, 3))
            self.button_surface.append(button_surface)
        self.button_surface_copy = self.button_surface

    def mouse_detect(self) -> list[int, int, int, int]:
        return (
            self.x + 10,
            self.y
            - 10
            + self.height
            - 28 * (len(self.button_list) - self.focused_button),
            self.width - 20,
            25,
            self.master.LARGE_CORNER,
        )

    def register_element(self) -> None:
        self.index = len(self.master.element_list)
        self.master.register(self)

    async def refresh_surface(self) -> None:
        y = 30
        for surface in self.text_surface:
            self.surface.blit(surface, (50, y))
            y += self.font_size + 3

    async def refresh_buttons(self) -> None:
        y = self.height - 10 - 28 * len(self.button_list)
        for button in self.button_surface_copy:
            self.surface.blit(button, (10, y))
            y += 28

    async def refresh_all(self) -> None:
        await self.refresh_buttons()
        await self.refresh_surface()
        self.draw_focused()

    async def draw_main_frame(self) -> None:
        pygame.draw.rect(
            self.surface,
            self.background,
            [0, 0, self.width, self.height],
            0,
            self.master.LARGE_CORNER,
        )

    async def refresh(self) -> None:
        """
        Refresh the element
        """
        if self.run:
            if not self.ANIMATING:
                await self.draw_main_frame()
                await self.refresh_all()
                self.screen.blit(self.surface, [self.x, self.y])
            if self.ANIMATING:
                self.y_present -= int((self.y_present - self.y) / 10) + 1
                if self.y_present <= self.y:
                    self.ANIMATING = False
                await self.draw_main_frame()
                await self.refresh_all()
                self.screen.blit(self.surface, [self.x, self.y_present])

            if not self.run and self.ANIMATING:
                self.y_present += (
                    int((self.master.screenHeight - self.y_present) / 10) + 1
                )
                if self.y_present >= self.screenHeight:
                    self.ANIMATING = False
                await self.draw_main_frame()
                await self.refresh_surface()
                await self.refresh_buttons()
                self.screen.blit(self.surface, [self.x, self.y_present])

    def activate(self) -> None:
        """
        ACtivate The messagebox
        """
        if self.master.debug:
            print("[DEBUG]: Messagebox activated")
        self.run = True
        self.ANIMATING = True

    def inactivate(self) -> None:
        """
        shutdown The messagebox
        """
        self.master.judge_debug("[DEBUG]: Messagebox inactivated")
        self.run = False
        self.ANIMATING = True
        self.FOCUSED = False

    def draw_focused(self):
        pygame.draw.rect(
            self.screen,
            self.master.THEME_COLOR,
            [
                self.x + 10,
                self.y
                - 10
                + self.height
                - 28 * (len(self.button_list) - self.focused_button),
                self.default_width,
                25,
            ],
            1,
            10,
        )

    def __bool__(self) -> bool:
        return self.FOCUSED

    def __repr__(self) -> str:
        return "[REPR]:MESSAGEBOX"

    def __iter__(self):
        for b in self.text:
            yield b

    def __next__(self, __index):
        try:
            yield self.text[__index + 1]
        except IndexError:
            raise StopIteration

    def __iadd__(self, __other):
        self.text += __other

    async def detect_mouse_motion(self):
        y = self.y + self.height - 10 - 28 * len(self.button_list)
        mousex, mousey = pygame.mouse.get_pos()
        if (
            mousey >= self.y
            and mousey <= self.y_border
            and self.x <= mousex
            and mousex <= self.x_border
        ):
            self.FOCUSED = True
        else:
            self.FOCUSED = False
        index = 0
        for button in self.button_list:
            if (
                mousex >= self.x + 10
                and mousex <= self.x_border
                and mousey >= y
                and mousey <= y + 25
            ):
                self.focused_button = index
                self.master.judge_debug(
                        "[DEBUG]: Button {} of the Messagebox has been focuseded ".format(
                            self.focused_button
                        )
                    )
            index += 1
            y += 28

    async def listen(self, event) -> None:
        """
        Detect if it has been clicked
        """
        if self.run:
            if event.type == pygame.MOUSEMOTION:
                await self.detect_mouse_motion()
            if event.type == pygame.MOUSEBUTTONUP:
                y = self.y + self.height - 10 - 28 * len(self.button_list)
                mousex, mousey = pygame.mouse.get_pos()
                for button in self.button_list:
                    # if the button is pressed,if so ,quit the messagebox
                    if (
                        mousex >= self.x + 10
                        and mousex <= self.x_border
                        and mousey >= y
                        and mousey <= y + 25
                    ):
                        self.result = button
                        self.inactivate()
                    y += 28
        return None

    def get_result(self) -> None:
        """
        Get The result of the message
        """
        return self.result
