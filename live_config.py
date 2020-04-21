import pygame
import matplotlib.pyplot as plt
from pygame.locals import *

def display(str):
    text = font.render(str, True, (255, 255, 255), (159, 182, 205))
    textRect = text.get_rect()
    textRect.centerx = screen.get_rect().centerx
    textRect.centery = screen.get_rect().centery

    screen.blit(text, textRect)
    pygame.display.update()

pygame.init()
screen = pygame.display.set_mode( (640,480) )
pygame.display.set_caption('Python numbers')
screen.fill((159, 182, 205))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 17)

fps=60
bg = [255,255,255]

button = pygame.Rect(100, 100, 50, 50)

num = 0
done = False
while not done:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos  # gets mouse position

            # checks if mouse position is over the button

            if button.collidepoint(mouse_pos):
                # prints current location of mouse
                print('button was pressed at {0}'.format(mouse_pos))

    screen.fill(bg)

    pygame.draw.rect(screen, [255, 0, 0], button)  # draw button

    pygame.display.update()
    clock.tick(fps)
