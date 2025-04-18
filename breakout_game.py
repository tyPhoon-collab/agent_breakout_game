import random
import sys

import pygame

# 初期化
pygame.init()

# 画面設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩し")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
COLORS = [RED, BLUE, GREEN, YELLOW]

# ゲーム速度
clock = pygame.time.Clock()
FPS = 60

# パドルの設定
paddle_width = 100
paddle_height = 15
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 30
paddle_speed = 10

# ボールの設定
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5 * random.choice([-1, 1])
ball_dy = -5

# ブロックの設定
block_width = 80
block_height = 30
block_rows = 4
block_cols = 8
block_gap = 5
blocks = []


# ブロック初期化
def init_blocks():
    blocks.clear()
    for i in range(block_rows):
        for j in range(block_cols):
            x = j * (block_width + block_gap) + block_gap
            y = i * (block_height + block_gap) + block_gap + 50
            color = COLORS[i % len(COLORS)]
            blocks.append([x, y, color])


# ゲームオーバー表示
def show_game_over():
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over!", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 30)
    restart_text = font.render("Press R to restart or ESC to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()


# クリア表示
def show_clear():
    font = pygame.font.Font(None, 50)
    text = font.render("Stage Clear!", True, GREEN)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 30)
    restart_text = font.render("Press R to restart or ESC to quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()


# スコア表示
def show_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


# ゲームの初期化
def restart_game():
    global paddle_x, paddle_y, ball_x, ball_y, ball_dx, ball_dy, game_over, cleared
    paddle_x = (WIDTH - paddle_width) // 2
    paddle_y = HEIGHT - 30
    ball_x = WIDTH // 2
    ball_y = HEIGHT // 2
    ball_dx = 5 * random.choice([-1, 1])
    ball_dy = -5
    init_blocks()
    game_over = False
    cleared = False


# ゲームの初期状態
init_blocks()
game_over = False
cleared = False
score = 0

# メインゲームループ
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            elif event.key == pygame.K_r and (game_over or cleared):
                restart_game()
                score = 0

    if not game_over and not cleared:
        # キー操作
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # ボールの移動
        ball_x += ball_dx
        ball_y += ball_dy

        # 壁との衝突
        if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
            ball_dx = -ball_dx
        if ball_y <= ball_radius:
            ball_dy = -ball_dy

        # パドルとの衝突
        if (
            ball_y + ball_radius >= paddle_y
            and ball_y <= paddle_y + paddle_height
            and ball_x >= paddle_x
            and ball_x <= paddle_x + paddle_width
        ):
            # パドルのどの位置に当たったかによって反射角を変える
            relative_x = (ball_x - paddle_x) / paddle_width
            angle = relative_x * 2 - 1  # -1 から 1 の範囲
            ball_dx = 5 * angle
            ball_dy = -abs(ball_dy)  # 必ず上向きに

        # ブロックとの衝突検出
        for block in blocks[:]:
            block_x, block_y, block_color = block
            if (
                ball_x + ball_radius > block_x
                and ball_x - ball_radius < block_x + block_width
                and ball_y + ball_radius > block_y
                and ball_y - ball_radius < block_y + block_height
            ):
                blocks.remove(block)
                ball_dy = -ball_dy
                score += 10
                break

        # ゲームオーバー判定
        if ball_y >= HEIGHT:
            game_over = True

        # クリア判定
        if len(blocks) == 0:
            cleared = True

    # 画面描画
    screen.fill(BLACK)

    if game_over:
        show_game_over()
    elif cleared:
        show_clear()
    else:
        # パドルの描画
        pygame.draw.rect(
            screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height)
        )

        # ボールの描画
        pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)

        # ブロックの描画
        for block in blocks:
            block_x, block_y, block_color = block
            pygame.draw.rect(
                screen, block_color, (block_x, block_y, block_width, block_height)
            )
            pygame.draw.rect(
                screen, WHITE, (block_x, block_y, block_width, block_height), 1
            )

        # スコアの表示
        show_score(score)

        pygame.display.flip()

    clock.tick(FPS)
