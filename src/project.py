import pygame

class Crawler:

    def __init__(self):

        resolution = (800,600)
        pygame.init()
        self.screen = pygame.display.set_mode((resolution))
        self.time = pygame.time.Clock()

    def main(self):

        resolution = (800,600)
        running = True
        fullscreen = 1

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:
                        fullscreen += 1
                    if fullscreen % 2 == 0:
                        fullscreen_resolution = (1920, 1080)
                        screen = pygame.display.set_mode(fullscreen_resolution, pygame.FULLSCREEN)
                        Crawler(fullscreen_resolution)
                    else:
                        screen = pygame.display.set_mode(resolution)
                        Crawler(resolution)

        black = pygame.Color(0, 0, 0)
        screen.fill(black)
        pygame.display.update()
        self.clock.tick(24)