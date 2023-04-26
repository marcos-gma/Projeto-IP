import pygame
from pygame.locals import *
from sys import exit
from random import randint

# Início do jogo
pygame.init()

pygame.mixer.music.set_volume(0.25)
musica_de_fundo =  pygame.mixer.music.load('soundtrack\BoxCat Games - CPU Talk.mp3')
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound('soundtrack\smw_1-up.wav')
som_colisao.set_volume(1)

largura = 640
altura = 480

x = largura / 2
y = altura / 2

x_azul = randint(40, 600)
y_azul = randint(50, 430)

pontos = 0
fonte = pygame.font.SysFont('courier new', 20, False, False)

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('THE FORBIDDEN GAME')
relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.fill((0, 0, 0))
    mensagem = f'PONTOS: {pontos}'
    texto_formatado = fonte.render(mensagem, False, (255, 255, 255))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        """if event.type == KEYDOWN:
            if event.key == K_a:
                x -= 20
            if event.key == K_d:
                x += 20
            if event.key == K_w:
                y -= 20
            if event.key == K_s:
                y += 20"""

    if pygame.key.get_pressed()[K_a]:
        x -= 20
    if pygame.key.get_pressed()[K_d]:
        x += 20
    if pygame.key.get_pressed()[K_w]:
        y -= 20
    if pygame.key.get_pressed()[K_s]:
        y += 20

    ret_vermelho = pygame.draw.rect(tela, (255, 0, 0), (x, y, 40, 50))
    ret_azul = pygame.draw.rect(tela, (0, 0, 255), (x_azul, y_azul, 40, 50))

    if ret_vermelho.colliderect(ret_azul):
        x_azul = randint(40, 600)
        y_azul = randint(50, 430)
        pontos += 1
        som_colisao.play()


    tela.blit(texto_formatado, (450, 40))

    pygame.display.update()



