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
musica_de_fundo =  pygame.mixer.music.load('soundtrack/BoxCat.mp3')
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound('soundtrack/smw_1-up.wav')
som_colisao.set_volume(1)

x = LARGURA / 2
y = ALTURA / 2
y=305

x_azul = randint(40, 600)
y_azul = 320


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

    KNUCKLES_IMG = pygame.image.load(os.path.join('sprites', 'knuckles.png'))
    SPRITE = pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS))

    def __init__(self, x, y, largura, altura):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, largura, altura)
        self.largura = largura
        self.altura = altura
    
    def draw(self, janela):
        self.sprite = self.SPRITE
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
anelgira=Anel(x_azul, y_azul, 40, 40)
todas_as_sprites.add(anelgira)

        
def draw_janela(texto_formatado, texto_formatado_2, background, player, todas_as_sprites, objeto):

    JANELA.fill(PRETO)
    JANELA.blit(background, (0,0))
    JANELA.blit(texto_formatado, (450, 40))
    JANELA.blit(texto_formatado_2, (100, 40))
    #objeto.draw(JANELA)
    player.draw(JANELA)
    todas_as_sprites.draw(JANELA)
    objeto.draw(JANELA)

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
    if keys[pygame.K_s] and player.rect.y < 305:
        player.baixo(VEL)

'''def colisao(player, objeto):
    objetos_colididos = []
    if pygame.sprite.collide(player,objeto):
        objetos_colididos.append(objeto)
        return True'''

def main():

    clock = pygame.time.Clock()
    rodar = True
    pontos = 0
    vida = 3
    direcao ='direita'

    fonte = pygame.font.SysFont('courier new', 20, False, False)

    player = Player(x, y, LARG_PERS,ALTU_PERS)

    objeto = Objeto(100, 200, LARG_PERS,ALTU_PERS)

    #anel = Objeto(x_azul, y_azul, LARG_PERS, ALTU_PERS)
    objeto.rect.y= 305



    while rodar:
        clock.tick(FPS)
        background = pygame.image.load('sprites/mapa.png')
        background = pygame.transform.scale(background,(LARGURA,ALTURA))
        mensagem = f'ANEIS: {pontos}'
        mensagem_2 = f'VIDA: {vida}'
        texto_formatado = fonte.render(mensagem, False, (255, 255, 255))
        texto_formatado_2 = fonte.render(mensagem_2, False, (255, 255, 255))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False
        player.loop(FPS)

        mover(player)

        draw_janela(texto_formatado, texto_formatado_2, background, player, todas_as_sprites,objeto)
        
        todas_as_sprites.update()
        
        if direcao == 'direita':
            objeto.rect.x += 4
        else:
            objeto.rect.x -= 4

        if objeto.rect.x >= 600:
            direcao = 'esquerda'import pygame
2
import os
3
from pygame.locals import *
4
from random import randint
5
​
6
#constantes
7
​
8
LARGURA = 640   
9
ALTURA = 580
10
TITULO = 'THE FORBIDDEN GAME'
11
FPS = 30
12
PRETO = (0, 0, 0)
13
BRANCO = (255,255,255)
14
LARG_PERS = 40
15
ALTU_PERS = 50
16
VEL = 10
17
​
18
pygame.init()
19
​
20
JANELA = pygame.display.set_mode((LARGURA, ALTURA))
21
pygame.display.set_caption(TITULO)
22
​
23
pygame.mixer.music.set_volume(0.25)
24
musica_de_fundo =  pygame.mixer.music.load('soundtrack/BoxCat.mp3')
25
pygame.mixer.music.play(-1)
26
​
27
som_colisao = pygame.mixer.Sound('soundtrack/smw_1-up.wav')
28
som_colisao.set_volume(1)
29
​
30
x = LARGURA / 2
31
y = ALTURA / 2
32
​
33
x_azul = randint(40, 600)
34
y_azul = 320
35
​
36
SONIC_IMG = pygame.image.load(os.path.join('sprites', 'sonic.png'))
37
SONIC_IMG = pygame.transform.scale(SONIC_IMG, (LARG_PERS,ALTU_PERS))
38
​
39
KNUCKLES_IMG = pygame.image.load(os.path.join('sprites', 'knuckles.png'))
40
KNUCKLES_IMG = pygame.transform.flip(pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS)), True, False)
41
​
42
​
43
class Player(pygame.sprite.Sprite):
44
​
45
    COR = (255, 0, 0)
46
    
47
    SONIC_IMG = pygame.image.load(os.path.join('sprites', 'sonic.png'))
48
    SPRITE = pygame.transform.scale(SONIC_IMG, (LARG_PERS,ALTU_PERS))
49
​
50
    def __init__(self, x, y, largura, altura):
51
        super().__init__()
52
        self.rect = pygame.Rect(x, y, largura, altura)
        if objeto.rect.x <= 0:
            direcao = 'direita'
 

        if player.rect.colliderect(anelgira):
            pontos += 1
            som_colisao.play()
            anelgira.rect.x = randint(40, 600)
            anelgira.rect.y = 305

        if player.rect.colliderect(objeto):
            vida -= 1
            som_colisao.play()
            objeto.rect.x = randint(40, 600)
            objeto.rect.y = 305
            if vida <= 0:
                pygame.quit()


    pygame.quit()

if __name__ == "__main__":
    main()
