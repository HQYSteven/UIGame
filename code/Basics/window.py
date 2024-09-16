"""
This file contains classes which can give a experience like tkinter
based on pygame
"""

from typing import Any
import pygame
import time
import json
import random
import asyncio
import os
from Basics.mouse import Mouse


class Window:
    """
    The window modules
    """

    def initialize(
        self,
        theme_color: list[int, int, int] | tuple[int, int, int] = [0, 0, 0],
        screenWidth: int = 500,
        screenHeight: int = 500,
        title: str = "",
        full_screen: bool = False,
        no_frame: bool = False,
        resizable: bool = False,
        switch_mode: bool = False,
        round_cursor: bool = False,
        window_x: int = 100,
        window_y: int = 100,
        rounded_mouse: bool = True,
        debug: bool = False,
    ):
        """
        @ theme_color:the main color(will not change with the change of the sys theme)
        @ screenWidth: The wifth of the screen
        @ screenHeight: The height of the screen
        @ title: The title of the screen
        @ full_screen: enable full screen mode
        @ no_frame: enable no_frame
        @ resizable: enable resizable(need to add refresh_window_size fuction)
        The init module
        """
        if not no_frame:
            self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        else:
            self.screen = pygame.display.set_mode(
                (screenWidth, screenHeight), pygame.NOFRAME
            )
        os.environ["SDL_VIDEO_WINDOW_POS"] = "510,110"
        pygame.display.set_caption(title)
        pygame.key.set_repeat(1000000, 1)
        self.element_list: list = []
        self.element_types: list = []
        self.resizable = resizable
        # set the pos of the window
        self.window_x: int = window_x
        self.window_y: int = window_y
        self.title = title  # set the window's title
        self.THEME_COLOR: list[int, int, int] | tuple[int, int, int] = theme_color
        self.screenHeight = screenHeight
        self.screenWidth = screenWidth
        self.switch_mode = switch_mode
        self.FOCUSED_ELEMENT_INDEX: int = 0
        self.element_list_length: int = 0  # the length of the element list
        # some booleans
        self.full_screen: bool = full_screen
        self.no_frame: bool = no_frame
        self.round_cursor: bool = round_cursor
        self.now_focused: pygame.Surface = None
        self.MODE_CHANGED: bool = False
        self.debug: bool = False
        self.KEYBOARD_TAKE_OVER: bool = False
        self.ENABLE_MOUSE_FOCUS: bool = True
        self.mouse = Mouse(self, rounded_mouse)
        if round_cursor:
            pygame.mouse.set_visible(False)
        Window.__key_words__(self)
        Window.__init_standwards__(self)
        self.load_window_icon()

    def destory(element) -> None:
        """
        Destory The element
        """
        element.run = False

    def set_master(self, master):
        self.index = len(master.element_list)
        self.master = master
        self.screen = master.screen
        self.background_color = master.background_color

    def activate(element) -> None:
        element.run = True

    def set_callback(self, func, options: list) -> None:
        """
        @ func: The function you want to enable when the switch is clicked
        set the call back of the switch when it is enabled
        """
        self.func_callback = func
        self.func_options = options
        self.func_result = None
        return None

    def get_result(self) -> None | Any:
        """
        Get the result of the callback(resored every loop)
        """
        return self.func_result

    def read_file(name: str, startRow: int = 0, endRow: int = 1) -> str:
        """
        @ name: The Name of the file\n
        @ startRow: The row you want to start\n
        @ endRow: The row you want to stop\n
        This fuction is used to read a file.
        """
        result = ""
        # open the file user want to read.
        with open(name, mode="r") as file:
            fileList = []
            fileList = file.readlines()
            if endRow > len(fileList):
                endRow = len(fileList)
            for index in range(0, endRow):
                if index >= startRow:
                    result += fileList[index]
                    continue
        return result

    def mouse_detect(self) -> list[int, int, int, int]:
        """
        Detect when the mouse nearby
        """
        pass

    def load_from_json(self) -> None:
        json_file = Window.read_file("./config/window.json", 0, 1000)
        self.config_dict = json.loads(json_file)
        return None

    def register(self, args) -> None:
        """
        Register element or you have to refresh the element by hand
        """
        self.element_list.append(args)
        self.element_list_length += 1
        if self.debug:
            print(
                "[DEBUG]: element_list_length is now {} ".format(
                    self.element_list_length
                )
            )
        return None

    def detect_resize(self, event, **args) -> bool:
        """
        @ event: the event you get from pygame.event.get(**args)
        The new window size detect fuction!\n
        detect if the window have resized
        """
        if event.type == pygame.VIDEORESIZE:
            self.screenHeight = self.screen.get_height()
            self.screenWidth = self.screen.get_width()
            for element in args:
                element.master = self
                element.screenHeight = self.screenHeight
                element.screenWidth = self.screenWidth
            return True
        return False

    def load_window_icon(self):
        system_icon = pygame.image.load(
            json.loads(Window.read_file("./config/titlebar.json", 0, 100))[
                "window_icon"
            ]
        )
        pygame.display.set_icon(system_icon)

    def set_coordinate(self, x, y) -> None:
        self.x = x
        self.y = y
        self.x_border: int = x + self.width
        self.Y_border: int = y + self.height

    def set_pos(x, y) -> None:
        """
        Set The pos of the mouse
        """
        pygame.mouse.set_pos((x, y))

    def set_mouse_visible(self) -> None:
        """
        Make The mouse visible
        """
        pygame.mouse.set_visible(True)

    def set_mouse_invisible(self) -> None:
        """
        Set The mouse invisible
        """
        pygame.mouse.set_visible(False)

    def draw_border(self):
        pygame.draw.rect(
            self.screen,
            self.theme_color,
            [self.x, self.y, self.width, self.height],
        )

    def __init_standwards__(self) -> None:
        self.standwards = json.loads(
            Window.read_file("./config/standward.json", 0, 100)
        )
        self.THEME_COLOR: list[int] = self.standwards["theme_color"]
        self.TITLE_COLOR: list[int] = self.standwards["title_color"]
        self.SUBTITLE_COLOR: list[int] = self.standwards["subtitle_color"]
        self.background_color: list[int] = self.standwards["background"]
        self.element_background: list[int] = self.standwards["element_background"]
        self.WARN_COLOR: list[int] = self.standwards["warn"]
        self.HIGHLIGHT_COLOR: list[int] = self.standwards["highlight"]
        self.TINY_CORNER: int = self.standwards["tiny_corner"]
        self.SMALL_CORNER: int = self.standwards["small_corner"]
        self.LARGE_CORNER: int = self.standwards["large_corner"]
        self.ENORMOUS_CORNER: int = self.standwards["enormous_corner"]
        self.HEADLINE_1: int = self.standwards["headline_1"]
        self.HEADLINE_2: int = self.standwards["headline_2"]
        self.HEADLINE_3: int = self.standwards["headline_3"]
        self.HEADLINE_4: int = self.standwards["headline_4"]
        self.HEADLINE_5: int = self.standwards["headline_5"]
        self.HEADLINE_6: int = self.standwards["headline_6"]
        self.HEADLINE_7: int = self.standwards["headline_7"]
        self.SUBTITLE_LARGE: int = self.standwards["subtitle_1"]
        self.SUBTITLE_MEDIUM: int = self.standwards["subtitle_2"]
        self.SUBTITLE_SMALL: int = self.standwards["subtitle_3"]
        self.BODY_LARGE: int = self.standwards["body_large"]
        self.BODY_MEDIUM: int = self.standwards["body_medium"]
        self.BODY_SMALL: int = self.standwards["body_small"]
        self.DEFAULT_PADDING: int = self.standwards["default_padding"]
        self.BODY_COLOR: list[int] = self.standwards["body_color"]
        self.PADDING_SMALL: int = self.standwards["padding_small"]
        self.PADDING_LARGE: int = self.standwards["padding_large"]

    def judge_debug(self,reprs:str = ""):
        if self.debug:
            print(repr)

    def __key_words__(self) -> None:
        self.load_from_json()
        self.EXPOSE: int = self.config_dict["EXPOSE"]
        self.font = pygame.font.Font(
            self.config_dict["font_path"], self.config_dict["font_size"]
        )
        self.DARK_MODE: bool = False
        self.TEXT: int = self.config_dict["TEXT"]
        self.BUTTON: int = self.config_dict["BUTTON"]
        self.SWITCH: int = self.config_dict["SWITCH"]
        self.TOPBAR: int = self.config_dict["TOPBAR"]
        self.ABOUTPAGE: int = self.config_dict["ABOUTPAGE"]
        self.SPINBOX: int = self.config_dict["SPINBOX"]
        self.PROGRESSBAR: str = self.config_dict["PROGRESSBAR"]
        self.MESSAGEBOX: str = self.config_dict["MESSAGEBOX"]
        self.SWITCHER = self.config_dict["SWITCHER"]
        self.RESIZE: int = self.config_dict["RESIZE"]
        self.LISTBOX: int = self.config_dict["LISTBOX"]
        self.FRAME: int = self.config_dict["FRAME"]
        self.MESSAGEBOX: int = self.config_dict["MESSAGEBOX"]
        self.FILL_X: str = self.config_dict["FILL_X"]
        self.FILL_Y: str = self.config_dict["FILL_Y"]
        self.CHART: str = self.config_dict["CHART"]
        self.step_global: int = 3
        self.FILL_BOTH: str = self.config_dict["FILL_BOTH"]
        self.ENTRY: str = self.config_dict["ENTRY"]
        self.AUTO: str = self.config_dict["AUTO"]
        self.TITLEBAR: str = self.config_dict["TITLEBAR"]
        self.POPUP: str = self.config_dict["POPUP"]
        self.interval: float = self.config_dict["interval"]
        self.LIGHT = self.config_dict["LIGHT"]
        self.DARK = self.config_dict["DARK"]
        self.run = True
        self.THEME_MODE: str = self.config_dict["THEME_MODE"]

    def __init__(
        self,
    ) -> None:
        """
        @ screenWidth: int; The width of the screen
        @ screenHeight: int; The height Of the screen
        @ title : str; The title of the window
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.clock.tick(144)
        Window.__key_words__(self)

    def appear(self) -> None:
        """
        make a element visible
        """
        self.run = True

    def disappear(self) -> None:
        """
        make a element invisible
        """
        self.run = False

    def change_fps(self, fps: int = 144) -> None:
        """
        Change the fps of the screen
        """
        self.clock.tick(fps)
        return None

    def set_window_resizable(self, resizable: bool = False) -> None:
        """
        Make The Window Resizable Or Not
        """
        self.resizable = resizable
        pygame.RESIZABLE = resizable

    def set_no_frame(self, no_frame: bool = False) -> None:
        """
        Make The Window have no frame
        """
        self.no_frame = no_frame
        pygame.NOFRAME = False

    def set_full_screen(self, full_screen: bool = False) -> None:
        """
        Make The Window fill The whole screen
        """
        self.full_screen = True
        pygame.FULLSCREEN = full_screen

    def set_fill_y(self) -> None:
        """
        Make The window fill the screen on y-axis
        """
        pygame.FULLSCREEN = True
        y = self.screen.get_rect()[1]
        pygame.FULLSCREEN = False
        self.screenHeight = y

    def set_fill_x(self) -> None:
        pygame.FULLSCREEN = True
        x = self.screen.get_rect()[0]
        pygame.FULLSCREEN = False
        self.screenWidth = x

    async def reverse_color(color: list[int, int, int]) -> list[int, int, int]:
        """
        @ color: r,g,b value\n
        Reverse the color you send in
        """
        if color == "white":
            return "black"
        if color == "black":
            return "white"
        if not isinstance(color, list):
            return color
        return [255 - c for c in color]

    def reverse_color_not_async(color: list[int, int, int]) -> list[int, int, int]:
        """
        @ color: r,g,b value\n
        Reverse the color you send in
        """
        if color == "white":
            return "black"
        if color == "black":
            return "white"
        if not isinstance(color, list):
            return color
        return [255 - c for c in color]

    def dark_mode(self):
        self.DARK_MODE = False if self.DARK_MODE else True
        self.MODE_CHANGED = True
        self.background_color = Window.reverse_color_not_async(self.background_color)
        self.BODY_COLOR = Window.reverse_color_not_async(self.BODY_COLOR)
        self.WARN_COLOR = Window.reverse_color_not_async(self.WARN_COLOR)
        self.THEME_COLOR = Window.reverse_color_not_async(self.THEME_COLOR)
        self.SUBTITLE_COLOR = Window.reverse_color_not_async(self.SUBTITLE_COLOR)
        self.HIGHLIGHT_COLOR = Window.reverse_color_not_async(self.HIGHLIGHT_COLOR)
        self.THEME_COLOR = Window.reverse_color_not_async(self.THEME_COLOR)
        self.element_background = Window.reverse_color_not_async(
            self.element_background
        )
        self.TITLE_COLOR = Window.reverse_color_not_async(self.TITLE_COLOR)

    def refresh() -> None:
        """
        Refresh The Whole Surface\n
        (Use ```pygame.display.update()```fuc)
        """
        pygame.display.update()
        return None

    def __repr__(self) -> str:
        return f"<Window Object>:{self.master.screenWidth},{self.master.screenHeight}"

    def switch_theme(self, mode: str = "LIGHT") -> None:
        """
        @ mode: string ("LIGHT" or "DARK" or "AUTO")\n
        A fuc that can switch light/dark mode
        """
        if mode in [self.AUTO, self.DARK, self.LIGHT]:
            self.mode = mode
        else:
            raise SyntaxError(f"{self.screen} have no theme called {mode} ")
        return None

    def set_background(self, color: list) -> None:
        """
        It sets The background Color
        """
        if color == "RANDOM":
            self.background_color = [
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            ]
            return None
        self.background_color = color
        return None

    def set_display_mode(self, mode="light"):
        """
        @ mode: WINDOW.LIGHT or WINDOW.DARK or WINDOW.AUTO
        This fuc will set the element's mode
        """
        self.THEME_MODE = mode
        self.MODE_CHANGED = True

    def set_theme(self, theme: str = "light") -> None:
        """
        This fuc will set the theme
        """
        self.THEME = theme
        return None

    async def catch_tab(self, event) -> None:
        """
        @ event: pygame.event.get() -> event
        Detect if the tab is clicked
        """
        if event.key == pygame.K_TAB:
            if not self.KEYBOARD_TAKE_OVER:
                print("[DEBUG]:BE IN KEYBOARD CONTROL")
                self.KEYBOARD_TAKE_OVER = True
                self.ENABLE_MOUSE_FOCUS = False
            self.FOCUSED_ELEMENT_INDEX += 1
            self.FOCUSED_ELEMENT_INDEX %= self.element_list_length
            print(self.FOCUSED_ELEMENT_INDEX)
        if event.key == pygame.K_ESCAPE:
            if self.debug:
                print("[DEBUG]:OUT OF KEYBOARD CONTROL")
            self.KEYBOARD_TAKE_OVER = False
            self.ENABLE_MOUSE_FOCUS = True
            self.now_focused = "Mouse"
            self.element_list[self.FOCUSED_ELEMENT_INDEX].FOCUSED = False
        return None

    def refresh_all_elements(self, event_list):
        """
        Refresh All The elements
        !!!Untested Experimental Feature
        """
        # This can be zero but if it is zero ,it will be too fast (I Think)
        time.sleep(self.interval)
        self.now_focused = "Mouse"
        self.screen.fill(self.background_color)
        index = 0
        for element in self.element_list:
            if self.MODE_CHANGED:
                if element.DARK_MODE != self.DARK_MODE:
                    asyncio.run(element.dark_mode(self))
                else:
                    self.MODE_CHANGED = False
            if element.FOCUSED and self.ENABLE_MOUSE_FOCUS:
                self.now_focused = element
            if index == self.FOCUSED_ELEMENT_INDEX and self.KEYBOARD_TAKE_OVER:
                self.now_focused = element
            for event in event_list:
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    asyncio.run(self.catch_tab(event))
                asyncio.run(element.listen(event))
            asyncio.run(element.refresh())
            index += 1
        self.MODE_CHANGED = (
            False if self.element_list[0].DARK_MODE == self.DARK_MODE else True
        )

    async def listen(self):
        if self.debug:
            print("WIN Called")

    def layer_upper(self, index) -> None:
        """
        Make the layer of the element upper
        """
        element = self.element_list[index]
        del self.element_list[index]
        self.element_list.insert(index - 1, element)

    def layer_lower(self, index) -> None:
        """
        Make the layer of the element upper
        """
        element = self.element_list[index]
        del self.element_list[index]
        self.element_list.insert(index + 1, element)

    def change_to(
        color: list[int, int, int], target: list[int, int, int]
    ) -> list[int, int, int]:
        """'
        Change animate
        """
        # I don't want to ctrl-c and ctrl-v so I use a loop <(.V.)>
        for index in range(3):
            if color[index] > target[index]:
                color[index] -= 1
            if color[index] < target[index]:
                target[index] += 1
        # return the final result
        return color

    def enable_debug_mode(self) -> None:
        """
        Enable the debug mode
        """
        self.debug = True

    def disable_debug_mode(self) -> None:
        """
        Disable the debug mode
        """
        self.debug = False

    def debug_mode(self) -> None:
        self.debug = False if self.debug else True

    def mainloop(self):
        while self.run:
            self.refresh_all_elements(pygame.event.get())
            asyncio.run(self.mouse.refresh())
            Window.refresh()
