import pygame
import constantes

JANELA = pygame.display.set_mode((constantes.LARGURA, constantes.ALTURA))

def draw_janela(texto_formatado, texto_formatado_2, background, todas_as_sprites, todos_os_sonic, inimigo, diamante, game_over, perdeu, vitoria, ganhou, iniciou, texto_menu, replay):

    JANELA.fill(constantes.PRETO)
    JANELA.blit(background, (0,0))
    if iniciou: #tela de gameplay
        JANELA.blit(texto_formatado, (450, 40))
        JANELA.blit(texto_formatado_2, (100, 40))
        if not ganhou and not perdeu:
            todas_as_sprites.draw(JANELA)
            inimigo.draw(JANELA)
            diamante.draw(JANELA)
            todos_os_sonic.draw(JANELA)
        if perdeu:
            JANELA.blit(game_over, (18, 270))
            JANELA.blit(replay, (80, 355))
        if ganhou:
            JANELA.blit(vitoria, (60, 270))
            JANELA.blit(replay, (80, 355))
    else: #tela inicial
        img = pygame.image.load(f'sprites/Titulo.png')
        img = pygame.transform.scale(img, (350,300))
        JANELA.blit(img, (140,40))
        JANELA.blit(texto_menu, (100, 355))
    pygame.display.update()
