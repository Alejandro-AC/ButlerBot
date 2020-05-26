import pygame.gfxdraw
from geometry_utils import *


class ProximitySensor:

    def __init__(self, offset_x, offset_y, angle_range, distance, orientation_angle):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.angle_range = angle_range
        self.distance = distance
        self.orientation_angle = orientation_angle

        self.obstacle_intersections = []
        self.sector = None

        self.font = pygame.font.SysFont("Calibri", 15)
        self.detected_distance = 0

    def draw_coverage(self, surface, color):
        radius = self.distance

        # clockwise
        angle_start = self.orientation_angle - self.angle_range / 2
        angle_end = angle_start + self.angle_range

        pygame.gfxdraw.pie(surface, int(self.sector.x), int(self.sector.y), radius, int(angle_start % 360), int(angle_end % 360), color)

    def calculate_intersections(self, obstacles):
        self.obstacle_intersections = []

        for obstacle in obstacles:
            # Wall (line)
            if len(obstacle) == 2:
                intersection_points = sector_line_intersection(obstacle[0], obstacle[1], self.sector)

                self.obstacle_intersections.append([obstacle, intersection_points])
            elif len(obstacle) == 3:

                intersection_points = sector_circle_intersection((obstacle[0], obstacle[1]), obstacle[2], self.sector)
                self.obstacle_intersections.append([obstacle, intersection_points])


    def draw_intersections(self, surface, intersection_color, text_color, debug=False):
        min_distance = -1
        detected_point = []

        for obstacle_intersections in self.obstacle_intersections:
            intersection_points = obstacle_intersections[1]
            obstacle = obstacle_intersections[0]

            if intersection_points:

                # Obstacle is a wall (line)
                if len(obstacle) == 2:
                    distance, nearest_point = get_nearest_point_within_sector(intersection_points, (obstacle[0], obstacle[1]),
                                                                          self.sector)
                else:
                    distance, nearest_point = distance_between_points(intersection_points[0], (self.sector.x, self.sector.y)), intersection_points[0]

                if distance < min_distance or min_distance == -1:
                    min_distance = distance
                    detected_point = nearest_point

                if len(intersection_points) == 2 and debug:
                    pygame.draw.circle(surface, intersection_color, (int(nearest_point[0]), int(nearest_point[1])), 4)

                    for p in intersection_points:
                        pygame.draw.circle(surface, (0, 255, 0), (int(p[0]), int(p[1])), 5)

                    pygame.draw.line(surface, (0, 0, 255), intersection_points[0], intersection_points[1])

        if (detected_point):
            pygame.draw.circle(surface, intersection_color, (int(detected_point[0]), int(detected_point[1])), 4)
            self.detected_distance = min_distance
            # label = self.font.render("Distance: " + str(min_distance), 1, text_color)
            # label_rect = surface.blit(label, (detected_point[0], detected_point[1]))
            # pygame.display.update(label_rect)
        else:
            self.detected_distance = 0


