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
class SmarterBot:
    def __init__(self, map_info):
        self.map_info = map_info
        self.angle_error = math.pi / 11
        
    def get_move(self, game_data):
        # unpacking the game data
        my_x, my_y, my_angle = game_data[0], game_data[1], game_data[2]
        other_x, other_y, other_angle = game_data[3], game_data[4], game_data[5]
        ball_x, ball_y = game_data[6], game_data[7]
        ball_velocity = Vector(game_data[8], game_data[9])

        self.spacing = (self.map_info[BOTTOM_BOUND] - my_y)

        # finding the angle of attack
        target_x, target_y = self.map_info[RIGHT_BOUND] // 2, self.map_info[BOTTOM_BOUND] - self.map_info[GOAL_HEIGHT]
        target_angle = math.atan2(ball_y - target_y, target_x - ball_x)
        current_angle = math.atan2(my_y - target_y, target_x - my_x)
        
        if abs(target_angle - current_angle) < self.angle_error:
            # we're in business, ready to take the shot
            return self.drive_to_point(ball_x, ball_y, my_x, my_y, my_angle)
        else:
            # we need to get to the correct position
            target_x, target_y = ball_x - self.spacing * math.cos(target_angle), ball_y - self.spacing * math.sin(target_angle)
            return self.drive_to_point(target_x, target_y, my_x, my_y, my_angle)
            
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
                return [1, 0, 0, 1, 1]
            else:
                # turn left and forward
                return [1, 0, 1, 0, 1]
        else:
            if diff < math.pi:
                # turn right and forward
                return [1, 0, 0, 1, 1]
            else:
                # turn left and forward
                return [1, 0, 1, 0, 1]
            
        
