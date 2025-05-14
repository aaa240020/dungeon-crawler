import pygame
from map import *

class World:

    def __init__(self):
        
        self.surface = pygame.display.get_surface()
        
        self.sprites = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        
        self.map()

    def map(self):
        for rindex,row in enumerate(FACE_MAP):
            for cindex, col in enumerate(row):
                x = cindex * tile_size
                y = rindex * tile_size
                if col == 'x':
                    SpriteTexture((x,y),[self.sprites])
                if col == '0':
    
    def main(self):

        self.sprites.draw(self.surface)


#class Main_Character:

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

            color = pygame.Color(0, 255, 255)
            self.screen.fill(color)
            pygame.display.update()
            self.time.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Crawler()
    game.main()