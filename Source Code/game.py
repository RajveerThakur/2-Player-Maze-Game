#imports
import pygame
import sys

#environment setup
mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption('2 Player Maze Game')
screen = pygame.display.set_mode((1200, 960),0,32)
 
#setting font settings
font = pygame.font.SysFont(None, 30)
 
#function to write the text
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
 
# A variable to check for the status later
click = False
 
# Main container function that holds the buttons and game functions
def main_menu():
    while True:
 
        screen.fill((38,38,38))
        draw_text('Main Menu', font, (0,255,0), screen, 550, 40)
 
        mx, my = pygame.mouse.get_pos()

        #creating buttons & their locations
        button_1 = pygame.Rect(500, 100, 200, 50)
        button_2 = pygame.Rect(500, 180, 200, 50)

        #defining functions when a certain button is pressed
        if button_1.collidepoint((mx, my)):
            if click:
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                options()
        pygame.draw.rect(screen, (0, 255, 0), button_1) #button colors
        pygame.draw.rect(screen, (0, 255, 0), button_2)
 
        #writing text on top of button
        draw_text('PLAY', font, (38,38,38), screen, 570, 115)
        draw_text('OPTIONS', font, (38,38,38), screen, 550, 195)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        mainClock.tick(60)
 
#output when PLAY is pressed
def game():
    running = True
    while running:
        screen.fill((0,0,0)) #being replaced by game run function
       
        draw_text('GAME SCREEN', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
       
        pygame.display.update()
        mainClock.tick(60)

#output when OPTIONS is pressed
def options():
    running = True
    while running:
        screen.fill((0,0,0)) #being replaced by options screen function
 
        draw_text('OPTIONS SCREEN', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
       
        pygame.display.update()
        mainClock.tick(60)
 
main_menu()