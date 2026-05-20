# Pixel Shooter

![Splash Art](assets/splash-art.png)

Jogo de tiro 2D em pixel art desenvolvido com Python e Pygame. O jogador enfrenta ondas de inimigos que surgem pelas bordas do mapa e precisam ser eliminados antes de alcançá-lo. A dificuldade aumenta progressivamente conforme o tempo passa.

---

## Especificações Técnicas

| Item | Valor |
|---|---|
| Linguagem | Python 3 |
| Biblioteca | Pygame |
| Resolução | 1200 × 650 px |
| Tamanho do mapa | 200 × 100 unidades (escala 6×) |
| Tamanho dos sprites | 8 × 8 px (48 × 48 na tela) |
| FPS alvo | 60 |

### Parâmetros de jogo

| Parâmetro | Valor |
|---|---|
| Velocidade do jogador | 60 unidades/s |
| Velocidade do projétil | 220 unidades/s |
| Cooldown de disparo | 0,5 s |
| Velocidade dos inimigos | 28 unidades/s |
| Intervalo inicial de spawn | 5,0 s |
| Intervalo mínimo de spawn | 0,8 s |
| Fator de redução do spawn | 0,93× por inimigo |

### Estrutura do projeto

```
implementacao-primeiro-jogo/
├── game.py           # Código-fonte principal
└── assets/
    ├── player.png        # Sprite do jogador
    ├── enemy01.png       # Sprite do inimigo
    ├── splash-art.png    # Arte do jogo
    ├── sound-start.mp3   # Som de início de partida
    ├── sound-laser.mp3   # Som de disparo
    └── sound-game-over.mp3  # Som de fim de jogo
```

---

## Como rodar

### Pré-requisitos

- Python 3.8 ou superior
- pip

### Instalação

```bash
# Clone o repositório
git clone <url-do-repositorio>
cd implementacao-primeiro-jogo

# Instale a dependência
pip install pygame
```

### Executando o jogo

```bash
python game.py
```

---

## Controles

| Tecla | Ação |
|---|---|
| `W` `A` `S` `D` | Mover o jogador |
| `↑` `↓` `←` `→` | Atirar nas 4 direções |

---

## Mecânicas

- **Spawn progressivo** — inimigos surgem pelas bordas do mapa e a frequência de aparecimento aumenta a cada inimigo gerado.
- **Colisão** — um inimigo que tocar o jogador encerra a partida.
- **Pontuação** — cada inimigo eliminado vale 1 ponto.
- **Telas** — Menu → Jogo → Game Over → Menu.
