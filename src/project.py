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

    def __init__(self, pos, groups, obsta, level):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/playerdown_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.attacking = False
        self.attack_cooldown = 0
        self.direction = pygame.math.Vector2()
        self.obsta = obsta
        self.look = 'down'

        self.attack_time = 2 / level
        
        #self.attack_damage = 10 * level

        #self.health = 100 * level
        
        self.speed = player_speed * level
        
        self.stamina = 100 * level

    def key_input(self):
        key = pygame.key.get_pressed()
        # up and down
        if key[pygame.K_w]:
            self.direction.y = -1
        elif key[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0
        # right and left
        if key[pygame.K_d]:
            self.direction.x = 1
        elif key[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        # running
        if key[pygame.K_LSHIFT]:
            self.speed = player_speed * 1.4
        else:
            self.speed = player_speed
        # stamina
        if self.speed == player_speed * 1.4:
            self.stamina -= 1
            if self.stamina <= 0:
                self.speed = player_speed
                self.stamina = 0
        else:
            if self.stamina < 100:
                self.stamina += 1
        # attack
        if key[pygame.K_SPACE]:
            if not self.attacking:
                self.attacking = True
                self.attack_cooldown = pygame.time.get_ticks()
            if self.attacking:
                if pygame.time.get_ticks() - self.attack_cooldown >= self.attack_time * 1000:
                    self.attacking = False
                    self.attack_cooldown = 0

    def look_direction(self):
        if self.attack_cooldown == 0:
            # up and down
            if self.direction.x == 1 and self.direction.y == 0:
                self.look = 'right'
            elif self.direction.x == -1 and self.direction.y == 0:
                self.look = 'left'
            elif self.direction.y == 1 and self.direction.x == 0:
                self.look = 'down'
            elif self.direction.y == -1 and self.direction.x == 0:
                self.look = 'up'
            # diagonals
            elif self.direction.x == 1 and self.direction.y == 1:
                self.look = 'downright'
            elif self.direction.x == 1 and self.direction.y == -1:
                self.look = 'upright'
            elif self.direction.x == -1 and self.direction.y == 1:
                self.look = 'downleft'
            elif self.direction.x == -1 and self.direction.y == -1:
                self.look = 'upleft'
        # attack
        if self.attack_cooldown != 0:
            if self.direction.x == 1 and self.direction.y == 0:
                self.look = 'attackright'
            elif self.direction.x == -1 and self.direction.y == 0:
                self.look = 'attackleft'
            elif self.direction.y == 1 and self.direction.x == 0:
                self.look = 'attackdown'
            elif self.direction.y == -1 and self.direction.x == 0:
                self.look = 'attackup'
            elif self.direction.x == 1 and self.direction.y == 1:
                self.look = 'attackdownright'
            elif self.direction.x == 1 and self.direction.y == -1:
                self.look = 'attackupright'
            elif self.direction.x == -1 and self.direction.y == 1:
                self.look = 'attackdownleft'
            elif self.direction.x == -1 and self.direction.y == -1:
                self.look = 'attackupleft'
        # attack images
        if self.direction.magnitude() != 0:
            if self.look == 'attackright':
                self.image = pygame.image.load('../textures/attackright_test.png').convert_alpha()
            elif self.look == 'attackleft':
                self.image = pygame.image.load('../textures/attackleft_test.png').convert_alpha()
            elif self.look == 'attackdown':
                self.image = pygame.image.load('../textures/attackdown_test.png').convert_alpha()
            elif self.look == 'attackup':
                self.image = pygame.image.load('../textures/attackup_test.png').convert_alpha()
            elif self.look == 'attackdownright':
                self.image = pygame.image.load('../textures/attackdownright_test.png').convert_alpha()
            elif self.look == 'attackupright':
                self.image = pygame.image.load('../textures/attackupright_test.png').convert_alpha()
            elif self.look == 'attackdownleft':
                self.image = pygame.image.load('../textures/attackdownleft_test.png').convert_alpha()
            elif self.look == 'attackupleft':
                self.image = pygame.image.load('../textures/attackupleft_test.png').convert_alpha()
        # images
        if self.direction.magnitude() != 0:
            if self.look == 'right':
                self.image = pygame.image.load('../textures/playerright_test.png').convert_alpha()
            elif self.look == 'left':
                self.image = pygame.image.load('../textures/playerleft_test.png').convert_alpha()
            elif self.look == 'down':
                self.image = pygame.image.load('../textures/playerdown_test.png').convert_alpha()
            elif self.look == 'up':
                self.image = pygame.image.load('../textures/playerup_test.png').convert_alpha()
            # diagonal images
            elif self.look == 'downright':
                self.image = pygame.image.load('../textures/playerdownright_test.png').convert_alpha()
            elif self.look == 'upright':
                self.image = pygame.image.load('../textures/playerupright_test.png').convert_alpha()
            elif self.look == 'downleft':
                self.image = pygame.image.load('../textures/playerdownleft_test.png').convert_alpha()
            elif self.look == 'upleft':
                self.image = pygame.image.load('../textures/playerupleft_test.png').convert_alpha()

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
        self.look_direction()
        self.movement(self.speed)

class EasyEnemy(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/enemy1_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        level = 1
        
        self.speed = enemy_speed * level

    def update(self):
        pass

class MediumEnemy(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/enemy2_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        level = 1.5
        
        self.speed = enemy_speed * level

    def update(self):
        pass

class HardEnemy(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/enemy3_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        level = 2
        
        self.speed = enemy_speed * level

    def update(self):
        pass

class FinalEnemy(pygame.sprite.Sprite):
    
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/enemy4_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.direction = pygame.math.Vector2()
        level = 2.5
        
        self.speed = enemy_speed * level

    def update(self):
        pass

class World:

    def __init__(self):
        
        self.surface = pygame.display.get_surface()
        
        self.sprites = pygame.sprite.Group() #visible
        self.obstacles = pygame.sprite.Group() #invisible
        self.player_level = 1
        
        self.map()

    def map(self):
        for rindex,row in enumerate(FACE_MAP):
            for cindex, col in enumerate(row):
                x = cindex * tile_size
                y = rindex * tile_size
                if col == 'x':
                    SpriteTexture((x,y),[self.sprites, self.obstacles])
                if col == '0':
                    self.character = MainCharacter((x,y),[self.sprites], self.obstacles, self.player_level)
                if col == 'e':
                    EasyEnemy((x,y),[self.sprites])
                if col == 'm':
                    MediumEnemy((x,y),[self.sprites])
                if col == 'h':
                    HardEnemy((x,y),[self.sprites])
                if col == 'f':
                    FinalEnemy((x,y),[self.sprites])
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