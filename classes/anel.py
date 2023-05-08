import pygame

class Anel(pygame.sprite.Sprite):

    def __init__(self, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        for i in range(1,11):
            self.sprites.append(pygame.image.load(f'sprites/aneis/ANEL{i}.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect=self.image.get_rect()
        self.rect = pygame.Rect(x, y, largura, altura)
        self.image = pygame.transform.scale(self.image, (33, 33))
    

    def update(self): #faz o anel girar
        self.atual+=1
        if self.atual>=len(self.sprites):
           self.atual=0
        self.image=self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (33, 33))