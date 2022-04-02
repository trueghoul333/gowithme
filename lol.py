from pygame import *
#приииииииивееееееееееееееееееееет

game = True
clock = time.Clock()
okno = display.set_mode((800, 300))
display.set_caption('треш')

back1 = transform.scale(image.load("fon.jpg"), (800, 300))
back2 = transform.scale(image.load("fon.jpg"), (800, 300))
back3 = transform.scale(image.load("fon.jpg"), (800, 300))


class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = transform.scale(image.load(img), (100, 70))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def ris(self):
        knopki = key.get_pressed()
        if knopki[K_RIGHT]:
            okno.blit(transform.flip(self.image, True, False), (self.rect.x, self.rect.y))
        else:
            okno.blit(self.image, (self.rect.x, self.rect.y))


class vesh(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = transform.scale(image.load(img), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def ris(self):
        global pos
        okno.blit(self.image, (self.rect.x + pos, self.rect.y))

class ship(GameSprite):
    def control(self):
        knopka = key.get_pressed()
        if knopka[K_UP] and self.rect.y > 0:
            self.rect.y -= 4
        if knopka[K_DOWN] and self.rect.y < 240:
            self.rect.y += 4

class pula(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = transform.scale(image.load(img), (110, 90))
        self.image = transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def letit(self):
        okno.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x += 6


class pulavraga(sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = transform.scale(image.load(img), (110, 90))
        self.image = transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def letit(self):
        okno.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x -= 6
pv = pulavraga('noj.png', 700, 140)


points = 15

from random import*


class enemy(GameSprite):
    def taran(self):
        self.ris()
        self.rect.x -= 2
        if self.rect.x < 0:
            global points
            points -= 5
            self.rect.y = randint(10, 200)
            self.rect.x = 800


dang = ship("spr.png", 50, 137)

pl = pula('noj.png', 50, 140)

en = [
    enemy('apple.png', 250, 800),
    enemy('apple.png', 250, 800),
    enemy('apple.png', 250, 800)]

strelki = []
for i in range(4):
    en2 = enemy('apple.png', 700, 70* i)
    strelki.append(en2)


finish = False

font.init()
lives = 5
UI = font.Font(None, 40)

mixer.init()
mixer.music.load('music.mp3')
mixer.music.play()

musicon = 1



pos = 0
x1 = 0

boom = mixer.Sound('m111.mp3')

while game:
    if musicon == 1:
        mixer.music.unpause()
    else:
        mixer.music.pause()
    for i in event.get():
        if i.type == QUIT:
            game = False

        if i.type == KEYUP:
            if i.key == K_SPACE and pl.rect.x > 800:
                pl.rect.x = dang.rect.x + 40
                pl.rect.y = dang.rect.y
                boom.play()
            if i.key == K_p:
                if musicon == 1:
                    musicon = 0
                else:
                    musicon = 1
            
    okno.blit(back1, (-800 - x1, 0))
    okno.blit(back2, (0 - x1, 0))
    okno.blit(back3, (800 - x1, 0))
    zhizn = UI.render(str(lives), True, (255, 255, 0))
    ochki = UI.render(str(points), True, (255, 255, 0))
    okno.blit(ochki,(100, 30))
    okno.blit(zhizn, (600, 30))
    dang.ris()
    dang.control()
    pl.letit()
    pv.letit()
    for i in strelki:
        i.ris()
        if sprite.collide_rect(i, pl):
            strelki.remove(i)
            points += 1
        if pv.rect.x < 0:
            shuffle(strelki)
            pv.rect.x = strelki[0].rect.x
            pv.rect.y = strelki[0].rect.y
    if points < 10 and len(strelki) < 4:
        for i in range(4):
            en2 = enemy('apple.png', 700, 70* i)
            strelki.append(en2)


    for i in en:
        i.taran()
        if sprite.collide_rect(i, pl):
            i.rect.y = randint(10, 250)
            i.rect.x = 800
            points += 1
        if sprite.collide_rect(i, dang):
            finish = True
            i.rect.y = randint(10, 250)
            i.rect.x = 800
            lives -= 1
    if lives < 1:
        game = False
    
    x1 += 1
    if x1  > 799:
        x1 = 0
    if x1  < -799:
        x1 = 0
    clock.tick(190)
    display.update()

pisatel = font.Font(None, 70)
text = pisatel.render('You lose!!', True, (0, 0, 0))
mixer.music.pause()
while finish:
    for i in event.get():
        if i.type == QUIT:
            finish = False
    okno.fill((255, 211, 254))
    okno.blit(text, (100, 250))
    display.update()
