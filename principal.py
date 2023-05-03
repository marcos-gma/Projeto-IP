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

def draw_janela(vermelho,azul,texto_formatado, background):
    JANELA.fill(PRETO)
    JANELA.blit(background, (0,0))
    JANELA.blit(KNUCKLES_IMG, (vermelho.x,vermelho.y))
    JANELA.blit(SONIC_IMG, (azul.x,azul.y))
    JANELA.blit(texto_formatado, (450, 40))
    pygame.display.update()

def vermelho_mov(keys_pressed,vermelho):
    if keys_pressed[pygame.K_a] and vermelho.x - VEL > 0: #ESQUERDA
        vermelho.x -= VEL
    if keys_pressed[pygame.K_d] and vermelho.x + VEL + vermelho.width < LARGURA: #DIREITA
        vermelho.x += VEL
    if keys_pressed[pygame.K_w] and vermelho.y - VEL > 0: #CIMA
        vermelho.y -= VEL
    if keys_pressed[pygame.K_s] and vermelho.y + VEL + vermelho.height < ALTURA: #BAIXO
        vermelho.y += VEL

def azul_mov(keys_pressed,azul):
    if keys_pressed[pygame.K_LEFT] and azul.x - VEL > 0: #ESQUERDA
        azul.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and azul.x + VEL + azul.width < LARGURA: #DIREITA
        azul.x += VEL
    if keys_pressed[pygame.K_UP] and azul.y - VEL > 0: #CIMA
        azul.y -= VEL
    if keys_pressed[pygame.K_DOWN] and azul.y + VEL + azul.height < ALTURA: #BAIXO
        azul.y += VEL

def main():
    vermelho = pygame.Rect(x, y, LARG_PERS, ALTU_PERS)
    azul = pygame.Rect(x_azul, y_azul, LARG_PERS, ALTU_PERS)

    clock = pygame.time.Clock()
    rodar = True
    pontos = 0
    fonte = pygame.font.SysFont('courier new', 20, False, False)


    while rodar:
        clock.tick(FPS)
        background = pygame.image.load('sprites/background_teste.png')
        background = pygame.transform.scale(background,(LARGURA,ALTURA))
        mensagem = f'PONTOS: {pontos}'
        texto_formatado = fonte.render(mensagem, False, (255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False

        keys_pressed = pygame.key.get_pressed()

        vermelho_mov(keys_pressed,vermelho)
        azul_mov(keys_pressed,azul)
        
        draw_janela(vermelho,azul,texto_formatado,background)

        if vermelho.colliderect(azul):
            pontos += 1
            som_colisao.play()

    pygame.quit()

if __name__ == "__main__":
    main()
