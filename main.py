import pygame
from game.game_engine import GameEngine

# Initialize Pygame and mixer for sounds
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

BLACK = (0, 0, 0)
clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    while running:
        if not engine.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            engine.handle_input()
            engine.update()
            engine.render(SCREEN)

        else:
            # Show game over + replay options
            engine.render(SCREEN)
            pygame.display.flip()

            # Wait for replay or exit
            if engine.handle_replay_input():
                continue  # restart loop with reset game

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
