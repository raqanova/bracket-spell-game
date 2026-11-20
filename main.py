import random
import pygame
from stack import Stack

PAIRS = {"(": ")", "[": "]", "{": "}", "<":">"}
KEYS = {pygame.K_v: ">", pygame.K_b: ")", pygame.K_n: "]", pygame.K_m: "}"}
CAPACITY = 8
WIN_LEVEL = 5

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BABY_PINK = (255, 182, 193)
PINK = (255, 16, 240)
GREEN = (57, 255, 20)
RED = (255, 0, 0)

pygame.init()
screen = pygame.display.set_mode((1020, 500))
pygame.display.set_caption("Хаалтын шившлэг")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)
big = pygame.font.SysFont("arial", 120)
big_result = pygame.font.SysFont(None, 125)
menu_title_font_size = pygame.font.SysFont("arial", 90, bold=True)

def new_enemy():
    global spell, last_cast
    spell = Stack(CAPACITY)
    for _ in range(2 + level):
        spell.push(random.choice("<([{"))
    last_cast = pygame.time.get_ticks()

def cast_delay():
    return 3500 - level*300

def enemy_cast():
    global lives, message, msg_color, state, last_cast
    last_cast = pygame.time.get_ticks()
    if spell.is_full():
        lives -= 1
        message = "Шившлэг дэлбэрлээ! -1 амь"
        msg_color = RED
        if lives == 0:
            state = "lost"
        else:
            new_enemy()
    else:
        spell.push(random.choice("<({["))
        message = "Дайсан шинэ хаалт нэмлээ!"
        msg_color = PINK
    print(spell)

def new_game():
    global level, lives, message, msg_color, state, score
    level = 1
    lives = 3
    score = 0
    message = "Хамгийн сүүлд нээгдсэн хаалтыг эхэлж хаа!"
    msg_color = WHITE
    state = "playing"
    new_enemy()

def press(input):
    global level, lives, message, msg_color, state, score
    if PAIRS[spell.peek()] == input:
        spell.pop()
        score += 5
        message = "+5 оноо нэмэгдлээ!"
        msg_color = GREEN
        if spell.is_empty():
            if level == WIN_LEVEL:
                state = "won"
                message = "Бүх дайсныг яллаа!"
            else:
                level += 1
                new_enemy()
                message = "Дараагийн үе рүү орлоо!"
    else:
        lives -= 1
        score -= 4
        msg_color = RED
        message = "Буруу! " + PAIRS[spell.peek()] + " дарах ёстой байлаа! -4 оноо хасагдлаа!"
        if lives == 0:
            state = "lost"
    print(spell)

def draw_menu():
    screen.fill(BLACK)
    screen.blit(menu_title_font_size.render("ХААЛТЫН ШИВШЛЭГ", True, PINK), (90, 60))
    screen.blit(font.render("Дайсан < ( [ { хаалтаар шившлэг хийнэ.", True, WHITE), (90, 190))
    screen.blit(font.render("Хамгийн сүүлийн хаалтыг эхэлж хаа:  > ) ] }  эсвэл  v b n m", True, WHITE), (90, 230))
    screen.blit(font.render("Дайсан тогтмол шинэ хаалт нэмнэ. 8 болбол дэлбэрнэ!", True, WHITE), (90, 270))
    screen.blit(font.render("5 дайсныг ял. Амь: 3", True, WHITE), (90, 310))
    screen.blit(font.render("SPACE - эхлэх", True, GREEN), (90, 390))
    pygame.display.flip()

def draw():
    if state == "menu":
        draw_menu()
        return
    screen.fill(BLACK)
    screen.blit(font.render(f"Түвшин {level} / {WIN_LEVEL}      Амь: {lives}      Оноо: {score}", True, WHITE), (60, 30))

    items = spell.items()
    x = 60
    for i, ch in enumerate(items if state == "playing" else []):
        color = PINK if i == len(items) - 1 else WHITE
        screen.blit(big.render(ch, True, color), (x, 100))
        x += 60

    if state == "playing":
        left = 1 - (pygame.time.get_ticks() - last_cast) / cast_delay()
        pygame.draw.rect(screen, PINK, (60, 285, int(600 * left), 8))

    screen.blit(font.render("Дарах:  >  )  ]  }     эсвэл  v  b  n  m", True, BABY_PINK), (60, 350))
    screen.blit(font.render(message, True, msg_color), (60, 400))

    screen.blit(font.render("Stack", True, WHITE), (865, 30))
    for i in range(CAPACITY):
        box = pygame.Rect(820, 410-i*48, 140, 40)
        if i < len(items):
            pygame.draw.rect(screen, PINK if i == len(items) - 1 else BABY_PINK, box)
            screen.blit(font.render(items[i], True, BLACK), (box.x + 65, box.y + 10))
        else:
            pygame.draw.rect(screen, BABY_PINK, box, 1)

    if state != "playing":
        screen.blit(big_result.render("БАЯР ХҮРГЭЕ!" if state == "won" else "ТА ЯЛАГДЛАА!", True, GREEN if state == "won" else RED), (60, 120))
        screen.blit(font.render(f"Таны оноо: {score}", True, WHITE), (60, 260))
        screen.blit(font.render("R - дахин тоглох", True, WHITE), (60, 290))

    pygame.display.flip()

new_game()
state = "menu"
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r or (state == "menu" and event.key == pygame.K_SPACE):
                new_game()
            elif state == "playing":
                input = event.unicode if event.unicode in (">", ")", "}", "]") else KEYS.get(event.key)
                if input:
                    press(input)
    if state == "playing" and pygame.time.get_ticks() - last_cast > cast_delay():
        enemy_cast()
    draw()
    clock.tick(60)
pygame.quit()