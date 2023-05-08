import pygame
import os

class Diamante(pygame.sprite.Sprite):

    DIAMANTE_IMG = pygame.image.load(os.path.join('sprites', 'diamante.png'))
    SPRITE = pygame.transform.scale(DIAMANTE_IMG, (40,33))

    def __init__(self, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.largura = largura
        self.altura = altura
        self.sprite = self.SPRITE
    
    def draw(self, janela):
        janela.blit(self.sprite, (self.rect.x,self.rect.y))