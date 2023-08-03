import pygame
from settings import *
from pygame import mixer

pygame.init()
mixer.init()

mixer.music.load("audio/game.wav")
mixer.music.play(-1)
mixer.music.set_volume(0.2)

shoot_sound = mixer.Sound("audio/shoot.wav")
hit_sound = mixer.Sound("audio/hit.wav")
lose_sound = mixer.Sound("audio/lose.wav")
win_sound = mixer.Sound("audio/win.wav")

clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_size, screen_size))

icon = pygame.image.load("images/mini_flower.png")
pygame.display.set_icon(icon)

pygame.display.set_caption("CrazyFlower")
#Photos
#Background_image
background_image = pygame.image.load("images/background.png")
background_image = pygame.transform.scale(background_image, (screen_size, screen_size))

#Player_image
pl_img_0 = pygame.image.load("images/flower_0.png")
pl_img_1 = pygame.image.load("images/flower_1.png")

player_list = [pl_img_0, pl_img_1]

#Snake_image

snake_img_0 = pygame.image.load("images/snake_1.png")
snake_img_1 = pygame.image.load("images/snake_2.png")
snake_img_2 = pygame.image.load("images/snake_3.png")
snake_img_3 = pygame.image.load("images/snake_4.png")
snake_img_4 = pygame.image.load("images/snake_0.png")

snake_list = [snake_img_0, snake_img_1, snake_img_2, snake_img_3, snake_img_4]

#Bird_image
bird_img_0 = pygame.image.load("images/bird_0.png")
bird_img_1 = pygame.image.load("images/bird_1.png")
bird_list = [bird_img_0, bird_img_1]


#Bullet Image
bullet_image = icon

#game_image
game_image = pygame.image.load("images/game.png")

#Score_images
for i in range(11):
    image = pygame.image.load(f"images/{i}.png")
    image = pygame.transform.scale(image, (150, 150))
    score_img.append(image)


#Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, img_list, speed, img_size):
        super().__init__()
        self.img_list = img_list
        self.speed = 0
        self.movement_speed = speed

        for i, img in enumerate(self.img_list):
            img = pygame.transform.scale(img, (img_size, img_size))
            self.img_list[i] = img
        self.image = self.img_list[0]
        self.rect = self.image.get_rect(centerx=screen_size/2, centery=screen_size-170)
        self.counter = 0
        self.shoot = False

    def draw(self):
        if self.shoot and self.counter < fps/3:
            self.image = self.img_list[1]
        else:
            self.image = self.img_list[0]
        screen.blit(self.image, self.rect)


    def shooting(self):
        if not self.shoot and self.counter == 0:
            self.shoot = True
            shoot_sound.play()
            bullet = Bullet(bullet_image, bullet_img_size, bullet_speed)
            bullet_group.add(bullet)
            self.image = self.img_list[1]



    def movement(self):
        self.rect.x += self.speed
        self.speed = 0

        key_list = pygame.key.get_pressed()

        if key_list[pygame.K_RIGHT] or key_list[pygame.K_d]:
            self.speed = self.movement_speed

        if key_list[pygame.K_LEFT] or key_list[pygame.K_a]:
            self.speed = -self.movement_speed

        if key_list[pygame.K_SPACE]:
            self.shooting()

        if self.rect.right >= screen_size - 25:
            self.rect.right = screen_size - 25
        if self.rect.left <= 25:
            self.rect.left = 25


    def update(self):
        self.draw()
        self.movement()

        if self.shoot == True:
            self.counter += 1
        if self.counter > fps * 2:
            self.shoot = False
            self.counter = 0





# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, img, bul_size, speed):
        super().__init__()
        self.image = img
        self.image = pygame.transform.scale(self.image, (bul_size, bul_size))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(centerx=player.rect.centerx, centery=player.rect.centery)
        self.speed = speed

    def movement(self):
        self.rect.centery += self.speed

        if self.rect.top < 30:
            self.kill()

    def update(self):
        global run
        self.movement()

        if pygame.sprite.collide_mask(self, snake):
            snake.hit = True
            score.i += 1
            self.kill()
            hit_sound.play()



#Bird
class Bird(pygame.sprite.Sprite):
    def __init__(self, img_list, img_size):
        super().__init__()
        self.img_list = img_list
        for i, img in enumerate(self.img_list):
            img = pygame.transform.scale(img, (img_size, img_size))
            self.img_list[i] = img
        self.i = 0
        self.image = self.img_list[self.i]
        self.rect = self.image.get_rect(centerx=screen_size-110, centery=screen_size-90)
        self.counter = 0

    def draw(self):
        self.image = self.img_list[self.i]
        screen.blit(self.image, self.rect)

    def update(self):
        global game_over, win
        if self.rect.collidepoint((snake.rect.centerx, snake.rect.centery)):
            game_over = True
            win = False
            snake.speed_x = 0
            lose_sound.play()



        if self.counter <= fps * 2:
            self.counter += 1
        else:
            self.counter = 0
            if self.i == 0:
                self.i = 1
            else:
                self.i = 0

        self.draw()

#Snake
class Snake(pygame.sprite.Sprite):
    def __init__(self, img_list, speed_x, speed_y):
        super().__init__()
        self.img_list = img_list

        self.img_list_left = img_list

        self.img_list_right = []

        for i, img in enumerate(self.img_list):
            img = pygame.transform.scale(img, (150, 150))
            self.img_list[i] = img

        for img in self.img_list_left:
            img = pygame.transform.flip(img, True, False)
            self.img_list_right.append(img)

        self.i = 0
        self.counter = 0
        self.image = self.img_list_right[i]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(centerx=120, centery=80)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.hit = False
        self.hit_counter = 0
        self.previous_speed = 0

    def draw(self):

        if self.speed_x > 0:
            self.img_list = self.img_list_right
        if self.speed_x < 0:
            self.img_list = self.img_list_left

        if self.counter == 0:
            if self.i < len(self.img_list)-2:
                self.i += 1
            else:
                self.i = 0

        self.image = self.img_list[self.i]

        if self.hit:
            self.hit = False
            self.previous_speed = self.speed_x
            self.speed_x = 0

        if self.speed_x == 0:
            snake.image = snake.img_list[-1]
        self.mask = pygame.mask.from_surface(self.image)
        screen.blit(self.image, self.rect)

    def movement(self):
        if self.rect.right >= screen_size - 25 or self.rect.left <= 25:
            self.rect.y += self.speed_y
            self.speed_x *= -1

        if self.speed_x == 0:
            self.hit_counter += 1
        if self.hit_counter > 50:
            self.hit_counter = 0
            self.hit = False
            self.speed_x = self.previous_speed

    def update(self):

        if self.counter < 10:
            self.counter += 1
        else:
            self.counter = 0

        self.draw()
        self.movement()
        self.rect.centerx += self.speed_x


# Score
class Score(pygame.sprite.Sprite):
    def __init__(self, img_list):
        super().__init__()
        self.img_list = img_list
        self.i = 0
        self.image = self.img_list[self.i]
        self.rect = self.image.get_rect(centerx=50, centery=screen_size - 50)

    def draw(self):
        self.image = self.img_list[self.i]
        screen.blit(self.image, self.rect)

    def update(self):
        global game_over, win
        self.draw()
        if self.i == len(self.img_list) - 1:
            game_over = True
            win = True
            self.i = 0
            win_sound.play()

class Button:
    def __init__(self, img):
        self.image = pygame.transform.scale(img, (300, 80))
        self.rect = self.image.get_rect(centerx=screen_size/2, centery=screen_size/2)

    def draw(self):
        screen.blit(self.image, self.rect)

player = Player(player_list, player_speed, player_img_size)
bird = Bird(bird_list, bird_img_size)
snake = Snake(snake_list, snake_speed_x, snake_speed_y)
score = Score(score_img)
button = Button(game_image)
bullet_group = pygame.sprite.Group()
snake_group = pygame.sprite.Group()

snake_group.add(snake)



run = True
while run:
    clock.tick(fps)
    if game_over == False:
        screen.blit(background_image, (0, 0))
        score.update()
        bullet_group.update()
        bullet_group.draw(screen)
        snake_group.update()
        bird.update()
        player.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    if game_over:
        button.draw()
        if button.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]:
            player.rect.center = (screen_size/2, screen_size-170)
            snake.rect.center = (120, 80)
            snake.img_list = snake.img_list_right
            if win:
                snake.speed_x = abs(snake.speed_x) + 2
                win = False
            else:
                snake_speed_x = abs(snake_speed_x)
            game_over = False

    pygame.display.update()

pygame.quit()