#!/usr/bin/env python3
import pygame
from pygame.locals import *

BLACK = (0, 0, 0)

ENEMY_MOVE_SPEED_Y = 1
ENEMY_MOVE_SPEED_X = 0

SHIP_MOVE_SPEED_X = 10

BULLET_MOVE_SPEED_Y = -15

WIDTH = 800
HEIGHT = 800

TRUE = False

class GameObject:
    def __init__(self, game, position, velocity):
        self.game = game
        self.velocity = velocity
        self.position = position

    def update(self):
        pass

    def draw(self):
        pass

    def collidesWith(self, other):
        # TODO 4 - Check if this object collides with the other object.
        #          Get object dimensions (not halfed) with object.rect.width and object.rect.height
        return False

class Enemy(GameObject):
    def __init__(self, game, position):
        super().__init__(game, position, [ENEMY_MOVE_SPEED_X, ENEMY_MOVE_SPEED_Y])

        self.is_alive = True;
        self.image = pygame.image.load("enemy.png")
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()

    def update(self):
        # TODO 2 - Make enemies move by adding velocity to their position


        # Do not write bellow here
        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

        if self.position[0] < 0:
            self.velocity[0] *= -1

        if self.position[0] > WIDTH:
            self.velocity[0] *= -1

        if not self.is_alive:
            self.game.enemyList.remove(self)
            self.game.gameObjects.remove(self)
            del self

    def draw(self):
        self.game.window.blit(self.image, self.rect.topleft)

class Ship(GameObject):
    def __init__(self, game):

        self.image = pygame.image.load("spaceship.png")
        self.image = pygame.transform.scale(self.image, (100, 100))

        self.rect = self.image.get_rect()

        self.rect.bottom = game.window.get_rect().bottom
        self.rect.centerx = game.window.get_rect().centerx

        super().__init__(game, [self.rect.centerx, self.rect.centery], [0, 0])

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

    def draw(self):
        self.game.window.blit(self.image, self.rect.topleft)

    def moveLeft(self):
        self.velocity[0] = -SHIP_MOVE_SPEED_X

    def moveRight(self):
        self.velocity[0] = SHIP_MOVE_SPEED_X

    def stop(self):
        self.velocity[0] = 0

    def shoot(self):
        bullet = Bullet(self.game, self.position)
        self.game.shots.append(bullet)
        self.game.gameObjects.append(bullet)


class Bullet(GameObject):
    def __init__(self, game, position):

        self.image = pygame.image.load("bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 20))

        self.rect = self.image.get_rect()

        self.rect.bottom = game.window.get_rect().bottom
        self.rect.centerx = game.window.get_rect().centerx

        self.is_alive = True

        super().__init__(game, [position[0], position[1]], [0, BULLET_MOVE_SPEED_Y])

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.rect.centerx = self.position[0]
        self.rect.centery = self.position[1]

        if not self.is_alive or self.position[1] < 0:
            self.game.shots.remove(self)
            self.game.gameObjects.remove(self)
            del self

    def draw(self):
        self.game.window.blit(self.image, self.rect.topleft)

class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Invaders")

        self.gameObjects = []
        self.shots = []

        self.enemyList = []


        self.ship = Ship(self)

        self.gameObjects.append(self.ship)

    def input(self):
        # TODO 3 - Make spaceship move and shoot
        #          Use its functions (moveLeft, shoot, etc)
        pass

    def collisionDetection(self):
        for shot in self.shots:
            for enemy in self.enemyList:
                if shot.collidesWith(enemy):
                    shot.is_alive = False
                    enemy.is_alive = False

    def update(self):

        for gameObject in self.gameObjects:
            gameObject.update()

        if not self.enemyList:
            for i in range (100, 600, 200):
                enemy = Enemy(self, [i, 100])
                self.gameObjects.append(enemy)
                self.enemyList.append(enemy)

        self.collisionDetection()

    def draw(self):
        self.window.fill(BLACK)

        for gameObject in self.gameObjects:
            gameObject.draw()

        pygame.display.update()
        pygame.time.Clock().tick(30)

    def run(self):
        while TRUE:
            self.input()
            self.update()
            self.draw()


def main():
    game = Game()
    game.run()

main()
