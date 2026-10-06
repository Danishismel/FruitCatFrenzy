import random
import pygame

# start pygame
pygame.init()

# audio safe mode so no crash if no speaker
audio_enabled = False
meow_sound = None
bomb_sound = None
miss_sound = None
gameover_sound = None

try:
    pygame.mixer.init()
    meow_sound = pygame.mixer.Sound("assets/meow.wav")
    bomb_sound = pygame.mixer.Sound("assets/bomb.wav")
    miss_sound = pygame.mixer.Sound("assets/miss.wav")
    gameover_sound = pygame.mixer.Sound("assets/gameover.wav")
    audio_enabled = True
except pygame.error:
    audio_enabled = False


def play_sound(sound):
    # play sound only if got speaker
    if audio_enabled and sound is not None:
        sound.play()


# screen size 600 by 900
WIDTH = 600
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fruit Cat Frenzy")

clock = pygame.time.Clock()
FPS = 60

# fonts for text
font = pygame.font.SysFont("arial", 36, bold=True)
small_font = pygame.font.SysFont("arial", 25)
big_font = pygame.font.SysFont("arial", 60, bold=True)
title_font = pygame.font.SysFont("arial", 70, bold=True)

# colour list
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PASTEL_YELLOW = (255, 244, 180)
PASTEL_PINK = (255, 190, 210)
PASTEL_GREEN = (190, 235, 190)
PASTEL_BLUE = (190, 220, 245)
PASTEL_PURPLE = (215, 190, 240)
GREEN = (50, 180, 80)
RED = (220, 60, 80)
PURPLE = (130, 80, 180)
BROWN = (100, 70, 40)

# dual language text list
current_lang = "EN"

TEXTS = {
    "EN": {
        "start": "START GAME",
        "instructions": "INSTRUCTIONS",
        "exit": "EXIT",
        "lang_btn": "Language: EN",
        "how_to_play": "HOW TO PLAY",
        "back": "BACK",
        "score": "Score: ",
        "lives": "Lives: ",
        "level": "Lv ",
        "level_msg": "LEVEL ",
        "paused": "PAUSED",
        "game_over": "GAME OVER",
        "final_score": "Final Score: ",
        "level_reached": "Level Reached: ",
        "restart": "Press R to Restart",
        "quit": "Press Q to Quit",
        "instructions_list": [
            "LEFT / RIGHT - Move basket",
            "Catch fruits to score points",
            "Avoid the bombs!",
            "Missed fruit = -1 life",
            "Bomb = -1 life",
            "P - Pause",
            "R - Restart after Game Over",
            "You have 60 seconds!",
            "",
            "Fruit Scores:",
            "Watermelon: +10",
            "Pineapple: +10",
            "Grape: +15",
            "Strawberry: +20",
        ],
    },
    "BM": {
        "start": "MULA GAME",
        "instructions": "PANDUAN",
        "exit": "KELUAR",
        "lang_btn": "Bahasa: BM",
        "how_to_play": "CARA MAIN",
        "back": "KEMBALI",
        "score": "Markah: ",
        "lives": "Nyawa: ",
        "level": "Tahap ",
        "level_msg": "TAHAP ",
        "paused": "JEDA",
        "game_over": "TAMAT GAME",
        "final_score": "Markah Akhir: ",
        "level_reached": "Tahap Dicapai: ",
        "restart": "Tekan R untuk Mula Semula",
        "quit": "Tekan Q untuk Keluar",
        "instructions_list": [
            "KIRI / KANAN - Gerak bakul",
            "Tangkap buah untuk kumpul markah",
            "Elakkan bom!",
            "Terlepas buah = -1 nyawa",
            "Kena bom = -1 nyawa",
            "P - Jeda (Pause)",
            "R - Mula semula lepas Tamat Game",
            "Masa bermain 60 saat!",
            "",
            "Markah Buah:",
            "Tembikai: +10",
            "Nanas: +10",
            "Anggur: +15",
            "Stroberi: +20",
        ],
    },
}

# load background pic
background = pygame.image.load("assets/background.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))


# basket player
class Player:

    def __init__(self):
        self.image = pygame.image.load("assets/basket.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (220, 150))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 40
        self.speed = 8

    def update(self):
        # press arrow key to move left right
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # block basket from going off screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self):
        screen.blit(self.image, self.rect)


# falling fruit and bomb
class Item:

    def __init__(self, item_type, speed):
        self.item_type = item_type
        self.is_bomb = item_type == "bomb"
        self.image_path = f"assets/{item_type}.png"
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 80))
        self.rect = self.image.get_rect()
        # drop from random x at top
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        screen.blit(self.image, self.rect)


# floating points text when catch or hit bomb
class ScoreFeedback:

    def __init__(self, text, x, y, colour):
        self.text = text
        self.x = x
        self.y = y
        self.colour = colour
        self.alpha = 255
        self.timer = 0

    def update(self):
        # float up slowly then fade out
        self.y -= 2
        self.timer += 1
        if self.timer > 30:
            self.alpha -= 8

    def draw(self):
        if self.alpha > 0:
            text_surface = small_font.render(self.text, True, self.colour)
            text_surface.set_alpha(self.alpha)
            screen.blit(
                text_surface, (self.x - text_surface.get_width() // 2, self.y)
            )

    def is_finished(self):
        return self.alpha <= 0


# pop up text when change level
class LevelMessage:

    def __init__(self, level):
        prefix = TEXTS[current_lang]["level_msg"]
        self.text = f"{prefix}{level}!"
        self.timer = 120

    def update(self):
        if self.timer > 0:
            self.timer -= 1

    def draw(self):
        if self.timer > 0:
            text_surface = big_font.render(self.text, True, PURPLE)
            screen.blit(
                text_surface,
                (
                    WIDTH // 2 - text_surface.get_width() // 2,
                    HEIGHT // 2 - 100,
                ),
            )


# 3 2 1 go count down before start
class Countdown:

    def __init__(self):
        self.count = 3
        self.finished = False
        self.start_time = pygame.time.get_ticks()

    def update(self):
        elapsed = pygame.time.get_ticks() - self.start_time
        if elapsed >= 4000:
            self.finished = True
        elif elapsed >= 3000:
            self.count = 0
        elif elapsed >= 2000:
            self.count = 1
        elif elapsed >= 1000:
            self.count = 2

    def draw(self):
        if self.finished:
            return
        text = str(self.count) if self.count > 0 else "GO!"
        text_surface = big_font.render(text, True, PURPLE)
        screen.blit(
            text_surface,
            (
                WIDTH // 2 - text_surface.get_width() // 2,
                HEIGHT // 2 - text_surface.get_height() // 2,
            ),
        )


ITEM_TYPES = ["watermelon", "pineapple", "grape", "strawberry", "bomb"]


# reset everything to default state
def reset_game():
    return (
        Player(),
        [],
        [],
        None,
        [],
        0,
        5,
        0,
        60,
        1,
        pygame.time.get_ticks(),
        Countdown(),
    )


# show caught fruits piling inside basket
def draw_caught_fruits(caught_fruits, player):
    positions = [
        (-70, -45),
        (-25, -55),
        (20, -50),
        (65, -40),
        (-50, -20),
        (0, -25),
        (45, -20),
        (80, -10),
    ]

    for i, fruit_path in enumerate(caught_fruits[:8]):
        fruit_image = pygame.image.load(fruit_path).convert_alpha()
        fruit_image = pygame.transform.scale(fruit_image, (45, 38))
        x_offset, y_offset = positions[i]
        fruit_x = player.rect.centerx + x_offset - fruit_image.get_width() // 2
        fruit_y = player.rect.bottom + y_offset - fruit_image.get_height()
        screen.blit(fruit_image, (fruit_x, fruit_y))


# draw top hud boxes
def draw_hud(score, lives, time_left, level):
    t = TEXTS[current_lang]

    # score box
    score_box = pygame.Rect(20, 100, 160, 55)
    pygame.draw.rect(screen, PASTEL_YELLOW, score_box, border_radius=15)
    score_text = font.render(f"{t['score']}{score}", True, GREEN)
    screen.blit(
        score_text,
        (
            score_box.centerx - score_text.get_width() // 2,
            score_box.centery - score_text.get_height() // 2,
        ),
    )

    # lives box
    lives_box = pygame.Rect(190, 100, 150, 55)
    pygame.draw.rect(screen, PASTEL_YELLOW, lives_box, border_radius=15)
    lives_text = font.render(f"{t['lives']}{lives}", True, RED)
    screen.blit(
        lives_text,
        (
            lives_box.centerx - lives_text.get_width() // 2,
            lives_box.centery - lives_text.get_height() // 2,
        ),
    )

    # time box
    time_box = pygame.Rect(350, 100, 110, 55)
    pygame.draw.rect(screen, PASTEL_YELLOW, time_box, border_radius=15)
    time_text = font.render(f"{time_left}", True, BROWN)
    screen.blit(
        time_text,
        (
            time_box.centerx - time_text.get_width() // 2,
            time_box.centery - time_text.get_height() // 2,
        ),
    )

    # level box
    level_box = pygame.Rect(470, 100, 110, 55)
    pygame.draw.rect(screen, PASTEL_YELLOW, level_box, border_radius=15)
    level_text = font.render(f"{t['level']}{level}", True, PURPLE)
    screen.blit(
        level_text,
        (
            level_box.centerx - level_text.get_width() // 2,
            level_box.centery - level_text.get_height() // 2,
        ),
    )


# draw colourful rainbow game title
def draw_title():
    title_text = "FRUIT CAT FRENZY"
    colours = [
        (255, 100, 130),
        (255, 170, 80),
        (255, 210, 70),
        (100, 190, 120),
        (100, 170, 230),
        (160, 120, 220),
    ]

    total_width = 0
    letter_surfaces = []

    for i, letter in enumerate(title_text):
        colour = colours[i % len(colours)]
        surface = title_font.render(letter, True, colour)
        letter_surfaces.append(surface)
        total_width += surface.get_width()

    x = WIDTH // 2 - total_width // 2
    for surface in letter_surfaces:
        screen.blit(surface, (x, 30))
        x += surface.get_width()


# draw rounded pastel button
def draw_button(text, rect, colour):
    pygame.draw.rect(screen, colour, rect, border_radius=20)
    button_text = font.render(text, True, BROWN)
    screen.blit(
        button_text,
        (
            rect.centerx - button_text.get_width() // 2,
            rect.centery - button_text.get_height() // 2,
        ),
    )


# main menu screen
def menu_screen():
    global current_lang

    start_button = pygame.Rect(150, 270, 300, 75)
    instructions_button = pygame.Rect(150, 365, 300, 75)
    exit_button = pygame.Rect(150, 460, 300, 75)
    lang_button = pygame.Rect(175, 560, 250, 60)

    while True:
        screen.blit(background, (0, 0))
        draw_title()

        t = TEXTS[current_lang]
        draw_button(t["start"], start_button, PASTEL_GREEN)
        draw_button(t["instructions"], instructions_button, PASTEL_BLUE)
        draw_button(t["exit"], exit_button, PASTEL_PINK)
        draw_button(t["lang_btn"], lang_button, PASTEL_PURPLE)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return "start"
                if instructions_button.collidepoint(event.pos):
                    return "instructions"
                if exit_button.collidepoint(event.pos):
                    return "exit"
                if lang_button.collidepoint(event.pos):
                    # flip language between EN and BM
                    current_lang = "BM" if current_lang == "EN" else "EN"

        clock.tick(FPS)


# instruction how to play screen
def instructions_screen():
    panel = pygame.Rect(50, 140, 500, 615)
    back_button = pygame.Rect(180, 770, 240, 60)

    while True:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, PASTEL_YELLOW, panel, border_radius=25)

        t = TEXTS[current_lang]
        title = font.render(t["how_to_play"], True, BROWN)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 160))

        y = 225
        for line in t["instructions_list"]:
            text = small_font.render(line, True, BROWN)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, y))
            y += 33

        draw_button(t["back"], back_button, PASTEL_PINK)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "exit"
            if (
                event.type == pygame.MOUSEBUTTONDOWN
                and back_button.collidepoint(event.pos)
            ):
                return "back"

        clock.tick(FPS)


# game over screen
def game_over_screen(score, level):
    play_sound(gameover_sound)
    t = TEXTS[current_lang]
    panel = pygame.Rect(70, 250, 460, 400)

    while True:
        screen.blit(background, (0, 0))
        pygame.draw.rect(screen, PASTEL_YELLOW, panel, border_radius=30)

        game_over_text = big_font.render(t["game_over"], True, RED)
        screen.blit(
            game_over_text,
            (WIDTH // 2 - game_over_text.get_width() // 2, 300),
        )

        score_text = font.render(f"{t['final_score']}{score}", True, GREEN)
        screen.blit(
            score_text,
            (WIDTH // 2 - score_text.get_width() // 2, 390),
        )

        level_text = font.render(
            f"{t['level_reached']}{level}", True, PURPLE
        )
        screen.blit(
            level_text,
            (WIDTH // 2 - level_text.get_width() // 2, 440),
        )

        restart_text = small_font.render(t["restart"], True, BROWN)
        screen.blit(
            restart_text,
            (WIDTH // 2 - restart_text.get_width() // 2, 510),
        )

        quit_text = small_font.render(t["quit"], True, BROWN)
        screen.blit(
            quit_text,
            (WIDTH // 2 - quit_text.get_width() // 2, 550),
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return "restart"
                if event.key == pygame.K_q:
                    return "quit"

        clock.tick(FPS)


# gameplay loop
def play_game():
    (
        player,
        items,
        feedbacks,
        level_message,
        caught_fruits,
        score,
        lives,
        spawn_timer,
        time_left,
        level,
        start_time,
        countdown,
    ) = reset_game()

    paused = False
    running = True

    while running:
        t = TEXTS[current_lang]

        # check keyboard and quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "quit"
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_p
                and countdown.finished
            ):
                paused = not paused

        # run 3 2 1 countdown first
        if not countdown.finished:
            countdown.update()
            screen.blit(background, (0, 0))
            draw_title()
            draw_hud(score, lives, 60, level)
            player.draw()
            draw_caught_fruits(caught_fruits, player)
            countdown.draw()
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # pause screen
        if paused:
            screen.blit(background, (0, 0))
            draw_title()
            draw_hud(score, lives, time_left, level)
            for item in items:
                item.draw()
            player.draw()
            draw_caught_fruits(caught_fruits, player)

            pause_text = big_font.render(t["paused"], True, PURPLE)
            screen.blit(
                pause_text,
                (
                    WIDTH // 2 - pause_text.get_width() // 2,
                    HEIGHT // 2,
                ),
            )
            pygame.display.flip()
            clock.tick(FPS)
            continue

        # count down 60 seconds
        elapsed_seconds = (
            pygame.time.get_ticks() - start_time - 4000
        ) // 1000
        time_left = max(0, 60 - elapsed_seconds)

        # change speed and spawn rate by level
        previous_level = level
        if time_left > 40:
            level = 1
            item_speed_min, item_speed_max, spawn_delay = 3, 6, 45
        elif time_left > 20:
            level = 2
            item_speed_min, item_speed_max, spawn_delay = 4, 7, 40
        else:
            level = 3
            item_speed_min, item_speed_max, spawn_delay = 5, 9, 35

        # show banner when enter new level
        if level != previous_level:
            level_message = LevelMessage(level)

        # move player
        player.update()

        # drop new item when timer hit delay
        spawn_timer += 1
        if spawn_timer >= spawn_delay:
            spawn_timer = 0
            item_type = random.choice(ITEM_TYPES)
            speed = random.randint(item_speed_min, item_speed_max)
            items.append(Item(item_type, speed))

        # update falling items
        for item in items[:]:
            item.update()

            # check catch with basket
            if player.rect.colliderect(item.rect):
                if item.is_bomb:
                    lives -= 1
                    play_sound(bomb_sound)
                    fb_text = "-1 LIFE" if current_lang == "EN" else "-1 NYAWA"
                    feedbacks.append(
                        ScoreFeedback(
                            fb_text, item.rect.centerx, item.rect.y, RED
                        )
                    )
                else:
                    # points value for fruits
                    pts = 10
                    if item.item_type == "grape":
                        pts = 15
                    elif item.item_type == "strawberry":
                        pts = 20

                    score += pts
                    play_sound(meow_sound)
                    caught_fruits.append(item.image_path)
                    feedbacks.append(
                        ScoreFeedback(
                            f"+{pts}", item.rect.centerx, item.rect.y, GREEN
                        )
                    )
                items.remove(item)

            # fruit hit floor lose life
            elif item.rect.top > HEIGHT:
                if not item.is_bomb:
                    lives -= 1
                    play_sound(miss_sound)
                items.remove(item)

        # update floating points text
        for feedback in feedbacks[:]:
            feedback.update()
            if feedback.is_finished():
                feedbacks.remove(feedback)

        # update level pop up text
        if level_message:
            level_message.update()
            if level_message.timer <= 0:
                level_message = None

        # draw game elements
        screen.blit(background, (0, 0))
        draw_title()
        draw_hud(score, lives, time_left, level)

        for item in items:
            item.draw()

        player.draw()
        draw_caught_fruits(caught_fruits, player)

        for feedback in feedbacks:
            feedback.draw()

        if level_message:
            level_message.draw()

        pygame.display.flip()

        # check if die or time out
        if lives <= 0 or time_left <= 0:
            result = game_over_screen(score, level)
            return result

        clock.tick(FPS)


# main program loop
def main():
    while True:
        menu_result = menu_screen()
        if menu_result == "exit":
            break

        if menu_result == "instructions":
            if instructions_screen() == "exit":
                break

        elif menu_result == "start":
            while True:
                if play_game() != "restart":
                    break

    pygame.quit()


# start game
if __name__ == "__main__":
    main()