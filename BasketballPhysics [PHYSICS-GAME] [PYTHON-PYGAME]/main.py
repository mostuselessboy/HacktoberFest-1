#SummerFields School 
#Basketball Physics Game
import pygame
from Player import player
from game import Game
from ForceBar import force
from Text import Text

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


def main():
    pygame.init()
    pygame_icon = pygame.image.load('assets/basketball.png')
    pygame.display.set_icon(pygame_icon)
    #pygame.mixer.music.load('assets/bgm.wav')
    #pygame.mixer.music.play(-1)
    clock = pygame.time.Clock()
    win_width = 1100
    win_height = 640
    screen = pygame.display.set_mode((win_width, win_height))
    pygame.display.set_caption("Basketball-Physics : Summer Fields School")
    game = Game()
    power = force()
    scoreboard = Text()
    game.add_rim("assets/basketball.png", 5).set_pos([970, 300])
    game.add_rim("assets/basketball.png", 5).set_pos([1075, 300])
    dt = 0.1
    while True:
        clock.tick(70)
        bg_img = pygame.image.load("assets/bg.jpg").convert()
        bg_img = (pygame.transform.scale(bg_img, (1100, 640)))
        screen.blit(bg_img, bg_img.get_rect())
        power.draw(screen)
        game.draw(screen)
        scoreboard.display_scores(game, screen)
        if not game.shot:
            power.start(game)
        else:
            won = game.update(dt, power)

        pygame.display.update()

if __name__ == "__main__":
    main()
