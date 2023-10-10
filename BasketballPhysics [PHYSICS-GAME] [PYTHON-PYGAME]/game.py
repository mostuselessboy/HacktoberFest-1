import pygame
import numpy as np
from Player import player
from Stand import rim_obj
import random
gravity = [4.8, 9.8, 18.6]
friction = [1, 2, 3]    
class Game:
    def __init__(self):
        grav = random.choice(gravity)
        frict = random.choice(friction)

        self.Player = player("assets/basketball.png", 15, 0.1, grav, frict).set_pos([30, 30])
        file = open("data/gravity.txt", "w")
        file.write(str(grav))
        file.close()

        file = open("data/friction.txt", "w")
        file.write(str(frict))
        file.close()


        self.rim = []
        self.e = 1.0 
        self.shot = False
        self.p1score = 00
        self.p2score = 0
        self.scored = False
        self.p1turn = True
        self.won = False
        self.shot_from = 20

    def reset(self, power):
        SND_ball_throw = pygame.mixer.Sound('assets/throw.wav')
        SND_ball_throw.play()
        grav = random.choice(gravity)
        frict = random.choice(friction)

        self.Player = player("assets/basketball.png", 15, 0.1, grav, frict).set_pos([30, 30])
        file = open("data/gravity.txt", "w")
        file.write(str(grav))
        file.close()

        file = open("data/friction.txt", "w")
        file.write(str(frict))
        file.close()
        self.shot = False
        if self.scored:
            self.update_score()
        self.scored = False
        self.Player = self.Player.set_pos([30, 30])
        self.shot_from = 30
        power.reset()

    def update_score(self):
        SND_ball_throw = pygame.mixer.Sound('assets/score.wav')
        SND_ball_throw.play()
        score = int((1030 - self.shot_from) / 100)
        self.p1score += score
    def add_rim(self, imgfile, radius):
        rim = rim_obj(imgfile, radius)
        self.rim.append(rim)
        return rim

    def draw(self, screen):
        self.Player.draw(screen)
        for rim in self.rim:
            rim.draw(screen)

    def update(self, dt, power):
        self.col()
        self.Player.update(dt)
        if (
            self.Player.state[0] > 1280 + self.Player.radius
            or self.Player.state[1] < 0 - self.Player.radius
        ):
            self.reset(power)
        top_of_ball = self.Player.state[1] + self.Player.radius
        if (
            self.Player.state[0] > 970
            and self.Player.state[0] < 1075
            and top_of_ball > 295
            and top_of_ball < 305
        ):
            self.scored = True
            SND_ball_throw = pygame.mixer.Sound('assets/throw.wav')
            SND_ball_throw.play()

    def normalize(self, v):
        return v / np.linalg.norm(v)

    def col(self):
        if self.rim_stand_col():
            return

        self.rim_col()

    def rim_stand_col(self):
        right_of_ball = self.Player.state[0] + self.Player.radius
        if right_of_ball >= 1075 and right_of_ball <= 1090:
            bottom_of_ball = self.Player.state[1] - self.Player.radius
            # hit top of backboard
            if bottom_of_ball > 390 and bottom_of_ball <= 395:
                self.Player.state = self.Player.prev_state
                self.Player.set_vel([self.Player.state[2], -self.Player.state[3]])
                SND_ball_throw = pygame.mixer.Sound('assets/metal.wav')
                SND_ball_throw.play()
                return True
            # hit side of backboard
            if bottom_of_ball > 0 and bottom_of_ball <= 390:
                self.Player.state = self.Player.prev_state
                self.Player.set_vel([-self.Player.state[2], self.Player.state[3]])
                SND_ball_throw = pygame.mixer.Sound('assets/metal.wav')
                SND_ball_throw.play()
                return True
        return False

    def rim_col(self):
        pos_i = self.Player.state[0:2]
        for j in range(0, len(self.rim)):
            pos_j = np.array(self.rim[j].state[0:2])
            dist_ij = np.sqrt(np.sum((pos_i - pos_j) ** 2))
            radius_j = self.rim[j].radius
            if dist_ij > self.Player.radius + radius_j:
                continue
            self.Player.state = self.Player.prev_state
            vel_i = np.array(self.Player.state[2:])
            n_ij = self.normalize(pos_i - pos_j)
            mass_i = self.Player.mass
            J = -(1 + self.e) * np.dot(vel_i, n_ij) / ((1.0 / mass_i + 1.0))
            vel_i_aftercollision = vel_i + n_ij * J / mass_i
            self.Player.set_vel(vel_i_aftercollision)
            return
