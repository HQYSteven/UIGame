import pygame
from Basics.window import Window
from Elements.button import Button

"""
This is a module aim to offer a convenient experience to switch element
"""


class Switcher(Window):
    """
    This is a module aim to offer a convenient experience to switch element
    """

    def __init__(
        self,
        master: Window,
        tabs: list[str] = ["A", "B", "C"],
        border: int = 0,
        x: int = 200,
        y: int = 150,
        width: int = 100,
        height: int = 100,
        switcher_width:int = 60,
        switcher_height:int = 30,
        elements:list[list] = [[],[],[]],
        tab_background: list[int, int, int] = [200, 200, 200],
        func_callback = None,
        func_args:list = []
    ) -> None:
        """
        @ element_list: The elements(self.BUTTON,self.SWITCH,etc)
        @ element_callback: The args you want to get in the element
        @ border: The width of the border
        @ border_color: The color of the border
        @ tabs: The str you want to display on the tabs

        """
        Window.__key_words__(self)
        self.x: int = x
        self.y: int = y
        self.master: Window = master
        self.screen = master.screen
        self.height: int = height
        self.width: int = width
        self.x_border = x + width
        self.y_border = y + height
        self.elements:list[list] = elements
        # the x y of the container
        self.switcher_width:int = switcher_width
        self.switcher_height:int = switcher_height
        self.container_x:int = self.x + int((width - switcher_width)/2)
        self.container_y:int = self.y - master.PADDING_SMALL - switcher_height
        self.tab_width:int = switcher_width//len(tabs)
        self.tab_height:int = switcher_height - 2*self.master.PADDING_SMALL
        # init the screen figures
        self.screenWidth = master.screenWidth
        self.screenHeight = master.screenHeight
        # load the font
        self.font = pygame.font.Font(master.config_dict["font_path"], self.master.BODY_SMALL)
        self.text_color: str = "white"
        self.font_size:int = master.BODY_SMALL
        # load the booleans
        self.FOCUSED: bool = False
        self.run: bool = True
        self.ANIMATING:bool = False
        self.FOCUSED_USED:bool = False
        # init the callback funcs
        self.func = func_callback
        self.func_args:list = func_args
        # init the types of the switcher(self.master.SWITCHER)
        self.type: int = master.SWITCHER
        self.tab_present: int = 0
        self.tab_focused: int = 0
        self.border: int = border
        # init the container of the main switcher
        self.container = pygame.Surface((self.width, 80))
        self.container.fill(self.master.background_color)
        # init the cover layer of the switcher
        self.cover:pygame.Surface = pygame.Surface((self.width,self.height))
        self.cover.fill(self.master.background_color)
        pygame.draw.rect(self.cover,tab_background,[0,0,self.width,self.height],0,master.SMALL_CORNER)
        self.cover.set_alpha(0)
        # init the colors
        self.tabs: list[str] = tabs
        self.tab_background: list[int, int, int] = tab_background
        self.button_list:list[Button] = []
        self.transparent:int = 0
        self.FADEOUT:bool = False
        add = 0
        index = 0
        for text in self.tabs:
            button = Button(self.master,self.container_x+add,self.container_y,self.master.element_background,self.tab_height,self.tab_width,text=text,func=Switcher.switcher_callback,func_options=[])
            button.set_callback(Switcher.switcher_callback,[self,button,index])
            self.button_list.append(button)
            add += self.tab_width + self.master.PADDING_SMALL
            index +=1
        self.register_element()


    def add_tab(self,title:str = '',elements:list = [])->None:
        '''
        @ title: The title of the tab
        @ elements: The element you want to switch in 
        Append a tab into the switcher
        '''
        self.tabs.append(title)
        self.elements.append(elements)
        self.force_reload()

    def switcher_callback(callback:list)->None:
        '''
        The callback of the switcher
        '''
        self,button,ind = callback
        self:Switcher
        button:Button
        self.ANIMATING = True
        self.tab_present = ind
        for list_element in self.elements:
            for e in list_element:
                e.run = False
        for element in self.elements[ind]:
            element.run = True


    def force_reload(self):
        '''
        Reload the whole switcher with override\n
        ATTENTION,THIS FUNC WILL RELOAD EVERYTHING INCLUDING THE THEME
        '''
        self.container_x:int = self.x + int((self.width - self.switcher_width)/2)
        self.container_y:int = self.y - self.master.DEFAULT_PADDING - self.switcher_height
        self.tab_width:int = self.switcher_width//len(self.tabs)
        self.tab_height:int = self.switcher_height - 2*self.master.PADDING_SMALL
        self.cover.fill(self.master.background_color)
        self.cover.set_alpha(0)
        self.master.screen.blit(self.cover,(self.x,self.y))

    async def dark_mode(self,master:Window):
        self.master = master
        self.force_reload()

    def register_element(self) -> None:
        """
        Register The Text Object
        """
        self.index = len(self.master.element_list)
        self.master.register(self)

    def __iter__(self):
        for element in self.tabs:
            yield element

    def __next__(self, index) -> str:
        try:
            return self.tabs[index + 1]
        except IndexError:
            raise StopIteration

    def mouse_detect(self) -> list[int]:
        # This func shouldn't be used
        if self.master.debug:
            print("[WARINING]: This part of the program shouldn't be run")
        return [0,0,0,0,0]

    async def refresh(self) -> None:
        """
        This fuc will refresh the tab
        """
        if self.run:
            self.cover.set_alpha(self.transparent)
            if self.ANIMATING:
                if not self.FADEOUT:
                    self.transparent += int((300-self.transparent)/5)+1
                    self.cover.set_alpha(self.transparent)
                    if self.transparent >= 300:
                        self.ANIMATING = False
                        self.FADEOUT = True
                else:
                    self.transparent -= int((self.transparent)/5)+1
                    self.cover.set_alpha(self.transparent)
                    if self.transparent <= 0:
                        self.FADEOUT = False
            if self.FOCUSED_USED:
                pygame.draw.rect(self.cover,self.master.THEME_COLOR,[0,0,self.width,self.height],self.FOCUSED_USED,self.master.SMALL_CORNER)
            else:
                pygame.draw.rect(self.cover,self.master.background_color,[0,0,self.width,self.height],self.FOCUSED_USED,self.master.SMALL_CORNER)
            self.master.screen.blit(self.cover,(self.x,self.y))
        return None

    async def listen(self,event):
        await self.detect()

    async def detect(self) -> None:
        if self.run:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_x > self.x and mouse_x < self.x_border and mouse_y > self.y and mouse_y < self.y_border:
                self.FOCUSED_USED = True
            else:
                self.FOCUSED_USED = False

            return None

    def set_transparent(self, alpha: int = 100):
        """
        Set The transparency if the button
        """
        self.container.set_alpha(alpha)
