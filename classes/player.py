import pygame
import constantes

class Player(pygame.sprite.Sprite):

    COR = (255, 0, 0)
    GRAVIDADE = 1
    
    def __init__(self, x, y, largura, altura):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites_e =[]
        i = 0
        for _ in range(16):
            sonic_img = pygame.transform.scale(pygame.image.load(f'sprites/SONIC/SONIC {i}.png'),(70, 70))
            self.sprites.append(sonic_img)
            self.sprites_e.append(pygame.transform.flip(sonic_img,True,False))
            i += 1
        self.index = 1
        self.image = self.sprites[self.index]
        self.rect=self.image.get_rect()
        self.rect = pygame.Rect(x, y, largura, altura)
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.x_vel = 0
        self.y_vel = 0
        self.largura = largura
        self.altura = altura
        self.queda_cont = 0
        self.pulo_cont = 0

    def pular(self):
        self.y_vel = -self.GRAVIDADE * 80
        self.pulo_cont += 1
        if self.pulo_cont == 1:
            self.queda_cont = 0
        
    def caiu(self):
        self.queda_cont = 0
        self.y_vel = 0
        self.pulo_cont = 0

    def movimento(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def esquerda(self, vel):
        self.x_vel = -vel

    def direita(self, vel):
        self.x_vel = vel
    
    def loop(self, fps):
        self.y_vel += 8 * (min(1, (self.queda_cont / fps) * self.GRAVIDADE))
        self.movimento(self.x_vel, self.y_vel)

        self.queda_cont += 1

    def draw(self, janela):
        janela.blit(self.image, (self.rect.x,self.rect.y))

    def update(self,keys): #animação do sonic
        if keys[pygame.K_a] or keys[pygame.K_d]:
           self.index+=1
           if self.index>=len(self.sprites):
                self.index = 1
           self.image=pygame.transform.scale(self.image,(70,70))
        if keys[pygame.K_a]:
           self.image = self.sprites_e[self.index]
        elif keys[pygame.K_d]:
           self.image=self.sprites[self.index]
        else:
           self.index = 0
           self.image = self.sprites[self.index]
           self.image=pygame.transform.scale(self.image,(55,70))

def mover(player): #função para mover o personagem
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    if player.rect.y >= 285:
        player.rect.y = 285

    if keys[pygame.K_a] and player.rect.x > 0:
        player.esquerda(constantes.VEL)
    if keys[pygame.K_d] and player.rect.x < 570:
        player.direita(constantes.VEL)