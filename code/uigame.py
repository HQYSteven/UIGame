'''
This is the start page of the module
'''
from Basics.window import Window
import json
import sys
import platform
from demo import run_programme
import pygame
import asyncio

class Shell(Window):
    def __init__(self) -> None:
        self.input_str:str = ''
        pygame.font.init()
        self.choices:list[str] = sys.argv 
        self.running:bool = True
        self.about:str = Shell.read_file("./README.md",0,100)
        self.license:str = Shell.read_file("./LICENSE",0,100)
        self.version:str = "uigame " + json.loads(Shell.read_file('./config/about.json',0,100))["version"]
        self.author:str = 'HQY'
        self.present_environment:str = sys.version
        self.operate_system_name:str = platform.system() +" "+ platform.release() + " "  + platform.machine() 
        self.greet_text :str = Shell.read_file("./config/greet.txt",0,100)
        self.debug_mode:bool = False

    def analyize(self,char:str= '') ->None:
        '''
        analyize the keyboard choices
        '''
        # Get the keyboard args
        medium = ''
        for string in char:
            if string == " " and medium != '':
                self.choices.append(medium)
                medium = ''
                continue
            medium += string
        if medium != "":
            self.choices.append(medium)
        
    def shell(input_list:list[str])->None:
        '''
        The shell of the uigame
        '''
        for choice in input_list:
            if choice == "q!":
                print("QUIT")
                self.running = False
                quit()

    def run(self):
        """
        Run the main shell
        """
        instruction_help:list[str] = ["--help",'-h','help']
        instruction_debug:list[str] = ["--debug",'-d','debug']
        instruction_demo:list[str] = ['--demo','demo']
        instruction_license:list[str] = ["--license",'license','-l']
        instruction_author:list[str] = ["--author",'author','-a']
        instruction_about:list[str] = ["--about",'about','-ab']
        instruction_version:list[str] = ['--version','version','-v']
        instruction_shell:list[str] = ["--shell",'shell','-s']
        print(self.greet_text.format(self.version,self.operate_system_name,self.present_environment),end = "")
        if len(self.choices ) > 1:
            self.choices = self.choices[1::]
            for choice in self.choices:
                if choice in instruction_help:
                    print('''
Thankyou for using uigame,this is the help page:
                          
--help/-h/help:             Display this helping page
--debug/-d/debug:           enable debug mode(not available yet)
--demo/demo:                Open the demonstration
--license/-l/license:       Display the license
--about/-ab/about:          Display the details about this module
--author/-a/author:         Display the information about the author
--version/-v/version        Display the version of the program
                          
''')
                if choice in instruction_debug:
                    print("[DEBUG]:Debug Mode Enabled")
                    self.debug_mode = True
                if choice in instruction_about:
                    print(self.about)
                if choice in instruction_author:
                    print(self.author)
                if choice in instruction_license:
                    print(self.license)
                if choice in instruction_demo:
                    print("Here is the demo of the uigame")
                    asyncio.run(run_programme(self.debug_mode))
                if choice in instruction_version:
                    print(self.version)
                if choice in instruction_shell:
                    while self.running:
                        Shell.shell(Shell.analyize(self,input("[UIGAME]:$ ")))

if __name__ == '__main__':
    self = Shell()
    Shell.run(self)

