import math, random
import numpy as np
from PhysicsObject import Ball, Car, Vector
from NNet import init_nnet

car_width = 120
car_height = 75
ball_width = 60
screen_w = 900
screen_h = 1000
goal_height = 100
goal_left_x = 289
goal_right_x = 611
map_info = [0, screen_w, goal_height, screen_h - goal_height, goal_height, goal_left_x, goal_right_x]


def gen_game_data(player_one, player_two, ball, player_num):
    if player_num == 1:
        data = [player_one.x, player_one.y, player_one.angle,
                player_two.x, player_two.y, player_two.angle,
                ball.x, ball.y, ball.velocity.i, ball.velocity.j]
    else:
        # tried to make it so it shows the data from the specific player's perspective
        data = [screen_w - player_two.x, screen_h - player_two.y, math.pi + player_two.angle,
                screen_w - player_one.x, screen_h - player_one.y, math.pi + player_one.angle,
                screen_w - ball.x, screen_h - ball.y, -ball.velocity.i, -ball.velocity.j]
    # should the data include the players' velocities? I think it wouldn't hurt, but might be unnecessary
    return np.asarray([data])

training = True

nnet = init_nnet()

while training:
    game_over = False
    players = []
    player_one = Car(screen_w // 2, 3 * screen_h // 4, Vector(0,0), car_width, car_height, math.pi / 2, 15)
    player_two = Car(screen_w // 2, screen_h // 4, Vector(0,0), car_width, car_height, -math.pi / 2, 15)
    players.append(player_one)
    players.append(player_two)
    game_ball = Ball(screen_w // 2, screen_h // 2, Vector(0,0), ball_width // 2)

    frame_num = 0
    record_interval = 4 # records every nth frame for training purposes

    inputs = []
    outputs = []

    while not game_over:
        player_one_data = gen_game_data(player_one, player_two, game_ball, 1)
        player_two_data = gen_game_data(player_one, player_two, game_ball, 2)

        player_one_inputs = []
        player_two_inputs = []
        
        player_one_result = nnet(player_one_data)
        for i in range(len(player_one_result[0])):
            player_one_inputs.append(round(player_one_result[0][i].numpy()))
        player_two_result = nnet(player_two_data)
        for i in range(len(player_two_result[0])):
            player_two_inputs.append(round(player_two_result[0][i].numpy()))

        if frame_num % record_interval == 0:
            inputs.append(player_one_data)
            outputs.append(player_one_inputs)
            inputs.append(player_two_data)
            outputs.append(player_two_inputs)

        result = game_ball.update(players, map_info)
        if result != -1:
            game_over = True
            winner = result
##        if frame_num == 100:
##            print('frame limit hit')
##            game_over = True
##            winner = 1

        if not game_over:
            for i in range(len(players)):
                player = players[i]
                if i == 0:
                    p_inputs = player_one_inputs
                else:
                    p_inputs = player_two_inputs
                player.update(p_inputs, map_info)

        frame_num += 1

    train_inputs = []
    train_outputs = []
    for i in range(winner - 1, len(outputs), 2):
        train_inputs.append(inputs[i][0])
        train_outputs.append(np.asarray(outputs[i]))
        
    x = np.asarray(train_inputs)
    y = np.asarray(train_outputs)
    
    nnet.fit(x, y, epochs=100)

    training = False
