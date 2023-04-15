import pygame
'''
这是我从plane War中提取的UI库
有大小框选框
开关
颜色取色器
'''
class hqyui(object):
    def colorChooser(screen):
        '''
        简陋的选色器
        '''
        r=0
        b=0
        g=0
        running = True
        x=0
        y=0
        down = False
        while running:
            for event in  pygame.event.get() :
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEMOTION:
                    x,y = pygame.mouse.get_pos()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    down = True
                if event.type == pygame.MOUSEBUTTONUP:
                    down = False
                    if x > 10 and x < 490 and y > 410 and y < 490:
                        return [r,g,b]
                if down:
                    x,y = pygame.mouse.get_pos()
                    if x >= 20 and x <= 220:
                        print("True")
                        if y >= 25 and y <= 55:
                            r = x-20
                        if y >= 55 and y <= 65 :
                            g = x-20
                        if y >= 85 and y <= 95:
                            print(y)
                            b = x-20
            screen.fill([r,g,b])
            pygame.draw.rect(screen,[155,155,155],[20,8,200,104])
            pygame.draw.circle(screen,[155,155,155],[20,20],12)
            pygame.draw.circle(screen,[155,155,155],[220,20],12)
            pygame.draw.circle(screen,[155,155,155],[220,100],12)
            pygame.draw.circle(screen,[155,155,155],[20,100],12)
            pygame.draw.rect(screen,[155,155,155],[8,20,12,80])
            pygame.draw.rect(screen,[155,155,155],[220,20,12,80])
            pygame.draw.rect(screen,[255,235,235],[20,25,200,16])
            pygame.draw.rect(screen,[235,255,235],[20,55,200,16])
            pygame.draw.rect(screen,[235,235,255],[20,85,200,16])
            pygame.draw.circle(screen,[255,235,235],[20,33],8)
            pygame.draw.circle(screen,[235,255,235],[20,63],8)
            pygame.draw.circle(screen,[235,235,255],[20,93],8)
            pygame.draw.circle(screen,[255,235,235],[220,33],8)
            pygame.draw.circle(screen,[235,255,235],[220,63],8)
            pygame.draw.circle(screen,[235,235,255],[220,93],8)
            pygame.draw.circle(screen,[r,g,b],[20+r,33],8)
            pygame.draw.circle(screen,[r,g,b],[20+g,63],8)
            pygame.draw.circle(screen,[r,g,b],[20+b,93],8)
            pygame.draw.rect(screen,[155,155,155],[10,420,480,70])
            pygame.display.update()
    def print_screen(screen,font,string="", pos=(210, 260), color='black'):
        screen.blit(font.render(
            string, True, color), pos)
    
    def draw_switch(screen,situation, pos, position):
        if position + pos[1] >= 50:
            if situation == True:
                pygame.draw.circle(screen, [200, 100, 100], [
                                   pos[0], pos[1]+5+position], 12)
                pygame.draw.circle(screen, [200, 100, 100], [
                                   pos[0]+20, pos[1]+5+position], 12)
                pygame.draw.rect(screen, [200, 100, 100], [
                                 pos[0], pos[1]-7+position, 20, 24])
                pygame.draw.circle(screen, [255, 255, 255], [
                                   pos[0]+20, pos[1]+5+position], 8)
            if situation == False:
                pygame.draw.circle(screen, [100, 100, 100], [
                                   pos[0], pos[1]+5+position], 12)
                pygame.draw.circle(screen, [100, 100, 100], [
                                   pos[0]+20, pos[1]+5+position], 12)
                pygame.draw.rect(screen, [100, 100, 100], [
                                 pos[0], pos[1]-7+position, 20, 24])
                pygame.draw.circle(screen, [255, 255, 255], [
                                   pos[0], pos[1]+position+5], 8)

    def bind_switch(event, pos, position):
        if event.type == pygame.MOUSEBUTTONUP and position + pos[1] >= 30:
            try:
                if pygame.mouse.get_pos()[0] >= pos[0]-5 and pygame.mouse.get_pos()[0] <= pos[0]+30 and pygame.mouse.get_pos()[1] >= pos[1]-5+position and pygame.mouse.get_pos()[1] <= pos[1]+24+position:
                    return True
            except:
                return None
            return False

    def switch(situation, pos, text, position):
        hqyui.draw_switch(
            situation, [pos[0]+360, pos[1]+10], position=position)
        hqyui.print_screen(text, pos, color='white')

    def draw_addbox(screen,value, pos, text, position):
        hqyui.print_screen(text, pos, color='white')
        if value <= 0:
            pygame.draw.rect(screen, [150, 100, 100], [
                             pos[0]+330, pos[1]+position, 20, 20])
        else:
            pygame.draw.rect(screen, [200, 100, 100], [
                             pos[0]+330, pos[1]+position, 20, 20])
        pygame.draw.rect(screen, [200, 100, 100], [
                         pos[0]+352, pos[1]+position, 40, 20])
        pygame.draw.rect(screen, [200, 100, 100], [
                         pos[0]+394, pos[1]+position, 20, 20])
        hqyui.print_screen(
            "-", [pos[0]+335, pos[1]-5+position], color='white')
        hqyui.print_screen(
            "+", [pos[0]+398, pos[1]-6+position], color='white')
        hqyui.print_screen(
            str(value), [pos[0]+356, pos[1]-4+position], color='white')

    def bind_addbox(pos):
        try:
            [pos1, pos2] = pygame.mouse.get_pos()
        except:
            return 0
        if pos1 > pos[0]+330 and pos1 < pos[0]+350 and pos2 > pos[1] and pos2 < pos[1]+20:
            return -1
        elif pos1 > pos[0]+394 and pos1 < pos[0]+414 and pos2 > pos[1] and pos2 < pos[1]+20:
            return 1
        else:
            return 0


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((500,500))
    hqyui.colorChooser(window)