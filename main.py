import pygame
from robot import Robot
from object_detection import ObjectDetection
from wall import Wall
from proximity_sensor import ProximitySensor
from geometry_utils import *
import configuration
from button import *
from obstacle import *
from destination import *
import navigation
import speech_recognition_module
import time


class PHASE:
    SET_OBSTACLES = 1
    SET_START = 2
    SET_DESTINATIONS = 3
    CHOOSE_DESTINATION = 4
    NAVIGATION = 5
    GO_DESTINATION = 6
    RETURN_TO_START = 7
    DELIVER_OBJECT = 8


class App:

    def __init__(self):
        self._running = True
        self._screen_ = None
        self.size = configuration.SCREEN_WIDTH, configuration.SCREEN_HEIGHT

        self.pressed_left = False
        self.pressed_right = False
        self.pressed_up = False
        self.pressed_down = False
        self.mouse = None
        self.click = False

        self.background = None
        self.walls = []
        self.obstacles = set([])
        self.robot = None

        self.phase = None
        self.button = None
        self.start_position = None
        self.destinations = set([])
        self.object_images = []
        self.pasillo = pygame.image.load('pasillo.png')

        self.trace = []
        self.path_to_objective = []
        self.objective_position = None
        self.objective_name = None
        self.tree = dict()

        self.found_object = None
        self.object_detection = None

    def on_init(self):
        pygame.init()
        self._screen_ = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)

        self.background = pygame.Surface(self._screen_.get_size())
        self.background = self.background.convert()
        self.background.fill(configuration.WHITE)

        # self.create_walls()
        self.create_robot()
        self.create_object_detection()

        self._running = True
        self.phase = PHASE.SET_OBSTACLES
        self.button = Button(configuration.BLACK, configuration.BUTTON_X, configuration.BUTTON_Y,
                             configuration.BUTTON_WIDTH, configuration.BUTTON_HEIGHT)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_LEFT:  # left arrow turns left
                self.pressed_left = True
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                self.pressed_right = True
            elif event.key == pygame.K_UP:  # up arrow goes up
                self.pressed_up = True
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                self.pressed_down = True
            elif event.key == pygame.K_SPACE:  # down arrow goes down
                self.robot.automove = not self.robot.automove
                self.robot.auto_move_point = (0, 0)
        elif event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_LEFT:  # left arrow turns left
                self.pressed_left = False
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                self.pressed_right = False
            elif event.key == pygame.K_UP:  # up arrow goes up
                self.pressed_up = False
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                self.pressed_down = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.click = False

        self.mouse = pygame.mouse.get_pressed()[0], pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]

    def on_loop(self):
        self.process_phase()

        if self.pressed_left:
            self.robot.rotate(configuration.ROBOT_SPEED)
        if self.pressed_right:
            self.robot.rotate(-configuration.ROBOT_SPEED)
        if self.pressed_up:
            self.robot.move(configuration.ROBOT_SPEED, True)
        if self.pressed_down:
            self.robot.move(configuration.ROBOT_SPEED, False)

        if self.robot.automove:
            self.robot.automove = self.robot.auto_move(configuration.ROBOT_SPEED)

        self.robot.update_sensors()
        self.calculate_sensor_intersections()

    def on_render(self):
        self._screen_.blit(self.background, (0, 0))

        pygame.draw.rect(self._screen_, configuration.BLACK, (
            configuration.GAME_x, configuration.GAME_y, configuration.GAME_width, configuration.GAME_height),
                         configuration.GAME_border)

        # self.draw_walls()
        self.draw_obstacles()

        self.draw_sensor_coverage(self.robot.proximity_sensors)
        self.draw_sensor_intersections(self.robot.proximity_sensors)

        self.draw_destinations()
        self.draw_tree()
        self.draw_path()

        self.robot.draw(self._screen_)

        self.draw_ui()

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

    def create_walls(self):
        self.walls.append(Wall(20, 20, 20, 100, configuration.RED))
        self.walls.append(Wall(60, 350, 120, 200, configuration.RED))
        self.walls.append(Wall(300, 20, 20, 20, configuration.RED))
        self.walls.append(Wall(400, 50, 300, 120, configuration.RED))
        self.walls.append(Wall(500, 60, 500, 220, configuration.RED))
        self.walls.append(Wall(100, 500, 500, 320, configuration.RED))
        self.walls.append(Wall(300, 400, 100, 120, configuration.RED))

    def create_robot(self):
        proximity_sensors = [
            ProximitySensor(0, configuration.ROBOT_HEIGHT, configuration.SENSOR_ANGLE_RANGE,
                            configuration.SENSOR_DISTANCE, configuration.SENSOR_1_ORIENTATION),
            ProximitySensor(0, -configuration.ROBOT_WIDTH, configuration.SENSOR_ANGLE_RANGE,
                            configuration.SENSOR_DISTANCE,
                            configuration.SENSOR_2_ORIENTATION),
            ProximitySensor(configuration.ROBOT_WIDTH, 0, configuration.SENSOR_ANGLE_RANGE,
                            configuration.SENSOR_DISTANCE,
                            configuration.SENSOR_3_ORIENTATION)
        ]

        self.robot = Robot(configuration.ROBOT_INITIAL_POS_X, configuration.ROBOT_INITIAL_POS_Y,
                           configuration.ROBOT_WIDTH, configuration.ROBOT_HEIGHT,
                           proximity_sensors)

    def create_destination(self, p, image_path):
        x, y = p
        image = pygame.image.load(image_path)
        dest = Destination(x, y, configuration.GREEN,
                           configuration.DESTINATION_WIDTH,
                           image, image_path)
        self.destinations.add(dest)

    def create_object_detection(self):
        self.object_detection = ObjectDetection(configuration.WEIGHTS_FILE, configuration.CLASSES_FILE,
                                                configuration.CONFIG_FILE)

    def process_phase(self):

        clicked = self.mouse[0]
        m_x, m_y = self.mouse[1], self.mouse[2]

        if self.click and point_inside_rect(self.button.x, self.button.y, self.button.width, self.button.height,
                                            m_x, m_y):
            self.change_phase()

        if self.phase is PHASE.SET_OBSTACLES:

            if clicked and self.point_inside_game(m_x, m_y):
                self.obstacles.add(Obstacle(m_x, m_y, configuration.BLACK, 10))

        elif self.phase is PHASE.SET_START:

            if clicked and self.point_inside_game(m_x, m_y):
                self.start_position = (m_x, m_y)
                self.robot.x, self.robot.y = self.start_position

        elif self.phase is PHASE.SET_DESTINATIONS:
            n_destinations = len(self.destinations)
            if self.click and self.point_inside_game(m_x, m_y) and n_destinations < configuration.N_DESTINATIONS:
                self.create_destination((m_x, m_y), configuration.DESTINATION_IMAGE_PATHS[n_destinations])
                self.click = False

        elif self.phase is PHASE.CHOOSE_DESTINATION:

            if not self.objective_name:

                voice_data = speech_recognition_module.record_audio()
                word = speech_recognition_module.respond(voice_data)

                if word == "manzana":
                    print("voy a por la manzana")
                    self.objective_name = 'apple'
                elif word == "botella":
                    print("voy a por la botella")
                    self.objective_name = 'bottle'
                elif word == "libro":
                    print("voy a por el libro")
                    self.objective_name = 'book'
                elif word == "taza":
                    print("voy a por la taza")
                    self.objective_name = 'cup'
                else:
                    print("repite")
                    time.sleep(0.5)

        elif self.phase is PHASE.NAVIGATION:
            random_point = random_point_within_rect(configuration.GAME_x + configuration.GAME_border,
                                                    configuration.GAME_y + configuration.GAME_border,
                                                    configuration.GAME_width - configuration.GAME_border,
                                                    configuration.GAME_height - configuration.GAME_border)

            is_valid_point, parent_node, next_point = navigation.rrt(random_point, self.tree, self.obstacles,
                                                                     configuration.STEP)

            if is_valid_point and next_point:
                next_point = (next_point[0], next_point[1])

                # Check new point not in obstacle or already visited
                if next_point not in self.tree:
                    self.tree[next_point] = parent_node

                # Check found objective
                destination = self.check_reached_objective(next_point)
                if destination:

                    pygame.display.update(self._screen_.blit(
                        pygame.transform.scale(destination.image,
                                               (configuration.CAMERA_WIDTH, configuration.CAMERA_HEIGHT)),
                        (configuration.CAMERA_X, configuration.CAMERA_Y)))

                    destination_label = self.identify_object(destination.image_path)

                    if destination_label == self.objective_name:
                        self.objective_position = next_point
                        self.destinations.clear()
                        self.destinations = [destination]
                        self.change_phase()
                    else:
                        self.found_object = None
                        self.destinations.remove(destination)

        elif self.phase is PHASE.GO_DESTINATION:
            if self.path_to_objective:
                if self.robot.automove:
                    self.robot.automove = self.robot.auto_move(configuration.ROBOT_SPEED)
                else:
                    self.robot.auto_move_point = self.path_to_objective.pop()
                    self.robot.automove = True

        elif self.phase is PHASE.RETURN_TO_START:
            if self.trace:
                if self.robot.automove:
                    self.robot.automove = self.robot.auto_move(configuration.ROBOT_SPEED)
                else:
                    self.robot.auto_move_point = self.trace.pop(0)
                    self.robot.automove = True
            else:
                self.change_phase()

        elif self.phase is PHASE.DELIVER_OBJECT:
            speech_recognition_module.speak("Aquí tiene su " + str(self.objective_name))

    def change_phase(self):

        self.phase += 1
        self.click = False

        if self.phase is PHASE.SET_OBSTACLES:
            self.button.colour = configuration.RED

        elif self.phase is PHASE.SET_START:
            self.button.colour = configuration.GREEN

        elif self.phase is PHASE.SET_DESTINATIONS:
            self.button.colour = configuration.BLUE
            self.tree[self.start_position] = self.start_position

        elif self.phase is PHASE.CHOOSE_DESTINATION:
            self.button.colour = configuration.GREEN

        elif self.phase is PHASE.NAVIGATION:
            self.button.colour = configuration.BLACK

        elif self.phase is PHASE.GO_DESTINATION:
            self.button.colour = configuration.ORANGE

            # build path to objective
            curr_pos = self.objective_position
            self.trace.append(curr_pos)

            while curr_pos != self.start_position:
                curr_pos = self.tree[curr_pos]
                self.trace.append(curr_pos)

            self.path_to_objective = self.trace.copy()

        elif self.phase is PHASE.RETURN_TO_START:
            self.button.colour = configuration.BLACK
            self.robot.carry_object_image = self.destinations[0].image
            self.destinations.clear()

        else:
            self.button.colour = configuration.YELLOW

    def calculate_sensor_intersections(self):
        walls = [(wall.point1, wall.point2) for wall in self.walls]
        obstacles = [(obstacle.x, obstacle.y, obstacle.width) for obstacle in self.obstacles]
        for sensor in self.robot.proximity_sensors:
            sensor.calculate_intersections(walls)
            sensor.calculate_intersections(obstacles)

    def identify_object(self, image_path):
        return self.object_detection.get_prediction(image_path)

    # Function Definition : Point inside Game ?
    def point_inside_game(self, x, y):
        return point_inside_rect(configuration.GAME_x, configuration.GAME_y, configuration.GAME_width,
                                 configuration.GAME_height, x, y)

    def check_reached_objective(self, point):
        for dest in self.destinations:
            if point_inside_rect(dest.x - dest.width / 2, dest.y - dest.width / 2, dest.width, dest.width, point[0],
                                 point[1]):
                return dest
        return False

    def draw_walls(self):
        for wall in self.walls:
            wall.draw(self._screen_)

    def draw_obstacles(self):
        for obstacle in self.obstacles:
            obstacle.draw(self._screen_)

    def draw_sensor_coverage(self, proximity_sensors):
        for prox_sensor in proximity_sensors:
            prox_sensor.draw_coverage(self._screen_, configuration.ORANGE)

    def draw_sensor_intersections(self, proximity_sensors):
        for prox_sensor in proximity_sensors:
            prox_sensor.draw_intersections(self._screen_, configuration.RED, configuration.YELLOW)

    def draw_destinations(self):
        for dest in self.destinations:
            dest.draw(self._screen_)

    def draw_tree(self):
        for key, value in self.tree.items():
            pygame.draw.line(self._screen_, configuration.BLUE, key, value)

    def draw_path(self):
        for p in self.trace:
            pygame.draw.line(self._screen_, configuration.GREEN, p, self.tree[p], 3)

    def draw_ui(self):

        self.button.draw(self._screen_)
        self.button.draw_text(self._screen_, configuration.WHITE)

        self.draw_text_center_rect(self._screen_, configuration.BLACK, 'Sensor (Right) Distance: ' + str(round(self.robot.proximity_sensors[0].detected_distance,2)),
                                   [configuration.CHATBOX_X - 100, configuration.CHATBOX_Y,
                                    configuration.PHASE_DESCRIPTION_WIDTH, 15])
        self.draw_text_center_rect(self._screen_, configuration.BLACK,
                                   'Sensor (Left) Distance: ' + str(round(self.robot.proximity_sensors[1].detected_distance,2)),
                                   [configuration.CHATBOX_X - 100, configuration.CHATBOX_Y + 15,
                                    configuration.PHASE_DESCRIPTION_WIDTH, 15])
        self.draw_text_center_rect(self._screen_, configuration.BLACK,
                                   'Sensor (Center) Distance: ' + str(round(self.robot.proximity_sensors[2].detected_distance,2)),
                                   [configuration.CHATBOX_X - 100, configuration.CHATBOX_Y + 30,
                                    configuration.PHASE_DESCRIPTION_WIDTH, 15])

        image = None
        if self.found_object:
            image = self.found_object.image
        else:
            image = self.pasillo

        self._screen_.blit(pygame.transform.scale(image, (configuration.CAMERA_WIDTH, configuration.CAMERA_HEIGHT)),
                           (configuration.CAMERA_X, configuration.CAMERA_Y))

        self.draw_text_center_rect(self._screen_, configuration.BLACK, configuration.PHASE_DESCRIPTION[self.phase - 1],
                                   [configuration.PHASE_DESCRIPTION_X, configuration.PHASE_DESCRIPTION_Y,
                                    configuration.PHASE_DESCRIPTION_WIDTH, configuration.PHASE_DESCRIPTION_HEIGHT])

        self.draw_text_center_rect(self._screen_, configuration.BLACK, 'CAMERA',
                                   [configuration.CAMERA_LABEL_X, configuration.CAMERA_LABEL_Y,
                                    configuration.CAMERA_LABEL_WIDTH, configuration.CAMERA_LABEL_HEIGHT])
        self.draw_text_center_rect(self._screen_, configuration.BLUE, configuration.PHASE_TITLE[self.phase - 1],
                                   [configuration.PHASE_DESCRIPTION_LABEL_X, configuration.PHASE_DESCRIPTION_LABEL_Y,
                                    configuration.PHASE_DESCRIPTION_LABEL_WIDTH,
                                    configuration.PHASE_DESCRIPTION_LABEL_HEIGHT])

    # Function Definition : Text on Button
    def draw_text_center_rect(self, screen, color, text, rect, font_size=18):
        font = pygame.font.SysFont("Calibri", font_size)
        text = font.render(text, True, color)
        textRect = text.get_rect()
        textRect.center = (rect[0] + rect[2] / 2, rect[1] + rect[3] / 2)
        screen.blit(text, textRect)


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
