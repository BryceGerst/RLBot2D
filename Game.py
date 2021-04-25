import pygame, sys, math, random
from PhysicsObject import Ball, Car, Vector


pygame.init()

#screen_w = 600
#screen_h = 800


# the following methods draw images onto the screen where x, y is the center
def draw_angle(surface, image, angle, x, y):
    rotated_image = pygame.transform.rotate(image, angle)
    coords = (x - (rotated_image.get_width() // 2), y - (rotated_image.get_height() // 2))
    surface.blit(rotated_image, coords)

def draw(surface, image, x, y):
    coords = (x - (image.get_width() // 2), y - (image.get_height() // 2))
    surface.blit(image, coords)

car = pygame.image.load('car.png')
ball = pygame.image.load('ball.png')
field = pygame.image.load('field.png')

screen_w, screen_h = field.get_width(), field.get_height()

##print(car.get_width())
##print(car.get_height())
##print(ball.get_width())
##print(screen_w, screen_h)

car.set_colorkey((12,36,21))

screen = pygame.display.set_mode([screen_w, screen_h])

playing = True
clock = pygame.time.Clock()


goal_height = 100
goal_left_x = 289
goal_right_x = 611
map_info = [0, screen_w, goal_height, screen_h - goal_height, goal_height, goal_left_x, goal_right_x]

games_left = 5

while games_left > 0:
    game_over = False
    players = []
    player_one = Car(screen_w // 5, 3 * screen_h // 4, Vector(0,0), car.get_width(), car.get_height(), math.pi / 6, 15)
    player_two = Car(4 * screen_w // 5, screen_h // 4, Vector(0,0), car.get_width(), car.get_height(), 7 * math.pi / 6, 15)
    players.append(player_one)
    players.append(player_two)
    game_ball = Ball(screen_w // 2, screen_h // 2, Vector(0,0), ball.get_width() // 2)
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                game_over = True
                games_left = -1

        keys_down = pygame.key.get_pressed()
        player_one_inputs = [keys_down[pygame.K_w], keys_down[pygame.K_s], keys_down[pygame.K_a], keys_down[pygame.K_d], keys_down[pygame.K_LSHIFT]]
        player_two_inputs = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]

        #screen.fill((0, 0, 0))

        screen.blit(field, (0,0))

        result = game_ball.update(players, map_info)
        if result != -1:
            #game_ball = Ball(screen_w // 2, screen_h // 2, Vector(0,0), ball.get_width() // 2)
            game_over = True
        draw(screen, ball, game_ball.x, game_ball.y)
        
        for i in range(len(players)):
            player = players[i]
            if i == 0:
                p_inputs = player_one_inputs
            else:
                p_inputs = player_two_inputs
            player.update(p_inputs, map_info)
            draw_angle(screen, car, math.degrees(player.angle), player.x, player.y)
            
        clock.tick(60)
        pygame.display.update()
            
    games_left -= 1
    


pygame.quit()
sys.exit()
