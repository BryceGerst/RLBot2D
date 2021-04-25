import math

class Vector:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def dot(self, v_2):
        return (self.i * v_2.i) + (self.j * v_2.j)

    def scale(self, scalar, modify_self=False):
        if not modify_self:
            return Vector(self.i * scalar, self.j * scalar)
        else:
            self.i *= scalar
            self.j *= scalar

    def plus(self, v_2, modify_self=False):
        if not modify_self:
            return Vector(self.i + v_2.i, self.j + v_2.j)
        else:
            self.i += v_2.i
            self.j += v_2.j

    def minus(self, v_2, modify_self=False):
        if not modify_self:
            return Vector(self.i - v_2.i, self.j - v_2.j)
        else:
            self.i -= v_2.i
            self.j -= v_2.j

    def projection(self, onto):
        numerator = self.dot(onto)
        denominator = onto.dot(onto)
        return onto.scale((numerator / denominator))

    def unit_norm(self):
        normalization = math.sqrt(self.dot(self))
        new_i = -self.j / normalization
        new_j = self.i / normalization
        return Vector(new_i, new_j)

    def scaled_twin(self, scale):
        if self.i != 0 and self.j != 0:
            normalization = math.sqrt(self.dot(self))
            new_i = (self.i / normalization) * scale
            new_j = (self.j / normalization) * scale
            return Vector(new_i, new_j)
        else:
            return Vector(0, 0)

    def __str__(self):
        return str(self.i) + "i + " + str(self.j) + "j"

class RotationMatrix:
    def __init__(self, angle):
        cos = math.cos(angle)
        sin = math.sin(-angle)
        self.top_x = cos
        self.top_y = -sin
        self.bot_x = sin
        self.bot_y = cos

    def rotate(self, vector):
        x = vector.i
        y = vector.j
        new_x = (self.top_x * x) + (self.top_y * y)
        new_y = (self.bot_x * x) + (self.bot_y * y)
        return Vector(new_x, new_y)


LEFT_BOUND = 0
RIGHT_BOUND = 1
TOP_BOUND = 2
BOTTOM_BOUND = 3
GOAL_HEIGHT = 4
GOAL_LEFT_X = 5
GOAL_RIGHT_X = 6

class Ball:
    def __init__(self, x, y, velocity, radius):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.radius = radius

    def update(self, cars, map_info):
        friction = 0.99

        old_x = self.x
        old_y = self.y
        self.x += self.velocity.i
        self.y += self.velocity.j

        for car in cars:
            if car.hit(self):
                #print(self.velocity)
                d = self.velocity.minus(car.velocity)
                n = car.hit_norm # needs to be the correct unit normal vector of the hit
                #print(n)
                #self.velocity = n.scale(4)
                self.velocity = d.minus(n.scale(2 * d.dot(n)))
                self.velocity.plus(car.velocity, modify_self=True)
                #print(self.velocity)
                #self.x = old_x + self.velocity.i
                #self.y = old_y + self.velocity.j

        if (self.x - self.radius) > map_info[GOAL_LEFT_X] and (self.x + self.radius) < map_info[GOAL_RIGHT_X]:
            if (self.y + self.radius) < map_info[TOP_BOUND]:
                return 2
            elif (self.y - self.radius) > map_info[BOTTOM_BOUND]:
                return 1
        else:
            if (self.y - self.radius) < map_info[TOP_BOUND]:
                self.y = map_info[TOP_BOUND] + self.radius
                self.velocity.j *= -1
            elif (self.y + self.radius) > map_info[BOTTOM_BOUND]:
                self.y = map_info[BOTTOM_BOUND] - self.radius
                self.velocity.j *= -1

        if (self.y - self.radius) >= map_info[TOP_BOUND] and (self.y + self.radius) <= map_info[BOTTOM_BOUND]:
            if (self.x - self.radius) < map_info[LEFT_BOUND]:
                self.x = map_info[LEFT_BOUND] + self.radius
                self.velocity.i *= -1
            elif (self.x + self.radius) > map_info[RIGHT_BOUND]:
                self.x = map_info[RIGHT_BOUND] - self.radius
                self.velocity.i *= -1
        else:
            if (self.x - self.radius) < map_info[GOAL_LEFT_X]:
                self.x = map_info[GOAL_LEFT_X] + self.radius
                self.velocity.i *= -1
            elif (self.x + self.radius) > map_info[GOAL_RIGHT_X]:
                self.x = map_info[GOAL_RIGHT_X] - self.radius
                self.velocity.i *= -1

        

        self.velocity.scale(friction, modify_self=True)
        return -1

class Car:
    def __init__(self, x, y, velocity, width, height, angle, max_speed):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.width = width
        self.height = height
        self.angle = angle # radians
        self.max_speed = max_speed
        self.hit_norm = Vector(0, 0)

    def update(self, inputs, map_info): # for now the cars won't collide
        # W and S move in the direction determined to be forward
        # W is index 0 of inputs, S is index 1
        # A and D have significant control over which direction is determined to be forward
        # A is index 2, D is index 3
        # shift is index 4
        wheel_angle = self.angle
        wheel_turn_strength = (math.pi / 48)
        if inputs[4]:
            wheel_turn_strength *= 1.25
            
        wheel_power = 0.7
        friction = 0.90

        if inputs[0] ^ inputs[1]:
            if inputs[0]:
                if inputs[2] or inputs[3]:
                    wheel_angle += ((inputs[2] - inputs[3]) * wheel_turn_strength)
                forward = Vector(math.cos(wheel_angle), -math.sin(wheel_angle))
                
                self.velocity.plus(forward.scale(wheel_power), modify_self=True)
                self.angle = math.atan2(-forward.j, forward.i)
            else:
                if inputs[2] or inputs[3]:
                    wheel_angle += ((inputs[3] - inputs[2]) * wheel_turn_strength)
                backward = Vector(math.cos(wheel_angle), -math.sin(wheel_angle))
                
                self.velocity.plus(backward.scale(-wheel_power), modify_self=True)
                self.angle = math.atan2(-backward.j, backward.i)
                
        # ensures the car is not speeding
        if self.velocity.dot(self.velocity) > (self.max_speed * self.max_speed):
            self.velocity = Vector(self.max_speed * math.cos(self.angle), self.max_speed * math.sin(self.angle))

        self.x += self.velocity.i
        self.y += self.velocity.j

        if (self.x - self.width / 2) < map_info[LEFT_BOUND]:
            self.x = map_info[LEFT_BOUND] + self.width / 2
        elif (self.x + self.width / 2) > map_info[RIGHT_BOUND]:
            self.x = map_info[RIGHT_BOUND] - self.width / 2
        if (self.y - self.height / 2) < map_info[TOP_BOUND]:
            self.y = map_info[TOP_BOUND] + self.height / 2
        elif (self.y + self.height / 2) > map_info[BOTTOM_BOUND]:
            self.y = map_info[BOTTOM_BOUND] - self.height / 2

        self.velocity.scale(friction, modify_self=True)

    def hit(self, ball):
        taxicab_distance = abs(self.x - ball.x) + abs(self.y - ball.y)
        if taxicab_distance < (ball.radius + (self.width / 2) + (self.height / 2)):
            matrix = RotationMatrix(self.angle)
            inverse = RotationMatrix(-self.angle)
            
            left_side_x = -self.width / 2
            right_side_x = -left_side_x
            top_side_y = self.height / 2
            bottom_side_y = -top_side_y
            
            P = Vector(ball.x - self.x, ball.y - self.y)
            #P = matrix.rotate(P)
            P = inverse.rotate(P)

            if bottom_side_y <= P.j <= top_side_y:
                if P.i < left_side_x and P.i + ball.radius >= left_side_x:
                    self.hit_norm = matrix.rotate(Vector(-1, 0))
                    teleport = matrix.rotate(Vector(left_side_x - ball.radius, P.j))
                    ball.x = self.x + teleport.i
                    ball.y = self.y + teleport.j
                    return True
                elif P.i > right_side_x and P.i - ball.radius <= right_side_x:
                    self.hit_norm = matrix.rotate(Vector(1, 0))
                    teleport = matrix.rotate(Vector(right_side_x + ball.radius, P.j))
                    ball.x = self.x + teleport.i
                    ball.y = self.y + teleport.j
                    return True
            elif left_side_x <= P.i <= right_side_x:
                if P.j < bottom_side_y and P.j + ball.radius >= bottom_side_y:
                    self.hit_norm = matrix.rotate(Vector(0, -1))
                    teleport = matrix.rotate(Vector(P.i, bottom_side_y - ball.radius))
                    ball.x = self.x + teleport.i
                    ball.y = self.y + teleport.j
                    return True
                elif P.j > top_side_y and P.j - ball.radius <= top_side_y:
                    self.hit_norm = matrix.rotate(Vector(0, 1))
                    teleport = matrix.rotate(Vector(P.i, top_side_y + ball.radius))
                    ball.x = self.x + teleport.i
                    ball.y = self.y + teleport.j
                    return True

            if left_side_x <= P.i <= right_side_x and bottom_side_y <= P.j <= top_side_y:
                self.hit_norm = P.scaled_twin(1)
                ball.x -= ball.velocity.i
                ball.y -= ball.velocity.j
                #print('inside')
                return True
                
                
        return False
                
