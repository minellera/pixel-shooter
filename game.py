import pygame
import sys
import math
import random
import os

# ---------- Variáveis

scale     = 6      # Multiplica a quantidade de pixels na tela
mapWidth  = 200    
mapHeight = 100
sprSize   = 8      # Tamanho do sprite em pixels
uiH       = 50     # Altura da barra de pontuação em pixels

# Definição do tamanho final da tela
winW      = mapWidth * scale           # 600 px
winH      = mapHeight * scale + uiH   # 650 px

playerSpeed = 60.0
bulletSpeed = 220.0
bulletCd    = 0.5     # Cooldown entre os tiros pewpew
enemySpeed  = 28.0    
spawnStart  = 5.0     # Intervalo inicial de spawn
spawnMin    = 0.8     # Intervalo mínimo de spawn
spawnDecay  = 0.93    # Fator de redução do intervalo de spawn

# Definição das cores do jogo em RGB
cMap      = (18,  58,  18)
cMapEdge  = (30,  80,  30)
cUi       = (10,  12,  28)
cBullet   = (255, 228,   0)
cWhite    = (255, 255, 255)
cGold     = (255, 215,   0)
cBtn      = ( 38, 128,  38)
cBtnHov   = ( 68, 188,  68)
cTitle    = (255, 218,  60)
cGameover = (220,  55,  55)

stateMenu, stateGame, stateGameover = 'menu', 'game', 'gameover'

assetsDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')

# ---------- Funções pra facilitar a vida depois

# Carrega um PNG da pasta assets e escala
def load_sprite(filename, scale):
    path = os.path.join(assetsDir, filename)
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    return pygame.transform.scale(img, (w * scale, h * scale))

# Carrega um arquivo de áudio e retorna um objeto Sound
def load_sound(filename):
    return pygame.mixer.Sound(os.path.join(assetsDir, filename))

# Desenha o botão bonitinho
def draw_button(surf, rect, text, font, hovered):
    pygame.draw.rect(surf, cBtnHov if hovered else cBtn, rect, border_radius=6)
    pygame.draw.rect(surf, cWhite, rect, 2, border_radius=6)
    lbl = font.render(text, False, cWhite)
    surf.blit(lbl, (rect.centerx - lbl.get_width() // 2,
                    rect.centery - lbl.get_height() // 2))

# Converte coordenadas de jogo em coordenadas de tela
def to_screen(gx, gy, oy=uiH):
    return int(gx * scale), int(gy * scale + oy)


# ---------- Classes de objetos do jogo

# Projétil disparado pelo player
class Bullet:

    gfxSize = 2  # tamanho pixels

    def __init__(self, x, y, dx, dy):
        self.x, self.y = float(x), float(y)
        self.dx, self.dy = float(dx), float(dy)
        self.alive = True

    # Move o projétil e o desativa ao sair do mapa
    def update(self, dt):
        self.x += self.dx * bulletSpeed * dt
        self.y += self.dy * bulletSpeed * dt
        if not (0 <= self.x <= mapWidth and 0 <= self.y <= mapHeight):
            self.alive = False

    # Renderiza o projétil
    def draw(self, surf, oy=uiH):
        sx, sy = to_screen(self.x, self.y, oy)
        half = self.gfxSize * scale // 2
        pygame.draw.rect(surf, cBullet,
                         (sx - half, sy - half,
                          self.gfxSize * scale, self.gfxSize * scale))

    # Retorna o rect de colisão em coordenadas
    def get_rect(self):
        h = self.gfxSize / 2.0
        return pygame.Rect(self.x - h, self.y - h, self.gfxSize, self.gfxSize)

# Personagem controlado pelo jogador
class Player:

    def __init__(self, sprite):
        self.x = mapWidth / 2.0
        self.y = mapHeight / 2.0
        self.sprite = sprite
        self.bullets = []
        self.cooldown = 0.0

    # Movimento (WASD) e disparo (setas)
    def update(self, dt, keys):
        dx = float(keys[pygame.K_d] - keys[pygame.K_a])
        dy = float(keys[pygame.K_s] - keys[pygame.K_w])
        if dx and dy:
            dx *= 0.7071
            dy *= 0.7071
        half = sprSize / 2.0
        self.x = max(half, min(mapWidth  - half, self.x + dx * playerSpeed * dt))
        self.y = max(half, min(mapHeight - half, self.y + dy * playerSpeed * dt))

        self.cooldown = max(0.0, self.cooldown - dt)
        if self.cooldown <= 0.0:
            dirKeys = (
                (pygame.K_UP,     0, -1),
                (pygame.K_DOWN,   0,  1),
                (pygame.K_LEFT,  -1,  0),
                (pygame.K_RIGHT,  1,  0),
            )
            for k, bdx, bdy in dirKeys:
                if keys[k]:
                    self.bullets.append(Bullet(self.x, self.y, bdx, bdy))
                    self.cooldown = bulletCd
                    break

    # Spawna o player
    def draw(self, surf, oy=uiH):
        sx, sy = to_screen(self.x, self.y, oy)
        w, h = self.sprite.get_size()
        surf.blit(self.sprite, (sx - w // 2, sy - h // 2))

    # Retorna o rect de colisão em coordenadas
    def get_rect(self):
        h = sprSize / 2.0
        return pygame.Rect(self.x - h, self.y - h, sprSize, sprSize)

# Inimigo que persegue o player
class Enemy:

    def __init__(self, x, y, sprite):
        self.x, self.y = float(x), float(y)
        self.sprite = sprite
        self.alive = True

    # Move em direção ao player
    def update(self, dt, px, py):
        dx, dy = px - self.x, py - self.y
        dist = math.hypot(dx, dy)
        if dist:
            self.x += (dx / dist) * enemySpeed * dt
            self.y += (dy / dist) * enemySpeed * dt

    # Desenha o sprite do inimigo
    def draw(self, surf, oy=uiH):
        sx, sy = to_screen(self.x, self.y, oy)
        w, h = self.sprite.get_size()
        surf.blit(self.sprite, (sx - w // 2, sy - h // 2))

    # Retorna o rect de colisão em coordenadas
    def get_rect(self):
        h = sprSize / 2.0
        return pygame.Rect(self.x - h, self.y - h, sprSize, sprSize)

# Spawna o inimigo
def spawn_enemy(sprite):
    side = random.randint(0, 3)
    rW = random.uniform(0, mapWidth)
    rH = random.uniform(0, mapHeight)
    coords = [(rW, 0), (rW, mapHeight), (0, rH), (mapWidth, rH)]
    x, y = coords[side]
    return Enemy(x, y, sprite)


# ---------- Telas do jogo

# Exibe o menu e retorna o próximo estado
def screen_menu(display, clock, playerSpr, fontBig, fontMed, sndStart):

    # Escala o sprite em +3×
    bigSpr = pygame.transform.scale(
        playerSpr, (sprSize * scale * 3, sprSize * scale * 3)
    )  # 144×144 px na tela

    btnW, btnH = 160, 56
    btn = pygame.Rect(winW // 2 + 40, winH // 2 - btnH // 2, btnW, btnH)

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        hov = btn.collidepoint(mx, my)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and hov:
                sndStart.play()  # toca o som de início ao clicar em JOGAR
                return stateGame

        display.fill(cUi)

        title = fontBig.render('PIXEL SHOOTER', False, cTitle)
        display.blit(title, (winW // 2 - title.get_width() // 2, 90))

        sprX = winW // 2 - bigSpr.get_width() - 60
        sprY = winH // 2 - bigSpr.get_height() // 2
        display.blit(bigSpr, (sprX, sprY))

        draw_button(display, btn, 'JOGAR', fontMed, hov)
        pygame.display.flip()

# Loop principal de jogo. Retorna (próximo_estado, pontuação_final)
def screen_game(display, clock, playerSpr, enemySpr, fontMed, sndLaser, sndGameover):
    player  = Player(playerSpr)
    enemies = []
    score   = 0

    spawnTimer    = 0.0
    spawnInterval = spawnStart

    while True:
        dt = clock.tick(60) / 1000.0

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        prevBulletCount = len(player.bullets)  # registra quantidade de projéteis antes do update
        player.update(dt, keys)
        if len(player.bullets) > prevBulletCount:  # novo projétil foi criado
            sndLaser.play()

        for b in player.bullets:
            b.update(dt)
        player.bullets = [b for b in player.bullets if b.alive]

        # Aumenta a frequência de spawn a cada inimigo gerado
        spawnTimer += dt
        if spawnTimer >= spawnInterval:
            spawnTimer = 0.0
            enemies.append(spawn_enemy(enemySpr))
            spawnInterval = max(spawnMin, spawnInterval * spawnDecay)

        # Atualiza inimigos e verifica colisões
        for e in enemies:
            if not e.alive:
                continue
            e.update(dt, player.x, player.y)

            # Verifica acerto no inimigo
            for b in player.bullets:
                if b.alive and b.get_rect().colliderect(e.get_rect()):
                    e.alive = False
                    b.alive = False
                    score += 1
                    break

            # Verifica se o player morreu
            if e.alive and e.get_rect().colliderect(player.get_rect()):
                sndGameover.play()  # toca o som de derrota
                return stateGameover, score

        enemies = [e for e in enemies if e.alive]
        player.bullets = [b for b in player.bullets if b.alive]

        # ---------- Renderização
        display.fill(cUi)
        pygame.draw.rect(display, cMap, (0, uiH, winW, winH - uiH))
        pygame.draw.rect(display, cMapEdge, (0, uiH, winW, winH - uiH), 3)

        for b in player.bullets:
            b.draw(display)
        for e in enemies:
            e.draw(display)
        player.draw(display)

        scoreTxt = fontMed.render(f'PONTUAÇÃO: {score}', False, cGold)
        display.blit(scoreTxt, (winW // 2 - scoreTxt.get_width() // 2, 12))

        pygame.display.flip()

# Tela de game over com pontuação e botão de reinício. Retorna o próximo estado
def screen_gameover(display, clock, score, fontBig, fontMed, sndStart):
    btnW, btnH = 210, 56
    btn = pygame.Rect(winW // 2 - btnW // 2, winH // 2 + 60, btnW, btnH)

    while True:
        clock.tick(60)
        mx, my = pygame.mouse.get_pos()
        hov = btn.collidepoint(mx, my)

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and hov:
                sndStart.play()  # toca o som de início ao clicar recomeçar
                return stateMenu

        display.fill(cUi)

        goTxt = fontBig.render('FIM DE JOGO', False, cGameover)
        display.blit(goTxt, (winW // 2 - goTxt.get_width() // 2, winH // 2 - 100))

        scTxt = fontMed.render(f'PONTUACAO: {score}', False, cGold)
        display.blit(scTxt, (winW // 2 - scTxt.get_width() // 2, winH // 2 - 10))

        draw_button(display, btn, 'RECOMECAR', fontMed, hov)
        pygame.display.flip()


# ---------- Inicialização e máquina de estados

# Inicializa o pygame e executa a máquina de estados do jogo
def main():
    pygame.init()
    display = pygame.display.set_mode((winW, winH))
    pygame.display.set_caption('Pixel Shooter')
    clock = pygame.time.Clock()

    fontBig = pygame.font.Font(None, 52)
    fontMed = pygame.font.Font(None, 34)

    playerSpr = load_sprite('player.png', scale)
    enemySpr  = load_sprite('enemy01.png', scale)

    # Carrega efeitos sonoros
    sndStart    = load_sound('sound-start.mp3')
    sndLaser    = load_sound('sound-laser.mp3')
    sndGameover = load_sound('sound-game-over.mp3')

    state = stateMenu
    score = 0

    while True:
        if state == stateMenu:
            state = screen_menu(display, clock, playerSpr, fontBig, fontMed, sndStart)
        elif state == stateGame:
            state, score = screen_game(display, clock, playerSpr, enemySpr, fontMed, sndLaser, sndGameover)
        elif state == stateGameover:
            state = screen_gameover(display, clock, score, fontBig, fontMed, sndStart)


if __name__ == '__main__':
    main()
