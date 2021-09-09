import pygame
import random
from classes.snake import Snake
from classes.apple import Apple
from classes.coin import Coin

pygame.init()

black = '#222222'
red = (213, 50, 80)
green = '#97c405'
background_color = black

dis_width = 1080
dis_height = 900
score_bar_height = 40
inset = 20
bounds = [40, dis_width - inset, dis_height - inset, inset] # top, right, bottom, left

font_style = pygame.font.SysFont("OCR A Std", 25)
dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)

clock = pygame.time.Clock()

high_score = 0
snake_block = 20
snake_speed = 15
game_screen = 'Game'  # 'Game' 'GameOver' 'Menu'

def draw_score(score):
    value = font_style.render(f"Your score: {str(score)}".upper(), True, green)
    dis.blit(value, [bounds[3], 8])

def draw_highscore(score):
    value = font_style.render(f"Highscore: {str(score)}".upper(), True, green)
    dis.blit(value, [dis_width / 2, 8])

def get_random_position_x():
    return round(random.randrange(bounds[3], bounds[1] - snake_block) / snake_block) * snake_block

def get_random_position_y():
    return round(random.randrange(bounds[0], bounds[2] - snake_block) / snake_block) * snake_block

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def set_score(high_score, score):
    draw_score(score)
    draw_highscore(high_score)

def draw_global():
    dis.fill(background_color)

    border = 4
    offset = 2
    top = bounds[0] - border - offset
    right = bounds[1] + border + offset
    bottom = bounds[2] + border + offset
    left = bounds[3] - border - offset

    pygame.draw.rect(
        dis,
        green,
        [
            left,
            top,
            right - left,
            bottom - top
        ],
    border, 1)

snake1 = Snake(pygame, dis, snake_block, green)
apple1 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())
apple2 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())
apple3 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())

def gameLoop():
    global high_score
    global game_screen
    global snake1
    global apple1
    global apple2
    global apple3
    img = pygame.image.load('Images/Menu.png')

    # Loading the sprite
    coin_sprite1 = pygame.sprite.Group()
    coin1 = Coin(0, 0)
    coin_sprite1.add(coin1)

    coin_sprite2 = pygame.sprite.Group()
    coin2 = Coin(0, 0)
    coin_sprite2.add(coin2)

    coin_sprite3 = pygame.sprite.Group()
    coin3 = Coin(0, 0)
    coin_sprite3.add(coin3)

    snake1.resetPosition(
        get_random_position_x(),
        get_random_position_y()
    )

    game_over = False

    while not game_over:
        if snake1.Length - 1 > high_score:
            high_score = snake1.Length - 1
            pygame.display.update()

        while game_screen == 'Menu':
            draw_global()
            img_size = 600
            dis.blit(img, (
                (dis_width/2) - img_size/2,
                (dis_height/2) - img_size/2,
                img_size,
                img_size
            ))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_screen = 'Game'
                    if event.key == pygame.K_c:
                        game_screen = 'Game'
                        gameLoop()

        while game_screen == 'GameOver':
            draw_global()
            message("You Lost! Press C-Play Again or Q-Quit", red)
            set_score(high_score, snake1.Length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_screen = 'Game'
                    if event.key == pygame.K_c:
                        game_screen = 'Game'
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake1.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    snake1.moveRight()
                elif event.key == pygame.K_UP:
                    snake1.moveUp()
                elif event.key == pygame.K_DOWN:
                    snake1.moveDown()

        draw_global()
        set_score(high_score, snake1.Length - 1)

        snake1.update()
        snake1.draw()
        apple1.draw()
        apple2.draw()
        apple3.draw()

        coin_sprite1.draw(dis)
        coin_sprite1.update(apple1.x, apple1.y)
        coin_sprite2.draw(dis)
        coin_sprite2.update(apple2.x, apple2.y)
        coin_sprite3.draw(dis)
        coin_sprite3.update(apple3.x, apple3.y)

        if snake1.isOutOfBounds(bounds) or snake1.isOverlappingItself():
            game_screen = 'GameOver'
            pygame.display.update()

        if (snake1.isOver(apple1.x, apple1.y)):
            apple1.changePosition(
                get_random_position_x(),
                get_random_position_y()
            )
            snake1.increaseLength()

        if (snake1.isOver(apple2.x, apple2.y)):
            apple2.changePosition(
                get_random_position_x(),
                get_random_position_y()
            )
            snake1.increaseLength()

        if (snake1.isOver(apple3.x, apple3.y)):
            apple3.changePosition(
                get_random_position_x(),
                get_random_position_y()
            )
            snake1.increaseLength()

        clock.tick(snake_speed)
        pygame.display.update()

    pygame.quit()
    quit()


gameLoop()
