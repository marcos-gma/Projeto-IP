import pygame
from pygame.locals import *
from random import randint
from classes.player import Player 
from classes.player import mover
from classes.inimigo import Inimigo
from classes.anel import Anel
from classes.diamante import Diamante
from tela import draw_janela
import constantes

#inicializando o pygame e atribuindo o titulo do jogo

pygame.init()
pygame.display.set_caption(constantes.TITULO)


#sons e músicas

pygame.mixer.music.set_volume(0.25)
musica_de_fundo =  pygame.mixer.music.load('soundtrack/GreenHillZone.mp3')
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound('soundtrack/pegou_anel.wav')
som_colisao.set_volume(1)

som_perde_aneis = pygame.mixer.Sound('soundtrack/PerdeuAneis.mp3')
som_perde_aneis.set_volume(0.2)

som_vida_extra = pygame.mixer.Sound('soundtrack/VidaExtra.mp3')
som_vida_extra.set_volume(0.5)

som_hit = pygame.mixer.Sound('soundtrack/Hit.mp3')
som_hit.set_volume(0.5)

som_diamante = pygame.mixer.Sound('soundtrack/pegou_diamante.mp3')
som_diamante.set_volume(0.15)

#posições dos personagens e itens 

x_player = 70
y_player = 285 

x_inimigo = 100
y_inimigo = 285

x_anel = randint(40, 600)
y_anel = 320

x_diamante = randint(40, 600)
y_diamante = 320


def main():

    clock = pygame.time.Clock()

    #variáveis 

    rodar = True
    pontos = 0
    vida = 3
    direcao_knuckles ='direita'
    jogando = True
    perdeu = False
    ganhou = False
    iniciou = False
    musica_original = True
    
    #fontes

    fonte = pygame.font.Font("joystix/joystix monospace.otf", 20)
    fonte2 = pygame.font.Font("joystix/joystix monospace.otf", 80)

    #criando os objetos do game
    
    todos_os_sonic = pygame.sprite.Group()
    sonic = Player(x_player, y_player,constantes.LARG_PERS, constantes.ALTU_PERS)
    todos_os_sonic.add(sonic)
    
    todos_os_aneis = pygame.sprite.Group()
    anel = Anel(x_anel, y_anel, 40, 40)
    todos_os_aneis.add(anel)

    diamante = Diamante(x_diamante, y_diamante, 33, 33)

    knuckles = Inimigo(x_inimigo, y_inimigo, constantes.LARG_PERS, constantes.ALTU_PERS)

    #while do jogo

    while rodar:

        clock.tick(constantes.FPS)
        background = pygame.image.load('sprites/mapa.png')
        background = pygame.transform.scale(background,(constantes.LARGURA,constantes.ALTURA))
        mensagem = f'ANEIS: {pontos}'

        if vida < 0:
            vida = 0

        if pontos > 20:
            pontos = 20

        #textos da tela
        mensagem_2 = f'VIDA: {vida}'
        texto_formatado = fonte.render(mensagem, False, (0, 0, 0))
        texto_formatado_2 = fonte.render(mensagem_2, False, (0, 0, 0))
        derrota = fonte2.render('GAME OVER', False, (255, 0, 0))
        vitoria = fonte2.render('VITÓRIA!', False, (255, 255, 0))
        mensagem_menu = fonte.render('APERTE ESPAÇO PARA COMEÇAR', False, (0, 0, 0))
        replay = fonte.render('APERTE ESPAÇO PARA RECOMEÇAR', False, (0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and sonic.pulo_cont < 2:
                    sonic.pular()
                if event.key == pygame.K_SPACE:
                    iniciou = True
                    jogando = True
                    vida = 3
                    pontos = 0
                    perdeu = False
                    ganhou = False
                    if not musica_original:
                        pygame.mixer.music.load('soundtrack/GreenHillZone.mp3')
                        pygame.mixer.music.play(-1)

        sonic.loop(constantes.FPS)

        mover(sonic)

        draw_janela(texto_formatado, texto_formatado_2, background, todos_os_aneis, todos_os_sonic, knuckles, diamante, derrota, perdeu, vitoria, ganhou, iniciou, mensagem_menu, replay)
        
        todos_os_aneis.update()

        keys = pygame.key.get_pressed()

        todos_os_sonic.update(keys)

        if diamante.rect.x == anel.rect.x:

            diamante.rect.x = randint(40, 600)
            anel.rect.x = randint(40, 600)
        
        if jogando and iniciou:
            if direcao_knuckles == 'direita':
                knuckles.rect.x += 8
            else:
                knuckles.rect.x -= 8
                
        #o knuckles inverte sua sprite quando bate nos limites

        if knuckles.rect.x >= 600:
            direcao_knuckles = 'esquerda'
            knuckles.mudar_direcao(direcao_knuckles)

        if knuckles.rect.x <= 0:
            direcao_knuckles  = 'direita'
            knuckles.mudar_direcao(direcao_knuckles)

        if sonic.rect.y >= 285:
            sonic.caiu()
      
        if sonic.rect.colliderect(anel):
            pontos += 1
            if iniciou:
                som_colisao.play()
            anel.rect.x = randint(40, 600) #o anel reaparece em outro lugar da tela que o sonic possa alcançar
            anel.rect.y = randint(120,285)
            if pontos == 20:
                jogando = False
                ganhou = True
                musica_original = False
                pygame.mixer.music.load('soundtrack/Vitoria.mp3')
                pygame.mixer.music.play(-1)

        if sonic.rect.colliderect(knuckles):
            if iniciou and jogando:
                if pontos > 0 :
                    som_perde_aneis.play()
                else:
                    som_hit.play()
            vida -= 1
            pontos = 0
            if direcao_knuckles == 'direita':
                knuckles.rect.x += 130 #o knuckles segue seu caminho
            else:
                knuckles.rect.x -= 130
            if vida <= 0:
                jogando = False
                perdeu = True
                musica_original = False
                pygame.mixer.music.load('soundtrack/GameOver.mp3')
                pygame.mixer.music.play(-1)

        #quando o jogador atingir essas pontuações um diamante irá aparecer 
        pontos_especiais = [5,10,15]

        if sonic.rect.colliderect(diamante):

            if pontos not in pontos_especiais: #quando o diamante aparece o jogador tem que aumentar sua pontuação para coletá-lo
                diamante.rect.x = 1000 #o diamante desaparece da tela visível
                if vida < 3:
                    vida += 1
                    if iniciou:
                        som_vida_extra.play()
                elif vida == 3:
                    som_diamante.play()

        if pontos in pontos_especiais:
            pontos_especiais.remove(pontos)
            
            if diamante.rect.x >= 640:
                diamante.rect.x = 30 * pontos
            
        
    pygame.quit()

if __name__ == "__main__":
    main()
