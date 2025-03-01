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

player_img = image.load("image/player.png")
enemy_img = image.load("image/enemy.png")
#coin_img = image.load("image/coin.png")
all_sprites = sprite.Group()
all_labels = sprite.Group()

#завантаження музики
#mixer.music.load("jungles.ogg")
#mixer.music.set_volume(0.2)
#mixer.music.play()

#kick_sound = mixer.Sound("kick.ogg")
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
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed_x = 10
        self.speed_y = 3
        self.hp = 100
        self.damage_timer = time.get_ticks()#фіксуєм час від початку гри
        self.rect.centerx = x
    
    def update(self):
        old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_ESCAPE]:
            run = False
        if keys[K_w] and self.rect.y > 0:
            if self.speed_y < 15:
                self.speed_y += 0.25
            #self.rect.y -= self.speed_y
        if keys[K_s] and self.rect.y < HEIGHT - self.rect.height:
            self.speed_y = 5
            #self.rect.y += self.speed_y
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed_x
            self.image = self.left_image
        if keys[K_d] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed_x
            self.image = self.right_image
        
        if not keys[K_w] and self.speed_y > 3:
            self.speed_y -= 0.1


player = Player(player_img, WIDTH // 2, HEIGHT-200, 70, 70)

finish = False
run = True

bg1_y = 0
bg2_y = -HEIGHT


while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                run = False

    if not finish:
        all_sprites.update()
    
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