from pygame import *
from random import randint


win_width = 700
win_height = 500

font.init()
font1 = font.Font('Arial', 36)
font2 = font.Font('Arial', 70)
fail = font2.render('YOU LOST!', True, (255,255,255))
wim = font2.render('YOU WON!', True, (255,255,255))

window = display.set_mode((win_width, win_height))
display.set_caption('Shooter Game')
background = transform.scale(image.load('background.jpg'), (win_width, win_height))
lost = 0

class GameSprite(sprite.Sprite):
	def __init__(self, pl_image, pl_x, pl_y, pl_speed, pl_height, pl_weight):
		super().__init__()
		self.image = transform.scale(image.load(pl_image), (pl_weight, pl_height))
		self.speed = pl_speed
		self.rect = self.image.get_rect()
		self.rect.x = pl_x
		self.rect.y = pl_y
	def reset(self):
		window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
	def update(self):
		keys = key.get_pressed()
		if keys[K_LEFT] and self.rect.x > 5:
			self.rect.x -= self.speed
		if keys[K_RIGHT] and self.rect.x < win_width - 80:
			self.rect.x += self.speed
	def fire(self):
		bullet = Bullet('pulya.png', self.rect.centerx, self.rect.top, -15, 20, 20)
		bullets.add(bullet)


class Enemy(GameSprite):
	def update(self):
		self.rect.y += self.speed
		global lost
		if self.rect.y > win_height:
			self.rect.y = -80
			self.rect.x = randint(0, win_width - 80)
			lost += 1

class Bullet(GameSprite):
	def update(self):
		self.rect.y += self.speed
		if self.rect.y < -5:
			self.kill()


player = Player('racket.jpg', 5, 400, 10, 100, 50 )
monsters = sprite.Group()

for i in range(1,6):
	monster = Enemy('nlo.jpg', randint(0, win_width - 80), -80, randint(1, 5), 50, 80)
	monsters.add(monster)

bullets = sprite.Group()

mets = sprite.Group()
for i in range(3):
	met = Enemy('meteorit.jpg', randint(0, win_width - 80), -80, 1, 50, 80)
	mets.add(met)


run = True
FPS = 60
clock = time.Clock()
max_lost = 10 
score = 0
finish = False
life = 3

while run:
	for e in event.get():
		if e.type == QUIT:
			run == False
		elif e.type == KEYDOWN:
			if e.key == K_SPACE:
				player.fire() 
			
				
	

	if not finish:
		window.blit(background, (0,0))
		sprite_list = sprite.groupcollide(monsters, bullets, True, True) 
		if sprite.spritecollide(player, monsters, True) and sprite.spritecollide(player, mets, True):
			life -= 1
		for c in sprite_list:
			score += 1
			monster = Enemy('nlo.jpg', randint(0, win_width - 80), -80, randint(1, 5), 50, 80)
			monsters.add(monster)

		if life <= 0 or lost >= max_lost:
			finish = True
			window.blit(fail, (200,200))
		if score >= 10:
			finish = True
			window.blit(win, (200,200))

		text = font1.render('Счёт: ' + str(score),1, (255,255,255))
		text_lose = font1.render('Пропущено:' + str(lost),1, (255,255,255))
		lifes = font1.render('Жизни:' + str(life), 1, (255,255,255))

		window.blit(text_lose, (10,50))
		window.blit(text, (10,20))
		window.blit(lifes, (550, 10))
		player.update()
		monsters.update()
		mets.update()
		player.reset()
		monsters.draw(window)
		mets.draw(window)
		bullets.draw(window)
		bullets.update()
		display.update() 
	clock.tick(FPS)
		