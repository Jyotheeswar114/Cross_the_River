import random
from sys import exit

import pygame
import pygame.font
from pygame.locals import *
from config import *

message = "not colloided"
pygame.init()
clock = pygame.time.Clock()
speed_of_moving_obstacle = 150
player_speed = 130
second = 0
interval_max = 1500
interval_min = 800
distance_max = 700
distance_min = 300
interval = 800
player_image = 'hanuman.png'
player_surface = pygame.image.load(player_image)
fixed_obstacle_image = 'devil.png'
fixed_obstacle_surface = pygame.image.load(fixed_obstacle_image)
moving_obstacle_image = 'ship.png'
moving_obstacle_surface = pygame.image.load(moving_obstacle_image)
screen_size = (960, 720)
list_of_fixed_obstacles = []
list_of_moving_obstacles = []
screen = pygame.display.set_mode(screen_size, 0, 32)
previous_obstacle_coordinates = [0, 0, 0, 0, 0]
player_pos = [0, 0]


class Fixed_Obstacle:
    def __init__(self, img, x, y, width, height):
        self.x_coordinate = x
        self.y_coordinate = y
        self.width = width
        self.height = height
        self.img_object = pygame.transform.scale(img, (width, height))

    def draw_obstacle(self, screen_to_draw):
        screen_to_draw.blit(
            self.img_object, (self.x_coordinate, self.y_coordinate))


class Moving_Obstacle(Fixed_Obstacle):
    def update_coordinates(self, distance):
        self.x_coordinate += distance


class Player:
    def __init__(self, x, y, img_surface, number):
        self.x_coordinate = x
        self.y_coordinate = y
        self.x_change = 0
        self.y_change = 0
        self.score = 0
        self.time = 0
        self.checked_slab = [1, 0, 0, 0, 0]
        self.checked_river = [1, 0, 0, 0, 0, 0]
        self.surface = img_surface
        self.player_number = number
        self.speed = player_speed
        self.round = 1

    def draw_player(self):
        screen.blit(self.surface, (self.x_coordinate, self.y_coordinate))

    def iscollide(self):
        player_rect = pygame.Rect(
            (self.x_coordinate, self.y_coordinate), (40, slab_length - 10))
        for i in list_of_fixed_obstacles:
            temp = pygame.Rect(
                (i.x_coordinate, i.y_coordinate), (slab_length, slab_length))
            if player_rect.colliderect(temp):
                return True
        for i in list_of_moving_obstacles:
            temp = pygame.Rect(
                (i.x_coordinate, i.y_coordinate), (100, river_length))
            if player_rect.colliderect(temp):
                return True
        return False

    def change_magnitide(self):
        return (self.x_change ** 2 + self.y_change ** 2) ** 0.5

    def update_change(self):
        try:
            magnitude = self.change_magnitide()
            self.x_change /= magnitude
            self.y_change /= magnitude
        except ZeroDivisionError:
            self.x_change = 0
            self.y_change = 0

    def update_positions(self):
        self.update_change()
        self.x_coordinate += self.x_change * player_speed * time_passed_seconds
        self.y_coordinate += self.y_change * player_speed * time_passed_seconds
        if self.x_coordinate < 0:
            self.x_coordinate = 0
        if self.x_coordinate > screen_size[0] - 40:
            self.x_coordinate = screen_size[0] - 40
        if self.y_coordinate < 0:
            self.y_coordinate = 0
        if self.y_coordinate > screen_size[1] - slab_length + 10:
            self.y_coordinate = screen_size[1] - slab_length + 10

    def update_round(self):
        self.round += 1
        self.checked_river = [1, 0, 0, 0, 0, 0]
        self.checked_slab = [1, 0, 0, 0, 0]
        global speed_of_moving_obstacle,\
            list_of_fixed_obstacles, list_of_moving_obstacles, obstacle_present
        speed_of_moving_obstacle += 40
        self.score += (100 // self.time)
        self.time = 0
        self.x_coordinate = 480
        obstacle_present = [0, 0, 0, 0, 0]
        list_of_moving_obstacles = []
        list_of_fixed_obstacles = []
        if (self.player_number == 1):
            self.y_coordinate = 680
        else:
            self.y_coordinate = 0
        global interval_max
        interval_max -= 100
        global interval_min
        interval_min -= 100
        global distance_max
        distance_max -= 50
        global distance_min
        distance_min -= 50
        intialize_fixed_obstacle_coordinates(
            river_length, slab_length, screen_size[0])

    def give_to_second_player(self):
        global obstacle_present,\
            list_of_moving_obstacles, list_of_fixed_obstacles,\
            turn, second, speed_of_moving_obstacle, interval_min,\
            interval_max, distance_max, distance_min, interval
        speed_of_moving_obstacle = 150
        interval_max = 1500
        interval_min = 800
        distance_max = 700
        distance_min = 300
        interval = 800
        turn = 2
        list_of_fixed_obstacles = []
        if self.player_number == 2:
            turn = 1
        intialize_fixed_obstacle_coordinates(
            river_length, slab_length, screen_size[0])
        second = 0
        obstacle_present = [0, 0, 0, 0, 0]
        list_of_moving_obstacles = []

    def display_score_time(self):
        text_surface = my_font.render(
            "Score : " + str(self.score)
            + " Time : " + str(self.time), True, (0, 0, 0))
        screen.blit(text_surface, (0, 0))

    def update_score_time(self):
        self.time += time_passed_seconds
        dl = river_length + slab_length
        if (self.player_number == 2):
            tempv = self.y_coordinate
            if dl + slab_length < tempv and self.checked_slab[1] != 1:
                self.checked_slab[1] = 1
                self.score += 15
            if 2 * dl + slab_length < tempv and self.checked_slab[2] != 1:
                self.checked_slab[2] = 1
                self.score += 15
            if 3 * dl + slab_length < tempv and self.checked_slab[3] != 1:
                self.checked_slab[3] = 1
                self.score += 15
            if 4 * dl + slab_length < tempv and self.checked_slab[4] != 1:
                self.checked_slab[4] = 1
                self.score += 15
            if dl < tempv and self.checked_river[1] != 1:
                self.checked_river[1] = 1
                self.score += obstacle_present[0] * 10
            if 2 * dl < tempv and self.checked_river[2] != 1:
                self.checked_river[2] = 1
                self.score += obstacle_present[1] * 10
            if 3 * dl < tempv and self.checked_river[3] != 1:
                self.checked_river[3] = 1
                self.score += obstacle_present[2] * 10
            if 4 * dl < tempv and self.checked_river[4] != 1:
                self.checked_river[4] = 1
                self.score += obstacle_present[3] * 10
            if 5 * dl < tempv and self.checked_river[5] != 1:
                self.checked_river[5] = 1
                self.score += obstacle_present[4] * 10
        if (self.player_number == 1):
            tempv = self.y_coordinate + slab_length - 10
            if 4 * dl > tempv and self.checked_slab[4] != 1:
                self.checked_slab[4] = 1
                self.score += 15
            if 3 * dl > tempv and self.checked_slab[3] != 1:
                self.checked_slab[3] = 1
                self.score += 15
            if 2 * dl > tempv and self.checked_slab[2] != 1:
                self.checked_slab[2] = 1
                self.score += 15
            if 1 * dl > tempv and self.checked_slab[1] != 1:
                self.checked_slab[1] = 1
                self.score += 15
            if 4 * dl + slab_length > tempv and self.checked_river[5] != 1:
                self.checked_river[5] = 1
                self.score += obstacle_present[4] * 10
            if 3 * dl + slab_length > tempv and self.checked_river[4] != 1:
                self.checked_river[4] = 1
                self.score += obstacle_present[3] * 10
            if 2 * dl + slab_length > tempv and self.checked_river[3] != 1:
                self.checked_river[3] = 1
                self.score += obstacle_present[2] * 10
            if dl + slab_length > tempv and self.checked_river[2] != 1:
                self.checked_river[2] = 1
                self.score += obstacle_present[1] * 10
            if slab_length > tempv and self.checked_river[1] != 1:
                self.checked_river[1] = 1
                self.score += obstacle_present[0] * 10

    def intialize(self):
        self.x_change = 0
        self.y_change = 0
        self.score = 0
        self.time = 0
        self.checked_slab = [1, 0, 0, 0, 0]
        self.checked_river = [1, 0, 0, 0, 0, 0]
        if self.player_number == 1:
            self.x_coordinate = 480
            self.y_coordinate = 680
        if self.player_number == 2:
            self.x_coordinate = 480
            self.y_coordinate = 0


def draw_fixed_obstacles():
    for i in list_of_fixed_obstacles:
        i.draw_obstacle(screen)


def draw_moving_obsacles():
    for i in list_of_moving_obstacles:
        i.draw_obstacle(screen)


def draw_rectangles(screen_width, screen_height):
    river = screen_height // 8
    slab = river // 2
    slab_y = 0
    for i in range(5):
        pygame.draw.rect(
            screen, slab_color, Rect((0, slab_y), (screen_width, slab)))
        pygame.draw.rect(
            screen, river_color,
            Rect((0, slab_y + slab), (screen_width, river)))
        slab_y += (river + slab)
    pygame.draw.rect(
        screen, slab_color,
        Rect((0, slab_y),
             (screen_width, screen_height - 5 * slab - 5 * river)))
    return river, slab


river_length, slab_length = draw_rectangles(screen_size[0], screen_size[1])


def intialize_fixed_obstacle_coordinates(
        river_length, slab_length, screen_width):
    obps = 3
    for i in range(1, 5):
        for j in range(1, 4):
            ob = Fixed_Obstacle(fixed_obstacle_surface,
                                random.randint(
                                    (j - 1) * (screen_width // obps),
                                    j * (screen_width // obps)),
                                i * (river_length + slab_length),
                                slab_length, slab_length)
            list_of_fixed_obstacles.append(ob)


intialize_fixed_obstacle_coordinates(river_length, slab_length, screen_size[0])
obstacle_present = [0, 0, 0, 0, 0]


def obstacle_sending():
    while True:
        t = random.choice([0, 1, 2, 3, 4])
        global obstacle_present
        if (obstacle_present[t] == 0):
            obstacle_present[t] += 1
            ob = Moving_Obstacle(
                moving_obstacle_surface, -100,
                slab_length + t * (slab_length + river_length), 100,
                                 river_length)
            list_of_moving_obstacles.append(ob)
            break
        else:
            if previous_obstacle_coordinates[t] > random.randint(
                    distance_min, distance_max):
                obstacle_present[t] += 1
                ob = Moving_Obstacle(
                    moving_obstacle_surface,
                    -100, slab_length + t * (slab_length + river_length), 100,
                                     river_length)
                list_of_moving_obstacles.append(ob)
                break


def update_moving_obstacles(distance):
    visited = [0, 0, 0, 0, 0]
    j = 0
    for i in list_of_moving_obstacles:
        i.update_coordinates(distance)
        t = (i.y_coordinate - slab_length) // (slab_length + river_length)
        if (visited[t] == 0):
            previous_obstacle_coordinates[t] = i.x_coordinate
            visited[t] = 1
        else:
            if (previous_obstacle_coordinates[t] > i.x_coordinate):
                previous_obstacle_coordinates[t] = i.x_coordinate
        if (i.x_coordinate > screen_size[0]):
            obstacle_present[t] -= 1
            list_of_moving_obstacles.pop(j)
        j += 1


player_suface = pygame.transform.scale(player_surface, (40, slab_length - 10))
player1 = Player(480, 680, player_suface, 1)
player2 = Player(480, 0, player_suface, 2)
turn = 1
game_over = False
run = True
while run:
    if second > interval:
        second = 0
        obstacle_sending()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    if game_over:
        if player1.score > player2.score:
            text_surface = my_font.render(
                player1_won, True, text_color, (255, 255, 255))
        elif player2.score > player1.score:
            text_surface = my_font.render(
                player2_won, True, text_color, (255, 255, 255))
        else:
            text_surface = my_font.render(
                noone, True, text_color, (255, 255, 255))
        screen.blit(text_surface, (0, 0))
        pygame.display.update()
        continue
    river_length, slab_length = draw_rectangles(screen_size[0], screen_size[1])
    draw_fixed_obstacles()
    draw_moving_obsacles()
    # Time waala
    time_passed = clock.tick(30)
    time_passed_seconds = time_passed / 1000.0
    second += time_passed
    distance = time_passed_seconds * speed_of_moving_obstacle
    pressed_keys = pygame.key.get_pressed()
    if (turn == 2):
        player2.x_change = 0
        player2.y_change = 0
        if pressed_keys[K_LEFT]:
            player2.x_change = -0.5
        elif pressed_keys[K_RIGHT]:
            player2.x_change = +0.5
        if pressed_keys[K_UP]:
            player2.y_change = -0.5
        elif pressed_keys[K_DOWN]:
            player2.y_change = +0.5
        player2.draw_player()
        player2.display_score_time()
        player2.update_positions()
        player2.update_score_time()
        if player2.iscollide():
            # intialize_fixed_obstacle_
            # coordinates(river_length, slab_length, screen_size[0])
            # player2.give_to_second_player()
            game_over = True
        if player2.y_coordinate > 5 * (slab_length + river_length):
            player2.update_round()

    if (turn == 1):
        player1.x_change = 0
        player1.y_change = 0
        if pressed_keys[K_a]:
            player1.x_change = -0.5
        elif pressed_keys[K_d]:
            player1.x_change = +0.5
        if pressed_keys[K_w]:
            player1.y_change = -0.5
        elif pressed_keys[K_s]:
            player1.y_change = +0.5
        player1.draw_player()
        player1.display_score_time()
        player1.update_positions()
        player1.update_score_time()
        if player1.y_coordinate < 10:
            player1.update_round()
        if player1.iscollide():
            player1.give_to_second_player()
    # print(speed_of_moving_obstacle)
    update_moving_obstacles(distance)
    interval = random.randint(interval_min, interval_max)
    pygame.display.update()
