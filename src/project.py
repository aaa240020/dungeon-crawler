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
        self.image = pygame.image.load('../textures/edges3.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

class MainCharacter(pygame.sprite.Sprite):

    def __init__(self, pos, groups, obsta, level):
        super().__init__(groups)
        self.image = pygame.image.load('../textures/playerdown_test.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.attacking = False
        self.attack_cooldown = 1
        self.direction = pygame.math.Vector2()
        self.obsta = obsta
        self.look = 'down'
        self.level = level

        self.attack_time = 3 / level

        self.stats = {
            'health': 100 * level,
            'stamina': 100 * level,
            'attack': 10 * level,
            'speed': 5 * level,
        }

        self.health = self.stats['health']
        self.stamina = self.stats['stamina']
        self.attack_damage = self.stats['attack']

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
        self.surface = pygame.display.get_surface()
        attack_bar = pygame.Rect(30, 80, 200, 20)
        pygame.draw.rect(self.surface, (125,125,125), attack_bar)
        if pygame.time.get_ticks() - self.attack_cooldown >= self.attack_time * 1000:
            pygame.draw.rect(self.surface, (0,0,255), attack_bar)
            pygame.draw.rect(self.surface, (25,25,25), attack_bar, 3)
        else:
            pygame.draw.rect(self.surface, (125,125,125), attack_bar)
            pygame.draw.rect(self.surface, (25,25,25), attack_bar, 3)

        if key[pygame.K_SPACE]:
            if not self.attacking:
                self.attacking = True
                self.attack_cooldown = pygame.time.get_ticks()
            if self.attacking:
                if pygame.time.get_ticks() - self.attack_cooldown >= self.attack_time * 1000:
                    self.attacking = False
                    self.attack_cooldown = 0

    def look_direction(self):
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
        #images
        if self.attack_cooldown == 0:
            if self.look == 'right':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
            elif self.look == 'left':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
            elif self.look == 'down':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
            elif self.look == 'up':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
            elif self.look == 'downright':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
            elif self.look == 'upright':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
            elif self.look == 'downleft':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
            elif self.look == 'upleft':
                self.image = pygame.image.load('../textures/attack.png').convert_alpha()
        elif self.attack_cooldown > 0:
            if self.look == 'right':
                self.image = pygame.image.load('../textures/playerright_test.png').convert_alpha()
            elif self.look == 'left':
                self.image = pygame.image.load('../textures/playerleft_test.png').convert_alpha()
            elif self.look == 'down':
                self.image = pygame.image.load('../textures/playerdown_test.png').convert_alpha()
            elif self.look == 'up':
                self.image = pygame.image.load('../textures/playerup_test.png').convert_alpha()
            elif self.look == 'downright':
                self.image = pygame.image.load('../textures/playerdownright_test.png').convert_alpha()
            elif self.look == 'upright':
                self.image = pygame.image.load('../textures/playerupright_test.png').convert_alpha()
            elif self.look == 'downleft':
                self.image = pygame.image.load('../textures/playerdownleft_test.png').convert_alpha()
            elif self.look == 'upleft':
                self.image = pygame.image.load('../textures/playerupleft_test.png').convert_alpha()

    def movement(self,speed,level):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed * level
        self.collision('x')
        self.rect.y += self.direction.y * speed * level
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
        self.movement(self.speed, self.level)

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

        self.ui = UI()

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
        self.ui.display(self.character)

class UI:

    def __init__(self):
        self.surface = pygame.display.get_surface()
        self.font = pygame.font.Font('../src/ARCADECLASSIC.ttf', 30)
        self.health_bar = pygame.Rect(30, 20, 200, 20)
        self.stamina_bar = pygame.Rect(30, 50, 200, 20)
        self.health_bar_color = (255, 0, 0)
        self.stamina_bar_color = (0, 255, 0)
        self.bg_color = (125, 125, 125)
        pygame.draw.rect(self.surface, self.bg_color, self.health_bar)
        pygame.draw.rect(self.surface, self.bg_color, self.stamina_bar)

    def ui_elements(self,current,max_value,background,color):
        pygame.draw.rect(self.surface, self.bg_color, background)

        ratio = current / max_value
        width = background.width * ratio
        new_rect = background.copy()
        new_rect.width = width

        pygame.draw.rect(self.surface, color, new_rect)
        pygame.draw.rect(self.surface, (25,25,25), background, 3)

    def display(self,player):
        self.ui_elements(player.health, player.stats['health'], self.health_bar, self.health_bar_color)
        self.ui_elements(player.stamina, player.stats['stamina'], self.stamina_bar, self.stamina_bar_color)



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

            background = pygame.image.load('../textures/background2.png').convert_alpha()
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