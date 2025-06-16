import pygame
from pygame.locals import *
import time
import requests
from random import choice, randint
from easygui import msgbox, enterbox, buttonbox

# ВАША ССЫЛКА НА ПАПКУ С ИГРОЙ
link = 'c:/Games/CATS VS YOU/CATS VS YOU'

Secret_code = enterbox('Укажите ссылку на папку "CATS VS YOU" в девятой строке кода\n\n Управление: wasd\n Котиков можно испепелять лазером, но длина лазера ограничена (Лазер — удерживать ЛКМ. Если не видно, значит не хватает длины)\n Зелёные снаряды можно разрезать лазером\n У вас 5 жизней (красная шкала внизу)\n Жмите Ок')
color_laser = buttonbox(' Выберите персонажа:', choices=(('Дарт Вейдер'), ('Пикачу'), ('Заяц'), ('Перри-утконос'), ('Бобр')))
hero = {'Дарт Вейдер': link + '/Images/Dart_Veyder.jpg','Пикачу': link + '/Images/Pokemon.jpg','Заяц': link + '/Images/Zayac.jpg','Перри-утконос': link + '/Images/Perry.jpg','Бобр': link + '/Images/Bobr_k....jpg'}[color_laser]
color_laser = {'Дарт Вейдер': (255, 0, 0), 'Пикачу': (255, 255, 0), 'Заяц': (0, 255, 0), 'Перри-утконос': (255, 0, 255), 'Бобр': (255, 69, 0)}[color_laser]
if Secret_code == 'Secret':
    hero = link + '/Images/Secret.jpeg'
    color_laser = (0, 255, 255)

link = link + '/1.jpeg'

fon = pygame.image.load(link[:-6] + 'Images/Что за цирк....jpg')
fon_rect = fon.get_rect()
N = 10

class Laser:


    def __init__(self, color_laser):
        self.laser = False
        self.col_laser = color_laser
        self.end_laser = (0, 0)
    
    def active(self, event):
        if event.type == MOUSEBUTTONDOWN:
            self.laser = True
            self.end_laser = event.pos
        if event.type == MOUSEMOTION and self.laser:
            self.end_laser = event.pos
        if event.type == MOUSEBUTTONUP:
            self.laser = False
            self.end_laser = event.pos
    
    def draw(self, screen, coordinates):
        if self.laser:
            len_laser = ((self.end_laser[0] - (coordinates[0] + 39))**2 + (self.end_laser[1] - (coordinates[1] + 39))**2)**0.5
            if len_laser <= 301:
                pygame.draw.lines(screen, self.col_laser, True, ((coordinates[0] + 39, coordinates[1] + 39), self.end_laser), 3)
    
    def get_end_laser(self):
        return self.end_laser
    
    def get_laser(self):
        return self.laser
    
    def get_len_laser(self, coordinates):
        return ((self.end_laser[0] - (coordinates[0] + 25))**2 + (self.end_laser[1] - (coordinates[1] + 13))**2)**0.5
    


class Player:


    def __init__(self):
        self.img_player = pygame.image.load(hero)
        self.player = self.img_player.get_rect()
        self.player.center = (650, 500)
        self.up = (0, 0)
        self.down = (0, 0)
        self.left = (0, 0)
        self.right = (0, 0)
        self.kol_hearts = 7
        self.hearts = Rect(10, 950, self.kol_hearts * 50, 40)
    
    def moving(self, event):
        if event.type == KEYDOWN:
            if event.key == K_w:
                self.up = (0, -1)
            if event.key == K_s:
                self.down = (0, 1)
            if event.key == K_a:
                self.left = (-1, 0)
            if event.key == K_d:
                self.right = (1, 0)
        
        if event.type == KEYUP:
            if event.key == K_w:
                self.up = (0, 0)
            if event.key == K_s:
                self.down = (0, 0)
            if event.key == K_a:
                self.left = (0, 0)
            if event.key == K_d:
                self.right = (0, 0)
                
    def update(self):   
        self.player.move_ip(self.up)
        self.player.move_ip(self.down)
        self.player.move_ip(self.left)
        self.player.move_ip(self.right)
    
    def draw(self, screen):
        screen.blit(self.img_player, self.player)
        pygame.draw.rect(screen, color_laser, self.player, 1)
        time.sleep(0.007)
    
    def get_coordinates(self):
        return [self.player.x, self.player.y]
    
    def injured(self, bullets, screen):
        if len(bullets) > 0:
            i = 0
            while i < len(bullets):
                if self.player.colliderect(bullets[i].get_rect()):
                    self.kol_hearts -= 1
                    self.hearts = Rect(10, 950, self.kol_hearts * 50, 40)
                    bullets.pop(i)
                    screen.fill((100, 0, 0))
                    pygame.display.flip()
                    time.sleep(0.001)
                    i -= 1
                    if self.kol_hearts == 0:
                        return '0'
                i += 1
    
    def draw_hearts(self, screen):
        pygame.draw.rect(screen, (150, 0, 0), self.hearts, 0)


class Enemies:

    def __init__(self, amount_enemies):
        self.time_start = time.time()
        self.t = 5
        self.num_enemy = -1
        self.enemy = []
        self.img_enemy = []
        self.time_damage = []
        self.first_touch = []
        self.colors = [(255, 0, 0), (255, 20, 147), (255, 69, 0), (255, 255, 0), (255, 0, 255), (0, 255, 0), \
                       (30, 144, 255), (0, 255, 255)]
        self.colors_enemies = []
        self.ramki_enemies = []
        self.moving = []
        self.speed = []
        for i in range(amount_enemies):
            cat_from_internet = requests.get('https://cataas.com/cat?type=xsmall')
            with open(link, 'wb') as file:
                file.write(cat_from_internet.content)
            self.img_enemy.append(pygame.image.load(link))
            cat = self.img_enemy[i].get_rect()
            cat.center = choice([(250, 200), (1050, 200), (250, 800), (1050, 800)])
            self.enemy.append(cat)
            self.time_damage += [0]
            self.first_touch += [0]
            self.colors_enemies += [choice(self.colors)]
            self.ramki_enemies += [1]
            self.moving += [0]
            self.speed += [(0, 0)]

        self.bullets_speeds_canbe = [(2, 0), (2, 2), (0, 2), (-2, 2), (-2, 0), (-2, -2), (0, -2), (2, -2)]
        self.Bullets = []
        self.timer_bullets = 0
        self.bullets_speeds = []
        self.green_or_orange = [1]
        self.victory = 0
        

    
    def draw(self, screen):
        if self.num_enemy < len(self.enemy) - 1:
            if (time.time() - self.time_start) > self.t:
                self.num_enemy += 1
                self.t += 7
                if self.green_or_orange[-1] == 1:
                    self.green_or_orange += [0]
                else:
                    self.green_or_orange += [1]
        if self.num_enemy >= 0:
            for p in range(self.num_enemy + 1):
                screen.blit(self.img_enemy[p], self.enemy[p])
                pygame.draw.rect(screen, self.colors_enemies[p], self.enemy[p], self.ramki_enemies[p])
                if self.moving[p] == 0:
                    self.moving[p] = 1
    
    def burn(self, laser, end_laser, len_laser):
        if laser:
            if self.num_enemy >= 0 and len_laser <= 301:
                    i = 0
                    while i < self.num_enemy + 1:
                        if self.enemy[i].collidepoint(end_laser):
                            if self.first_touch[i] == 0:
                                self.first_touch[i] = time.time()

                            self.time_damage[i] += int(time.time() - self.first_touch[i])
                            self.ramki_enemies[i] += int((time.time() - self.first_touch[i]) / 1.5)
                            if self.time_damage[i] > 150:
                                self.enemy.pop(i)
                                self.img_enemy.pop(i)
                                self.first_touch.pop(i)
                                self.time_damage.pop(i)
                                self.colors_enemies.pop(i)
                                self.ramki_enemies.pop(i)
                                self.num_enemy -= 1
                                self.moving.pop(i)
                                self.green_or_orange.pop(i)
                                self.victory += 1
                        i += 1
                    
                    j = 0
                    while j < len(self.Bullets):
                        if self.Bullets[j].get_size() == 30:
                            if self.Bullets[j].get_rect().collidepoint(end_laser):
                                self.Bullets.pop(j)
                                self.bullets_speeds.pop(j)
                                j -= 1
                        j += 1
    
    def update(self):
        for i in range(self.num_enemy + 1):
            a = self.enemy[i].x
            b = self.enemy[i].y
            if a <= 0:
                self.speed[i] = (1, 0)
            elif b <= 0:
                self.speed[i] = (0, 1)
            elif a >= 1300:
                self.speed[i] = (-1, 0)
            elif b >= 1000:
                self.speed[i] = (0, -1)
            else:
                if self.moving[i] % 100 == 0:
                    self.speed[i] = (randint(-1, 1), randint(-1, 1))
            self.moving[i] += 1
            self.enemy[i].move_ip(self.speed[i][0], self.speed[i][1])
        
    def update_bullets(self, pl_coord):
        if self.timer_bullets % 120 == 0:
            k = -1
            for i in range(self.num_enemy + 1):
                if self.green_or_orange[i] == 1:
                    for j in range(8):
                        self.Bullets += [Bullet(self.enemy[i].x, self.enemy[i].y, 7)]
                        k += 1
                        self.bullets_speeds += [self.bullets_speeds_canbe[k]]
                        if k % 7 == 0 and k != 0:
                            k = -1
                else:
                    if self.timer_bullets % 360 == 0:
                        self.Bullets += [Bullet(self.enemy[i].x, self.enemy[i].y, 30)]
                        self.bullets_speeds += [(2.5, 2.5)]

        
        bul = 0
        while bul < len(self.Bullets):
            X = self.Bullets[bul].get_coordinates()[0]
            Y = self.Bullets[bul].get_coordinates()[1]
            if X < 0 or Y < 0 or X > 1300 or Y > 1000:
                self.Bullets.pop(bul)
                self.bullets_speeds.pop(bul)
                bul -= 1
            bul += 1

        for p in range(len(self.Bullets)):
            self.Bullets[p].update(self.bullets_speeds[p], pl_coord)
    
        self.timer_bullets += 1
            
    def draw_bullets(self, screen):
        for i in self.Bullets:
            i.draw(screen)
    
    def get_bullets(self):
        return self.Bullets
    
    def get_victory(self):
        return self.victory
    

class Game:


    def __init__(self):
        self.screen = pygame.display.set_mode((1300, 1000))
        self.player = Player()
        self.laser = Laser(color_laser)
        self.enemies = Enemies(N)
        self.url_quote = 'http://api.forismatic.com/api/1.0/'
        self.params = {'method': 'getQuote', 'format': 'json', 'lang': 'ru'}
        self.running = True
        self.living = True
    
    def run(self):
        while self.running == True:

            for event in pygame.event.get():
                if self.living == False or event.type == QUIT:
                    self.running = False
                    for i in range(10):
                        if i % 2 == 0:
                            self.screen.fill((0, 0, 0))
                        else:
                            self.screen.fill((100, 0, 0))
                        pygame.display.flip()
                        time.sleep(0.05)
                    important_words = requests.get(self.url_quote, params=self.params)
                    msgbox('Игра окончена. Вывод:\n\n' + important_words.text[13:-87].replace('"quoteAuthor":', '\n\n                                                  '))
                    pygame.display.quit()
                
                self.player.moving(event)
                self.laser.active(event)
            
            if self.enemies.get_victory() == N:
                pobeda = pygame.image.load(link[:-6] + 'Images/Победа!.jpg')
                pobeda_rect = pobeda.get_rect()
                pobeda_rect.center = (650, 500)
                self.screen.fill((255, 255, 255))
                self.screen.blit(pobeda, pobeda_rect)
                pygame.display.flip()
                important_words = requests.get(self.url_quote, params=self.params)
                msgbox('Игра окончена. Вывод:\n\n' + important_words.text[13:-87].replace('"quoteAuthor":', '\n\n                                                  '))
                pygame.display.quit()

            if self.player.injured(self.enemies.get_bullets(), self.screen) == '0':
                self.living = False
            self.update()
            self.draw()
    
    def update(self):
        self.player.update()
        self.enemies.update()
        self.enemies.burn(self.laser.get_laser(), self.laser.get_end_laser(), self.laser.get_len_laser(self.player.get_coordinates()))
        self.enemies.update_bullets(self.player.get_coordinates())

    def draw(self):
        self.screen.blit(fon, fon_rect)
        self.player.draw_hearts(self.screen)
        self.player.draw(self.screen)
        self.enemies.draw(self.screen)
        self.enemies.draw_bullets(self.screen)
        self.laser.draw(self.screen, self.player.get_coordinates())
        pygame.display.flip()


class Bullet:

    def __init__(self, x, y, size):
        self.size = size
        self.bullet = Rect(x , y, self.size, self.size)
    
    def update(self, bul_speed, pl_coord):
        if self.size == 30:
            if self.bullet.x >= pl_coord[0] and self.bullet.y >= pl_coord[1]:
                self.bullet.move_ip(-2, -2)
            elif self.bullet.x >= pl_coord[0] and self.bullet.y <= pl_coord[1]:
                self.bullet.move_ip(-2, 2)
            elif self.bullet.x <= pl_coord[0] and self.bullet.y >= pl_coord[1]:
                self.bullet.move_ip(2, -2)
            elif self.bullet.x <= pl_coord[0] and self.bullet.y <= pl_coord[1]:
                self.bullet.move_ip(2, 2)
        else:
            self.bullet.move_ip(bul_speed[0], bul_speed[1])

    def draw(self, screen):
        if self.size == 7:
            pygame.draw.rect(screen, (255, 69, 0), self.bullet, 0)
        else:
            pygame.draw.rect(screen, (0, 129, 0), self.bullet, 0)
    
    def get_coordinates(self):
        return (self.bullet.x, self.bullet.y)
    
    def get_rect(self):
        return self.bullet
    
    def get_size(self):
        return self.size


if __name__ == '__main__':
    Game().run()