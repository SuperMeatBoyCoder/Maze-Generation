import random
import pygame

n, m = map(int, input().split())
n = 2 * n - 1
m = 2 * m - 1
grid = [[0] * m for _ in range(n)]
for i in range(n):
    for j in range(m):
        if i % 2 == 1 and j % 2 == 1:
            grid[i][j] = 1

pygame.init()
cell_size = 20
width, height = m * cell_size, n * cell_size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Генерация лабиринта")


def draw_grid():
    screen.fill((255, 255, 255))
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                color = (0, 0, 0)
                if j == 0 or grid[i][j-1] == 1:
                    pygame.draw.rect(screen, color, (j * cell_size, i * cell_size + cell_size // 2, cell_size // 2, 2))
                if j == m - 1 or grid[i][j+1] == 1:
                    pygame.draw.rect(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2, cell_size // 2, 2))
                if i == 0 or grid[i-1][j] == 1:
                    pygame.draw.rect(screen, color, (j * cell_size + cell_size // 2, i * cell_size, 2, cell_size // 2))
                if i == n - 1 or grid[i+1][j] == 1:
                    pygame.draw.rect(screen, color, (j * cell_size + cell_size // 2, i * cell_size + cell_size // 2, 2, cell_size // 2))
    pygame.display.flip()


blocks = []
blocks.append((0, n, 0, m))
auto_mode = False
running = True
draw_grid()

while blocks and running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                auto_mode = True
            elif event.key == pygame.K_SPACE:
                auto_mode = False

    if auto_mode or not blocks:
        pygame.time.delay(100)
    else:
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting = False
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_RETURN:
                        auto_mode = True
                        waiting = False

    if not running:
        break
    best = 0
    for i in range(len(blocks)):
        if (blocks[best][1] - blocks[best][0]) * (blocks[best][3] - blocks[best][2]) < (blocks[i][1] - blocks[i][0]) * (blocks[i][3] - blocks[i][2]):
            best = i
    i1, i2, j1, j2 = blocks[best]
    blocks.pop(best)
    w = i2 - i1 + 1
    h = j2 - j1 + 1
    if random.random() < w / (w + h):
        p = random.choice(list(range(i1 + 1, i2, 2)))
        e = random.choice(list(range(j1, j2 + 1, 2)))
        for j in range(j1, j2 + 1, 2):
            grid[p][j] = 1
        grid[p][e] = 0
        if p - 1 - i1 > 1:
            blocks.append((i1, p - 1, j1, j2))
        if i2 - (p + 1) > 1:
            blocks.append((p + 1, i2, j1, j2))
    else:
        p = random.choice(list(range(j1 + 1, j2, 2)))
        e = random.choice(list(range(i1, i2 + 1, 2)))
        for i in range(i1, i2 + 1, 2):
            grid[i][p] = 1
        grid[e][p] = 0
        if p - 1 - j1 > 1:
            blocks.append((i1, i2, j1, p - 1))
        if j2 - (p + 1) > 1:
            blocks.append((i1, i2, p + 1, j2))

    draw_grid()

pygame.time.delay(10000)
pygame.quit()
