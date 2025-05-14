import pygame

def main():
    pygame.init()
    pygame.display.set_caption("Digital Rain")

    clock = pygame.time.Clock()
    dt = 0
    resolution = (800, 600)
    screen = pygame.display.set_mode(resolution)
    rain = Rain(resolution)

    running = True
    fullscreen = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen += 1

                if fullscreen % 2 == 0:
                    fullscreen_resolution = (1920, 1080)
                    screen = pygame.display.set_mode(fullscreen_resolution, pygame.FULLSCREEN)
                    rain = Rain(fullscreen_resolution)
                else:
                    screen = pygame.display.set_mode(resolution)
                    rain = Rain(resolution)

        rain.update(dt)

        black = pygame.Color(0, 0, 0)
        screen.fill(black)

        rain.draw(screen)

        pygame.display.flip()
        dt = clock.tick(24)

    pygame.quit()