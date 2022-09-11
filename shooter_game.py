#Створи власний Шутер!

from pygame import *
from random import randint

init()
mixer.init()
font.init() #підключаємо шрифти
#створи вікно гри
WIDTH = 900
HEIGHT = 600
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Shooter")
clock = time.Clock()



font1 = font.SysFont("Impact", 50) #1) створюємо шрифт
result = font1.render("", True, (255,0,0)) #2) створюємо напис шрифтом font1


fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.4) #задаємо гучність музики

#класи для наших спрайтів
class GameSprite(sprite.Sprite):
   def __init__(self, image_name, x, y, width, height):
      super().__init__()
      self.image = transform.scale(image.load(image_name), (width, height))
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
      self.width = width
      self.height = height
   def draw(self):
      window.blit(self.image, self.rect)

class Player(GameSprite):
   def __init__(self):
      super().__init__("rocket.png", 400, HEIGHT-200, 80, 120)
      self.speed = 5
      self.hp = 100
      self.points = 0
      self.bullets = sprite.Group()

   def fire(self): #постріл
      new_bullet = Bullet(self.rect.centerx-7, self.rect.y+5) #сворюємо кулю
      self.bullets.add(new_bullet) #додаємо в групу куль нову кулю
      fire_sound.play()

   def update(self):
      keys = key.get_pressed()
      if keys[K_LEFT] and self.rect.x > 0:
         self.rect.x -= self.speed
      if keys[K_RIGHT] and self.rect.x < WIDTH - self.width:
         self.rect.x += self.speed
      if keys[K_SPACE]: #якщо натиснуто пробіл
         self.fire() #робимо постріл
   

class Ufo(GameSprite):
   def __init__(self):
      rand_x = randint(0, WIDTH-120)
      rand_y = randint(-400, -100)
      super().__init__("ufo.png", rand_x, rand_y, 120, 60)
      self.speed = randint(3,5)
      self.hp = 100

   def update(self):
      self.rect.y += self.speed #постійний рух вниз
      if self.rect.y > HEIGHT + self.height: #якщо ми дійшли до низу вікна
         self.rect.x = randint(0, WIDTH-120) #переносим спрайт 
         self.rect.y = randint(-400, -100) #у випадкові координати нагорі

class Bullet(GameSprite):
   def __init__(self, x, y):
      super().__init__("bullet.png", x, y, 15, 20)
      self.speed = 5

   def update(self):
      self.rect.y -= self.speed #постійний рух вгору
      if self.rect.y < 0 - self.height: #якщо ми дійшли до верху вікна
         self.kill() #видаляє спрайт з гри

bg_image = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))
player = Player()
ufos = sprite.Group() #створюємо групу спрайтів
for i in range(5):
   ufo = Ufo()
   ufos.add(ufo)


#створюємо шрифт
font2 = font.SysFont("Impact", 25)
#створюємо написи
points_text = font2.render("Рахунок: " + str(player.points), True, (255,255,255))
hp_text = font2.render("Життя: " + str(player.hp), True, (255,255,255))

run = True
finish = False
FPS = 60
rand_ufo = 300

while run:
   window.blit(bg_image, (0,0))
   for e in event.get():
      if e.type == QUIT:
         run = False

   if not finish:
      player.update() #рух спрайтів
      ufos.update()
      player.bullets.update() #кулі
      #зіткнення
      #якщо одна з куль стикається з одним з прибульців - вони видаляються
      collides = sprite.groupcollide(ufos, player.bullets, True, True)
      for i in collides: #щоразу як куля стикається з прибульцем
         player.points += 1 #збільшуємо очки
         points_text = font2.render("Рахунок: " + str(player.points), True, (255,255,255))

      collide_list = sprite.spritecollide(player, ufos, True)
      
      rand_num = randint(0, rand_ufo)
      if rand_num == 5:
         ufo = Ufo()    
         ufos.add(ufo)
         if rand_ufo >= 50:
            rand_ufo -= 20

      for kick in collide_list:
         player.hp -= 25 #зменшуємо хп на 25
         hp_text = font2.render("Життя: " + str(player.hp), True, (255,255,255))


      if player.hp <=0:
         finish = True
         result = font1.render("Ви програли!", True, (255,0,0))

      if player.points >= 10:
         finish = True
         result = font1.render("Ви перемогли!", True, (255,0,0))

      player.draw()  #відрисовка спрайтів
      ufos.draw(window)
      player.bullets.draw(window)
      window.blit(points_text, (30,30))
      window.blit(hp_text, (WIDTH - 150,30))
   else:
      window.blit(result, (200, 200))

   display.update()
   clock.tick(FPS)