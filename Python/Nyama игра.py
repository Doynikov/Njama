import pygame as pg
import random
import threading

pg.init()

pg.font.init()

default_screen_width = 1024
default_screen_height = 768
screen_step_k = 1

screen = pg.display.set_mode((default_screen_width, default_screen_height), pg.RESIZABLE)
screen_width, screen_height = screen.get_size()
bg_image_load = pg.image.load('assets/images/bg.jpg').convert()
bg_image = pg.transform.scale(bg_image_load, (screen_width, screen_height))

screen.blit(bg_image, (0, 0))
nam_bang = pg.image.load('assets/images/nyama_bang.png').convert_alpha()
nam_die = pg.image.load('assets/images/nyama_die.png').convert_alpha()
nam_normal = pg.image.load('assets/images/nyama_norm.png').convert_alpha()
nam_red = pg.image.load('assets/images/nyama_red.png').convert_alpha()
nam_die_dn = pg.image.load('assets/images/nyama_die_dn.png').convert_alpha()
bang_image = pg.image.load('assets/images/bang.png').convert_alpha()
nam_njam = pg.image.load('assets/images/nyama_njam.png').convert_alpha()
nam_press = pg.image.load('assets/images/nyama_press.png').convert_alpha()
nam_jump = pg.image.load('assets/images/nyama_fly.png').convert_alpha()
gift_hide = pg.image.load('assets/images/gift_hide.png').convert_alpha()
nam_wall_left = pg.image.load('assets/images/nyama_wall_left.png').convert_alpha()
nam_wall_right = pg.image.load('assets/images/nyama_wall_right.png').convert_alpha()
nam_die_up_star = pg.image.load('assets/images/nyama_die_up_star.png').convert_alpha()
nam_down_star = pg.image.load('assets/images/nyama_down_star.png').convert_alpha()
intro_image = pg.image.load('assets/images/intro.png').convert_alpha()
rat_image_l = pg.image.load("assets/images/rat_big_l.png").convert_alpha()
rat_image_r = pg.image.load("assets/images/rat_big_r.png").convert_alpha()
rat_die = pg.image.load("assets/images/rat_die.png").convert_alpha()
rat_break = pg.image.load("assets/images/rat_break.png").convert_alpha()
nam_blood_1 = pg.image.load("assets/images/nyama_blood_1.png").convert_alpha()
nam_blood_2 = pg.image.load("assets/images/nyama_blood_2.png").convert_alpha()

bang_snd = pg.mixer.Sound('assets/sounds/bang.mp3')
wall_fall_snd = pg.mixer.Sound('assets/sounds/wall_fall.mp3')
wall_hit_snd = pg.mixer.Sound('assets/sounds/wall_hit.mp3')
fu_snd = pg.mixer.Sound('assets/sounds/fu.mp3')
eat_snd = pg.mixer.Sound('assets/sounds/eat.mp3')
boom_dzin_snd = pg.mixer.Sound('assets/sounds/boom-dzin.mp3')
boom_up_down_snd = pg.mixer.Sound('assets/sounds/boom-up-down.mp3')
rat_eat_snd = pg.mixer.Sound('assets/sounds/rat_eat.mp3')
rat_cry_snd = pg.mixer.Sound('assets/sounds/rat_cry.mp3')

gifts_image_list = [
    {'name': 'bomb', 'img': pg.image.load('assets/images/bomb.png').convert_alpha()},
    {'name': "candy_red", 'img': pg.image.load("assets/images/candy_red.png").convert_alpha()},
    {'name': "candy_green", 'img': pg.image.load("assets/images/candy_green.png").convert_alpha()},
    {'name': "cake", 'img': pg.image.load("assets/images/cake.png").convert_alpha()},
    {'name': "brick", 'img': pg.image.load("assets/images/brick.png").convert_alpha()}
]
gifts_list = []
thread_list = []

step_nam = 4
step_jump_nam = 5
step_fall_nam = 7
delay_fall_gift = 1
lives_start_count = 4
lives_max_count = 8
step_gift_by_list_level = [0, 2, 5]

sound_active = True


class Rat(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = rat_image_l
        self.rect = self.image.get_rect(center=(x, y))
        self.direct = 'right'
        self.active = True
        self.move_action = True
        self.eat_action = False
        self.bomb_action = False
        self.press_action = False
        self.step = 2
        self.step_count = 0
        self.eat_delay_counter = 0
        self.bomb_delay_counter = 0
        self.press_delay_counter = 0

    def eat(self):
        self.eat_delay_counter += 1

        if self.eat_delay_counter == 1:
            nyama.change_img(nam_blood_1, 1)
            play_sounds(rat_eat_snd, True)
            nyama.active = False
            self.move_action = False

        if self.eat_delay_counter == 40:
            nyama.change_img(nam_blood_2, 1)

        if self.eat_delay_counter == 80:
            nyama.change_img(nam_die, 1)
            nyama.rect.centery = screen_height - 50
            rat_eat_snd.stop()
            self.active = True
            self.move_action = True
            lives_text.draw_lives(-1)

        if self.eat_delay_counter == 120:
            if self.direct == 'left':
                self.rect.x -= 150
            else:
                self.rect.x += 150
            update()

        if self.eat_delay_counter == 500:
            self.eat_delay_counter = 0
            self.eat_action = False
            nyama.active = True
            nyama.rect.centerx = screen_width/2
            nyama.set_normal()

    def pressed(self):
        self.press_delay_counter += 1
        if self.press_delay_counter == 1:
            rat.image = rat_die
            nyama.rect.bottom = screen_height - 40
            play_sounds(rat_cry_snd, True)
            self.move_action = False
            self.eat_action = False
            nyama.active = False
            update()

        if 1 < self.press_delay_counter < 30:
            nyama.rect.y -= 5
            update()
        if 30 < self.press_delay_counter < 60:
            nyama.rect.y += 5
            update()
        if 60 < self.press_delay_counter < 90:
            nyama.rect.y -= 5
            update()
        if 90 < self.press_delay_counter < 120:
            nyama.rect.y += 5
            update()

        if self.press_delay_counter == 125:
            self.press_delay_counter = 0
            self.press_action = False
            self.move_action = True
            nyama.active = True
            if self.direct == 'left':
                self.rect.x = - 200
            else:
                self.rect.x = screen_width + 200
            update()
            rat_cry_snd.stop()

    def bomb(self):
        self.bomb_delay_counter += 1
        if self.bomb_delay_counter == 1:
            if self.direct == 'left':
                rat.image = pg.transform.flip(rat_break, 1, 0)
            else:
                rat.image = rat_break
            update()
            play_sounds(rat_cry_snd, True)
            self.move_action = False

        if self.bomb_delay_counter == 30:
            self.bomb_delay_counter = 0
            self.bomb_action = False
            self.move_action = True
            if self.direct == 'left':
                self.rect.x = - 200
            else:
                self.rect.x = screen_width + 200
            update()
            rat_cry_snd.stop()

    def get_current_rat(self):
        if self.step_count == 60:
            self.step_count = 0
        if self.step_count < 30:
            return rat_image_l
        return rat_image_r

    def move(self):
        self.step_count += 1
        if self.direct == 'right':
            if self.rect.x < screen_width + 300:
                self.image = self.get_current_rat()
                self.rect.x += self.step
                update()
            else:
                self.direct = 'left'
        else:
            if self.rect.x > -300:
                self.image = pg.transform.flip(self.get_current_rat(), 1, 0)
                self.rect.x -= self.step
                update()
            else:
                self.direct = 'right'

        rat_eat_rect = pg.Rect(self.rect.x, self.rect.y+30, self.rect.width, 30)
        if (rat_eat_rect.collidepoint(nyama.rect.centerx, nyama.rect.bottom)
                and nyama.active
                and not self.bomb_action
                and not self.eat_action):
            self.press_action = True

        rat_eat_rect = pg.Rect(self.rect.x + 20, self.rect.y + 30, self.rect.width - 20, self.rect.height - 30)

        if ((rat_eat_rect.collidepoint(nyama.rect.x+30, nyama.rect.bottom-5) and self.direct == 'right')
                or (rat_eat_rect.collidepoint(nyama.rect.right-30, nyama.rect.bottom-5) and self.direct == 'left')
                and nyama.active
                and not self.bomb_action
                and not self.press_action
                and not self.eat_action):
            self.eat_action = True


class Nyama(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = nam_normal
        self.rect = self.image.get_rect(center=(x, y))
        self.active = True
        self.moving_direct = 'stop'
        self.moving_active = False

        self.fly_direct = 'stop'
        self.fly_active = False

        self.jump_direct = 'stop'
        self.jump_active = False

        self.die_active = False
        self.die_delay_counter = 0

        self.jump_delay_counter = 0
        self.start_jump_delay_counter = 0

        self.eat_active = False
        self.eat_delay_counter = 0
        self.eat_type = ""

        self.step = step_nam
        self.step_jump = step_jump_nam
        self.step_fall = step_fall_nam
        self.direct = 'left'
        self.active = True

    def move_left(self):
        if self.direct == 'right':
            self.image = pg.transform.flip(nyama.image, 1, 0)
            self.direct = 'left'
        if self.rect.x > 0:
            self.rect.x -= self.step * screen_step_k
            update()

    def fly_down(self):
        if self.rect.bottom < screen_height:
            self.rect.y += 10
        else:
            self.set_normal()
            if sound_active:
                wall_fall_snd.stop()
            self.fly_active = False
            lives_text.draw_lives(-0.5)

    def fly_left(self):
        if self.rect.x > 0:
            self.rect.move_ip(-self.step * screen_step_k * 3, -self.step * screen_step_k * 2)
        else:
            self.rect.x = 0
            play_sounds(wall_hit_snd, True)
            self.change_img(nam_wall_left, 10)
            play_sounds(wall_fall_snd, True)
            self.fly_direct = 'down'

    def fly_right(self):
        if self.rect.right < screen_width:
            self.rect.move_ip(self.step * screen_step_k * 3, -self.step * screen_step_k * 2)
            update()
        else:
            self.rect.right = screen_width
            play_sounds(wall_hit_snd, True)
            self.change_img(nam_wall_right, 10)
            play_sounds(wall_fall_snd, True)
            self.fly_direct = 'down'

    def move_right(self):
        if self.direct == 'left':
            self.image = pg.transform.flip(nyama.image, 1, 0)
            self.direct = 'right'
        if self.rect.x < screen_width - self.rect.width:
            self.rect.x += self.step * screen_step_k
            update()

    def jump(self):
        if self.start_jump_delay_counter == 0:
            self.change_img(nam_press, 0)
            self.rect.y += 20
        self.start_jump_delay_counter += 1
        if self.start_jump_delay_counter > 8:
            if self.image != nam_jump and not self.eat_active and not self.die_active and not self.fly_active:
                self.change_img(nam_jump, 0)
            if self.rect.y > 0:
                self.rect.y -= self.step_jump * screen_step_k
                update()
            else:
                self.start_jump_delay_counter = 0
                play_sounds(wall_fall_snd, True)
                self.jump_direct = "down"

    def jump_break(self):
        if self.jump_delay_counter == 0:
            self.change_img(nam_die_up_star, 0)
            play_sounds(boom_up_down_snd, True)

        self.jump_delay_counter += 1

        if self.jump_delay_counter == 15:
            self.jump_delay_counter = 0
            lives_text.draw_lives(-0.5)
            self.jump_direct = ""

    def fall(self):
        if self.rect.bottom < screen_height:
            self.rect.y += self.step_fall
        else:
            self.jump_active = False
            self.start_jump_delay_counter = 0
            self.rect.bottom = screen_height
            self.set_normal()
            stop_all_sounds()

    def die(self):
        if self.die_delay_counter == 0:
            self.change_img(nam_bang, 0)
        self.die_delay_counter += 1
        if self.die_delay_counter == 40:
            self.change_img(nam_die_dn, 0)
        if self.die_delay_counter == 60:
            nyama.rect.bottom = screen_height
            self.change_img(nam_die, 0)
        if self.die_delay_counter > 68:
            lives_text.draw_lives(-1)
            self.die_delay_counter = 0
            self.set_normal()
            self.die_active = False

    def eat(self):
        if self.eat_delay_counter == 0:
            if self.eat_type == "bad":
                self.change_img(nam_red, 200)
                play_sounds(fu_snd, True)
            elif self.eat_type == "brick":
                self.change_img(nam_down_star, 200)
                play_sounds(boom_dzin_snd, True)
            else:
                self.change_img(nam_njam, 200)
                eat_snd.stop()
                play_sounds(eat_snd, True)

        self.eat_delay_counter += 1
        if ((self.eat_delay_counter == 100 and self.eat_type != "brick") or
                (self.eat_delay_counter == 140 and self.eat_type == "brick")):
            self.eat_delay_counter = 0
            self.set_normal()
            self.eat_active = False
            if self.eat_type != "good":
                lives_text.draw_lives(-0.5)
            else:
                lives_text.draw_lives(0.5)

    def change_img(self, img, delay):
        if self.image != img:
            self.image = img
            if self.direct == 'right':
                self.image = pg.transform.flip(nyama.image, 1, 0)
                update()
            if delay > 0:
                update()
                pg.display.update()
                pg.time.delay(delay)

    def set_normal(self):
        self.change_img(nam_normal, 0)


class Gift(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.el = gifts_image_list[0]
        self.image = self.el['img']
        self.name = self.el['name']
        self.rect = self.image.get_rect(center=(-100, -100))
        self.moving = 'stop'
        self.step = step_gift_by_list_level[lives_text.level] * screen_step_k
        self.direct = 'left'
        self.active = False
        self.path = 0
        self.hide_delay_counter = 0

    def start_new(self):
        self.el = gifts_image_list[random.randint(0, len(gifts_image_list) - 1)]
        #self.el = gifts_image_list[0]
        self.image = self.el['img']
        self.name = self.el['name']
        self.rect.y = 30
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.active = True
        self.path = random.randint(int(screen_height * 0.5), screen_height - 100)
        self.hide_delay_counter = 0
        self.step = step_gift_by_list_level[lives_text.level] * screen_step_k

    def bomb_bang(self):
        self.rect.x -= 100
        self.rect.y -= 100
        self.change_img(bang_image, 150)
        self.active = False
        self.rect.y = -200
        play_sounds(bang_snd, True)
        update()

    def bad_food(self):
        self.active = False
        self.rect.y = -200
        nyama.eat_active = True
        nyama.eat_type = "bad"

    def good_food(self):
        self.active = False
        self.rect.y = -200
        nyama.eat_active = True
        nyama.eat_type = "good"

    def brick(self):
        self.active = False
        self.rect.y = -200
        nyama.eat_active = True
        nyama.eat_type = "brick"

    def fall(self):

        if self.active and lives_text.level <= lives_text.max_level:
            if self.rect.bottom < screen_height:
                self.rect.y += self.step
                update()
                pg.time.delay(delay_fall_gift)

                if (self.rect.collidepoint(rat.rect.center) and
                        self.name == 'bomb'):
                    rat.bomb_action = 'bomb'

                if self.rect.collidepoint(nyama.rect.center) and nyama.active:
                    nyama.eat_delay_counter = 0
                    if self.name == 'bomb':
                        nyama.die_active = True
                        self.bomb_bang()
                    elif self.name == 'brick':
                        self.brick()
                    elif self.name == 'candy_red':
                        self.bad_food()
                    elif self.name == 'candy_green':
                        self.good_food()
                    elif self.name == 'cake':
                        self.good_food()
                    self.deactivate()

                elif self.name != 'bomb' and self.rect.bottom > self.path:
                    if self.hide_delay_counter == 0:
                        self.change_img(gift_hide, 0)
                    self.hide_delay_counter += 1
                    if self.hide_delay_counter > 20:
                        self.deactivate()
            else:
                if self.name == 'bomb':
                    if self.rect.x - nyama.rect.x > 0:
                        if (self.rect.x - nyama.rect.x < nyama.rect.width * 2 and
                                self.rect.y - nyama.rect.y < nyama.rect.height * 2 + self.rect.height and
                                nyama.active):

                            nyama.fly_active = True
                            nyama.fly_direct = 'left'
                    else:
                        if (nyama.rect.x - self.rect.x < nyama.rect.width + self.rect.width and
                                self.rect.y - nyama.rect.y < nyama.rect.height * 2 + self.rect.height and
                                nyama.active):
                            nyama.fly_active = True
                            nyama.fly_direct = 'right'
                    self.bomb_bang()
                self.deactivate()

    def deactivate(self):
        self.active = False
        self.rect.y = -200
        update()
        self.start_new()

    def change_img(self, img, delay):
        if self.image != img:
            self.image = img
            if delay > 0:
                update()
                pg.display.update()
                pg.time.delay(delay)


class Txt:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lives_start_count = lives_start_count
        self.lives_count = self.lives_start_count
        self.lives_max_count = lives_max_count
        self.font = pg.font.Font('assets/fonts/segoe-ui-symbol.ttf', 30)
        self.lives_pos = ''

        self.out_txt = None
        self.out_pos = None
        self.out_font = pg.font.SysFont('arial.ttf', 80)

        self.con_txt = None
        self.con_pos = None
        self.con_font = pg.font.SysFont('arial.ttf', 80)

        self.game_over_txt = None
        self.game_over_pos = None
        self.game_over_font = pg.font.SysFont('segoe-ui-symbol.ttf', 90)

        self.win_txt = None
        self.win_pos = None
        self.win_font = pg.font.SysFont('segoe-ui-symbol.ttf', 90)

        self.next_level_txt = None
        self.next_level_pos = None
        self.next_level_font = pg.font.SysFont('arial.ttf', 80)

        self.restart_txt = None
        self.restart_pos = None
        self.restart_font = pg.font.SysFont('arial.ttf', 80)

        self.level = 1
        self.max_level = 2

    def draw_repeat_or_out(self, con_text_button):
        surf = pg.Surface((screen_width, screen_height))
        surf.set_alpha(200)
        pg.draw.rect(surf, (0, 0, 0), (0, 0, screen_width, screen_height))
        screen.blit(surf, (0, 0))

        self.game_over_txt = self.game_over_font.render("win", 1, (255, 255, 255))

        self.game_over_pos = self.game_over_txt.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
        screen.blit(self.game_over_txt, self.game_over_pos)
        self.out_txt = self.out_font.render("выйти", 1, (255, 9, 0))
        self.con_txt = self.con_font.render(con_text_button, 1, (255, 255, 0))
        self.out_pos = self.out_txt.get_rect(topleft=(
            (screen_width - self.out_txt.get_width() - self.con_txt.get_width() - 25) / 2,
            screen_height / 2 + 50))

        self.con_pos = self.con_txt.get_rect(topleft=(self.out_pos.right + 50, self.out_pos.y))

        screen.blit(self.out_txt, self.out_pos)
        screen.blit(self.con_txt, self.con_pos)
        nyama.fly_active = False

    def draw_lives(self, d):
        self.lives_count += d
        if self.lives_count <= 0:
            self.draw_repeat_or_out('продолжить')
        elif self.lives_count < self.lives_max_count:
            s = "level " + str(self.level) + " ♥ " * int(self.lives_count)
            if self.lives_count > int(self.lives_count):
                s += "♡ "
            lives_txt = self.font.render(s, 1, (255, 9, 0))
            lives_pos = lives_txt.get_rect(center=(self.x - 200, self.y))
            screen.blit(lives_txt, lives_pos)
        elif self.level < self.max_level:
            surf = pg.Surface((screen_width, screen_height))
            surf.set_alpha(200)
            pg.draw.rect(surf, (0, 0, 0), (0, 0, screen_width, screen_height))
            screen.blit(surf, (0, 0))
            self.win_txt = self.win_font.render("WIN", 1, (255, 255, 255))
            self.win_pos = self.win_txt.get_rect(center=(screen_width / 2, screen_height / 2 - 50))
            screen.blit(self.win_txt, self.win_pos)
            self.next_level_txt = self.next_level_font.render("перейти на 2 уровень", 1, (255, 255, 0))
            self.out_txt = self.out_font.render("выйти", 1, (255, 9, 0))
            self.out_pos = self.out_txt.get_rect(topleft=(
                (screen_width - self.out_txt.get_width() - self.next_level_txt.get_width() - 25) / 2,
                screen_height / 2 + 50))
            self.next_level_pos = self.next_level_txt.get_rect(topleft=(self.out_pos.right + 50, self.out_pos.y))

            screen.blit(self.out_txt, self.out_pos)
            screen.blit(self.next_level_txt, self.next_level_pos)
        else:
            self.draw_repeat_or_out('начать снова')


def stop_all_sounds():
    fu_snd.stop()
    boom_dzin_snd.stop()
    boom_up_down_snd.stop()


def play_sounds(name, stop_all):
    if sound_active:
        if stop_all:
            stop_all_sounds()
        name.play(0)


def update():
    screen.blit(bg_image, (0, 0))
    screen.blit(nyama.image, nyama.rect)
    screen.blit(rat.image, rat.rect)
    for gift_item in gifts_list:
        if gift_item.active:
            screen.blit(gift_item.image, gift_item.rect)
    lives_text.draw_lives(0)


nyama = Nyama(screen_width / 2, screen_height - 50)
rat = Rat(-60, screen_height - 50)
lives_text = Txt(screen_width, 30)

for i in range(3):
    gifts_list.append(Gift())
    threading.Timer(random.randint(10, 40) / 10, gifts_list[i].start_new).start()

pg.time.Clock().tick(10)

screen.blit(bg_image, (0, 0))
screen.blit(intro_image,
            ((screen_width - intro_image.get_width()) / 2, (screen_height - intro_image.get_height()) / 2 - 30))
play_sounds(eat_snd, True)
intro = True

running = True
while running:
    if not nyama.fly_active and not nyama.die_active:

        for event in pg.event.get():
            if event.type == pg.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen_step_k = screen_height / default_screen_height
                screen = pg.display.set_mode((screen_width, screen_height), pg.RESIZABLE)
                bg_image = pg.transform.scale(bg_image_load, (screen_width, screen_height))
                screen.blit(bg_image, (0, 0))
                nyama.rect.bottom = screen_height
                nyama.rect.x = screen_width / 2
                screen.blit(intro_image, (
                    (screen_width - intro_image.get_width()) / 2, (screen_height - intro_image.get_height()) / 2 - 40))

            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN and nyama.active:
                if intro:
                    intro = False
                    eat_snd.stop()
                if event.key == pg.K_UP and not nyama.jump_active:
                    if nyama.rect.bottom > screen_height - 10:
                        nyama.change_img(nam_press, 20)
                        nyama.change_img(nam_jump, 0)
                    nyama.jump_direct = 'up'
                    nyama.jump_active = True
                elif event.key == pg.K_LEFT:
                    nyama.moving_direct = 'left'
                    nyama.moving_active = True
                elif event.key == pg.K_RIGHT:
                    nyama.moving_direct = 'right'
                    nyama.moving_active = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP:
                    nyama.jump_direct = 'fall'
                if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                    nyama.moving_active = False

            if event.type == pg.MOUSEBUTTONDOWN:
                if intro:
                    intro = False
                    eat_snd.stop()

                if pg.mouse.get_pressed()[0]:
                    pos = pg.mouse.get_pos()
                    if lives_text.out_pos and lives_text.out_pos.collidepoint(pos):
                        running = False
                    elif lives_text.con_pos and lives_text.con_pos.collidepoint(pos):
                        lives_text.level = 1
                        lives_text.lives_count = lives_start_count
                    elif lives_text.next_level_pos and lives_text.next_level_pos.collidepoint(pos):
                        lives_text.level += 1
                        lives_text.lives_count = lives_start_count

    if 0 < lives_text.lives_count < lives_text.lives_max_count and (not intro):
        if nyama.active:

            if nyama.die_active:
                nyama.die()
            else:
                if nyama.eat_active:
                    nyama.eat()
                if nyama.fly_active:
                    if nyama.fly_direct == "left":
                        nyama.fly_left()
                    elif nyama.fly_direct == "right":
                        nyama.fly_right()
                    elif nyama.fly_direct == "down":
                        nyama.fly_down()
                else:
                    if nyama.moving_active:
                        if nyama.moving_direct == "left":
                            nyama.move_left()
                        elif nyama.moving_direct == "right":
                            nyama.move_right()

                    if nyama.jump_active:
                        if nyama.jump_direct == "up":
                            nyama.jump()
                        elif nyama.jump_direct == "down":
                            nyama.jump_break()
                        else:
                            nyama.fall()

        for gift in gifts_list:
            if gift.active:
                gift.fall()

        if lives_text.level == 1:
            if rat.move_action and not rat.bomb_action and not rat.press_action:
                rat.move()
            if rat.eat_action and not rat.bomb_action and not rat.press_action:
                rat.eat()
            if rat.bomb_action and not rat.press_action:
                rat.bomb()
            if rat.press_action:
                rat.pressed()
    pg.display.update()
    pg.time.delay(4)

pg.quit()
