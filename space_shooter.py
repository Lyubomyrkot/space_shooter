from pygame import *
import random 

init()
font.init()
#mixer.init()


FONT = "Play-Bold.ttf"

FPS = 60

scr_info = display.Info()
WIDTH, HEIGHT = scr_info.current_w, scr_info.current_h
window = display.set_mode((WIDTH, HEIGHT), flags=FULLSCREEN)
display.set_caption("Space_shooter")#назва вікна
clock = time.Clock()

#завантаження картинок
bg = image.load("image/background.jpg")
bg = transform.scale(bg, (WIDTH, HEIGHT))

player_img = image.load("image/player1.png")
player_blinck_img = image.load("image/player_blinck1.png")
enemy_img = image.load("image/enemy.png")
enemy_img1 = image.load("image/enemy1.png")
fire_img = image.load("image/player.png")
#coin_img = image.load("image/coin.png")
all_sprites = sprite.Group()
all_labels = sprite.Group()

#завантаження музики
#mixer.music.load("jungles.ogg")
#mixer.music.set_volume(0.2)
#mixer.music.play()

#fire_sound = mixer.Sound("kick.ogg")
#fire_sound.set_volume(0.5)
#money_sound = mixer.Sound("money.ogg")

#створення класу для тексту
class Label(sprite.Sprite):
    def __init__(self, text, x, y, fontsize = 30, color = (255, 255, 255), font_name = FONT):
        super().__init__()
        self.color = color
        self.font = font.Font(FONT, fontsize)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        all_labels.add(self)

    def set_text(self, new_text,color=(255, 255, 255)):
        self.image = self.font.render(new_text, True, color)


#створення класу для спрайтів
class BaseSprite(sprite.Sprite):
    def __init__(self, image, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x, y, width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)


    def draw(self, window):
        window.blit(self.image, self.rect)



#створення класу гравця
class Player(BaseSprite):
    def __init__(self, image, x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.original = self.image
        self.blinck_img = transform.scale(player_blinck_img, (width, height))
        self.speed_x = 10
        self.speed_y = 3
        self.max_speed = 15
        self.hp = 100
        self.score = 0
        self.damage_timer = time.get_ticks()#фіксуєм час від початку гри
        self.rect.centerx = x
        self.bullets = sprite.Group()
        self.fire_timer = time.get_ticks()
        self.blinck = False
        self.blinck_timer = time.get_ticks()


    def fire(self):
        bullet = Bullet(self.rect, fire_img, 20, 20)
        self.bullets.add(bullet)
        #fire_sound.play()


    
    def update(self):
        old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()


        if keys[K_SPACE]:
            now = time.get_ticks()
            if now - self.fire_timer > 300:
                self.fire_timer = now
                self.fire() 

        if keys[K_ESCAPE]:
            run = False

        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed_x

        if keys[K_d] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed_x

        if keys[K_w] and self.rect.y > 0:
            if self.speed_y < self.max_speed:
                self.speed_y += 0.1
            if self.rect.y > HEIGHT // 2:
                self.rect.y -= self.speed_x

        if keys[K_s] and self.rect.y < HEIGHT and self.speed_y>0:
            self.speed_y -= 0.25
            if self.rect.bottom < HEIGHT:
                self.rect.y += self.speed_x

        if not keys[K_w] and self.speed_y > 3:
            self.speed_y -= 0.1


        coll_list = sprite.spritecollide(self, enemy_group, False, sprite.collide_mask)
        if len(coll_list)>0:
            now = time.get_ticks()
            if now-self.damage_timer > 1000:
                self.damage_timer = time.get_ticks() #обнуляємо таймер дамагу
                self.hp -= 10 #віднімаємо HP
                self.blinck = True
                self.blinck_timer = time.get_ticks()
                hp_label.set_text(f"HP: {self.hp}")
        
        if self.blinck:
            self.image = self.blinck_img

            if time.get_ticks() - self.blinck_timer > 500:
                self.blinck = False
                self.image = self.original
            

        
                

#створення класу ворога
class Enemy(BaseSprite):
    def __init__(self, image, width, height):
        x = random.randint(0, WIDTH - width)
        y = random.randint(400, HEIGHT) * -1
        super().__init__(image, x, y, width, height)
        self.speed_x = 10
        self.speed_y = 3
        self.max_speed = 15
        self.hp = 100
    
    def update(self):
        self.rect.y += self.speed_y + player.speed_y
        if self.rect.y > HEIGHT:
            self.kill()
        
class Bullet(BaseSprite):
    def __init__(self, player_rect, image, width, height):
        super().__init__(image, player_rect.x, player_rect.y, width, height)
        self.speed_y = 10
        self.rect.bottom = player_rect.top
        self.rect.centerx = player_rect.centerx
    
    def update(self):
        self.rect.y -= self.speed_y
        if self.rect.bottom < 0:
            self.kill()



player = Player(player_img, WIDTH // 2, HEIGHT-200, 50, 50)

finish = False
run = True

bg1_y = 0
bg2_y = -HEIGHT

result = Label("", 300, 300, fontsize=70)
restart = Label("Press R to restart", 300, 450, fontsize=40)
all_labels.remove(restart)
hp_label = Label(f"HP: {player.hp}", 10, 10)
score_label = Label(f"HP: {player.score}", 10, 40)

spawn_time = time.get_ticks()
enemy_group = sprite.Group()
max_spawn_time = 1000

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False


    if not finish:
        all_sprites.update()
        now = time.get_ticks()
        if now - spawn_time > random.randint(400, max_spawn_time):
            spawn_time = now
            enemy_img_rand = random.choice([enemy_img, enemy_img1])
            enemy_count = random.randint(1,2)
            for i in range(enemy_count):
                enemy_group.add(Enemy(enemy_img_rand, 60, 60))

        collide_list = sprite.groupcollide(enemy_group, player.bullets, True, True)
        for enemy in collide_list:
            player.score += 10
            score_label.set_text(f"Score: {player.score}")
            #money_sound.play()

        if player.hp <= 0:
            finish = True
            result.set_text("Game over")
            all_labels.add(restart)
            player.kill()
            for e in enemy_group:
                e.kill()
        bg1_y += player.speed_y
        bg2_y += player.speed_y
        if bg1_y > HEIGHT:
            bg1_y = -HEIGHT
        if bg2_y > HEIGHT:
            bg2_y = -HEIGHT
    window.blit(bg, (0, bg1_y))
    window.blit(bg, (0, bg2_y))

    all_sprites.draw(window)
    all_labels.draw(window)

    display.update()
    clock.tick(FPS)