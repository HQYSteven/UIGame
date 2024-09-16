from Basics.window import Window
import pygame
# preparations


class Aboutpage(Window):
    """
    I will write an example so that you don't have to write another
    """

    def __init__(
        self,
        master: Window,
        authors: list = ["hqy"],
        texts: list = ["This is an example", "Author hqy is a programmer"],
        text_font_size: int = 12,
        x_start: int = 50,
        y_start: int = 330,
    ) -> None:
        self.authors = " ".join(authors)
        self.text = texts
        self.master: Window = master
        self.text_color: str = "black"
        self.x, self.y = 0, 0
        self.width: int = self.master.screenWidth
        self.height: int = self.master.screenHeight
        self.force_reload()
        self.main_container.set_alpha(0)
        self.transparent: int = 0
        self.icon_y = 80
        self.text_font_size: int = text_font_size
        self.width_present: int = 0
        self.height_present: int = 0
        self.x_start: int = x_start
        self.y_start: int = y_start
        self.TYPE: int = self.master.ABOUTPAGE
        self.FOCUSED: bool = False
        self.ANIMATING: bool = False
        self.run: bool = False
        self.DARK_MODE: bool = False
        self.register_element()

    def register_element(self):
        self.index = len(self.master.element_list)
        self.master.register(self)

    def force_reload(self):
        self.master.judge_debug("[DEBUG]: Aboutpage Module reloaded")
        self.main_container: pygame.Surface = pygame.Surface((self.width, self.height))
        self.OK_text: pygame.Surface = self.master.font.render("了解", 0, "white")
        _, _, w, h = self.OK_text.get_rect()
        self.button_surface: pygame.Surface = pygame.Surface((w + 20, h + 20))
        self.button_surface.fill([100, 100, 100])
        pygame.draw.rect(
            self.button_surface, self.master.THEME_COLOR, [0, 0, w + 20, h + 20], 0, 5
        )
        self.button_surface.blit(self.OK_text, (10, 10))
        self.button_pos: int = (int(self.width * 0.8), int(self.height * 0.7))
        self.main_container.blit(self.button_surface, self.button_pos)
        font = pygame.font.Font(
            self.master.config_dict["font_path"], self.master.HEADLINE_3
        )
        self.title_surface: pygame.Surface = font.render(
            "关于", 1, self.master.TITLE_COLOR
        )
        self.title_pos: list[int] = (int(self.width * 0.05), int(self.height * 0.05))
        self.row_pos: list[int] = []
        self.text_surfaces: list[pygame.Surface] = []
        x = int(self.width * 0.05)
        y = self.title_pos[0] + self.master.HEADLINE_2 + self.master.PADDING_LARGE
        self.font = pygame.font.Font(
            self.master.config_dict["font_path"], self.master.BODY_LARGE
        )
        for txt in self.text:
            self.text_surfaces.append(self.font.render(txt, 1, self.master.BODY_COLOR))
            self.row_pos.append((x, y))
            y += self.master.PADDING_LARGE + self.master.BODY_LARGE

    async def dark_mode(self, master: Window):
        self.master.judge_debug("[DEBUG]: Aboutpage turn to dark mode")
        self.master = master
        self.DARK_MODE = True if not self.DARK_MODE else False
        # force reload the surface
        self.force_reload()

    async def refresh_text(self) -> None:
        index = 0
        for txt_surface in self.text_surfaces:
            self.main_container.blit(txt_surface, self.row_pos[index])
            index += 1

    async def refresh_container_while_fade_in(self) -> None:
        """
        Refresh the container while the container is FOCUSED and self.ANIMATING is True
        """
        self.transparent += int((250 - self.transparent) / 10) + 1
        self.width_present += (
            int((self.master.screenWidth - self.width_present) / 10) + 1
        )
        pygame.draw.rect(
            self.main_container,
            [self.transparent, self.transparent, self.transparent],
            [0, 0, self.width_present, self.master.screenHeight],
            0,
            self.master.ENORMOUS_CORNER,
        )
        self.main_container.set_alpha(self.transparent)
        self.main_container.blit(self.title_surface, self.title_pos)
        self.main_container.blit(self.button_surface, self.button_pos)

    async def refresh_container_while_fade_out(self):
        """
        Refresh the container while the container isn't FOCUSED and self.ANIMATING is True
        """
        self.transparent -= int((self.transparent) / 10) + 1
        self.width_present -= int((self.width_present) / 10) + 1
        pygame.draw.rect(
            self.main_container,
            [self.transparent, self.transparent, self.transparent],
            [0, 0, self.width_present, self.master.screenHeight],
            0,
            self.master.ENORMOUS_CORNER,
        )
        self.main_container.set_alpha(self.transparent)
        self.main_container.blit(self.title_surface, self.title_pos)
        self.main_container.blit(self.button_surface, self.button_pos)

    async def refresh(self) -> None:
        """
        The main loop
        """
        if self.run:
            self.main_container.fill(self.master.element_background)
            if self.ANIMATING:
                if self.FOCUSED:
                    await self.refresh_text()
                    await self.refresh_container_while_fade_in()
                    # if the surface is not transparent anymore,stop animating
                    if self.transparent >= 255:
                        self.ANIMATING = False
                        self.transparent = 255
                        self.master.judge_debug("[DEBUG]: Aboutpage animatation ended")
                else:
                    await self.refresh_text()
                    await self.refresh_container_while_fade_out()
                    # if the surface has been faded out,animate stops
                    if self.transparent <= 0:
                        self.ANIMATING = False
                        self.run = False
                        self.transparent = 0
                        self.master.judge_debug("[DEBUG]: Aboutpage animatation ended")

            else:
                self.main_container.fill([255, 255, 255])
                self.main_container.blit(self.title_surface, self.title_pos)
                index = 0
                for txt_surface in self.text_surfaces:
                    self.main_container.blit(txt_surface, self.row_pos[index])
                    index += 1
                self.main_container.blit(self.button_surface, self.button_pos)
            self.master.screen.blit(self.main_container, (0, 0))

    def mouse_detect(self):
        return (
            self.button_pos[0],
            self.button_pos[1],
            self.button_surface.get_rect()[2],
            self.button_surface.get_rect()[3],
            self.master.TINY_CORNER,
        )

    async def listen(self, event):
        if self.run:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.run = True
                self.ANIMATING = True
                self.FOCUSED = False
                self.master.judge_debug("[DEBUG]: Aboutpage animatation started\n[DEBUG]: Aboutpage get focused")

    def activate(self):
        self.run = True
        self.ANIMATING = True
        self.FOCUSED = True
