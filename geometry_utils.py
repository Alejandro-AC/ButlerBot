import math
from random import randint as ri


class Sector:
    def __init__(self, x, y, radius, start_angle, end_angle):
        self.x = x
        self.y = y
        self.radius = radius
        self.start_angle = start_angle % 360
        self.end_angle = end_angle % 360


# Function to get the intersection between a sector and a line
def sector_line_intersection(p, q, sector):
    p_adjusted = adjust_to_origin(p, sector)
    q_adjusted = adjust_to_origin(q, sector)
    center = (0, 0)
    a, b, c = line_equation_parameters_from_points(p_adjusted, q_adjusted)

    circle_intersection_points = intersection_line_circle(sector.radius, a, b, c)
    sector_points_adjusted = []

    # No intersection
    if not circle_intersection_points:
        return False
    # Whole Circle Intersection
    else:

        # Poke cases
        if check_point_in_sector(p_adjusted, sector):
            sector_points_adjusted.append(p_adjusted)
        if check_point_in_sector(q_adjusted, sector):
            sector_points_adjusted.append(q_adjusted)

        # Sector lines intersection
        line_arc_1_x = sector.radius * math.cos(math.radians(sector.start_angle))
        line_arc_1_y = sector.radius * math.sin(math.radians(sector.start_angle))
        line_arc_2_x = sector.radius * math.cos(math.radians(sector.end_angle))
        line_arc_2_y = sector.radius * math.sin(math.radians(sector.end_angle))

        point_arc_1 = line_arc_1_x, line_arc_1_y
        point_arc_2 = line_arc_2_x, line_arc_2_y

        point_arc_1_intersection = intersection_line_segments(center, point_arc_1, p_adjusted, q_adjusted)
        if len(sector_points_adjusted) != 2 and point_arc_1_intersection:
            sector_points_adjusted.append(point_arc_1_intersection)
        point_arc_2_intersection = intersection_line_segments(center, point_arc_2, p_adjusted, q_adjusted)
        if len(sector_points_adjusted) != 2 and point_arc_2_intersection:
            sector_points_adjusted.append(point_arc_2_intersection)

        # Sector arc intersection
        circle_intersection_points = [intersection for intersection in circle_intersection_points if
                                      is_between_points(p_adjusted, intersection, q_adjusted)]

        if len(sector_points_adjusted) != 2 and len(circle_intersection_points) > 0 and check_point_in_sector(
                circle_intersection_points[0], sector):
            sector_points_adjusted.append(circle_intersection_points[0])
        if len(sector_points_adjusted) != 2 and len(circle_intersection_points) == 2 and check_point_in_sector(
                circle_intersection_points[1], sector):
            if check_point_in_sector(circle_intersection_points[1], sector):
                sector_points_adjusted.append(circle_intersection_points[1])

    sector_points = unadjust_from_origin(sector_points_adjusted, sector)

    return sector_points


def sector_circle_intersection(c_center, c_radius, sector):
    c_center_adjusted = adjust_to_origin(c_center, sector)
    center = (0, 0)

    # Too far
    if distance_between_points(center, c_center_adjusted) > sector.radius + c_radius:
        return False

    sector_points_adjusted = []

    # sector center in circle
    if check_point_in_circle((sector.x, sector.y), c_center, c_radius):
        return [(sector.x, sector.y)]

    # center of circle in sector
    if check_point_in_sector(c_center_adjusted, sector):
        vX, vY = c_center_adjusted
        magV = math.sqrt(vX * vX + vY * vY)
        aX = c_center_adjusted[0] - vX / magV * c_radius
        aY = c_center_adjusted[1] - vY / magV * c_radius

        return unadjust_from_origin([(aX, aY)], sector)

    '''
    # circle intersects circle
    line_arc_1_x = sector.radius * math.cos(math.radians(sector.start_angle))
    line_arc_1_y = sector.radius * math.sin(math.radians(sector.start_angle))
    line_arc_2_x = sector.radius * math.cos(math.radians(sector.end_angle))
    line_arc_2_y = sector.radius * math.sin(math.radians(sector.end_angle))

    point_arc_1 = line_arc_1_x, line_arc_1_y
    point_arc_2 = line_arc_2_x, line_arc_2_y

    a, b, c = line_equation_parameters_from_points(point_arc_1, center)
    point_arc_1_intersection = intersection_line_circle(c_radius, a, b, c)
    for point in point_arc_1_intersection:
        if is_between_points(point, center, point_arc_1):
            sector_points_adjusted.append(point)

    a, b, c = line_equation_parameters_from_points(point_arc_2, center)
    point_arc_2_intersection = intersection_line_circle(c_radius, a, b, c)
    for point in point_arc_2_intersection:
        if is_between_points(point, center, point_arc_2):
            sector_points_adjusted.append(point)

    if len(sector_points_adjusted) > 0:
        return unadjust_from_origin(sector_points_adjusted, sector)
    '''

    # circle intersects arc
    return False


# reference https://stackoverflow.com/questions/6270785/how-to-determine-whether-a-point-x-y-is-contained-within-an-arc-section-of-a-c
# Function to check if a given point is within a sector
def check_point_in_sector(point, sector):
    x, y = point

    # counter clockwise
    start_angle = sector.start_angle
    end_angle = sector.end_angle
    radius = sector.radius

    if x * x + y * y <= radius * radius + 10:
        angle = math.atan2(y, x)
        angle = math.degrees(angle) % 360

        if start_angle < end_angle:
            if start_angle < angle < end_angle:
                return True
        else:
            if end_angle > angle or angle > start_angle:
                return True

    return False


def check_point_in_circle(p, c_center, c_radius):
    dx = int(abs(p[0] - c_center[0]))
    dy = int(abs(p[1] - c_center[1]))

    if dx > c_radius:
        return False
    if dy > c_radius:
        return False
    if dx + dy <= c_radius:
        return True
    if dx ^ 2 + dy ^ 2 <= c_radius ^ 2:
        return True
    else:
        return False


# Line equation: Ax+By+C=0
# assumes center of circle at origin
# Function to get the intersection(s) between a line and a circle
def intersection_line_circle(r, a, b, c):
    EPS = 0.001

    x0 = -a * c / (a * a + b * b)
    y0 = -b * c / (a * a + b * b)
    if c * c > r * r * (a * a + b * b) + EPS:
        return False

    elif abs(c * c - r * r * (a * a + b * b)) < EPS:
        p = (x0, y0)
        return [p]

    else:
        d = r * r - c * c / (a * a + b * b)
        mult = math.sqrt(d / (a * a + b * b))
        ax = x0 + b * mult
        bx = x0 - b * mult
        ay = y0 - a * mult
        by = y0 + a * mult

        p = (ax, ay)
        q = (bx, by)

        return [p, q]


# Function to get the intersection between two line segments
def intersection_line_segments(p0, p1, p2, p3):
    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0:
        return None  # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive:
        return None  # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive:
        return None  # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive:
        return None  # no collision

    # collision detected

    t = t_numer / denom

    intersection_point = [p0[0] + (t * s10_x), p0[1] + (t * s10_y)]

    return intersection_point


# Function to get the nearest point from the given list or of the given line within the given sector
def get_nearest_point_within_sector(points, line, sector):
    center = (sector.x, sector.y)
    if len(points) == 2:
        return distance_point_line(center, points[0], points[1])
    else:
        if check_point_in_sector(line[0], sector):
            point_in_sector = line[0]
        else:
            point_in_sector = line[1]

        return distance_point_line(center, points[0], point_in_sector)


# Calc minimum distance from a point and a line segment (i.e. consecutive vertices in a polyline).
def distance_point_line(point, line_point1, line_point2):
    px, py = point
    x1, y1 = line_point1
    x2, y2 = line_point2

    line_length = distance_between_points_as_coord(x1, y1, x2, y2)

    if line_length < 0.0001:
        return 0, point

    u1 = (((px - x1) * (x2 - x1)) + ((py - y1) * (y2 - y1)))
    u = u1 / (line_length * line_length)

    if (u < 0.00001) or (u > 1):
        # // closest point does not fall within the line segment, take the shorter distance
        # // to an endpoint
        d1 = distance_between_points_as_coord(px, py, x1, y1)
        d2 = distance_between_points_as_coord(px, py, x2, y2)
        if d1 > d2:
            distance = d2
            intersecting_x, intersecting_y = x2, y2
        else:
            distance = d1
            intersecting_x, intersecting_y = x1, y1
    else:
        # Intersecting point is on the line, use the formula
        intersecting_x = x1 + u * (x2 - x1)
        intersecting_y = y1 + u * (y2 - y1)
        distance = distance_between_points_as_coord(px, py, intersecting_x, intersecting_y)

    intersecting_point = (intersecting_x, intersecting_y)

    return distance, intersecting_point


# Function Definition : Point inside given Rectangle ?
def point_inside_rect(xr, yr, wr, hr, x, y):
    if x > xr and x < xr + wr:
        if y > yr and y < yr + hr:
            return True
    return False


# The angle should be given in radians.
# Function to Rotate a point counterclockwise by a given angle around a given origin.
def rotate(origin, point, angle):
    angle = math.radians(angle)

    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy


# Functions to find the distance between 2 points
def distance_between_points_as_coord(x1, y1, x2, y2):
    return math.sqrt(math.pow((x2 - x1), 2) + math.pow((y2 - y1), 2))


def distance_between_points(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)


# Function to find the line equation parameters given two points
def line_equation_parameters_from_points(p, q):
    a = q[1] - p[1]
    b = p[0] - q[0]
    c = -1 * (a * (p[0]) + b * (p[1]))

    return a, b, c


# Function to determine if a given point p is between the points r and q
def is_between_points(p, r, q):
    return math.isclose(distance_between_points(p, r) + distance_between_points(r, q), distance_between_points(p, q))


def adjust_to_origin(p, sector):
    return p[0] - sector.x, p[1] - sector.y


def unadjust_from_origin(points, sector):
    points_unadjusted = []
    for p in points:
        points_unadjusted.append((p[0] + sector.x, p[1] + sector.y))

    return points_unadjusted


# Function Definition : Random Point Generator inside Game
def random_point_within_rect(x, y, w, h):
    x_random = ri(x, x + w - 1)
    y_random = ri(y, y + h - 1)
    return ((x_random, y_random))

# angles in degrees
def find_rotation_direction(cur_angle, target_angle):
    diff = target_angle - cur_angle
    if diff < 0:
        diff += 360
    if diff > 180:
        return -1
    else:
        return 1
