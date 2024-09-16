"""
Frame Module
From Module "Tab"
"""

from Basics.window import Window
import pygame


class Frame(Window):
    def __init__(
        self,
        master: Window,
        x: int = 0,
        y: int = 0,
        border: int = 0,
        border_color: list[int, int, int] = [100, 100, 100],
        background: list[int, int, int] = [250, 250, 250],
        width: int = 100,
        height: int = 100,
        element_list: list = [],
        radius: int = 5,
    ) -> None:
        Window.__key_words__(self)
        Window.__init_standwards__(self)
        self.master_old: Window = master
        self.screen = master.screen
        self.screenHeight = master.screenHeight
        self.screenWidth = master.screenWidth
        self.element_list: list = element_list
        self.resizable = False
        self.ANIMATING:bool = True
        self.transparent:int = 0
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.x_border: int = x + width
        self.y_border: int = y + height
        self.height: int = height
        self.border_color: int = border_color
        self.border: int = border
        self.radius: int = radius
        self.THEME_COLOR:list[int,int,int] = self.master_old.THEME_COLOR
        self.FOCUSED: bool = False
        self.theme_color: list[int, int, int] = master.THEME_COLOR
        self.run:bool = True
        self.surface:pygame.Surface = pygame.Surface((width,height))
        self.surface.fill(self.master_old.background_color)
        self.master = self
        self.TYPE:str = self.master_old.FRAME
        self.focused_index:int = -1
        self.background_color = background
        self.background = background
        index = 0
        for element in self.element_list:
            if (
                element.x >= self.width
                or element.y >= self.height
                or element.x <= self.x
                or element.y <= self.y
            ):
                del self.element_list[index]
            Window.set_master(self.element_list[index],self.master)
            index += 1
        self.register_element()
        return None

    def register(self,args):
        del self.master_old.element_list[args.index]
        Window.set_master(args,self.master)
        self.element_list.append(args)

    def __repr__(self) -> str:
        s = ""
        s += "\nFrom <Frame Object>"
        return s

    def __iter__(self):
        for element in self.element_list:
            yield element

    def __next__(self, index):
        try:
            yield self.element_list[index]
        except IndexError:
            yield StopIteration

    def register_element(self) -> None:
        """
        Register The element
        """
        Window.register(self.master_old,self)
        return None

    async def listen(self, event) -> None:
        """
        detect it the frame is focused
        """
        if self.run:
            x, y = pygame.mouse.get_pos()
            if self.x <= x and self.y <= x and self.x_border >= x and self.y_border >= y:
                self.FOCUSED = True
            else:
                self.FOCUSED = False
                pygame.draw.rect(
                    self.screen,
                    self.background_color,
                    [self.x, self.y, self.width, self.height],
                    1,
                    self.radius,
                )
            return None

    def mouse_detect(self) -> list[int]:
        try:
            return self.element_list[self.focused_index].mouse_detect()
        except IndexError:
            pass

    def refresh(self):
        """
        Refresh The Frame Module
        """
        if self.run:
            if self.FOCUSED:
                pygame.draw.rect(
                    self.screen,
                    self.theme_color,
                    [self.x, self.y, self.width, self.height],
                    1,
                    self.radius,
                )
            if not self.ANIMATING:
                pygame.draw.rect(self.surface,self.background_color,[0,0,self.height,self.width],0,self.master_old.LARGE_CORNER)
                i = 0
                sum_num = 0
                for element in self.element_list:
                    element.refresh()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            quit()
                        result = element.listen(event)
                        if result:
                            self.focused_index = i
                            self.FOCUSED = True
                        if self.focused_index == -1:
                            self.FOCUSED = False
                        sum_num += result
                        
                    i+=1
                if sum_num <= 0:
                    self.FOCUSED = False
                    self.focused_index = -1
                self.master_old.screen.blit(self.surface,(self.x,self.y))
                print("loop")
            else:
                self.transparent += int((300-self.transparent)/5)+1
                self.surface.set_alpha(self.transparent)
                if self.transparent >= 300:
                    self.ANIMATING = False
