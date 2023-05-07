import pygame
import os
from pygame.locals import *
from random import randint

#constantes

LARGURA = 640   
ALTURA = 580
TITULO = 'SONIC RUN'
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
musica_de_fundo =  pygame.mixer.music.load('soundtrack/GreenHillZone.mp3')
pygame.mixer.music.play(-1)

som_colisao = pygame.mixer.Sound('soundtrack/smw_1-up.wav')
som_colisao.set_volume(1)

som_perde_aneis = pygame.mixer.Sound('soundtrack/PerdeuAneis.mp3')
som_perde_aneis.set_volume(0.2)

som_vida_extra = pygame.mixer.Sound('soundtrack/VidaExtra.mp3')
som_vida_extra.set_volume(0.5)

x = 70
y = 285 

y=285

x_anel = randint(40, 600)
y_anel = 320

x_diamante = randint(40, 600)
y_diamante = 320


KNUCKLES_IMG = pygame.image.load(os.path.join('sprites', 'knuckles.png'))
KNUCKLES_IMG = pygame.transform.flip(pygame.transform.scale(KNUCKLES_IMG, (LARG_PERS,ALTU_PERS)), True, False)


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
        self.direcao = "esquerda"
        self.largura = largura
        self.altura = altura
        self.animacao_cont = 0
        self.queda_cont = 0
        self.pulo_cont = 0

    def pular(self):
        self.y_vel = -self.GRAVIDADE * 80
        self.animacao_cont = 0
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
        if self.direcao != "esquerda":
            self.direcao = "esquerda"
            self.animacao_cont = 0

    def direita(self, vel):
        self.x_vel = vel
        if self.direcao != "direita":
            self.direcao = "direita"
            self.animacao_cont = 0
    
    def loop(self, fps):
        self.y_vel += 8 * (min(1, (self.queda_cont / fps) * self.GRAVIDADE))
        self.movimento(self.x_vel, self.y_vel)

        self.queda_cont += 1

    def draw(self, janela):
        janela.blit(self.image, (self.rect.x,self.rect.y))

    def update(self,keys):
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
        

    def mudar_direcao(self, direcao):
        if direcao == "esquerda":
            self.sprite = pygame.transform.scale(self.image, (self.largura, self.altura))
        else:
            self.sprite = pygame.transform.flip(pygame.transform.scale(self.image, (self.largura, self.altura)), True, False)

todos_os_sonic = pygame.sprite.Group()
sonic=Player(x, y, 70, 70)
todos_os_sonic.add(sonic)

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
        for i in range(1,11):
            self.sprites.append(pygame.image.load(f'sprites/aneis/ANEL{i}.png'))
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

        
def draw_janela(texto_formatado, texto_formatado_2, background, todas_as_sprites, objeto, diamante, game_over, perdeu, vitoria, ganhou, iniciou, texto_menu):

    JANELA.fill(PRETO)
    JANELA.blit(background, (0,0))
    if iniciou:
        JANELA.blit(texto_formatado, (450, 40))
        JANELA.blit(texto_formatado_2, (100, 40))
        if not ganhou and not perdeu:
            todas_as_sprites.draw(JANELA)
            objeto.draw(JANELA)
            diamante.draw(JANELA)
            todos_os_sonic.draw(JANELA)
        if perdeu:
            JANELA.blit(game_over, (18, 270))
        if ganhou:
            JANELA.blit(vitoria, (60, 270))
    else:
        img = pygame.image.load(f'sprites/Titulo.png')
        img = pygame.transform.scale(img, (350,300))
        JANELA.blit(img, (140,40))
        JANELA.blit(texto_menu, (100, 355))
    pygame.display.update()

def mover(player):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    player.y_vel = 0
    if player.rect.y >= 285:
        player.rect.y = 285

    if keys[pygame.K_a] and player.rect.x > 0:
        player.esquerda(VEL)
    if keys[pygame.K_d] and player.rect.x < 600:
        player.direita(VEL)



def main():

    clock = pygame.time.Clock()
    rodar = True
    pontos = 0
    vida = 3
    direcao_knuckles ='direita'
    jogando = True
    perdeu = False
    ganhou = False
    iniciou = False

    fonte = pygame.font.Font("joystix/joystix monospace.otf", 20)
    fonte2 = pygame.font.Font("joystix/joystix monospace.otf", 80)

    knuckles = Inimigo(100, 200, LARG_PERS, ALTU_PERS)

    knuckles.rect.y= 285

    diamante = Diamante(x_diamante, y_diamante, 33, 33)


    while rodar:
        clock.tick(FPS)
        background = pygame.image.load('sprites/mapa.png')
        background = pygame.transform.scale(background,(LARGURA,ALTURA))
        mensagem = f'ANEIS: {pontos}'
        if vida < 0:
            vida = 0
        mensagem_2 = f'VIDA: {vida}'
        texto_formatado = fonte.render(mensagem, False, (0, 0, 0))
        texto_formatado_2 = fonte.render(mensagem_2, False, (0, 0, 0))
        derrota = fonte2.render('GAME OVER', False, (255, 0, 0))
        vitoria = fonte2.render('VITÓRIA!', False, (255, 255, 0))
        mensagem_menu = fonte.render('APERTE ESPAÇO PARA COMEÇAR', False, (0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodar = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and sonic.pulo_cont < 2:
                    sonic.pular()
                if event.key == pygame.K_SPACE:
                    iniciou = True
                    vida = 3
                    pontos = 0


        sonic.loop(FPS)

        mover(sonic)

        draw_janela(texto_formatado, texto_formatado_2, background, todas_as_sprites, knuckles, diamante, derrota, perdeu, vitoria, ganhou, iniciou, mensagem_menu)
        
        todas_as_sprites.update()

        keys = pygame.key.get_pressed()

        todos_os_sonic.update(keys)

        if diamante.rect.x == anelgira.rect.x:

            diamante.rect.x = randint(40, 600)
            anelgira.rect.x = randint(40, 600)
        
        if jogando and iniciou:
            if direcao_knuckles == 'direita':
                knuckles.rect.x += 7
            else:
                knuckles.rect.x -= 7

        if knuckles.rect.x >= 600:
            direcao_knuckles = 'esquerda'
            knuckles.mudar_direcao(direcao_knuckles)

        if knuckles.rect.x <= 0:
            direcao_knuckles  = 'direita'
            knuckles.mudar_direcao(direcao_knuckles)

        if sonic.rect.y >= 285:
            sonic.caiu()
      
        if sonic.rect.colliderect(anelgira):
            pontos += 1
            if iniciou:
                som_colisao.play()
            anelgira.rect.x = randint(40, 600)
            anelgira.rect.y = randint(120,285)
            if pontos == 20:
                jogando = False
                ganhou = True
                pygame.mixer.music.load('soundtrack/Vitoria.mp3')
                pygame.mixer.music.play(-1)

        if sonic.rect.colliderect(knuckles):
            if pontos > 0 :
                som_perde_aneis.play()
            vida -= 1
            pontos = 0
            if direcao_knuckles == 'direita':
                knuckles.rect.x += 130
            else:
                knuckles.rect.x -= 130
            if vida <= 0:
                jogando = False
                perdeu = True
                pygame.mixer.music.load('soundtrack/GameOver.mp3')
                pygame.mixer.music.play(-1)

        pontos_especiais = [5,10,15]

        if pontos in pontos_especiais:
            pontos_especiais.remove(pontos)
            
            if diamante.rect.x >= 640:
                diamante.rect.x = 30 * pontos

        if sonic.rect.colliderect(diamante):

            diamante.rect.x = 1000
            if vida < 3:
                vida += 1
                if iniciou:
                    som_vida_extra.play()
            
        
    pygame.quit()

if __name__ == "__main__":
    main()
