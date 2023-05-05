import pygame
import os
from pygame.locals import *
from random import randint

#constantes

LARGURA = 640   
ALTURA = 580
TITULO = 'THE FORBIDDEN GAME'
FPS = 30
PRETO = (0, 0, 0)
BRANCO = (255,255,255)
LARG_PERS = 40
ALTU_PERS = 50
VEL = 10

pygame.init()

JANELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption(TITULO)

pygame.mixer.music.set_volume(0.25)
musica_de_fundo =  pygame.mixer.music.load('soundtrack\BoxCat Games - CPU Talk.mp3')
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound('soundtrack\smw_1-up.wav')
som_colisao.set_volume(1)

x = LARGURA / 2
y = ALTURA / 2

x_azul = randint(40, 600)
y_azul = randint(50, 430)

SONIC_IMG = pygame.image.load(os.path.join('sprites', 'sonic.png'))
SONIC_IMG = pygame.transform.scale(SONIC_IMG, (LARG_PERS,ALTU_PERS))

KNUCKLES_IMG = pygame.image.load(os.path.join('sprites', 'knuckles.png'))
KNUCKLES_IMG = pygame.transform.flip(pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS)), True, False)


class Player(pygame.sprite.Sprite):
    COR = (255, 0, 0)
    
    SONIC_IMG = pygame.image.load(os.path.join('sprites', 'sonic.png'))
    SPRITE = pygame.transform.scale(SONIC_IMG, (LARG_PERS,ALTU_PERS))

    def __init__(self, x, y, largura, altura):
        super().__init__()
        self.rect = pygame.Rect(x, y, largura, altura)
        self.x_vel = 0
        self.y_vel = 0
        self.direcao = "esquerda"
        self.animacao_cont = 0

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
        if self.direcao != "cima":
            self.direcao = "cima"
            self.animacao_cont = 0
    
    def baixo(self, vel):
        self.y_vel = +vel
        if self.direcao != "baixo":
            self.direcao = "baixo"
            self.animacao_cont = 0
    
    def loop(self, fps):
        self.movimento(self.x_vel, self.y_vel)

    def draw(self, janela):
        self.sprite = self.SPRITE
        janela.blit(self.sprite, (self.rect.x,self.rect.y))

class Objeto(pygame.sprite.Sprite):

    ANEL = pygame.image.load(os.path.join('sprites','aneis', 'ANEL1.png'))
    SPRITE = pygame.transform.scale(ANEL, (30,30))

    def __init__(self, x, y, largura, altura, nome=None):
        super().__init__()
        self.imagem = pygame.Surface((largura,altura), pygame.SRCALPHA)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.largura = largura
        self.altura = altura
        self.nome = nome
        self.image_files = ('ANEL1.png','ANEL2.png')

    def draw(self, janela):
        self.sprite = self.SPRITE
        janela.blit(self.sprite, (self.rect.x, self.rect.y))

    def update(self, collided):
        if collided:
            self.kill()

def draw_janela(texto_formatado, background, player, objeto):

    JANELA.fill(PRETO)
    JANELA.blit(background, (0,0))
    JANELA.blit(texto_formatado, (450, 40))
    objeto.draw(JANELA)
    player.draw(JANELA)

    pygame.display.update()

def mover(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0

    if keys[pygame.K_a] and player.rect.x > 0:
        player.esquerda(VEL)
    if keys[pygame.K_d] and player.rect.x < 600:
        player.direita(VEL)
    if keys[pygame.K_w] and player.rect.y > 0:
        player.cima(VEL)
    if keys[pygame.K_s] and player.rect.y < 530:
        player.baixo(VEL)

def colisao(player, objeto):
    objetos_colididos = []
    if pygame.sprite.collide(player,objeto):
        objetos_colididos.append(objeto)
        return True

def main():

    clock = pygame.time.Clock()
    rodar = True
    pontos = 0
    fonte = pygame.font.SysFont('courier new', 20, False, False)

    player = Player(x, y, LARG_PERS, ALTU_PERS)

    anel = Objeto(x_azul, y_azul, LARG_PERS, ALTU_PERS)

    while rodar:
        clock.tick(FPS)
        background = pygame.image.load('sprites/background_teste.png')
        background = pygame.transform.scale(background,(LARGURA,ALTURA))
        mensagem = f'PONTOS: {pontos}'
        texto_formatado = fonte.render(mensagem, False, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False
        
        player.loop(FPS)

        mover(player)

        draw_janela(texto_formatado, background, player, anel)

        if player.rect.colliderect(anel):
            anel.rect.x = 100000
            pontos += 1
            som_colisao.play()
        update_rect = background.blit(background, anel, anel)

    pygame.quit()

if __name__ == "__main__":
    main()
