import pygame
import os
import time
from pygame.locals import *
from random import randint

#constantes

LARGURA = 640   
ALTURA = 580
TITULO = 'THE FORBIDDEN GAME'
FPS = 30
PRETO = (0, 0, 0)
BRANCO = (255,255,255)
LARG_PERS = 70
ALTU_PERS = 70
VEL = 10

pygame.init()

JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

pygame.mixer.music.set_volume(0.25)
musica_de_fundo =  pygame.mixer.music.load('soundtrack/BoxCat.mp3')
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound('soundtrack/smw_1-up.wav')
som_colisao.set_volume(1)

x = LARGURA / 2
y = ALTURA / 2

y=305

x_anel = randint(40, 600)
y_anel = 320

x_diamante = randint(40, 600)
y_diamante = 320


KNUCKLES_IMG = pygame.image.load(os.path.join('sprites', 'knuckles.png'))
KNUCKLES_IMG = pygame.transform.flip(pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS)), True, False)


class Player(pygame.sprite.Sprite):

    COR = (255, 0, 0)
    GRAVIDADE = 1
    
    SONIC_IMG = pygame.image.load(os.path.join('sprites', 'SONIC','SONIC 1.png'))
    SPRITE = pygame.transform.scale(SONIC_IMG, (LARG_PERS,ALTU_PERS))

    def __init__(self, x, y, largura, altura):

        super().__init__()
        self.rect = pygame.Rect(x, y, largura, altura)
        self.x_vel = 0
        self.y_vel = 0
        self.direcao = "esquerda"
        self.queda_cont = 0

    def movimento(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    
    def esquerda(self, vel):
        self.x_vel = -vel
        if self.direcao != "esquerda":
            self.direcao = "esquerda"
            self.animacao_cont = 0

    def direita(self, vel):
        self.x_vel = vel
        if self.direcao != "direita":
            self.direcao = "direita"
            self.animacao_cont = 0

    def cima(self, vel):
        self.y_vel = -vel
    
    
    def loop(self, fps):
        self.y_vel += 8 * (min(1, (self.queda_cont / fps) * self.GRAVIDADE))
        self.movimento(self.x_vel, self.y_vel)

        self.queda_cont += 1

    def draw(self, janela):
        self.sprite = self.SPRITE
        janela.blit(self.sprite, (self.rect.x,self.rect.y))

    '''def update(self):
        self.atual+=1
        if self.atual>=len(self.sprites):
           self.atual=0
        self.image=self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (33, 33))'''

class Inimigo(pygame.sprite.Sprite):

    KNUCKLES_IMG = pygame.image.load(os.path.join('sprites', 'knuckles.png'))
    SPRITE = pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS))

    def __init__(self, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.largura = largura
        self.altura = altura
        self.sprite = self.SPRITE
    
    def draw(self, janela):
        janela.blit(self.sprite, (self.rect.x,self.rect.y))

    def mudar_direcao(self, direcao):
        if direcao == "esquerda":
            self.sprite = pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS))
        else:
            self.sprite = pygame.transform.flip(pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS)), True, False)

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

            
class Anel(pygame.sprite.Sprite):

    def __init__(self, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL1.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL2.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL3.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL4.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL5.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL6.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL7.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL8.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL9.png'))
        self.sprites.append(pygame.image.load('sprites/aneis/ANEL10.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect=self.image.get_rect()
        self.rect = pygame.Rect(x, y, largura, altura)
        self.image = pygame.transform.scale(self.image, (33, 33))
    

    def update(self):
        self.atual+=1
        if self.atual>=len(self.sprites):
           self.atual=0
        self.image=self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image, (33, 33))
    
todas_as_sprites=pygame.sprite.Group()
anelgira=Anel(x_anel, y_anel, 40, 40)
todas_as_sprites.add(anelgira)

        
def draw_janela(texto_formatado, texto_formatado_2, background, player, todas_as_sprites, objeto, diamante):

    JANELA.fill(PRETO)
    JANELA.blit(background, (0,0))
    JANELA.blit(texto_formatado, (450, 40))
    JANELA.blit(texto_formatado_2, (100, 40))
    #objeto.draw(JANELA)
    player.draw(JANELA)
    todas_as_sprites.draw(JANELA)
    objeto.draw(JANELA)
    diamante.draw(JANELA)

    pygame.display.update()

def mover(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    if player.rect.y >= 305:
        player.rect.y = 305

    if keys[pygame.K_a] and player.rect.x > 0:
        player.esquerda(VEL)
    if keys[pygame.K_d] and player.rect.x < 600:
        player.direita(VEL)
    if keys[pygame.K_w] and player.rect.y == 305 :
        player.cima(300)

def main():

    clock = pygame.time.Clock()
    rodar = True
    pontos = 0
    vida = 3
    direcao ='direita'
    desapareceu = False

    #fonte = pygame.font.SysFont('courier new', 20, False, False)

    fonte = pygame.font.Font("joystix/joystix monospace.otf", 20)

    sonic = Player(x, y, LARG_PERS,80)

    knuckles = Inimigo(100, 200, LARG_PERS, ALTU_PERS)

    #anel = Objeto(x_azul, y_azul, LARG_PERS, ALTU_PERS)
    knuckles.rect.y= 305

    diamante = Diamante(x_diamante, y_diamante, 33, 33)

    while rodar:
        tempo_inicial=time.time()
        clock.tick(FPS)
        background = pygame.image.load('sprites/mapa.png')
        background = pygame.transform.scale(background,(LARGURA,ALTURA))
        mensagem = f'ANEIS: {pontos}'
        mensagem_2 = f'VIDA: {vida}'
        texto_formatado = fonte.render(mensagem, False, (216, 213, 0))
        texto_formatado_2 = fonte.render(mensagem_2, False, (0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False

        sonic.loop(FPS)


        mover(sonic)

        draw_janela(texto_formatado, texto_formatado_2, background, sonic, todas_as_sprites, knuckles, diamante)
        
        todas_as_sprites.update()

        if diamante.rect.x == anelgira.rect.x:

            diamante.rect.x = randint(40, 600)
            anelgira.rect.x = randint(40, 600)
        
        if direcao == 'direita':
            knuckles.rect.x += 7
        else:
            knuckles.rect.x -= 7

        if knuckles.rect.x >= 600:
            direcao = 'esquerda'
            knuckles.mudar_direcao(direcao)

        if knuckles.rect.x <= 0:
            direcao  = 'direita'
            knuckles.mudar_direcao(direcao)

        if sonic.rect.colliderect(anelgira):
            pontos += 1
            som_colisao.play()
            anelgira.rect.x = randint(40, 600)
            anelgira.rect.y = 305
            if pontos == 20:
                pygame.quit()

        if sonic.rect.colliderect(knuckles):
            vida -= 1
            pontos = 0
            som_colisao.play()
            knuckles.rect.x = randint(40, 600)
            knuckles.rect.y = 305
            if vida <= 0:
                pygame.quit()

        if sonic.rect.colliderect(diamante):
            diamante.rect.x = 1000
            if vida < 3:
                vida += 1

        pontos_especiais = [5,10,15]

        if pontos in pontos_especiais:
            pontos_especiais.remove(pontos)
            diamante.rect.x = randint(40,600)
            
        
    pygame.quit()

if __name__ == "__main__":
    main()
