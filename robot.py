from geometry_utils import *
import pygame
import math


class Robot:
    EPS = 0.001

    def __init__(self, x, y, width, height, proximity_sensors, carry_object_image=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.proximity_sensors = proximity_sensors

        self.direction = 0

        self.automove = False
        self.auto_move_point = (0,0)

        self.carry_object_image = carry_object_image

    def move(self, speed, forward=True):
        # `math.radians` can be used instead of `* (math.pi / 180)`
        if forward:
            self.x += speed * math.cos(math.radians(self.direction))
            self.y += speed * math.sin(math.radians(self.direction))
        else:
            self.x -= speed * math.cos(math.radians(self.direction))
            self.y -= speed * math.sin(math.radians(self.direction))

    def auto_move(self, speed):
        if distance_between_points(self.auto_move_point, (self.x, self.y)) < speed:
            return False
        x, y = self.auto_move_point
        direction = math.degrees(math.atan2(y - self.y, x - self.x)) % 360

        angle_difference = direction - self.direction

        if math.isclose(angle_difference, 0, abs_tol=0.001):
            self.move(speed)

        else:
            if angle_difference < 0:
                angle_difference += 360

            if angle_difference > speed:
                self.rotate(speed * find_rotation_direction(self.direction, direction))
            else:
                self.rotate(angle_difference * find_rotation_direction(self.direction, direction))

        return True

    def rotate(self, angle):
        self.direction = (angle + self.direction) % 360

        for sensor in self.proximity_sensors:
            sensor.orientation_angle += angle

    def update_sensors(self):

        for sensor in self.proximity_sensors:
            sensor_position_x = sensor.offset_x + self.x
            sensor_position_y = sensor.offset_y + self.y

            sensor_position_x, sensor_position_y = rotate((self.x, self.y), (sensor_position_x, sensor_position_y),
                                                          self.direction)

            radius = sensor.distance
            angle_start = sensor.orientation_angle - sensor.angle_range / 2
            angle_end = angle_start + sensor.angle_range

            sensor.sector = Sector(sensor_position_x, sensor_position_y, radius, angle_start, angle_end)

            sensor.wall_intersections = []

    def draw(self, screen):
        # pygame.draw.rect(screen, (0, 128, 255),pygame.Rect(self.x, self.y, self.width, self.height))
        pygame.draw.circle(screen, (0, 128, 255), (int(self.x), int(self.y)), self.height)
        if self.carry_object_image:
            screen.blit(pygame.transform.scale(self.carry_object_image, (self.width, self.width)),
                        (self.x - self.width / 2, self.y - self.width / 2))


