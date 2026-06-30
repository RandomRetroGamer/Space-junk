
import sys
import multiprocessing




import pygame as py
import math
import random

import time

# Colors
black = (0, 0, 0)


def main():

    red = (255, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    yellow = (255, 255, 0)
    orange = (255, 150, 0)


    random_color_list = [red, white, green, blue, yellow, orange]


    dark_gray = (50, 50, 50)





    py.init()
    py.mixer.init()

    screen_h = 800
    screen_w = 800

    main_block = py.Rect(355, 600, 50, 20)

    screen = py.display.set_mode((screen_w, screen_h))
    py.display.set_caption("Space Junk")

    clock = py.time.Clock()





    class SPlayer(py.sprite.Sprite):

        def __init__(self, x, y, width, height, color):
            super().__init__()

            pos_x, pos_y = 400, 300
            self.color = color  # <-- FIX 1: Save the color attribute!

            self.original_image = py.Surface((width, height), py.SRCALPHA)
        
            triangle_points = [
                (width // 2, 0),       
                (0, height),     
                (width, height) 
            ]

            py.draw.polygon(self.original_image, color, triangle_points)

            self.image = self.original_image.copy()
            self.rect = self.image.get_rect(center=(x, y))

            self.speed = 5
            self.angle = 0

            # Invincibility Variables
            self.is_invisible = False
            self.invisible_timer = 0
            self.invincible_duration = 5000  # <-- FIX 3: 5000ms = 5 seconds

            # Blinking Variables
            self.visible = True
            self.blink_timer = 0 
            self.blink_interval = 150

        def update(self, screen_w, screen_h):
            keys = py.key.get_pressed()
            current_time = py.time.get_ticks()
            moved = False 


            if self.is_invisible:

                if current_time - self.invisible_timer >= self.invincible_duration:
                    self.is_invisible = False
                    self.visible = True

                    self.original_image.fill((0, 0, 0, 0))
                    py.draw.polygon(self.original_image, self.color, [(self.original_image.get_width() // 2, 0), (0, self.original_image.get_height()), (self.original_image.get_width(), self.original_image.get_height())])
                else:
                    if current_time - self.blink_timer >= self.blink_interval:
                        self.visible = not self.visible
                        self.blink_timer = current_time 

                if not self.visible:
                    self.original_image.fill((0, 0, 0, 0))
                else:
                    self.original_image.fill((0, 0, 0, 0))
                    py.draw.polygon(self.original_image, self.color, [(self.original_image.get_width() // 2, 0), (0, self.original_image.get_height()), (self.original_image.get_width(), self.original_image.get_height())])

            if keys[py.K_LEFT] or keys[py.K_a]:
                self.rect.x -= self.speed
                self.angle = 90
                moved = True
                if self.rect.left < 0:
                    self.rect.left = 0

            elif keys[py.K_RIGHT] or keys[py.K_d]:
                self.rect.x += self.speed
                self.angle = 270
                moved = True
                if self.rect.right > screen_w:
                    self.rect.right = screen_w

            elif keys[py.K_UP] or keys[py.K_w]:
                self.rect.y -= self.speed
                self.angle = 0
                moved = True
                if self.rect.top < 0:
                    self.rect.top = 0

            elif keys[py.K_DOWN] or keys[py.K_s]:
                self.rect.y += self.speed
                self.angle = 180
                moved = True
                if self.rect.bottom > screen_h:
                    self.rect.bottom = screen_h

            elif keys[py.K_q]:
                self.angle += 5
                moved = True

            elif keys[py.K_e]:
                self.angle -= 5
                moved = True

            if moved or self.is_invisible:
                old_center = self.rect.center 
                self.image = py.transform.rotate(self.original_image, self.angle)
                self.rect = self.image.get_rect(center=old_center)

        def shoot(self):
            distance = self.original_image.get_height() / 2
            rad = math.radians(self.angle)
            tip_x = self.rect.centerx - (distance * math.sin(rad))
            tip_y = self.rect.centery - (distance * math.cos(rad))
            new_bullet = Bullet(tip_x, tip_y, self.angle)
            return new_bullet

        def trigger_invinciblility(self):
            self.is_invisible = True
            self.invisible_timer = py.time.get_ticks()
            self.blink_timer = py.time.get_ticks()
            self.visible = True


    class Bullet(py.sprite.Sprite):
        def __init__(self, x, y, angle):
            super().__init__()


            self.image = py.Surface((6, 6), py.SRCALPHA)
            py.draw.circle(self.image, random.choice(random_color_list), (3, 3), 4)

            self.rect = self.image.get_rect(center=(x, y))

            self.speed = random.randrange(10, 15)

            random_num = random.randrange(-5, 5)

            self.angle = angle + random_num

            rad = math.radians(self.angle)

            self.dx = -self.speed * math.sin(rad)
            self.dy = -self.speed * math.cos(rad)


        def update(self, *args):
            self.rect.x += self.dx
            self.rect.y += self.dy


            if self.rect.bottom < 0 or self.rect.top > screen_h or self.rect.right < 0 or self.rect.left > screen_w:
                self.kill()


    
    class roids(py.sprite.Sprite):

        def __init__(self, x, y):

            super().__init__()

            self.original_image = py.Surface((random.randrange(10, 40), random.randrange(10, 40)), py.SRCALPHA) 
            self.original_image.fill(random.choice(random_color_list))

            self.image = self.original_image.copy()

            self.rect = self.image.get_rect()

            self.rect.x = x
            self.rect.y = y

            self.speed_x = random.randrange(-3, 3)
            self.speed_y = random.randrange(-3, 3)

            self.angle = 0 
            self.rotation_speed = random.randrange(-5, 5)




        def update(self):

            self.rect.x += self.speed_x
            self.rect.y += self.speed_y


            if self.rect.right >= screen_w:
                self.speed_x = -abs(self.speed_x)
                self.speed_y = random.randrange(-4, 4)
            

            elif self.rect.left <= 0:
                self.speed_x = abs(self.speed_x)
                self.speed_y = random.randrange(-4, 4)


            if self.rect.bottom >= screen_h:
                self.speed_y = -abs(self.speed_y)

            elif self.rect.top <= 0:
                self.speed_y = abs(self.speed_y)


            self.angle = (self.angle + self.rotation_speed) % 360 

            self.image = py.transform.rotate(self.original_image, self.angle)

            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        



    player = SPlayer( 400, 400, 20, 40, red)

    all_sprites = py.sprite.Group()
    all_sprites.add(player)

    game_font = py.font.Font(None, 36)

    bullet_group = py.sprite.Group()

    roids_obj = py.sprite.Group()

    level_0 = random.randrange(5, 10)
    current_level = 0

    multipler = 0

    current_astroids = level_0

    game_life = 3

    clock_num = 60

    def create_astriods(num):

        for i in range(num):

            obj = roids(random.randrange(screen_h - 50), random.randrange(screen_w - 50))
            roids_obj.add(obj)

            print("created junk")

    main_menu = True
    running = True

    create_astriods(level_0)
    while main_menu:
        for event in py.event.get():
            if event.type == py.QUIT:

                main_menu = False
                running = False

            elif event.type == py.KEYDOWN:
                running = True
                player.trigger_invinciblility()
                main_menu = False
    
        dt = clock.tick(60) / 1000.0

        screen.fill(black)

        title = game_font.render("Space junk", True, red)
        screen.blit(title, (screen_w // 2 - title.get_width() // 2, 40))

        dis = game_font.render(" Press any button to continue ", True, white)
        screen.blit(dis, (screen_w // 2 - dis.get_width() // 2, screen_h - 100))

        controls = game_font.render("move: W.A.S.D || right, left, up, down arrow ", True, red)
        screen.blit(controls,(screen_w // 2 - controls.get_width() // 2, screen_h - 200))

        shoot = game_font.render(" Space to shoot ", True, random.choice(random_color_list))
        screen.blit(shoot, (screen_w // 2 - shoot.get_width() // 2, screen_h - 150))


        roids_obj.update()
        roids_obj.draw(screen)

    
        py.display.flip()

    while running:
        for event in py.event.get():
            if event.type == py.QUIT:
                running = False

            elif event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    bullet = player.shoot()
    
                    all_sprites.add(bullet)

                    bullet_group.add(bullet)





        if not player.is_invisible:
            player_hit = py.sprite.spritecollide(player, roids_obj, False)
            if player_hit:
                game_life -= 1 

                print("hit!")
                player.trigger_invinciblility()


        if game_life == 0:


            game_over = game_font.render("GAME OVER", True, red)
            screen.blit(game_over, (screen_w / 2 - game_over.get_width() / 2, 100))

            py.display.flip()

            py.time.wait(5000)
            running = False





        dt = clock.tick(clock_num) / 1000.0


        all_sprites.update(screen_w, screen_h)



        screen.fill(black)

        title = game_font.render("Space junk", True, dark_gray)
        screen.blit(title, (screen_w // 2 - title.get_width() // 2, 20))

        level = game_font.render("level : " + str(current_level), True, red)
        screen.blit(level, (10 // 2, 10))

        game_life_title = game_font.render("HP : " + str(game_life), True, white)
        screen.blit(game_life_title, (screen_w - 100, 10))

        roids_obj.update()
        roids_obj.draw(screen)

        collisions = py.sprite.groupcollide(bullet_group, roids_obj, True, True)

        if collisions:
            current_astroids -=len(collisions)

            print("current", current_astroids)

        if current_astroids == 0:
            current_level += 1
            multipler += 1
            clock_num += 5
            print(clock_num)

            spawn_count = (random.randrange(5 + multipler, 10 + multipler))

            create_astriods(spawn_count)
            current_astroids = spawn_count

            player.trigger_invinciblility()



        all_sprites.draw(screen)
    
        py.display.flip()

    py.quit()


if __name__ == '__main__':
    multiprocessing.freeze_support()  

    main() 