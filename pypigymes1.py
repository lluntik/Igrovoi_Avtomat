import pygame
import random
import time
# импортируем функцию для масштабирования картинок
from pygame.transform import scale
# описываем класс "космический корабль", расширяющий встроенный класс Sprite
class Asteroid(pygame.sprite.Sprite):
    # конструктор, в который передаются стартовые координаты
    def __init__(self, x, y, speed_x, speed_y):
        pygame.sprite.Sprite.__init__(self)

        # загружаем картинку с астероидом и масштабируем под размер 50 на 50
        self.image = scale(pygame.image.load("aster.png"), (50, 50))
        # задаем прямоугольную область 50 на 50
        self.rect = pygame.Rect(x, y, 50, 50)
        # задаем скорость
        self.xvel = speed_x
        self.yvel = speed_y

    # функция рисования астероида
    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # функция перемещения астероида
    def update(self):
        self.rect.x += self.xvel
        self.rect.y += self.yvel

        # если астероид за границей карты - он умирает
        if self.rect.x < 0:
            self.kill()
class Spaceship(pygame.sprite.Sprite):
    # конструктор - функция, в которую мы передаем начальные координаты
    def __init__(self, x, y):
        # инициализируем спрайт
        pygame.sprite.Sprite.__init__(self)

        # выбираем прямоугольную область размера 50 на 100
        self.rect = pygame.Rect(x, y, 40, 40)

        # загружаем картинку с кораблем
        self.image = scale(pygame.image.load("ship.png"), (50, 50))

        # задаем начальную скорость по оси x
        self.xvel = 0

        self.yvel = 0

        # добавим кораблю здоровье
        self.life = 100

    # функция рисования корабля
    def draw(self, screen):
        # рисуем корабль на экране на месте занимаемой им прямоугольной области
        screen.blit(self.image, (self.rect.x, self.rect.y))

    # функция перемещения, параметры - нажата ли стрелочки влево и вправо
    def update(self, left, right, up, down, asteroids):
        # если нажата клавиша влево, уменьшаем скорость
        if left and self.xvel < 3 and self.xvel > -3:
            self.xvel -= 3
        # если нажата клавиша вправо, увеличиваем скорость
        if right and self.xvel > -3 and self.xvel < 3:
            self.xvel += 3
        # если ничего не нажато - тормозим
        if not (left or right):
            self.xvel = 0
        # изменяем координаты на скорость
        self.rect.x += self.xvel

        # если нажата клавиша вверх, уменьшаем скорость
        if up and self.yvel < 3 and self.yvel > -3:
            self.yvel -= 3
        # если нажата клавиша вниз, увеличиваем скорость
        if down and self.yvel > -3 and self.yvel < 3:
            self.yvel += 3
        # если ничего не нажато - тормозим
        if not (up or down):
            self.yvel = 0
        # изменяем координаты на скорость
        self.rect.y += self.yvel

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.x = mouse_x - 25
        self.rect.y = mouse_y - 25

        # для каждого астероида
        for asteroid in asteroids:
            # если область, занимаемая астероидом пересекает область корабля
            if self.rect.colliderect(asteroid.rect):
                # уменьшаем жизнь
                self.life -= 1


pygame.init()

infoObject = pygame.display.Info()
screen = pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
pygame.display.set_caption("Asteroids")

# загружаем картинку из папки
big_sky = pygame.image.load("sky_pixel.png")
# масштабируем картинку под размер экрана
sky = scale(big_sky, (infoObject.current_w, infoObject.current_h))
# создаем корабль в точке 400 400
ship = Spaceship(400, 400)
# заведем переменные, чтобы помнить, какие клавиши нажаты
left = False
right = False
up = False
down = False
clock = pygame.time.Clock()
# создадим группу спрайтов, в которой будут храниться все астероиды
asteroids = pygame.sprite.Group()
# загрузим системный шрифт
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', 30)

death_frame = None

while True:
    # с некоторой вероятность будем добавлять астероиды сверху экрана
    if ship.life > 0:
        if random.randint(1, 2000) > infoObject.current_w + 100:
            # выбираем координату по оси x
            asteroid_y = random.randint(-100, infoObject.current_h - 100)
            # выбираем точку за верхней граничей экрана
            asteroid_x = infoObject.current_w + 100
            # создаем астероид
            asteroid = Asteroid(asteroid_x, asteroid_y, -5, 0)
            # и добавляем его в группу
            asteroids.add(asteroid)
        if random.randint(1, 2000) > infoObject.current_w + 100:
            asteroid_x = random.randint(-100, infoObject.current_w - 100)
            asteroid_y = -100
            asteroid = Asteroid(asteroid_x, asteroid_y, 0, 5)
            asteroids.add(asteroid)

    for e in pygame.event.get():
        # если нажата клавиша - меняем переменную
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
            left = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
            right = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
            up = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
            down = True

        # если отпущена клавиша - меняем переменную
        if e.type == pygame.KEYUP and e.key == pygame.K_LEFT:
            left = False
        if e.type == pygame.KEYUP and e.key == pygame.K_RIGHT:
            right = False
        if e.type == pygame.KEYUP and e.key == pygame.K_UP:
            up = False
        if e.type == pygame.KEYUP and e.key == pygame.K_DOWN:
            down = False

        if e.type == pygame.QUIT:
            raise SystemExit("QUIT")

    # рисуем картинку с небом на экране
    screen.blit(sky, (0, 0))
    # перемещаем корабль
    ship.update(left, right, up, down, asteroids)
    # просим корабль нарисоваться
    ship.draw(screen)
    # перемещаем и рисуем каждый астероид в группе
    for asteroid in asteroids:
        if ship.life > 0:
            asteroid.update()
            asteroid.draw(screen)
    # выведем жизнь на экран белым цветом
    if ship.life > 0:
        life = font.render(f'HP: {ship.life}', False, (255, 255, 255))
        screen.blit(life, (20, 20))

    if ship.life <= 0:
        if death_frame == None:
            death_frame = 0
        elif death_frame < 180:
            death_frame += 1
        else:
            raise SystemExit("QUIT")
        game_over = font.render(f'Game Over', False, (255, 255, 255))
        ship.life = 0
        screen.blit(game_over, (infoObject.current_w // 2, infoObject.current_h // 2))

    pygame.display.update()
    clock.tick(60)