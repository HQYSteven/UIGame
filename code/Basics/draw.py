'''
Draw copenents
This class is used to draw gragh on the screen 
'''
from Basics.window import Window
import pygame

class Draw(Window):
    """
    Draw compenent
    Use ME to draw graphics instead of pygame!
    """
    def rect(surface,color:list[int,int,int],x:int,y:int,width:int,height:int,border:int = 0,border_radius:int = 0) -> None:
        '''
        @ color: The color of the rect(rgb)
        @ x: The x-axis coordinate
        @ y: The y-axis coordinate
        @ width: The width of the rect(above 0)
        @ height: The height of the rect(above 0)
        @ border: The border of the rect(0 for no border)
        @ border_radius: border radius of the rect(0 or -1 for no radius)
        Draw rect
        '''
        pygame.draw.rect(surface.screen,color,[x,y,width,height],border,border_radius)
    
    def circle(surface,color:list[int,int,int],x:int,y:int,border:int = 0,radius:int = 0) -> None:
        '''
        @ color: The color of the circle(rgb)
        @ x: The x-axis coordinate
        @ y: The y-axis coordinate
        @ border: The border of the circle(0 for no border)
        @ radius: radius of the circle
        Draw circle
        '''
        pygame.draw.circle(surface.screen,color,[x,y],border,radius)

    def string(surface,color:list[int,int,int],x1:int,y1:int,x2:int,y2:int,width:int = 1) -> None:
        '''
        @ color: The color of the string(rgb)
        @ x1: The x-axis coordinate of the first point
        @ y1: The y-axis coordinate of the first point
        @ x2: The x-axis coordinate of the second point
        @ y2: The y-axis coordinate of the second pointmeizu
        @ width: The width of the string
        Draw a string
        '''
        pygame.draw.line(surface.screen,color,[x1,y1],[x2,y2],width)

    def curve(surface,color:list[int,int,int],pos_list:list[list[int,int]],width:int = 1) -> None:
        '''
        @ color: The color of the string(rgb)
        @ pos_list: The list of the coordinates on the string
        @ width: The width of the string
        Draw a set of string
        '''
        index1 = 0
        index2 = 1
        limit = len(pos_list) -1
        while index2 <= limit:
            pygame.draw.line(surface.screen,color,pos_list[index1],pos_list[index2],width)
            index1 += 1
            index2 += 1
