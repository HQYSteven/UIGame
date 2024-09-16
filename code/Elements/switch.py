from typing import Any
import pygame
from Basics.window import Window


class Switch(Window):
    """
    The switch modules
    """

    def __init__(
        self,
        master: Window,
        inactive_background: list = [100, 100, 100],
        active_background: list = [100, 100, 220],
        foreground: list = [255, 255, 255],
        width: int = 40,
        font_path: str = "./asserts/default.otf",
        font_size: int = 12,
        height: int = 20,
        x: int = 0,
        y: int = 0,
        func=None,
        func_options: list = [],
    ) -> None:
        """
        @ screen: The screen you want to draw the element on
        @ screenWidth: The `width of the window`
        @ screenHeight: The `height of the element`
        @ inactive_background: The background when the element is `inactive`(Your mouse isn't on the element,rgb only,you can't use rgba list)
        @ active_background: The background when the element is `active`(Your mouse is on the element,rgb only,you can't use rgba list)
        @ foreground: The color of the choices `when the mouse is on the choice` (rgb only,you can't use rgba list)
        @ width: The `width` of the element
        @ height: The `height` of the element
        @ font_path; The `path of the font` you want to choose
        @ font_size: The `size of the text`
        @ x: The x-axis coordinate(`int only`)
        @ y: The y-axis coordinate(`int only)`
        @ fuc_callback: Th fuction when active\n
        If You Want to see its default userface,just give it the `screen` and `self`
        """
        self.master: Window = master
        Window.__key_words__(self)
        self.THEME: str = "light"
        self.TYPE: str = master.SWITCH
        self.screen = master.screen
        self.screenWidth: int = master.screenWidth
        self.screenHeight: int = master.screenHeight
        self.font = pygame.font.Font(font_path, font_size)
        self.add: int = 0
        self.ANIMATING: bool = False
        self.main_container = pygame.Surface((width, height))
        self.inactive_background: list[int] = inactive_background
        self.theme_color = master.THEME_COLOR
        self.active_background: list[int] = active_background
        self.foreground: list[int] = foreground
        self.activate_status = False
        self.slide_x = 2 + int((height - 4) / 2)
        self.x_border: int = x + width
        self.y_border: int = y + height
        self.slide_y = 2 + int((height - 4) / 2)
        self.FOCUSED: bool = False
        self.color: list[int] = inactive_background
        self.height: int = height
        self.border_radius = int((height - 4) / 2)
        self.x_present = self.slide_x
        self.width: int = width
        self.x = x
        self.DARK_MODE:bool = False
        self.y = y
        self.func_result: None | Any = None
        self.func_callback = func
        self.func_options: list = func_options
        self.register_element()
        return None

    def register_element(
        self,
    ) -> Window:
        self.index = len(self.master.element_list)
        self.master.register(self)


    def change_options(self, options: list) -> None:
        self.func_options = options

    def set_coordinate(self, x, y) -> None:
        self.x = x
        self.y = y
        self.x_border = x + self.width
        self.y_border = y + self.height
        self.slide_x = 2 + int((self.height - 4) / 2)
        self.slide_y = 2 + int((self.height - 4) / 2)

    async def dark_mode(self,master:Window)->None:
        self.DARK_MODE = False if self.DARK_MODE else True
        self.master = master
        self.foreground = await Window.reverse_color(self.foreground)
        self.color = await Window.reverse_color(self.color)


    async def detect(self):
        x, y = pygame.mouse.get_pos()
        if self.x <= x and self.x_border >= x and self.y <= y and self.y_border >= y:
            self.FOCUSED = True
        else:
            self.FOCUSED = False

    def __iadd__(self, __other) -> None:
        self.y += int(__other)
        return None

    def __isub__(self, __other) -> None:
        self.y -= int(__other)
        return None

    def __ilshift__(self, __scalar) -> None:
        self.x -= int(__scalar)
        return None

    def __irshift__(self, __scalar) -> None:
        self.x += int(__scalar)
        return None

    def __bool__(self):
        return bool(self.activate_status)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return Switch.refresh(self, *args, **kwds)

    def activate(self) -> bool:
        """
        This fuc will set the activate status of the element\n
        `if the element is activated,then disable it.`
        """
        self.activate_status = False if self.activate_status else True
        return self.activate_status

    def get_activate_status(self) -> bool:
        """
        This fuc will get the activate status and return it(True/False)\n
        if The element `is` activated:\n
        `Switch.get_activate_status(self) is True`\n
        if The element `isn't` activated:\n
        `Switch.get_activate_status(self) is False`
        """
        return not self.activate_status

    def mouse_detect(self) -> list[int, int, int, int]:
        return self.x, self.y, self.width, self.height,self.border_radius

    async def refresh(self) -> None:
        """
        It will refresh the switch
        """
            # draw the rect with border_radius(10 if the default)
        if self.run:
            if self.color == self.AUTO:
                self.color = self.theme_color
            self.main_container.fill(self.master.background_color)
            pygame.draw.rect(
                self.main_container,
                self.color,
                [0, 0, self.width, self.height],
                0,
                self.border_radius,
            )
            if not self.ANIMATING:
                # draw the circle
                pygame.draw.circle(
                    self.main_container,
                    self.foreground,
                    [self.slide_x, self.slide_y],
                    self.border_radius,
                )
            else:
                if self.activate_status:
                    self.x_present += int((self.x - self.x_present) / 50) + 1
                    if self.x_present >= self.slide_x:
                        self.ANIMATING = False
                else:
                    self.x_present -= int((self.x - self.x_present) / 50) + 1
                    if self.x_present <= self.slide_x:
                        self.ANIMATING = False
                pygame.draw.circle(
                    self.main_container,
                    self.foreground,
                    [self.x_present, self.slide_y],
                    self.border_radius,
                )
            if self.FOCUSED:
                pygame.draw.rect(
                    self.main_container,
                    self.theme_color,
                    [0, 0, self.width, self.height],
                    2,
                    self.border_radius,
                )
            self.screen.blit(self.main_container, (self.x, self.y))

    def callback(self) -> None | Any:
        """
        call back
        """
        if self.func_callback is not None:
            return self.func_callback(self.func_options)
        return None

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

    async def listen(self, event) -> bool:
        """
        This fuc will detect of the switch has been activated
        """
        if self.run:
            await self.detect()
            # detetc if it if clicked
            if self.FOCUSED and event.type == pygame.MOUSEBUTTONUP:
                # change the status
                self.func_result = self.callback()
                self.activate_status = False if self.activate_status else True
                self.ANIMATING = True
                # change the button's pos(outlook)
                if self.activate_status:
                    self.color = self.active_background
                    self.slide_x = self.width - 2 - int((self.height - 4) / 2)
                else:
                    self.slide_x = 2 + int((self.height - 4) / 2)
                    self.color = self.inactive_background
                # return The status of the switch
                return self.activate_status
            return False

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.main_container.set_alpha(alpha)
