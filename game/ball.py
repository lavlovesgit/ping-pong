import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height,
                 sound_wall=None, sound_paddle=None, sound_score=None):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])

        self.sound_wall = sound_wall
        self.sound_paddle = sound_paddle
        self.sound_score = sound_score

    def move(self, player, ai):
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Bounce off top/bottom
        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            if self.sound_wall:
                self.sound_wall.play()

        # Paddle collision
        if self.rect().colliderect(player.rect()):
            self.x = player.x + player.width
            self.velocity_x *= -1
            if self.sound_paddle:
                self.sound_paddle.play()
        elif self.rect().colliderect(ai.rect()):
            self.x = ai.x - self.width
            self.velocity_x *= -1
            if self.sound_paddle:
                self.sound_paddle.play()

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)
