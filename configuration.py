# Define the colors we will use in RGB format
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 188, 0)

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

GAME_x = 20
GAME_y = 40
GAME_width = SCREEN_WIDTH - GAME_x*2
GAME_height = 500
GAME_border = 3

EPSILON = 0.001

SENSOR_ANGLE_RANGE = 40
SENSOR_DISTANCE = 150

# Clockwise (start at x axis)
SENSOR_1_ORIENTATION = 90
SENSOR_2_ORIENTATION = 270
SENSOR_3_ORIENTATION = 0

ROBOT_SPEED = 0.5
ROBOT_WIDTH = 20
ROBOT_HEIGHT = 20
ROBOT_INITIAL_POS_X = -200
ROBOT_INITIAL_POS_Y = -200

# Navigation

STEP = 10

OBSTACLE_WIDTH = 10
DESTINATION_WIDTH = 45
N_DESTINATIONS = 4

# IMAGES
DESTINATION_IMAGE_PATHS = ['./objects/botella.png',
                           './objects/libro.png',
                           './objects/manzana.png',
                           './objects/taza.png']
# YOLOv3
CLASSES_FILE = './yolo/yolov3.txt'
WEIGHTS_FILE = './yolo/yolov3.weights'
CONFIG_FILE = './yolo/yolov3.cfg'

# UI

DESCRIPTION_PHASE_1 = "Draw the Obstacles, then CLICK BLACK Button"
DESCRIPTION_PHASE_2 = "Draw the Starting point, then CLICK RED Button"
DESCRIPTION_PHASE_3 = "Draw the Destination point, then CLICK OBJECT1 Button"

DESCRIPTION_PHASE_4 = "Path is being explored using RRT Algorithm"


BUTTON_WIDTH = 150
BUTTON_HEIGHT = 75
BUTTON_X = GAME_width / 2 - BUTTON_WIDTH/2 + 60
BUTTON_Y = GAME_y * 5 + GAME_height

BUTTON_TEXT_OFFSET_X = 10
BUTTON_TEXT_OFFSET_Y = BUTTON_HEIGHT/2

CHATBOX_WIDTH = 300
CHATBOX_HEIGHT = 200
CHATBOX_X = GAME_x * 2
CHATBOX_Y = GAME_y * 2 + GAME_height

CAMERA_WIDTH = 200
CAMERA_HEIGHT = 200
CAMERA_X = SCREEN_WIDTH - GAME_x * 2 - CAMERA_WIDTH
CAMERA_Y = GAME_y * 2 + GAME_height

PHASE_DESCRIPTION_WIDTH = 400
PHASE_DESCRIPTION_HEIGHT = 100
PHASE_DESCRIPTION_X = GAME_width / 2 - PHASE_DESCRIPTION_WIDTH/2 + 60
PHASE_DESCRIPTION_Y = GAME_y * 2 + GAME_height

CAMERA_LABEL_X = CAMERA_X
CAMERA_LABEL_Y = CAMERA_Y - GAME_y / 2 - 10
CAMERA_LABEL_WIDTH = CAMERA_WIDTH
CAMERA_LABEL_HEIGHT = GAME_y / 2 + 5

PHASE_DESCRIPTION_LABEL_X = PHASE_DESCRIPTION_X
PHASE_DESCRIPTION_LABEL_Y = PHASE_DESCRIPTION_Y - GAME_y / 2 - 10
PHASE_DESCRIPTION_LABEL_WIDTH = PHASE_DESCRIPTION_WIDTH
PHASE_DESCRIPTION_LABEL_HEIGHT = GAME_y / 2 + 5

PHASE_TITLE = ['Set the obstacles:',
               'Set the starting point:',
               'Set the objects to find:',
               'Choose object to retrieve:',
               'Exploration:',
               'Navigation:',
               'Retrieval:',
               'Deliver:']

PHASE_DESCRIPTION = ['Set the obstacles by clicking within the game area.',
               'Set the starting point for ButlerBot by clicking within the game area.',
               'Set the objects to search by clicking within the game area.',
               'Tell the robot which object you want to be retrieved. (By voice)',
               'ButlerBot explores the map. Identifies objects. Creates path',
               'ButlerBot goes to the specified object. Follows path',
               'ButlerBot picks up the specified object and returns to the starting point carrying it.',
               'ButlerBot delivers the object and tells you so.']