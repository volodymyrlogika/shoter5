from pygame import *
from random import randint

mixer.init()
font.init() #підключаємо шрифти
#створи вікно гри
WIDTH = 900
HEIGHT = 600
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Шутер")
clock = time.Clock()

mixer.music.load("space.ogg")
mixer.music.set_volume(0.5) #задаємо гучність музики
# mixer.music.play() 

font1 = font.SysFont("Impact", 50)
result = font1.render("", True, (255,0,0))

#класи для наших спрайтів
class GameSprite(sprite.Sprite):
   def __init__(self, image_name, x, y, width, height):
      super().__init__()
      self.img = transform.scale(image.load(image_name), (width, height))
      self.rect = self.img.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.width = width
      self.height = height
   
   def draw(self):
      window.blit(self.img, self.rect)

class Player(GameSprite):
   def __init__(self):
      super().__init__("rocket.png", 400, HEIGHT-200, 80, 120)
      self.speed = 5
      self.hp = 100

   def update(self):
      keys = key.get_pressed()
      if keys[K_LEFT] and self.rect.x > 0:
         self.rect.x -= self.speed
      if keys[K_RIGHT] and self.rect.x < WIDTH - self.width:
         self.rect.x += self.speed

class Ufo(GameSprite):
   def __init__(self):
      rand_x = randint(0, WIDTH-120)
      super().__init__("ufo.png", rand_x,  -100, 120, 60)
      self.speed = 3
      self.hp = 100

   def update(self):
      self.rect.y += self.speed

      
bg_image = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))
player = Player()
nlo = Ufo()

run = True
finish = False
FPS = 60
while run:
   window.blit(bg_image, (0,0))
   for e in event.get():
      if e.type == QUIT:
         run = False
   
   player.update() #запускаємо рух гравця
   nlo.update()
   player.draw()
   nlo.draw()

   display.update()
   clock.tick(FPS)
