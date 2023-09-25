from pygame import *

window = display.set_mode((700, 500))
display.set_caption('Oh God')
pic = transform.scale(image.load('1.jpg'), (700, 500))

GREEN = (0, 255, 0)
wind_len = 700
wind_heig = 500

run = True

class GameSprite(sprite.Sprite):
    def __init__(self, picture, w, h, x, y):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, picture, w, h, x, y, x_speed, y_speed):
        super().__init__(picture, w, h, x, y)
        self.x_speed = x_speed
        self.y_speed = y_speed
    def dvi(self):
        if self.rect.x > 0 and self.x_speed < 0 or self.rect.x < 700-80 and self.x_speed > 0:
            self.rect.x += self.x_speed
        if self.rect.y > 0 and self.y_speed < 0 or self.rect.y < 500-80 and self.y_speed > 0:
            self.rect.y += self.y_speed
    def shoot(self):
        ball = Ball('spy.png', 30, 30, self.rect.x + 25, self.rect.y + 25, vx, vy)
        balls.add(ball)
class Ball(GameSprite):
    def __init__(self, picture, w, h, x, y, vel_x, vel_y):
        super().__init__(picture, w, h, x, y)
        self.vel_x = vel_x
        self.vel_y = vel_y
    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if not (0 <= self.rect.x <= 700 and 0 <= self.rect.y <= 500) or len(sprite.spritecollide(self, walls, False)) != 0:
            self.kill()
        window.blit(self.image, (self.rect.x, self.rect.y))

balls = sprite.Group()
walls = sprite.Group()
enemies = sprite.Group()

window.blit(pic, (0, 0))
hero = Player('pac-10.png', 80, 80, 20, 20, 0, 0)
hero.reset()
enemy = GameSprite('ufo_4.png', 130, 80, 190, 350)
enemy.reset()
enemies.add(enemy)

wall1 = GameSprite('wall.png', 30, 240, 520, 100)
wall2 = GameSprite('wall.png', 120, 20, 350, 100)
wall3 = GameSprite('wall.png', 80, 80, 80, 250)
wall1.reset()
wall2.reset()
wall3.reset()
walls.add(wall1)
walls.add(wall2)
walls.add(wall3)

final = GameSprite('trophy.png', 80, 100, 595, 390)
final.reset()

win = transform.scale(image.load('thumb_1.jpg'), (700, 500))
lose = transform.scale(image.load('game-over-3.jpg'), (700, 500))

finish = False
n = 'up'
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN and e.key == K_UP:
            ball = Ball('spy.png', 50, 50, hero.rect.x + 25, hero.rect.y + 25, 0, - 30)
            balls.add(ball)
        if e.type == KEYDOWN and e.key == K_DOWN:
            ball = Ball('spy.png', 50, 50, hero.rect.x + 25, hero.rect.y + 25, 0, 30)
            balls.add(ball)
        if e.type == KEYDOWN and e.key == K_LEFT:
            ball = Ball('spy.png', 50, 50, hero.rect.x + 25, hero.rect.y + 25, -30, 0)
            balls.add(ball)
        if e.type == KEYDOWN and e.key == K_RIGHT:
            ball = Ball('spy.png', 50, 50, hero.rect.x + 25, hero.rect.y + 25, 30, 0)
            balls.add(ball)
        if e.type == KEYDOWN and e.key == K_RETURN:
            hero.rect.x = 0
            hero.rect.y = 0
            enemies.add(enemy)
            finish = False
    if key.get_pressed()[K_w]:
        hero.y_speed = -5
        hero.dvi()
    elif key.get_pressed()[K_s]:
        hero.y_speed = 5
        hero.dvi()
    elif key.get_pressed()[K_a]:
        hero.x_speed = -8
        hero.dvi() 
    elif key.get_pressed()[K_d]:
        hero.x_speed = 8
        hero.dvi()   
    hero.x_speed = 0
    hero.y_speed = 0
    
    if finish != True:        
        window.blit(pic, (0, 0))
        hero.reset()
        wall1.reset()
        wall2.reset()
        wall3.reset()
        final.reset()
        balls.update()
        balls.draw(window)
        enemies.draw(window)
        if n == 'up':
            if enemy.rect.y > 0:
                enemy.rect.y -= 10
            else:
                n = 'down'
        elif n == 'down':
            if enemy.rect.y < 500 - 80:
                enemy.rect.y += 10
            else:
                n = 'up'
        if sprite.collide_rect(hero, final):
            finish = True
            window.blit(win, (0, 0))
        if sprite.spritecollide(hero, enemies, True):
            finish = True
            window.blit(lose, (0, 0))
        for let in wall1, wall2, wall3:
            if sprite.collide_rect(hero, let):
                window.blit(lose, (0, 0))
                finish = True
        sprite.groupcollide(enemies, balls, True, True)
        sprite.groupcollide(balls, walls, True, False)
    display.update()
