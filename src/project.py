import pygame
from crawlerinfo import *

class SpriteTexture(pygame.sprite.Sprite):

    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/sprite_texture_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class Edges(pygame.sprite.Sprite):
    
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/edges_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class MainCharacter(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obsta):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/player_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()
        self.speed = player_speed
        self.obsta = obsta

    def key_input(self):
        key = pygame.key.get_pressed()
        
        if key[pygame.K_w]:
            self.direction.y = -1
        elif key[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
                
        if key[pygame.K_d]:
            self.direction.x = 1
        elif key[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if key[pygame.K_LSHIFT]:
            self.speed = player_speed * 1.5
        else:
            self.speed = player_speed

    def stamina(self):
        if self.speed == player_speed * 1.5:
            self.stamina -= 1
            if self.stamina <= 0:
                self.speed = player_speed
                self.stamina = 0
        else:
            if self.stamina < 100:
                self.stamina += 1



    def movement(self,speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision('x')
        self.rect.y += self.direction.y * speed
        self.collision('y')

    def collision(self,direction):
        if direction == 'x':
            for sprite in self.obsta:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0:
                        self.rect.left = sprite.rect.right

        if direction == 'y':
            for sprite in self.obsta:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0:
                        self.rect.top = sprite.rect.bottom

    def update(self):
        self.key_input()
        self.movement(self.speed)

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/enemy_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        
        self.direction = pygame.math.Vector2()
        self.speed = enemy_speed

    def update(self):
        pass

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
                    self.character = MainCharacter((x,y),[self.sprites], self.obstacles)
                if col == 'e':
                    Enemy((x,y),[self.sprites])
                if col == '1':
                    Edges((x,y),[self.sprites, self.obstacles])
    
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

            background = pygame.image.load('../textures/background.png').convert_alpha()
            fill = (0,0,0)
            self.screen.fill(fill)
            self.screen.blit(background, (0,0))

            self.world.main()

            pygame.display.update()
            self.time.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Crawler()
    game.main()