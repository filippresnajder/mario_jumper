import sys
import pygame
from game import Game
from os.path import join

# Initialize pygame
pygame.init()
pygame.display.set_caption("Mario Jumper")

# Window and Frame variables
WIDTH, HEIGHT = 1280, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Initialize game
game = Game(screen)

menu_bg = pygame.transform.scale(pygame.image.load(join("assets", "background.png")), (screen.get_width(), screen.get_height()))


# Render menu screen
def menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    play()

        screen.blit(menu_bg, (0, 0))
        generate_start_menu_text()
        generate_start_menu_actions()

        pygame.display.flip()


# Render the game
def play():
    # Activate the player, game and themes
    game.player.is_alive = True
    game.run = True
    game.generate_map()
    game.day_theme.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    game.restart()

        if game.run:
            game.update()

        if game.player.win:
            generate_win_text()
        elif not game.player.is_alive:
            generate_game_over_text()

        generate_player_data()

        pygame.display.flip()
        clock.tick(FPS)


def generate_start_menu_text():
    font_l = get_mario_font(22)
    font_xl = get_mario_font(24)
    top_text_shadow = font_xl.render("Mario Jumper", False, (0, 0, 0))
    top_text = font_l.render("Mario Jumper", False, (255, 255, 255 ))
    screen.blit(top_text_shadow, (calculate_horizontal_text_center(top_text_shadow), 98))
    screen.blit(top_text, (calculate_horizontal_text_center(top_text), 100))
def generate_start_menu_actions():
    rect_width = 400
    rect_height = 300
    font = get_mario_font(12)
    menu_rect = pygame.Rect(screen.get_width() // 2 - rect_width // 2, screen.get_height() // 2 - rect_height // 2, rect_width, rect_height)
    pygame.draw.rect(screen, (255, 255, 255), menu_rect)
    pygame.draw.rect(screen, (0, 0, 0), menu_rect, 3)
    start_game = font.render("Press UP Arrow to start", False, (0, 0, 0))
    controls = font.render("Controls:", False, (0, 0, 0))
    movement = font.render("WAD - Movement", False, (0, 0, 0))
    sprint = font.render("Space - Sprint", False, (0, 0, 0))
    pipe_enter = font.render("S - Enter Pipe", False, (0, 0, 0))
    shoot = font.render("Q - Shoot", False, (0, 0, 0))
    restart = font.render("R - Restart", False, (0, 0, 0))
    exit_game = font.render("ESC - Exit Game", False, (0, 0, 0))
    screen.blit(start_game, (calculate_horizontal_text_center(start_game), calculate_vertical_text_center(start_game) - 125))
    screen.blit(controls, (calculate_horizontal_text_center(controls), calculate_vertical_text_center(controls) - 90))
    all_controls = [controls, movement, sprint, pipe_enter, shoot, restart, exit_game]
    for i in range(len(all_controls)):
        screen.blit(all_controls[i], (calculate_horizontal_text_center(all_controls[i]), calculate_vertical_text_center(all_controls[i]) - 90 + (i * 30)))
def generate_player_data():
    custom_font = get_mario_font(16)
    custom_font_lg = get_mario_font(18)
    score_shadow = custom_font_lg.render("Score: " + str(game.player.score), False, (0, 0, 0))
    ammo_shadow = custom_font_lg.render("Ammo x " + str(game.player.ammo), False, (0, 0, 0))
    score = custom_font.render("Score: " + str(game.player.score), False, (255, 255, 255))
    ammo = custom_font.render("Ammo x " + str(game.player.ammo), False, (255, 255, 255))
    screen.blit(score_shadow, (40, 20))
    screen.blit(ammo_shadow, (screen.get_width() - ammo.get_width() - 60, 20))
    screen.blit(score, (50, 20))
    screen.blit(ammo, (screen.get_width() - ammo.get_width() - 50, 20))
def generate_win_text():
    custom_font = get_mario_font(16)
    custom_font_lg = get_mario_font(18)
    win_shadow = custom_font_lg.render("You Win", False,  (0, 0, 0))
    win = custom_font.render("You Win", False, (255, 255, 255))
    screen.blit(win_shadow, (calculate_horizontal_text_center(win_shadow), calculate_vertical_text_center(win_shadow)))
    screen.blit(win, (calculate_horizontal_text_center(win), calculate_vertical_text_center(win)))
def generate_game_over_text():
    custom_font = get_mario_font(16)
    custom_font_lg = get_mario_font(18)
    game_over_shadow = custom_font_lg.render("Game Over", False,  (0, 0, 0))
    game_over = custom_font.render("Game Over", False, (255, 255, 255))
    screen.blit(game_over_shadow, (calculate_horizontal_text_center(game_over_shadow), calculate_vertical_text_center(game_over_shadow)))
    screen.blit(game_over, (calculate_horizontal_text_center(game_over), calculate_vertical_text_center(game_over)))
def get_mario_font(size):
    return pygame.font.Font(join("assets", "fonts", "MarioFont.ttf"), size)
def calculate_horizontal_text_center(text):
    return screen.get_width() // 2 - text.get_width() // 2
def calculate_vertical_text_center(text):
    return screen.get_height() // 2 - text.get_height() // 2


if __name__ == "__main__":
    menu()
