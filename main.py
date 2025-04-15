import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1000, 800))
clock = pygame.time.Clock()
fnt_1 = pygame.font.SysFont('Arial', 50)
fnt_2 = pygame.font.SysFont('Arial', 35)


class Object:
    def __init__(self):
        self.x = random.randint(50, screen.get_width() - 50)
        self.y = random.randint(50, screen.get_height() - 50)
        self.shape = random.randint(0, 1)
        self.s_x = self.x
        self.s_y = self.y
        self.moving = False
        self.scr = 0
        self.size = random.randint(30, 80)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def draw(self):
        if self.shape == 0:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        elif self.shape == 1:
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self):
        mouse_get = pygame.mouse.get_pos()
        mouse_get_press = pygame.mouse.get_pressed()
        if not self.moving:
            if self.shape == 0:
                if self.x + self.size > mouse_get[0] > self.x and self.y + self.size > mouse_get[1] > self.y:
                    if mouse_press[0] == 1:
                        self.moving = True
            elif self.shape == 1:
                temp_dist = math.sqrt((self.x - mouse_get[0]) ** 2 + (self.y - mouse_get[1]) ** 2)
                if self.size >= temp_dist:
                    if mouse_press[0] == 1:
                        self.moving = True
        elif self.moving:
            if mouse_get_press[0] == 1:
                if self.shape == 0:
                    self.x = mouse_get[0] - self.size / 2
                    self.y = mouse_get[1] - self.size / 2
                elif self.shape == 1:
                    self.x = mouse_get[0]
                    self.y = mouse_get[1]
            else:
                self.moving = False

    def mix(self):
        self.x = random.randint(50, screen.get_width() - 50)
        self.y = random.randint(50, screen.get_height() - 50)

    def score(self):
        self.scr = math.floor(math.sqrt((self.x - self.s_x) ** 2 + (self.y - self.s_y) ** 2))
        return self.scr


clk = 0
sec = 0
cl = 0
scene = 0
scene_1_start = False
scene_1_prep = False
scene_1_game = False
scene_1_score = False
running = True
objects = []
obj_count = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    mouse = pygame.mouse.get_pos()
    mouse_press = pygame.mouse.get_pressed()

    screen.fill((0, 0, 0))

    if scene == 0:
        txt_1 = fnt_2.render("Start", True, (0, 0, 0))
        txt_2 = fnt_1.render("The Game!", True, (255, 255, 255))
        rect_1 = pygame.rect.Rect(screen.get_width() / 10, screen.get_height() / 3, txt_1.get_width() * 2,
                                  txt_1.get_height() + 10)

        pygame.draw.rect(screen, (255, 255, 255), rect_1)
        screen.blit(txt_1, (15 + screen.get_width() / 10, 5 + screen.get_height() / 3))
        screen.blit(txt_2, ((screen.get_width() / 2) - txt_2.get_width() / 2, screen.get_height() / 10))

        if rect_1.collidepoint(mouse):
            if mouse_press[0] == 1:
                scene = 1
                scene_1_start = True
    if scene == 1:
        if scene_1_score:
            temp_score = 0
            for obj in objects:
                temp_score += obj.score()
            temp_score = 1000 - temp_score
            if temp_score < 0:
                temp_score = 0
            txt_1_2 = fnt_1.render("Score: " + str(temp_score), True, (255, 255, 255))
            txt_1_3 = fnt_2.render("Replay", True, (0, 0, 0))
            rect_2 = pygame.rect.Rect(
                (screen.get_width() / 2) - txt_1_3.get_width(),
                (8 * screen.get_height() / 10) - txt_1_3.get_height(),
                txt_1_3.get_width() * 2,
                txt_1_3.get_height() + 10)
            screen.blit(txt_1_2, ((screen.get_width() / 2) - txt_1_2.get_width() / 2, screen.get_height() / 10))
            pygame.draw.rect(screen, (255, 255, 255), rect_2)
            screen.blit(txt_1_3, ((screen.get_width() / 2) - txt_1_3.get_width() / 2,
                                  (8 * screen.get_height() / 10) - txt_1_3.get_height() + 5))
            if rect_2.collidepoint(mouse):
                if mouse_press[0] == 1:
                    scene_1_start = True
                    scene_1_score = False

        if scene_1_game:
            for obj in objects:
                obj.draw()
                obj.move()
            txt_1_1 = fnt_1.render(str(cl - sec), True, (255, 255, 255))
            screen.blit(txt_1_1, ((screen.get_width() / 2) - txt_1_1.get_width() / 2, screen.get_height() / 10))
            if cl - sec == 0:
                scene_1_score = True
                scene_1_game = False

        if scene_1_prep:
            for obj in objects:
                obj.draw()
            txt_1_0 = fnt_1.render(str(cl - sec), True, (255, 255, 255))
            screen.blit(txt_1_0, ((screen.get_width() / 2) - txt_1_0.get_width() / 2, screen.get_height() / 10))
            if cl - sec == 0:
                for obj in objects:
                    obj.mix()
                cl = sec + 10
                scene_1_game = True
                scene_1_prep = False

        if scene_1_start:
            obj_count = random.randint(3, 5)
            objects = []
            for i in range(obj_count):
                objects.append(Object())
            cl = sec + 8
            scene_1_prep = True
            scene_1_start = False

    clk += 1
    if clk == 60:
        clk = 0
        sec += 1
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
