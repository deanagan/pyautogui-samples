import pygame
import os


pygame.init()
screen = pygame.display.set_mode((500, 300))
done = False
clock = pygame.time.Clock()

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True

        screen.fill((255, 255, 255))

        screen.blit(pygame.image.load(r'Img/TwoDiamonds.png'), (5, 5))
        screen.blit(pygame.image.load(r'Img/ThreeDiamonds.png'), (45, 5))
        screen.blit(pygame.image.load(r'Img/FourDiamonds.png'), (85, 5))
        screen.blit(pygame.image.load(r'Img/FiveDiamonds.png'), (125, 5))
        screen.blit(pygame.image.load(r'Img/SixDiamonds.png'), (165, 5))

        pygame.display.flip()
        clock.tick(60)
