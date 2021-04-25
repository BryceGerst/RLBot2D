import math, random
from PhysicsObject import Ball, Car, Vector

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
                ball.x, ball.y]
    else:
        # tried to make it so it shows the data from the specific player's perspective
        data = [screen_w - player_two.x, screen_h - player_two.y, math.pi + player_two.angle,
                screen_w - player_one.x, screen_h - player_one.y, math.pi + player_one.angle,
                screen_w - ball.x, screen_h - ball.y, -ball.velocity.i, -ball.velocity.j]
    # should the data include the players' velocities? I think it wouldn't hurt, but might be unnecessary

training = True

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
        player_one_inputs = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]#nnet output
        player_two_inputs = [random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1), random.randint(0, 1)]#nnet output

        if frame_num % record_interval == 0:
            inputs.append(gen_game_data, player_one, player_two, game_ball, 1)
            outputs.append(player_one_inputs)
            inputs.append(gen_game_data, player_one, player_two, game_ball, 2)
            outputs.append(player_two_inputs)

        result = game_ball.update(players, map_info)
        if result != -1:
            game_over = True
            winner = result
        
        for i in range(len(players)):
            player = players[i]
            if i == 0:
                p_inputs = player_one_inputs
            else:
                p_inputs = player_two_inputs
            player.update(p_inputs, map_info)

    train_inputs = []
    train_outputs = []
    for i in range(winner - 1, len(outputs), 2):
        train_inputs.append(inputs[i])
        train_outputs.append(outputs[i])

    training = False
