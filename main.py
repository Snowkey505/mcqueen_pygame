# Автор программы: Сойников Павел, ИУ7-24Б
# Назначение программы: циклическая анимация на pygame


import pygame as pg
from math import sin, cos, pi

W = 1200
H = 700

# Цвета, FPS
WHITE = (255, 255, 255)
BLUE_SKY = (190, 215, 255)
DARK_SKY = (15, 40, 80)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_GREY = (20, 20, 20)
GREY = (50, 50, 50)
LIGHT_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 120


# Вращение координат относительно точки на угол
def rotated_coordinates(x, y, x0, y0, a):
    x_new = (x - x0) * cos(a) - (y - y0) * sin(a) + x0
    y_new = (x - x0) * sin(a) + (y - y0) * cos(a) + y0
    return x_new, y_new


# Вращение полигона относительно точки на угол
def rotate_polygon(coords, x0, y0, a0):
    a = a0 * pi / 180
    for i in range(len(coords)):
        x_, y_ = rotated_coordinates(coords[i][0], coords[i][1], x0, y0, a)
        coords[i][0] = x_
        coords[i][1] = y_


# Отрисовка по кругу n секторов (аналогично спицам на колесе, a - угол поворота)
def draw_n_sectors(s, x, y, n, w0, h0, w1, h1, a, color):
    coords = [[x-w0, y-h0], [x+w0, y-h0], [x+w1, y-h1], [x-w1, y-h1]]
    rotate_polygon(coords, x, y, a)
    for i in range(n):
        pg.draw.polygon(s, color, coords)
        rotate_polygon(coords, x, y, 360 / n)


# Отрисовка колеса
def draw_wheel(sc, x, y, a):
    pg.draw.circle(sc, DARK_GREY, (x, y), 66)
    pg.draw.circle(sc, GREY, (x, y), 58, 11)
    pg.draw.circle(sc, RED, (x, y), 40, 30)
    pg.draw.circle(sc, BLACK, (x, y), 37, 2)
    draw_n_sectors(sc, x, y, 7, 5, 31, 3, 14, a, BLACK)
    draw_n_sectors(sc, x, y, 5, 12, 60, 7, 40, a, BLACK)

    pg.draw.circle(sc, RED, (x, y), 23, 3)
    pg.draw.circle(sc, BLACK, (x, y), 21, 2)
    pg.draw.circle(sc, RED, (x, y), 19, 2)


def fire_draw(sc, x, y):
    f_rect_1 = fire.get_rect(bottomleft=(x + 188, y + 18))
    sc.blit(fire, f_rect_1)
    f_rect_2 = fire.get_rect(bottomleft=(x + 158, y + 15))
    sc.blit(fire, f_rect_2)


# Отрисовка маккуина
def draw_mcqueen(mcq, sc, x, y, a, with_fire):
    mc_rect = mcq.get_rect(bottomleft=(x, y))
    sc.blit(mcq, mc_rect)
    draw_wheel(sc, x + 155, y-63, a)
    draw_wheel(sc, x + 529, y-63, a+11)
    if with_fire:
        fire_draw(sc, x, y)


# Отрисовка фона
def draw_phone(phon, sc, x, y, vis):
    phon.set_alpha(vis)
    phone_rect = phon.get_rect(bottomleft=(x, y))
    sc.blit(phon, phone_rect)


# Отрисовка фона, сменяющего день и ночь
def draw_phone_day_night(day_p, night_p, surf, x, y, vis):
    draw_phone(day_p, surf, -x, y, vis)
    draw_phone(day_p, surf, W - x, y, vis)

    draw_phone(night_p, surf, -x, y, 255 - vis)
    draw_phone(night_p, surf, W - x, y, 255 - vis)


def drive():
    pg.mixer.init()
    pg.mixer.music.load('Nightcall.mp3')
    pg.mixer.music.play(-1)


pg.init()
sc = pg.display.set_mode((W, H))

mcqueen = pg.image.load("lightning-mcqueen.png")
day_ph = pg.image.load("stone-and-rocks.jpg")
night_ph = pg.image.load("stone_night.jpg")
fir = pg.transform.scale(pg.image.load("fire.png"), (85, 45))
fire = pg.transform.rotate(fir, 195)
day_ph = pg.transform.scale(day_ph, (W, H))
night_ph = pg.transform.scale(night_ph, (W, H))


phoneSc = pg.Surface((W, H))
opened = True
first = True
a = 0
phone_s = 0
x = 300
fire_cnt = 0
y = 600
vis = 255
cnt = 0
day = True
HIGHWAY = DARK_GREY

drive()
while opened:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            opened = False
            pg.quit()  # Выход
        elif event.type == pg.MOUSEBUTTONDOWN:
            fire_cnt = 1
            pg.mixer.init()
            kchew = pg.mixer.Sound("kchau.mp3")
            kchew.play()

    if opened:  # Цикл
        if not day:
            vis = 255 - cnt  # Прозрачность для наложения фото дня и ночи
        else:
            vis = cnt

        if fire_cnt > 0:
            fire_cnt += 1

        if fire_cnt > 25:
            fire_cnt = 0

        draw_phone_day_night(day_ph, night_ph, phoneSc, phone_s, 700, vis)
        sc.blit(phoneSc, (0, 0))
        draw_mcqueen(mcqueen, sc, x, y, a, fire_cnt)
        pg.draw.rect(sc, HIGHWAY, (0, H - 98, W, H))

        a += 17
        phone_s += 40
        if phone_s == W:
            phone_s = 0

        cnt += 1

        if cnt % 2 == 0:
            x += 2
        else:
            x -= 2

        if day and cnt == 700:
            day = False
            cnt = 0

        if not day and cnt == 700:
            day = True
            cnt = 0

        # Изменение цвета дороги утром и вечером
        if 125 < cnt <= 250 and HIGHWAY[0] < 100 and day:
            HIGHWAY = HIGHWAY[0] + 1, HIGHWAY[1] + 1, HIGHWAY[2] + 1

        elif 125 < cnt <= 250 and HIGHWAY[0] > 20 and not day:
            HIGHWAY = HIGHWAY[0] - 1, HIGHWAY[1] - 1, HIGHWAY[2] - 1

        pg.display.flip()
    pg.time.Clock().tick(FPS)