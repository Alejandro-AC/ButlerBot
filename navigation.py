from geometry_utils import *


INT_MAX = 100000000000000

def point_in_obstacles(p, obstacles):
    for obstacle in obstacles:
        distance = math.sqrt((p[0] - obstacle.x) ** 2 + (p[1] - obstacle.y) ** 2)
        if distance <= obstacle.width:
            return True

    return False

# Function Definition :RRT Algorithm
def rrt(p, parent, obstacles, step):
    """
        Summary line.

        Extended description of function.

        Parameters
        ----------
        p : (int, int)
            starting point
        parent : []
            Parent Node point Coordinates
        obstacles : [(int x, int y, int width), ...]
            List of Obstacles (circles)
        step : int
            Number of forward Steps towards random sampled point

        Returns
        -------
        good : boolean
            Wether the given start point is valid
        m : (int, int)
            Parent Node Point Coordinates
        ans : (int, int)
            Coordinates of next point

        """
    x, y = p
    if (x, y) not in parent and not point_in_obstacles((x, y), obstacles):
        x_m, y_m = -1, -1
        cur_min = INT_MAX
        for v in parent:
            distance = distance_between_points(v, (x, y))
            if distance < cur_min:
                x_m, y_m = v
                cur_min = distance

        good = True
        ans = []
        if abs(x_m - x) < abs(y_m - y):
            if y_m < y:
                for u in range(y_m + 1, y + 1):
                    x_cur = int(((x_m - x) / (y_m - y)) * (u - y) + x)
                    y_cur = u
                    if point_in_obstacles((x_cur, y_cur), obstacles):
                        good = False
                        break
                if good:
                    ans = [int(((x_m - x) / (y_m - y)) * (y_m + step - y) + x), y_m + step]
            else:
                for u in range(y, y_m):
                    x_cur = int(((x_m - x) / (y_m - y)) * (u - y) + x)
                    y_cur = u
                    if point_in_obstacles((x_cur, y_cur), obstacles):
                        good = False
                        break
                if good:
                    ans = [int(((x_m - x) / (y_m - y)) * (y_m - step - y) + x), y_m - step]

        else:
            if x_m < x:
                for u in range(x_m + 1, x + 1):
                    x_cur = u
                    y_cur = int(((y_m - y) / (x_m - x)) * (u - x) + y)
                    if point_in_obstacles((x_cur, y_cur), obstacles):
                        good = False
                        break
                if good:
                    ans = [x_m + step, int(((y_m - y) / (x_m - x)) * (x_m + step - x) + y)]
            else:
                for u in range(x, x_m):
                    x_cur = u
                    y_cur = int(((y_m - y) / (x_m - x)) * (u - x) + y)
                    if point_in_obstacles((x_cur, y_cur), obstacles):
                        good = False
                        break
                if good:
                    ans = [x_m - step, int(((y_m - y) / (x_m - x)) * (x_m - step - x) + y)]

        return good, (x_m, y_m), ans

    return False, (-1, -1), []
