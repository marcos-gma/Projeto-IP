import pygame
import os

class Inimigo(pygame.sprite.Sprite):

    KNUCKLES_IMG = pygame.image.load(os.path.join('sprites', 'knuckles.png'))
    SPRITE = pygame.transform.scale(KNUCKLES_IMG, (70,70))

    def __init__(self, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.largura = largura
        self.altura = altura
        self.sprite = self.SPRITE
    
    def draw(self, janela):
        janela.blit(self.sprite, (self.rect.x,self.rect.y))

    def mudar_direcao(self, direcao): #muda o sentido do knuckles
        if direcao == "direita":
            self.sprite = pygame.transform.scale(self.KNUCKLES_IMG, (70,70))
        else:
            self.sprite = pygame.transform.flip(pygame.transform.scale(self.KNUCKLES_IMG, (70,70)), True, False)