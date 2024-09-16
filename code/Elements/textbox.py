"""
This is a text box module
Developing,but i have to finish all the commits first
I Almost forget that i have a unfinished element to write OHHHHHH
"""

import pygame
from Elements.entry import Entry


class Textbox(Entry):
    def __init__(
        self,
        master: Entry,
        x: int,
        y: int,
        default_str: str = "",
        height: int = 30,
        width: int = 150,
        background: list[int] | tuple[int, int, int] = ...,
        border: int = 0,
        border_radius: int = 5,
        body_color: list[int, int, int] = [200, 200, 200],
        text_color: list[int] = ...,
        font_size: int = 12,
        notice: str = "",
    ) -> None:
        super().__init__(
            master,
            x,
            y,
            default_str,
            height,
            width,
            background,
            border,
            border_radius,
            text_color,
            font_size,
            notice,
        )
        self.rows: list[str] = [self.default_str]
        self.rows_displaying: list[str] = []
        self.cursor_pos_row: int = 0
        self.cursor_pos_column: int = 0
        self.FOCUSED: bool = False
        self.body_color: list[
            int,
            int,
            int,
        ] = body_color
        self.maxium_rows: int = self.height / (self.font_size + 5)
        self.maxium_columns: int = self.width / 2 * 3 / (self.font_size)
        return None

    def __iter__(self):
        for row in self.rows:
            yield row

    def __next__(self, index):
        try:
            yield self.rows[index + 1]
        except IndexError:
            yield StopIteration

    def __hash__(self) -> int:
        return hash(self.rows)

    def __repr__(self) -> str:
        return "<Textbox Object>"

    def refresh(self) -> None:
        """
        Refresh The textbx
        """
        pygame.draw.rect(
            self.screen,
            self.body_color,
            [self.x, self.y, self.width, self.height],
            self.border,
            self.border_radius,
        )
        pygame.draw.rect(
            self.screen,
            self.theme_color,
            [
                self.x + 10,
                self.y + 5 + (self.font_size + 5) * self.cursor_pos_row,
                self.width - 20,
                self.font_size + 5,
            ],
        )
        text_x = self.x + 10
        text_y = self.y + 10
        for row in self.rows_displaying:
            text = self.font.render(row, color=self.text_color)
            self.screen.blit(text, (text_x, text_y))
            text_x += self.font_size + 5

    def detect(self):
        x, y = pygame.mouse.get_pos()
        if (
            self.x <= x
            and self.x + self.width >= x
            and self.y <= y
            and self.y + self.height >= y
        ):
            self.FOCUSED = True
            pygame.draw.rect(
                self.screen,
                self.theme_color,
                [self.x, self.y, self.width, self.height],
                1,
                self.border_radius,
            )
        else:
            self.FOCUSED = False

    def listen(self, event) -> None:
        """
        Dtect if the Textbox is activated
        """
        self.detect()
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
        return None
