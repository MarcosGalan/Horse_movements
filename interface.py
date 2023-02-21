import math

import pygame
from pygame import font
from algoritmo_caballo import horse_pathfinder

# SETTING WINDOW AND ROWS
WIDTH = 768
ROWS = 8
SQUARE_SIZE = WIDTH / ROWS
WIN_SIZE = (WIDTH, WIDTH)

# SETTING COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Casilla:
    """
    This class represent each of the squares in the board with his own properties
    """

    def __init__(self, xpos, ypos, row, column, color):
        self.xpos = xpos
        self.ypos = ypos
        self.row = row
        self.column = column
        self.path_finded = False
        self.color = color
        self.text = ""
        self.text_angle = 0
        self.text_size = int(SQUARE_SIZE * 0.75)

    def set_color(self, color):
        """
        This function sets a color to the square
        :param color:
        :return:
        """
        self.color = color

    def isColor(self, color):
        """
        This function checks if the square is of a determined color.
        :param color: rgb tuple
        :return:
            True if color matches false if not
        """
        return self.color == color

    def draw(self):
        """
        This function draws the square in the screen
        """
        pygame.draw.rect(WIN, self.color, pygame.Rect(self.xpos, self.ypos, WIDTH, WIDTH))
        if self.text != "":
            font = pygame.font.SysFont("chalkduster", self.text_size)
            img = font.render(self.text, True, (255, 50, 50))
            img = pygame.transform.rotate(img, angle=self.text_angle)
            if self.text_angle == 0:
                WIN.blit(img, (self.xpos + SQUARE_SIZE * 0.25, self.ypos))
            else:
                WIN.blit(img, (self.xpos, self.ypos))


class Tablero:

    def __init__(self, width, rows):

        self.width = width
        self.rows = rows
        self.square_size = width / rows
        self.tablero = []
        for i in range(rows):
            temp_list = []
            for j in range(rows):
                color = BLACK if is_even(i) == is_even(j) else WHITE
                temp_list.append(Casilla(i * self.square_size, j * self.square_size, i, j, color))
            self.tablero.append(temp_list)

        self.start = (0, 0)
        self.end = (8, 8)

    def draw_board(self):
        """This function draw the board in the display"""
        for row in self.tablero:
            for block in row:
                block.draw()

    def path_horse(self, start, end):
        """This functions calls the algorithm and modifies some squares"""

        path = horse_pathfinder(tablero, start, end)
        for counter, i in enumerate(path):
            underscore_pos = i.index("_")
            self.tablero[int(i[:underscore_pos])][int(i[underscore_pos + 1:])].text = str(counter + 1)
            self.tablero[int(i[:underscore_pos])][int(i[underscore_pos + 1:])].text_size = int(SQUARE_SIZE * 0.75)
            self.tablero[int(i[:underscore_pos])][int(i[underscore_pos + 1:])].text_angle = 0


def get_block_by_pos(click_pos, rows, width) -> (int, int):
    """
    Calculates the block that the cursor have clicked.
    :param click_pos: contains the coordinates of the click
    :param rows: number of rowsin grid
    :param width: width of the screen
    :return:tuple:(row, col)
    """
    gap = int(width / rows)
    row = math.floor(click_pos[1] / gap)
    col = math.floor(click_pos[0] / gap)
    return row, col


def is_even(num: int):
    if num % 2 == 0:
        return True

    return False


run = True
tablero = Tablero(WIDTH, ROWS)

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('HORSE ALGORITHM')

pygame.init()

start = [False, ()]
end = [False, ()]
while run:
    tablero.draw_board()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if start[0] and end[0]:
                    tablero.path_horse(start[1], end[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                tablero = Tablero(WIDTH, ROWS)
                start = [False, ()]
                end = [False, ()]

    if pygame.mouse.get_pressed()[1]:
        mouse_pos = pygame.mouse.get_pos()
        col, row = get_block_by_pos(mouse_pos, ROWS, WIDTH)
        if not start[0]:
            tablero.tablero[row][col].text = "START"
            start = [True, (row, col)]
        elif start[0] and not end[0] and (row, col) != start[1]:
            tablero.tablero[row][col].text = "END"
            end = [True, (row, col)]

        tablero.tablero[row][col].text_size = int(SQUARE_SIZE * 0.3)
        tablero.tablero[row][col].text_angle = 45

    pygame.display.flip()
