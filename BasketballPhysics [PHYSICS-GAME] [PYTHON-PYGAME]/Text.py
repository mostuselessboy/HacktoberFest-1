import pygame
RED = (255, 0, 0)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)


class Text:
    def textobj(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def display_scores(self, game, screen):
        p1color = RED if game.p1turn else BLACK
        p2color = BLACK if game.p1turn else RED
        self.displayy(
            screen, 50, str(game.p1score), 535, 145, GREY
        )
        file = open("data/gravity.txt", "r")
        grav = file.read()
        file.close()

        file = open("data/friction.txt", "r")
        frict = file.read()
        file.close()

        self.displayy(
            screen, 20, str(grav)+"m/s", 995, 142, GREY
        )

        self.displayy(
            screen, 20, str(frict)+"x", 995, 175, GREY
        )

    def displayy(self, screen, font_size, text, center_x, center_y, color):
        largeText = pygame.font.Font("freesansbold.ttf", font_size)
        TextSurf, TextRect = self.textobj(text, largeText, color)
        TextRect.center = (center_x, center_y)
        screen.blit(TextSurf, TextRect)
