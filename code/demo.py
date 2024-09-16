from Basics.window import Window
from Elements.text import Text
from Elements.button import Button
from Elements.titlebar import Titlebar
from Elements.switch import Switch
from Elements.entry import Entry
from Elements.aboutpage import Aboutpage

"""'
This is The demostration of the ui module
This file was written to help the freshman to know how to use the basic modules of UIGame
UIGame provides a tkinter-like graphic experice,uses the uigame library(>=2.6.0)
And show the power of UIGame to the visitor of the project
If you want some more information,visit the following website
https://www.gitee.com/HQYSTEVEN/uigame_doc.git 
Wish you a pleasant learning experience!
"""


def get_status_of_the_switch(figures: list):
    """
    When the status of the switch has changed,this func will change the status of the Aboutpage Object at the same time.
    """
    win, switch, aboutpage = figures
    win: Window
    switch: Switch
    aboutpage: Aboutpage
    win.dark_mode()
    if switch.get_activate_status():
        aboutpage.activate()


def run(debug: bool = False):
    """
    @ debug: This boolean decides whether the UIGame will show the debug information or not,usually it should be False
    """
    self = Window()  # create the Window object
    Window.initialize(
        self,
        [100, 100, 200],
        500,
        500,
        "hello!",
        round_cursor=True,
        no_frame=1,
        debug=debug,
    )  # initialize the UIGame module
    Button(
        self, 50, 80, [244, 245, 244], 50, 100, text="New Button", border=10
    )  # initialize a Button Object
    Text(self, x=50, y=45, text="This is a The Demostration of the UIGame")
    Text(self, x=50, y=300, text="This is a Switch")
    Titlebar(self, "HELLO")  # initalize an Titlebar object
    swi = Switch(
        self, x=70, y=340, func=get_status_of_the_switch, func_options=[]
    )  # initialize a Switch object and stores it
    swi.change_options(
        [self, swi, Aboutpage(self)]
    )  # set the options of the switch,bind the switch with the activate status of the Aboutpage object created above
    Entry(
        self,
        100,
        200,
        "Here",
    )  # initialize an Entry object
    self.mainloop()  # you don't have to write the mainloop,UIGame will do it for you !


if __name__ == "__main__":
    # run the demo if __name__ is "__main__"
    run()
