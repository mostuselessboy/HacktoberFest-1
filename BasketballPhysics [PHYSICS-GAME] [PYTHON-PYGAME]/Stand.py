import pygame


class rim_obj(pygame.sprite.Sprite):
    def __init__(self, imgfile, radius):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(imgfile)
        self.image = pygame.transform.scale(self.image, (radius/10, radius/10))
        self.radius = radius
        self.state = [0, 0, 0, 0]

    def set_pos(self, pos):
        self.state[0:2] = pos
        return self

    def draw(self, surface):
        rect = self.image.get_rect()
        rect.center = (self.state[0], 640 - self.state[1])  # Flipping y
        surface.blit(self.image, rect)
