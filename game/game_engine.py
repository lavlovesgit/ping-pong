import pygame
import sys
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        # Initialize paddles
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)

        # Load sounds
        self.sound_paddle = pygame.mixer.Sound("sounds/paddle_hit.wav")
        self.sound_wall = pygame.mixer.Sound("sounds/wall_bounce.wav")
        self.sound_score = pygame.mixer.Sound("sounds/score.wav")

        # Ball with sounds
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height,
                         sound_wall=self.sound_wall,
                         sound_paddle=self.sound_paddle,
                         sound_score=self.sound_score)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_font = pygame.font.SysFont("Arial", 60)
        self.menu_font = pygame.font.SysFont("Arial", 40)
        self.game_over = False
        self.win_score = 5  # default winning score

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        if self.game_over:
            return

        # Move the ball and check collision
        self.ball.move(self.player, self.ai)

        # Scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.sound_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.sound_score.play()
            self.ball.reset()

        # AI tracks ball
        self.ai.auto_track(self.ball, self.height)

        # Check for game over
        self.check_game_over()

    def check_game_over(self):
        if self.player_score == self.win_score or self.ai_score == self.win_score:
            self.game_over = True

    def render(self, screen):
        screen.fill(BLACK)

        # Draw paddles, ball, center line
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))

        # Draw scores
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))

        # Game over message + replay menu
        if self.game_over:
            self.show_game_over(screen)

    def show_game_over(self, screen):
        if self.player_score == self.win_score:
            winner = "Player Wins!"
        else:
            winner = "AI Wins!"

        screen.fill(BLACK)
        text_surface = self.game_over_font.render(winner, True, WHITE)
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 3))
        screen.blit(text_surface, text_rect)

        # Replay options
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        for i, option in enumerate(options):
            option_text = self.menu_font.render(option, True, WHITE)
            rect = option_text.get_rect(center=(self.width // 2, self.height // 2 + i * 50))
            screen.blit(option_text, rect)

    def handle_replay_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in (pygame.K_3, pygame.K_5, pygame.K_7):
                    self.reset_game(int(event.unicode))
                    return True
        return False

    def reset_game(self, new_target):
        self.player_score = 0
        self.ai_score = 0
        self.win_score = new_target
        self.game_over = False
        self.ball.reset()
