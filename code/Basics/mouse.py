import pygame
import json


class Mouse:
    """
    The mouse modules
    """

    def __init__(self, master, expanded: bool = True) -> None:
        self.screen = master.screen
        self.IN_ELEMENT: bool = False
        self.master = master
        self.expanded_mouse: bool = expanded
        self.element = master.element_list
        self.cursor_x, self.cursor_y = pygame.mouse.get_pos()
        self.cursor_color: list[int] = [100, 100, 100]
        self.cursor_default_color: list[int] = [100, 100, 100]
        self.cursor_click_color: list[int] = [200, 200, 200]
        self.dict:json = json.loads(Mouse.read_file("./config/mouse.json",0,100))
        self.mouse_height, self.mouse_width = self.dict["width"], self.dict["height"]
        self.step_x: int = 0
        self.step_y: int = 0
        self.color:list[int] = self.dict["color"]
        self.speed:int = self.dict["speed"]
        self.radius:int = self.dict["radius"]
        self.add: int = 0

    async def refresh_surface(self):
        self.mouse_surface = pygame.Surface((self.mouse_width, self.mouse_height))
        self.mouse_surface.fill(self.master.background_color)
        self.mouse_surface.set_alpha(100)
        pygame.draw.rect(
            self.mouse_surface,
            self.color,
            [0, 0, self.mouse_width, self.mouse_height],
            0,
            self.radius,
        )


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
    
    async def refresh(self):
        """
        Update the mouse
        """
        await self.listen(self.master)
        await self.refresh_surface()
        self.screen.blit(self.mouse_surface, [self.cursor_x, self.cursor_y])

    async def listen(self, master):
        """
        @ event: The event from `pygame.event.get()`
        """
        await Mouse.expand(self, master)

    async def expand(self, master) -> None:
        """
        @ msater: The master
        Expend the rect
        """
        if self.expanded_mouse:
            try:
                master.now_focused.TYPE
            except AttributeError:
                self.mouse_width, self.mouse_height = await self.change_to(
                    [self.dict["width"], self.dict["height"]], [self.mouse_width, self.mouse_height]
                )
                self.cursor_x, self.cursor_y = await self.change_to(
                    pygame.mouse.get_pos(), [self.cursor_x, self.cursor_y]
                )
                return None
            if not master.now_focused.ANIMATING:
                x, y, w, h,self.radius = master.now_focused.mouse_detect()
                self.mouse_width, self.mouse_height = await self.change_to(
                    [w, h],
                    [self.mouse_width, self.mouse_height],
                )
                self.cursor_x, self.cursor_y = await self.change_to(
                    [x, y], [self.cursor_x, self.cursor_y]
                )

    async def change_to(
        self, target: list[int, int], present: list[int, int]
    ) -> list[int, int]:
        """
        @ target: The aim rect
        @ present: The rect present
        Change the width,height to which you want
        """
        if target[0] > present[0]:
            present[0] += int((target[0] - present[0]) / self.speed) + 1
        if target[0] < present[0]:
            present[0] -= int((present[0] - target[0]) / self.speed) + 1
        if target[1] > present[1]:
            present[1] += int((target[1] - present[1]) / self.speed) + 1
        if target[1] < present[1]:
            present[1] -= int((present[1] - target[1]) / self.speed) + 1
        return present

    def set_pos(x, y) -> None:
        """
        Set The pos of the mouse
        """
        pygame.mouse.set_pos((x, y))

    def set_mouse_visible() -> None:
        """
        Make The mouse visible
        """
        pygame.mouse.set_visible(True)

    def set_mouse_invisible() -> None:
        """
        Set The mouse invisible
        """
        pygame.mouse.set_visible(False)

    def __bool__(self):
        return pygame.mouse.get_visible()

    def __abs__(self):
        return abs(self.x)

    def __add__(self, _value):
        return self.y + int(_value)

    def __iadd__(self, _value) -> None:
        self.y += int(_value)

    def __sub__(self, _value):
        return self.y - int(_value)

    def __isub__(self, _value):
        self.y -= int(_value)

    def __lshift__(self, _value):
        return self.x - int(_value)

    def __rshift__(self, _value):
        return self.x + int(_value)
