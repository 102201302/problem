from pickle import REDUCE

import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH, HEIGHT = 600, 645
TILE_SIZE = 100
ROWS, COLS = 6, 6
FPS = 30
MAX_TIME = 20  # 游戏最大时间（秒）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (200, 200, 200)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("铁了个铁小游戏")

# 字体设置
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 74)

# 加载图案图片
patterns = [pygame.image.load(f"pattern_{i}.png") for i in range(1, 7)]
patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in patterns]

# 创建游戏板
board = [[random.choice(patterns) for _ in range(COLS)] for _ in range(ROWS)]
selected = []

# 记录游戏开始时间
start_time = 0

# 加载界面图片
start_screen_img = pygame.image.load("start_screen.png")
start_screen_img = pygame.transform.scale(start_screen_img, (WIDTH, HEIGHT))
game_over_screen_img = pygame.image.load("game_over_screen.png")
game_over_screen_img = pygame.transform.scale(game_over_screen_img, (WIDTH, HEIGHT))

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

def draw_timer(time_left):
    timer_text = font.render(f"Time Left: {int(time_left):02d}", True, BLACK)
    timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT - timer_text.get_height() - 10))
    screen.blit(timer_text, timer_rect)

def draw_button(text, x, y, width, height, inactive_color, active_color, font_size=36):
    """绘制按钮"""
    font = pygame.font.Font(None, font_size)
    text_img = font.render(text, True, WHITE)
    text_rect = text_img.get_rect(center=(x + width // 2, y + height // 2))
    pygame.draw.rect(screen, inactive_color, (x, y, width, height), 2)
    screen.blit(text_img, text_rect)
    # 检查鼠标是否在按钮上
    mouse_pos = pygame.mouse.get_pos()
    if x <= mouse_pos[0] <= x + width and y <= mouse_pos[1] <= y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height), 2)

def start_screen():
    screen.blit(start_screen_img, (0, 0))  # 渲染开始界面图片
    # 绘制开始游戏按钮
    button_x, button_y = WIDTH // 4, HEIGHT // 2 - 50
    button_width, button_height = WIDTH // 2, 100
    # 增大按钮文本的字号
    draw_button("Start", button_x, button_y, button_width, button_height, BLACK, (0, 100, 0), font_size=72)
    pygame.display.flip()

    # 等待按钮点击
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 检查鼠标点击是否在按钮区域内
                if button_x <= event.pos[0] <= button_x + button_width and button_y <= event.pos[
                    1] <= button_y + button_height:
                    return  # 返回，结束start_screen函数

def game_over_screen(score=0):
    screen.blit(game_over_screen_img, (0, 0))  # 渲染结束界面图片
    # 使用game_over_font来渲染分数，以增大字号
    score_text = game_over_font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # 假设位置在屏幕中心
    screen.blit(score_text, score_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def check_match():
    global score  # 声明全局变量score
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if board[r1][c1] == board[r2][c2]:
            board[r1][c1] = None
            board[r2][c2] = None
            score += 10  # 增加分数
        selected.clear()

def main():
    global start_time, score  # 声明全局变量start_time和score
    score = 0  # 初始化分数为0
    running = True
    clock = pygame.time.Clock()
    # 显示开始画面
    start_screen()
    # 开始游戏
    start_time = pygame.time.get_ticks()  # 重新开始计时
    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000
        time_left = max(MAX_TIME - elapsed_time, 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS and board[row][col] is not None:
                    if (row, col) not in [(s[0], s[1]) for s in selected]:
                        selected.append((row, col))
                    if len(selected) == 2:
                        check_match()
        screen.fill(BG_COLOR)
        draw_board()
        draw_timer(time_left)
        if time_left <= 0:
            running = False
            game_over_screen(score)  # 传递分数到game_over_screen函数
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()