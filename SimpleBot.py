import math
import numpy as np
from PhysicsObject import Ball, Car, Vector


LEFT_BOUND = 0
RIGHT_BOUND = 1
TOP_BOUND = 2
BOTTOM_BOUND = 3
GOAL_HEIGHT = 4
GOAL_LEFT_X = 5
GOAL_RIGHT_X = 6

# this bot should drive towards the ball
class SimpleBot:
    def get_move(self, game_data):
        # unpacking the game data
        my_x, my_y, my_angle = game_data[0], game_data[1], game_data[2]
        other_x, other_y, other_angle = game_data[3], game_data[4], game_data[5]
        ball_x, ball_y = game_data[6], game_data[7]
        ball_velocity = Vector(game_data[8], game_data[9])

        return self.drive_to_point(ball_x, ball_y, my_x, my_y, my_angle)
            
    def drive_to_point(self, target_x, target_y, my_x, my_y, my_angle):
        target_angle = math.atan2(my_y - target_y, target_x - my_x)
        if target_angle < 0:
            target_angle += 2 * math.pi

        diff = abs(my_angle - target_angle)
        
        if diff == 0:
            return [1, 0, 0, 0, 0]
        if my_angle < target_angle:
            if diff > math.pi:
                # turn right and forward
                return [1, 0, 0, 1, 0]
            else:
                # turn left and forward
                return [1, 0, 1, 0, 0]
        else:
            if diff < math.pi:
                # turn right and forward
                return [1, 0, 0, 1, 0]
            else:
                # turn left and forward
                return [1, 0, 1, 0, 0]
        
