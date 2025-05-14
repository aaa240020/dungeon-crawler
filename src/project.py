import pygame

class Crawler:

    def __init__(self):

        pygame.init()
        self.screen = pygame.display.set_mode((self.resolution))
        pygame.display.set_caption("Crawler")
        self.time = pygame.time.Clock()

    def main(self):

        running = True
        self.resolution = (800,600)
        self.fullscreen_resolution = (1920,1080)
        self.fullscreen = False

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
            self.clock.tick(24)

        pygame.quit()
