import os, sys, pygame
from random import randint, choice


class Ball(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.Surface((10, 10)).convert()
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)
        self.speed_x = 0
        self.speed_y = 0

    def change_y(self):
        self.speed_y *= -1

    def change_x(self):
        self.speed_x *= -1

    def start(self, speed_x, speed_y):
        self.speed_x = speed_x
        self.speed_y = speed_y

    def stop(self):
        self.speed_x = 0
        self.speed_y = 0

    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)

    def reset(self):
        self.rect = self.image.get_rect(center=self.pos)


class Pad(pygame.sprite.Sprite):
    def __init__(self, pos=(0, 0), color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((20, 70)).convert()
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.max_speed_y = 10
        self.max_speed_x = 5
        self.speed_x = 0
        self.speed_y = 0

    def move_up(self):
        self.speed_y = self.max_speed_y * -1

    def move_down(self):
        self.speed_y = self.max_speed_y * 1

    def move_right(self):
        self.speed_x = self.max_speed_x * 1

    def move_left(self):
        self.speed_x = self.max_speed_x * -1

    def stop(self):
        self.speed_y = 0
        self.speed_x = 0

    def update(self):
        self.rect.move_ip(self.speed_x, self.speed_y)


class Score(pygame.sprite.Sprite):
    def __init__(self, font, pos=(0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.font = font
        self.pos = pos
        self.score = 0
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)

    def score_up(self):
        self.score += 1

    def update(self):
        self.image = self.font.render(str(self.score), 0, (255, 255, 255))
        self.rect = self.image.get_rect(center=self.pos)


def main():
    pygame.init()

    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Agressive Pong - X7REME13")

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            "assets",
            "graphics",
            "background.jpg")
        background = pygame.image.load(filename)
        background = background.convert()

    except pygame.error as e:
        print("Cannot load image: ", filename)
        raise SystemExit(str(e))

    if not pygame.font:
        raise SystemExit('Pygame does not support fonts')

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'assets',
            'fonts',
            'wendy.ttf')
        font = pygame.font.Font(filename, 90)
    except pygame.error as e:
        print('Cannot load font: ', filename)
        raise SystemExit(str(e))

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'assets',
            'sounds',
            'bounce.wav')
        bounce = pygame.mixer.Sound(filename)

    except pygame.error as e:
        print('Cannot load sound: ', filename)
        raise SystemExit(str(e))

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'assets',
            'sounds',
            'point.ogg')
        point = pygame.mixer.Sound(filename)
    except pygame.error as e:
        print('Cannot load sound: ', filename)
        raise SystemExit(str(e))

    try:
        filename = os.path.join(
            os.path.dirname(__file__),
            'assets',
            'sounds',
            'ambient.wav')
        ambient = pygame.mixer.Sound(filename)
    except pygame.error as e:
        print('Cannot load sound: ', filename)
        raise SystemExit(str(e))

    pygame.mixer.init()

    ambient.play(-1)

    left_score = Score(font, (width / 3, height / 8))
    right_score = Score(font, (2 * width / 3, height / 8))

    pad_left = Pad((width / 6, height / 4), (30, 180, 233))
    pad_right = Pad((5 * width / 6, 3 * height / 4), (180, 233, 30))

    ball = Ball((width / 2, height / 2))

    sprites = pygame.sprite.Group(pad_left, pad_right, ball, left_score, right_score)

    clock = pygame.time.Clock()
    fps = 60

    pygame.key.set_repeat(1, int(2000 / fps))

    top = pygame.Rect(0, 0, width, 5)
    bottom = pygame.Rect(0, height - 5, width, 5)

    screen_rect = screen.get_rect().inflate(0, -10)
    pad_left.rect.clamp_ip(screen_rect)
    pad_right.rect.clamp_ip(screen_rect)

    left = pygame.Rect(0, 0, 5, height)
    right = pygame.Rect(width - 5, 0, 5, height)
    arena_right = pygame.Rect(width - int(width * 0.75), 2, int(width * 0.75), height)
    arena_left = pygame.Rect(0, 1, int(width * 0.75), height)
    starteado = True



    while 1:

        clock.tick(fps)

        pad_left.stop()
        pad_right.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] and starteado:
                ball.start(2 * choice((-1, 1)), randint(1, 3) * choice((-1, 1)))
                starteado = False

            if keys[pygame.K_w]:  # 276
                pad_left.move_up()
            if keys[pygame.K_s]:  # 275
                pad_left.move_down()
            if keys[pygame.K_a]:  # 97
                pad_left.move_left()
            if keys[pygame.K_d]:  # 100
                pad_left.move_right()

            if keys[pygame.K_UP]:  # 97
                pad_right.move_up()
            if keys[pygame.K_DOWN]:  # 100
                pad_right.move_down()
            if keys[pygame.K_LEFT]:  # 276
                pad_right.move_left()
            if keys[pygame.K_RIGHT]:  # 275
                pad_right.move_right()

        screen_rect = screen.get_rect().inflate(0, -10)

        pad_left.rect.clamp_ip(arena_left)
        pad_right.rect.clamp_ip(arena_right)

        if ball.rect.colliderect(top) or ball.rect.colliderect(bottom):
            ball.change_y()
            bounce.set_volume(0.2)
            bounce.play()

        elif (ball.rect.colliderect(pad_left.rect) or
              ball.rect.colliderect(pad_right.rect)):
            ball.change_x()
            bounce.set_volume(0.2)
            bounce.play()

        if ball.rect.colliderect(left):
            point.set_volume(1)
            point.play()
            right_score.score_up()
            ball.reset()
            ball.stop()
            # ball.start(1*randint(1, right_score.score+1), randint(1, 3) * choice((-1, 1)))
            starteado = True
        elif ball.rect.colliderect(right):
            point.set_volume(1)
            point.play()
            left_score.score_up()
            ball.reset()
            ball.stop()
            # ball.start(-1*randint(1, left_score.score+1)), randint(1, 3) * choice((-1, 1))
            starteado = True


        sprites.update()

        screen.blit(background, (0, 0))
        sprites.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
