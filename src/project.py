import pygame
from map import *

class SpriteTexture(pygame.sprite.Sprite):

    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/sprite_texture_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class MainCharacter(pygame.sprite.Sprite):

    def __init__(self,pos,groups,obstacle):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/player_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle = obstacle

    def key_input(self):
        key = pygame.key.get_pressed()
        
        if key == [pygame.K_w]:
            self.direction.y = -1
        elif key == [pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
                
        if key == [pygame.K_a]:
            self.direction.x = 1
        elif key == [pygame.K_d]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def movement(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.center += self.direction * speed

    def update(self):
        self.key_input()
        self.movement(self.speed)

class World:

    def __init__(self):
        
        self.surface = pygame.display.get_surface()
        
        self.sprites = pygame.sprite.Group() #visible
        self.obstacles = pygame.sprite.Group() #invisible
        
        self.map()

    def map(self):
        for rindex,row in enumerate(FACE_MAP):
            for cindex, col in enumerate(row):
                x = cindex * tile_size
                y = rindex * tile_size
                if col == 'x':
                    SpriteTexture((x,y),[self.sprites, self.obstacles])
                if col == '0':
                    self.character = MainCharacter((x,y),[self.sprites], self.obstacle)
    
    def main(self):

        self.sprites.draw(self.surface)
        self.sprites.update()

class Crawler:

    def __init__(self):

        self.resolution = (800,600)
        self.fullscreen_resolution = (1920,1080)
        self.fullscreen = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.resolution))
        pygame.display.set_caption("Crawler")
        self.time = pygame.time.Clock()

        self.world = World()

    def main(self):

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        self.fullscreen = not self.fullscreen
                        if self.fullscreen:
                            self.screen = pygame.display.set_mode(self.fullscreen_resolution, pygame.FULLSCREEN)
                        else:
                            self.screen = pygame.display.set_mode(self.resolution)

            background = pygame.Color(0, 0, 0)
            self.screen.fill(background)

            self.world.main()

            pygame.display.update()
            self.time.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Crawler()
    game.main()