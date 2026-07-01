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
largura_tela = info.current_w
altura_tela = info.current_h

x = largura_tela
y = altura_tela

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
img_vida = pygame.image.load("teste 1/imagens/Vida.png").convert_alpha()
img_escudo = pygame.image.load("teste 1/imagens/Escudo.png").convert_alpha()
img_food = pygame.image.load("teste 1/imagens/Comida.png").convert_alpha()
img_intangivel = pygame.image.load("teste 1/imagens/Intangibilidade.png").convert_alpha()
img_coracao = pygame.image.load("teste 1/imagens/Vida.png").convert_alpha()
img_coracao = pygame.transform.scale(img_coracao,(32,32))
img_tiro = pygame.transform.scale(img_tiro, (30, 30))
img_vida = pygame.transform.scale(img_vida, (30, 30))
img_escudo = pygame.transform.scale(img_escudo, (30, 30))
img_food = pygame.transform.scale(img_food, (30, 30))
img_intangivel = pygame.transform.scale(img_intangivel, (30, 30))

# Jogador
px, py = 420, 420
vel = 10

#Boss
boss_ativo = False
boss_x = 0
boss_y = -200
boss_vida = 0
boss_invulneravel = False
tempo_boss_hit = 0
cooldown_boss_hit = 1000  # 1 segundo

# Dash
vel_dash = 200  # distância do dash
cooldown_dash = 5000  # 5 segundos
ultimo_dash = -cooldown_dash

#Intagibilidade
intangivel = False
tempo_intangivel = 0

#Escudo
escudo = False
escudo_hits = 0

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
kills = 0
kills_boss = 0
kills_itens = 0

game_over = False

# Itens
itens_tipos = [
    "vida",
    "intangibilidade",
    "escudo",
    "comida"
]

item_spawnado = False
item_tipo = None
item_x = 0
item_y = 0

# Explosão
explosao = False
ex, ey = 0, 0
timer = 0

# Botão
botao = pygame.Rect(x//2 - 100, y//2 + 60, 300, 60)

# Funções
def reset_inimigo():
    global ix, iy
    ix = randint(100, x-100)
    iy = -200

def reset_jogo():
    global vida, hits, kills, kills_boss, kills_itens, px, py, tx, ty, tiro_ativo, game_over, escudo, escudo_hits, intangivel, item_spawnado

    vida = 3
    hits = 0
    kills = 0
    kills_boss = 0
    kills_itens = 0
    px, py = 420, 420
    reset_inimigo()
    tx, ty = px, py
    tiro_ativo = False
    game_over = False
    escudo = False
    escudo_hits = 0
    intangivel = False
    item_spawnado = False


def spawn_boss():
    global boss_ativo, boss_x, boss_y, boss_vida, ix, iy

    boss_ativo = True
    boss_x = randint(100, x - 100)
    boss_y = -200
    boss_vida = 20

def barra_vida():
    largura = 250
    altura = 22

    # fundo
    pygame.draw.rect(janela, (60, 60, 60), (20, 20, largura, altura))

    # barra baseada em vida total
    vida_total = vida * 3
    vida_atual = vida * 3 - hits

    if vida_atual < 0:
        vida_atual = 0

    percent = vida_atual / vida_total if vida_total > 0 else 0

    # COR baseada em hits atuais do coração
    if hits == 0:
        cor = (0, 255, 0)      # verde
    elif hits == 1:
        cor = (255, 255, 0)    # amarelo
    else:
        cor = (255, 0, 0)      # vermelho

    pygame.draw.rect(janela, cor, (20, 20, largura * percent, altura))

    # borda
    pygame.draw.rect(janela, (255, 255, 255), (20, 20, largura, altura), 2)

def desenhar_coracoes():
    for i in range(vida):
        janela.blit(img_coracao, (20 + i * 40, 85))

def barra_dash():
    restante = max(0, cooldown_dash - (pygame.time.get_ticks() - ultimo_dash))

    largura = 250
    altura = 18

    y_pos = 55  # alinhado visualmente com HUD

    pygame.draw.rect(janela, (70, 70, 70), (20, y_pos, largura, altura))

    if restante == 0:
        cor = (0, 180, 255)
        fill = largura
    else:
        cor = (0, 180, 255)
        fill = largura * (1 - restante / cooldown_dash)

    pygame.draw.rect(janela, cor, (20, y_pos, fill, altura))
    pygame.draw.rect(janela, (255, 255, 255), (20, y_pos, largura, altura), 2)


def tela_game_over():
    janela.fill((0, 0, 0))

    txt = fonte.render("SE FUDEU, FOI COMIDO PELO NEGÃO!", True, (255, 0, 0))
    janela.blit(txt, (x//2 - txt.get_width()//2, y//2 - 130))

    txt2 = fonte.render(f"GOZOU: {kills} VEZES MANO!", True, (0, 255, 0))
    janela.blit(txt2, (x//2 - txt2.get_width()//2, y//2 - 60))

    pygame.draw.rect(janela, (180, 0, 0), botao)

    btn = fonte_btn.render("NÃO SER COMIDO", True, (255, 255, 255))
    janela.blit(btn, (botao.x + 20, botao.y + 15))


def colisao():
    global hits, vida, kills, kills_boss, kills_itens, explosao, ex, ey, timer, escudo, escudo_hits, item_spawnado, item_tipo, item_x, item_y, boss_ativo, boss_vida, tiro_ativo, tempo_boss_hit, boss_invulneravel

    player = pygame.Rect(px, py, 50, 50)
    inimigo = pygame.Rect(ix, iy, 50, 50)
    tiro = pygame.Rect(tx, ty, 10, 10)

    if tiro.colliderect(inimigo):
        kills += 1
        kills_boss += 1
        kills_itens += 1
        explosao = True
        ex, ey = ix, iy
        timer = 10
        reset_inimigo()

        if kills_itens >= 10 and not item_spawnado:
            kills_itens = 0
            item_spawnado = True
            item_tipo = itens_tipos[randint(0, len(itens_tipos)-1)]
            item_x = randint(50, x - 50)
            item_y = randint(80, y - 80)

    if kills_boss >= 50 and not boss_ativo:
        kills_boss = 0
        spawn_boss()

    if boss_ativo:
        boss_rect = pygame.Rect(boss_x+40, boss_y+40, 220, 220)
        tiro_rect = pygame.Rect(tx, ty, 10, 10)

        # cooldown de dano do boss
        if boss_invulneravel:
            if pygame.time.get_ticks() - tempo_boss_hit >= cooldown_boss_hit:
                boss_invulneravel = False

        if player.colliderect(boss_rect) and not intangivel and not boss_invulneravel:
            boss_invulneravel = True
            tempo_boss_hit = pygame.time.get_ticks()

            if escudo:
                escudo_hits -= 2
                if escudo_hits <= 0:
                    escudo = False
            else:
                hits += 2
                if hits >= 3:
                    hits = 0
                    vida -= 1
                    som_morte.play()
                    
        if tiro_rect.colliderect(boss_rect) and tiro_ativo:
            boss_vida -= 1
            tiro_ativo = False
            if boss_vida <= 0:
                kills += 5
                kills_itens += 3
                explosao = True
                ex, ey = boss_x, boss_y
                timer = 10
                boss_ativo = False

    if player.colliderect(inimigo) and not intangivel:
        reset_inimigo()
        if escudo:
            escudo_hits -= 1
            if escudo_hits <= 0:
                escudo = False
        else:
            hits += 1

            if hits >= 3:
                hits = 0
                vida -= 1
                som_morte.play()

def pegar_item():
    global item_spawnado, kills_itens, item_tipo, vida, escudo, escudo_hits, hits, intangivel, tempo_intangivel

    if not item_spawnado:
        return
    player_rect = pygame.Rect(px, py, 50, 50)
    item_rect = pygame.Rect(item_x, item_y, 30, 30)
    if player_rect.colliderect(item_rect):
        if item_tipo == "vida":
            vida += 1
        elif item_tipo == "escudo":
            escudo = True
            escudo_hits = 2

        elif item_tipo == "comida":
            hits = 0
        elif item_tipo == "intangibilidade":
            intangivel = True
            tempo_intangivel = pygame.time.get_ticks()

        # Some o item
        item_spawnado = False
        item_tipo = None
        kills_itens = 0

# Loop
rodando = True

while rodando:
    clock.tick(60)
    tempo_atual = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
            teclas = pygame.key.get_pressed()
            if event.key == pygame.K_LSHIFT:
                if tempo_atual - ultimo_dash >= cooldown_dash:
                    if teclas[pygame.K_w]:
                        py -= vel_dash
                    elif teclas[pygame.K_s]:
                        py += vel_dash
                    elif teclas[pygame.K_a]:
                        px -= vel_dash
                    elif teclas[pygame.K_d]:
                        px += vel_dash
                    ultimo_dash = tempo_atual     

        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_over and botao.collidepoint(event.pos):
                reset_jogo()

    if boss_ativo:
        boss_y += 2  # boss desce devagar
        if boss_y > 150:
            boss_y = 150  # trava posição

    # Estados
    if vida <= 0:
        game_over = True

    if game_over:
        tela_game_over()
        pygame.display.update()
        continue

    janela.blit(fundo, (0, 0))

    teclas = pygame.key.get_pressed()

    #Intangivel
    if intangivel:

        if pygame.time.get_ticks() - tempo_intangivel >= 15000:

            intangivel = False

    # Movimentação
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

    # Inimigo nasce mais longe
    iy += vel_inimigo
    if iy > y:
        ix = randint(100, x - 100)
        # evita nasce em cima do jogador
        while abs(ix - px) < 120:
            ix = randint(100, x - 100)
        iy = -200

    colisao()
    pegar_item()

    # Explosão
    if explosao:
        pygame.draw.circle(janela, (255, 200, 0), (ex, ey), 30)
        timer -= 1
        if timer <= 0:
            explosao = False

    janela.blit(img_player, (px, py))
    if escudo:
        pygame.draw.circle(
            janela,
            (0,180,255),
            (px+25,py+25),
            35,
            3
        )
    janela.blit(img_inimigo, (ix, iy))
    if item_spawnado:
        if item_tipo == "vida":
            janela.blit(img_vida,(item_x,item_y))
        elif item_tipo == "escudo":
            janela.blit(img_escudo,(item_x,item_y))
        elif item_tipo == "comida":
            janela.blit(img_food,(item_x,item_y))
        elif item_tipo == "intangibilidade":
            janela.blit(img_intangivel,(item_x,item_y))

    if boss_ativo:
        boss_img = pygame.transform.scale(img_inimigo, (300, 300))
        janela.blit(boss_img, (boss_x, boss_y))
        pygame.draw.rect(janela, (0, 0, 0), (boss_x, boss_y - 10, 120 * (boss_vida / 20), 5))

    if tiro_ativo:
        janela.blit(img_tiro, (tx, ty))

    barra_vida()
    barra_dash()
    desenhar_coracoes()

    pygame.display.update()

pygame.quit()