import pygame
from pygame import mixer
from time import sleep
from random import randint
from random import Random

pygame.init()
mixer.init()

janela = pygame.display.set_mode((960, 540))

pygame.display.set_caption("A Grande Corrida")


#Carregamento de imagens do jogo
imagem_fundo = pygame.image.load("teste 1\imagens\Fundo.png")
jogador_player = pygame.image.load("teste 1\imagens\Jogador.png")
janela.blit(imagem_fundo, (0, 0))
jogador_inimigo = pygame.image.load("teste 1\imagens\Inimigo.png")
tiro = pygame.image.load('teste 1\imagens\Tiro.png')
tiro = pygame.transform.scale(tiro, (30,30))


tiro_alvo = False


#Posiçao do jogador
posicao_x_jogador = 420
posicao_y_jogador = 420
velocidade_jogador = 3.5


#Posiçao do Inimigo
posicao_x_inimigo = 420
posicao_y_inimigo = 10
velocidade_inimigo= 5.5


#Posiçao do Tiro
vel_x_tiro= 10
posicao_x_tiro = 420
posicao_y_tiro = 470

pontuacao = 0

loop = True

while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False


    teclas = pygame.key.get_pressed()


    #Movimentação do jogador
    # Ir para cima
    if teclas[pygame.K_w]:
        posicao_y_jogador -= velocidade_jogador
    # Ir para baixo
    if teclas[pygame.K_s]:
        posicao_y_jogador += velocidade_jogador
    # Ir para esquerda
    if teclas[pygame.K_a]:
        posicao_x_jogador -= velocidade_jogador
    #ir para direita
    if teclas[pygame.K_d]:
        posicao_x_jogador += velocidade_jogador


    #Movimento nave Inimiga
    posicao_y_inimigo += 2


    #
    if posicao_y_inimigo > 530:
        random_y = randint(1, 460)
        random_x = randint(1, 890)
        posicao_y_inimigo -= 470
        posicao_y_inimigo = random_y
        posicao_x_inimigo = random_x


    # Limites da tela
    if posicao_y_jogador <= -10:
        posicao_y_jogador = -10
    if posicao_y_jogador >= 440:
        posicao_y_jogador = 440
    if posicao_x_jogador <= -20:
        posicao_x_jogador = -20
    if posicao_x_jogador >= 900:
        posicao_x_jogador = 900

    janela.blit(jogador_player, (posicao_x_jogador, posicao_y_jogador))
    janela.blit(jogador_inimigo, (posicao_x_inimigo,posicao_y_inimigo))

    pygame.display.update()