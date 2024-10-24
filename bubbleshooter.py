import math
import pygame
import random
import pygame.gfxdraw
from pygame.locals import *

# Constants
FPS = 120
WIN_WIDTH = 940
WIN_HEIGHT = 740
TEXT_HEIGHT = 20
BUBBLE_RADIUS = 20
BUBBLE_DIAMETER = BUBBLE_RADIUS * 2
BUBBLE_LAYERS = 5
BUBBLE_ADJUST = 5
START_X = WIN_WIDTH / 2
START_Y = WIN_HEIGHT - 26
ARRAY_WIDTH = 25
ARRAY_HEIGHT = 20
RIGHT = 'right'
LEFT = 'left'
BLANK = '.'

# Colors
VBLUE = (51, 255, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLUE = (0, 0, 205)
RED = (255, 0, 0)
PINK = (255, 192, 203)
PEACH = (255, 229, 180)
GREEN = (0, 255, 0)
DEEPPINK = (255, 20, 147)
PEACOCKBLUE = (0, 164, 180)
GRAPECOLOR = (128, 49, 167)
AMBER = (255, 198, 0)
COMIC = (0, 174, 239)
LYTGRAY = (217, 217, 214)

# Background color
BG_COLOR = VBLUE

# List of colors used for bubbles
CLR_LIST = [GREY, BLUE, RED, WHITE, PINK, PEACH, GREEN, DEEPPINK, PEACOCKBLUE, GRAPECOLOR, AMBER, COMIC, LYTGRAY]

# Pygame Initialization
pygame.init()
fps_clock = pygame.time.Clock()

# Create Display
disp_surf = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption('Bubble Shooter')


class Bubble(pygame.sprite.Sprite):
    def __init__(self, color, row=0, col=0):
        super().__init__()
        self.rect = pygame.Rect(0, 0, BUBBLE_DIAMETER, BUBBLE_DIAMETER)
        self.rect.centerx = int(START_X)
        self.rect.centery = START_Y
        self.speed = 10
        self.color = color
        self.radius = BUBBLE_RADIUS
        self.angle = 90
        self.row = row
        self.col = col

    def update(self):
        if self.angle == 90:
            x_move = 0
            y_move = self.speed * -1
        elif self.angle < 90:
            x_move = self.x_calc(self.angle)
            y_move = self.y_calc(self.angle)
        else:
            x_move = self.x_calc(180 - self.angle) * -1
            y_move = self.y_calc(180 - self.angle)
        self.rect.x += int(x_move)
        self.rect.y += int(y_move)

    def draw(self):
        pygame.gfxdraw.filled_circle(disp_surf, self.rect.centerx, self.rect.centery, self.radius, self.color)
        pygame.gfxdraw.aacircle(disp_surf, self.rect.centerx, self.rect.centery, self.radius, GREY)

    def x_calc(self, angle):
        radians = math.radians(angle)
        return math.cos(radians) * self.speed

    def y_calc(self, angle):
        radians = math.radians(angle)
        return math.sin(radians) * self.speed * -1


class Arrow(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.angle = 90
        # Load image for arrow
        self.image = pygame.image.load('Arrow.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = int(START_X)
        self.rect.centery = START_Y

    def update(self, direction):
        if direction == LEFT and self.angle < 180:
            self.angle += 2
        elif direction == RIGHT and self.angle > 0:
            self.angle -= 2

        self.image = pygame.transform.rotate(pygame.image.load('Arrow.png').convert_alpha(), self.angle)
        self.rect = self.image.get_rect(center=(START_X, START_Y))

    def draw(self):
        disp_surf.blit(self.image, self.rect)


class Score(object):
    def __init__(self):
        self.total = 0
        self.font = pygame.font.SysFont('Comic Sans MS', 35)
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)
        self.rect = self.render.get_rect()
        self.rect.left = 5
        self.rect.bottom = WIN_HEIGHT - 5

    def update(self, dellst):
        self.total += len(dellst) * 10
        self.render = self.font.render('Score: ' + str(self.total), True, BLACK, WHITE)

    def draw(self):
        disp_surf.blit(self.render, self.rect)


def game_loop():
    direction = None
    launch_bubble = False
    new_bubble = None

    arrow = Arrow()
    score = Score()

    next_bubble = Bubble(CLR_LIST[0])
    next_bubble.rect.right = WIN_WIDTH - 5
    next_bubble.rect.bottom = WIN_HEIGHT - 5

    while True:
        disp_surf.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    direction = LEFT
                elif event.key == K_RIGHT:
                    direction = RIGHT
            elif event.type == KEYUP:
                direction = None
                if event.key == K_SPACE:
                    launch_bubble = True
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        arrow.update(direction)
        arrow.draw()

        # Handle bubble launching and collision
        if launch_bubble:
            if new_bubble is None:
                new_bubble = Bubble(next_bubble.color)
                new_bubble.angle = arrow.angle

            new_bubble.update()
            new_bubble.draw()

            # Collision with walls
            if new_bubble.rect.right >= WIN_WIDTH - 5 or new_bubble.rect.left <= 5:
                new_bubble.angle = 180 - new_bubble.angle

            # Handle collisions with other bubbles or top
            # (Collision logic should go here)

        next_bubble.draw()

        score.draw()

        pygame.display.update()
        fps_clock.tick(FPS)


def main():
    game_loop()


if __name__ == '__main__':
    main()
