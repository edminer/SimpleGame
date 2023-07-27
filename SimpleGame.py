import random, copy

import pgzrun
from pgzhelper import *     # https://www.aposteriori.com.sg/pygame-zero-helper/
import pygame

class Obstacle():
    def __init__(self, imageName, name, speed):
        self.actor = Actor(imageName, anchor=('left', 'top'))
        self.name = name
        self.speed = speed

    def __repr__(self):
        return f"Obstacle: {self.name}, speed={self.speed}, {self.actor.x}, {self.actor.y}"

WIDTH  = 1200
HEIGHT = 720
OBSTACLE_OFFSET = 305
game_over = False
isJump = False
jumpCount = 8
countdown_timer = 120
score = 0

cat = Actor("costume1", bottomleft=(WIDTH/3, HEIGHT))
# cat.scale = 0.5
cat.incr = 0
cat.name = "cat"
cat.images = ["costume1", "costume2"]

cat = cat
background_speed = 12
actor_collision_detected = False
actor_lives = 10
actor_direction = "right"

backdrops = [Actor("bluesky", anchor=('left', 'top')), Actor("bluesky2", anchor=('left', 'top')), Actor("bluesky4", anchor=('left', 'top')), Actor("bluesky3", anchor=('left', 'top'))]
backdrops[0].topleft = (0, 0)
for i in range(1, len(backdrops)):
    backdrops[i].topleft = (backdrops[i-1].x + backdrops[i-1].width, 0)

AVAILABLE_OBSTACLES = [
    Obstacle("obstacle1", "yellowrock", 15),
    Obstacle("obstacle2", "bluerock", 10),
    Obstacle("obstacle3", "redrock", 10),
    Obstacle("obstacle4", "dragon", 20)
]
# obstacle_offset = 1000
# obstacles[0].actor.topleft = (WIDTH-200, HEIGHT - obstacles[0].actor.height)
# for i in range(1, len(obstacles)):
#     obstacles[i].actor.topleft = (obstacles[i-1].actor.x + obstacles[i-1].actor.width + obstacle_offset, HEIGHT - obstacles[i].actor.height)
obstacles = []


def draw():
    screen.clear()
    for backdrop in backdrops:
        backdrop.draw()
    for obstacle in obstacles:
        obstacle.actor.draw()

    cat.draw()

    font = pygame.font.SysFont("Arial", 30)
    width, height = font.size(f"Lives Remaining: {actor_lives}")
    screen.draw.text(f"Lives Remaining: {actor_lives}", (15, 20), color="BLUE", fontsize=30)
    screen.draw.text(f"Time Remaining: {countdown_timer}", (300, 20), color="BLUE", fontsize=30)
    screen.draw.text(f"Score: {score}", (600, 20), color="BLUE", fontsize=30)
    if game_over:
        screen.draw.text(f"Game Over!", (150, 80), color="RED", fontsize=60)

def update():
    global cat, actor_collision_detected, actor_direction, game_over, actor_lives, isJump, jumpCount

    if game_over:
        return

    if abs(backdrops[0].x) > backdrops[0].width:
        backdrops.append(backdrops.pop(0))
        backdrops[-1].x = backdrops[-2].x + backdrops[-2].width

    if backdrops[0].x > 0:
        backdrops.insert(0, backdrops.pop(-1))
        backdrops[0].x = 0 - backdrops[0].width + background_speed

    for obstacle in obstacles[:]:
        if actor_direction == "right" and obstacle.actor.x < 0 and abs(obstacle.actor.x) > obstacle.actor.width:
            obstacles.remove(obstacle)
            print(f"Obstacle {obstacle.name} REMOVED!")

        # if actor_direction == "left" and obstacles[-1].actor.x > WIDTH:
        #     obstacles.remove(obstacle)

    if keyboard.a:
        cat.fps = 10
        cat.animate()
        pygame.time.wait(200)

    if keyboard.f:  # Toggle FULLSCREEN
        toggle_fullscreen()

    if keyboard.r:      # RESET position
        cat.pos = (WIDTH/2, HEIGHT/2)
        cat.angle = 0
        cat.incr = 0
        cat.flip_x = False
        cat.flip_y = False

    if keyboard.right:
        cat.flip_x = False
        cat.animate()
        actor_direction = "right"
        for backdrop in backdrops:
            backdrop.x -= background_speed
        for obstacle in obstacles:
            obstacle.actor.x -= obstacle.speed

    # if keyboard.left:
    #     cat.flip_x = True
    #     cat.animate()
    #     actor_direction = "left"
    #     for backdrop in backdrops:
    #         backdrop.x += background_speed
    #     for obstacle in obstacles:
    #         obstacle.actor.x += obstacle.speed

    # if keyboard.up:
    #     cat.direction = 90
    #     cat.animate()
    #     cat.move_in_direction(background_speed)
    #     if cat.y < cat.height / 2:
    #         cat.direction = -90
    #         cat.move_in_direction(background_speed)
    #
    # if keyboard.down:
    #     cat.direction = -90
    #     cat.animate()
    #     cat.move_in_direction(background_speed)
    #     if cat.y > HEIGHT - cat.height / 2:
    #         cat.direction = 90
    #         cat.move_in_direction(background_speed)

    # For jumping code, see here: https://www.techwithtim.net/tutorials/game-development-with-python/pygame-tutorial/jumping
    if keyboard.space:
        isJump = True
        #pygame.time.wait(200)

    if isJump:
        if jumpCount >= -8:
            cat.y -= (jumpCount * abs(jumpCount)) * 2.5
            jumpCount -= 1
            if actor_direction == "right":
                for backdrop in backdrops:
                    backdrop.x -= background_speed
                for obstacle in obstacles:
                    obstacle.actor.x -= obstacle.speed + 2
            else:
                for backdrop in backdrops:
                    backdrop.x += background_speed
                for obstacle in obstacles:
                    obstacle.actor.x += obstacle.speed

        else:  # This will execute if our jump is finished
            jumpCount = 8
            isJump = False

    # Check if the cat has collided with any obstacles
    obstacle_actors = []
    for obstacle in obstacles:
        obstacle_actors.append(obstacle.actor)
    #hit = cat.obb_collidepoints(obstacle_actors)
    hit = cat.collidelist(obstacle_actors)
    if hit != -1:
        if actor_collision_detected == False:
            actor_collision_detected = True
            actor_lives -= 1
            if not actor_lives:
                game_over = True
                print("Game Over!")
                tone.play("E3", 2)
            else:
                tone.play("E4", .25)
                print(f"Lives remaining: {actor_lives}")

    else:
        actor_collision_detected = False

    # if cat.obb_collidepoints([lion]) != -1:
    #     if actor_collision_detected == False:
    #         tone.play("E4", .25)
    #         actor_collision_detected = True
    # else:
    #     actor_collision_detected = False


def reporter():
    if game_over:
        return
    for i in range(len(obstacles)):
        print(f"Obstacle{i} {obstacles[i].name}: {obstacles[i].actor.x}")


def update_obstacles():
    global obstacles
    if game_over:
        return

    # Verify that there isn't already an obstacle waiting to be scrolled into view
    if obstacles:
        if obstacles[-1].actor.x >= WIDTH - OBSTACLE_OFFSET:
            clock.schedule_unique(update_obstacles, 1)
            return
    # Pick an obstacle that is not already in play
    while True:
        obstacle = random.choice(AVAILABLE_OBSTACLES)
        if not obstacle in obstacles:
            break
    obstacle.actor.x = WIDTH
    obstacle.actor.y = HEIGHT - obstacle.actor.height
    obstacles.append(obstacle)
    clock.schedule_unique(update_obstacles, random.randrange(2, 6))

def update_countdown_timer():
    global countdown_timer, game_over
    if game_over:
        return
    countdown_timer -= 1
    if not countdown_timer:
        game_over  = True

clock.schedule_interval(reporter, 2)
clock.schedule_unique(update_obstacles, 1)
clock.schedule_interval(update_countdown_timer, 1)

pgzrun.go()
