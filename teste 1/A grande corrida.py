import pygame
from pygame import mixer
from random import randint

pygame.init()
mixer.init()

# Sons
som_tiro = mixer.Sound("teste 1/imagens/Tiro.mp3")
som_morte = mixer.Sound("teste 1/imagens/Morte.mp3")

# Tela
info = pygame.display.Info()
x, y = info.current_w, info.current_h

janela = pygame.display.set_mode((x, y), pygame.FULLSCREEN)
pygame.display.set_caption("A Grande Corrida")

fonte = pygame.font.SysFont("Arial", 40)
fonte_btn = pygame.font.SysFont("Arial", 30)

clock = pygame.time.Clock()

# Imagens
fundo = pygame.image.load("teste 1/imagens/Fundo.png")
fundo = pygame.transform.scale(fundo, (x, y))

img_player = pygame.image.load("teste 1/imagens/Jogador.png").convert_alpha()
img_inimigo = pygame.image.load("teste 1/imagens/Inimigo.png").convert_alpha()
img_tiro = pygame.image.load("teste 1/imagens/Tiro.png").convert_alpha()
img_tiro = pygame.transform.scale(img_tiro, (30, 30))

# Jogador
px, py = 420, 420
vel = 7
# colisão com bordas da tela
if px < 0:
    px = 0
if px > x - 50:
    px = x - 50
if py < 0:
    py = 0
if py > y - 50:
    py = y - 50

# Inimigo
ix, iy = randint(100, x-100), -100
vel_inimigo = 7

# Tiro
tx, ty = px, py
tiro_ativo = False
vel_tiro = 12

# Vida/Estado
vida = 3
hits = 0
pontuacao = 0

game_over = False
vitoria = False

# Explosão
explosao = False
ex, ey = 0, 0
timer = 0

# Botão
botao = pygame.Rect(x//2 - 100, y//2 + 60, 260, 60)

# Funções
def reset_inimigo():
    global ix, iy
    ix = randint(100, x-100)
    iy = -200


def reset_jogo():
    global vida, hits, pontuacao, px, py, tx, ty, tiro_ativo, game_over, vitoria

    vida = 3
    hits = 0
    pontuacao = 0

    px, py = 420, 420

    reset_inimigo()

    tx, ty = px, py
    tiro_ativo = False

    game_over = False
    vitoria = False


def barra_vida():
    largura = 200
    altura = 20

    percent = vida / 3

    cor = (
        int(255 * (1 - percent)),
        int(255 * percent),
        0
    )

    pygame.draw.rect(janela, (50, 50, 50), (20, 20, largura, altura))
    pygame.draw.rect(janela, cor, (20, 20, largura * percent, altura))


def tela_game_over():
    janela.fill((0, 0, 0))

    txt = fonte.render("SE FUDEU, FOI COMIDO PELO NEGÃO!", True, (255, 0, 0))
    janela.blit(txt, (x//2 - txt.get_width()//2, y//2 - 80))

    pygame.draw.rect(janela, (180, 0, 0), botao)

    btn = fonte_btn.render("NÃO SER COMIDO", True, (255, 255, 255))
    janela.blit(btn, (botao.x + 25, botao.y + 15))


def tela_vitoria():
    janela.fill((0, 0, 0))

    txt = fonte.render("PARABENS, VOCÊ QUE COMEU O NEGÃO!", True, (0, 255, 0))
    janela.blit(txt, (x//2 - txt.get_width()//2, y//2 - 80))

    txt2 = fonte_btn.render("ESC PARA SAIR", True, (0, 200, 0))
    janela.blit(txt2, (x//2 - txt2.get_width()//2, y//2))


def colisao():
    global hits, vida, pontuacao, explosao, ex, ey, timer

    player = pygame.Rect(px, py, 50, 50)
    inimigo = pygame.Rect(ix, iy, 50, 50)
    tiro = pygame.Rect(tx, ty, 10, 10)

    if tiro.colliderect(inimigo):
        pontuacao += 1
        explosao = True
        ex, ey = ix, iy
        timer = 10
        reset_inimigo()

    if player.colliderect(inimigo):
        hits += 1
        reset_inimigo()

        if hits >= 3:
            hits = 0
            vida -= 1
            som_morte.play()


# Loop
rodando = True

while rodando:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and botao.collidepoint(event.pos):
                reset_jogo()

    # Estados
    if vida <= 0:
        game_over = True

    if pontuacao >= 10:
        vitoria = True

    if game_over:
        tela_game_over()
        pygame.display.update()
        continue

    if vitoria:
        tela_vitoria()
        pygame.display.update()
        continue

    # Gameplay
    janela.blit(fundo, (0, 0))

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_w]: py -= vel
    if teclas[pygame.K_s]: py += vel
    if teclas[pygame.K_a]: px -= vel
    if teclas[pygame.K_d]: px += vel

    # MOVIMENTO
    if teclas[pygame.K_w]:
        py -= vel
    if teclas[pygame.K_s]:
        py += vel
    if teclas[pygame.K_a]:
        px -= vel
    if teclas[pygame.K_d]:
        px += vel
    if px < 0:
        px = 0
    if px > x - img_player.get_width():
        px = x - img_player.get_width()
    if py < 0:
        py = 0
    if py > y - img_player.get_height():
        py = y - img_player.get_height()

    # Tiro Mouse
    if pygame.mouse.get_pressed()[0] and not tiro_ativo:
        tx, ty = px, py
        tiro_ativo = True
        som_tiro.play()

    if tiro_ativo:
        ty -= vel_tiro
        if ty < -40:
            tiro_ativo = False

    # inimigo spawn mais longe
    iy += vel_inimigo
    if iy > y:
        ix = randint(100, x - 100)
        # evita spawn em cima do jogador
        while abs(ix - px) < 120:
            ix = randint(100, x - 100)
        iy = -200

    colisao()

    # explosão
    if explosao:
        pygame.draw.circle(janela, (255, 200, 0), (ex, ey), 30)
        timer -= 1
        if timer <= 0:
            explosao = False

    janela.blit(img_player, (px, py))
    janela.blit(img_inimigo, (ix, iy))

    if tiro_ativo:
        janela.blit(img_tiro, (tx, ty))

    barra_vida()

    pygame.display.update()

pygame.quit()