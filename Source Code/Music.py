from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame,sys,time

pygame.mixer.init()
pygame.mixer.music.load('you-win-sequence-1-183948.mp3')
pygame.mixer.music.play()

input('Enter to exit')
