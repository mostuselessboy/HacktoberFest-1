import pygame, sys
from math import atan, radians, cos, sin
BLACK = (70, 70, 70)
BLUE = (70, 70, 70)
class force:
    def __init__(self):
        self.power = 0
        self.direction = 1
        self.running = True

    def draw(self, screen):
        pygame.draw.rect(screen, BLACK, (675, 35, 350, 25), 1)
        pygame.draw.rect(screen, BLUE, (675, 35, self.power * 350 / 100, 25), 0)

    def get_angle(self, game):
        x, y = pygame.mouse.get_pos()
        dx = x - game.Player.state[0]
        dy = 640 - y - game.Player.state[1]
        if dx == 0:
            angle = radians(90)
        else:
            angle = atan(dy / float(dx))
            if angle < 0:
                angle = 0
            elif angle > 90:
                angle = radians(90)
        return angle

    def start(self, game):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a and game.Player.state[0] > 30:
                game.Player.set_pos([game.Player.state[0] - 20, game.Player.state[1]])
            elif event.key == pygame.K_d and game.Player.state[0] < 450:
                game.Player.set_pos([game.Player.state[0] + 20, game.Player.state[1]])
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.shoot_ball(game)
        self.move_bar()

    def shoot_ball(self, game):
        angle = self.get_angle(game)
        game.shot = True
        game.shot_from = game.Player.state[0]
        vel = 150 * self.power / 80
        vel_x = vel * cos(angle)
        vel_y = vel * sin(angle)
        game.Player.set_vel([vel_x, vel_y])
    def move_bar(self):
        self.power += self.direction
        if self.power <= 0 or self.power >= 100:
            self.direction *= -1

    def reset(self):
        self.power = 0
        self.direction = 1
