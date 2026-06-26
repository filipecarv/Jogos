import pygame

janela = pygame.display.set_mode((960, 540))

pygame.display.set_caption("A Grande Corrida")

imagem_fundo = pygame.image.load("imagens\Fundo.png")
jogador_player = pygame.image.load("imagens\jogador.png")
jogador_inimigo = pygame.image.load("imagens\inimigo.png")

#Posiçao do jogador
posicao_x_jogador = 420
posicao_y_jogador = 420
velocidade_jogador = 3.5


loop = True

while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False


    teclas = pygame.key.get_pressed()

    #Movimentação do jogador
    # Ir para cima
    if teclas[pygame.K_UP]:
        posicao_y_jogador -= velocidade_jogador
    # Ir para baixo
    if teclas[pygame.K_DOWN]:
        posicao_y_jogador += velocidade_jogador
    # Ir para esquerda
    if teclas[pygame.K_LEFT]:
        posicao_x_jogador -= velocidade_jogador
    #ir para direita
    if teclas[pygame.K_RIGHT]:
        posicao_x_jogador += velocidade_jogador

    # Limites da tela
    if posicao_y_jogador <= -10:
        posicao_y_jogador = -10
    if posicao_y_jogador >= 440:
        posicao_y_jogador = 440
    if posicao_x_jogador <= -20:
        posicao_x_jogador = -20
    if posicao_x_jogador >= 900:
        posicao_x_jogador = 900


    janela.blit(imagem_fundo, (0, 0))
    janela.blit(jogador_player, (posicao_x_jogador, posicao_y_jogador))
    janela.blit(jogador_inimigo, (420,10))

    pygame.display.update()