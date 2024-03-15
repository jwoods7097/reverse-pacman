import pygame

# Define events
LEVEL_UPDATE = pygame.USEREVENT + 1

def invoke(event):
    pygame.event.post(pygame.event.Event(event))
