import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import argparse
import glob
import random
import numpy as np


class ObjectDetection:
    def __init__(self, weights, classes, config):
        self.weights = weights
        self.classes = classes
        self.config = config

    def get_prediction(self, image_path):
        image = cv2.imread(image_path, 1)

        width = image.shape[1]
        height = image.shape[0]
        scale = 0.00392

        with open(self.classes, 'r') as f:
            classes = [line.strip() for line in f.readlines()]

        net = cv2.dnn.readNet(self.weights, self.config)

        blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)

        outs = net.forward(self.get_output_layers(net))

        class_ids = []
        confidences = []
        boxes = []
        conf_threshold = 0.5
        nms_threshold = 0.4

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w / 2
                    y = center_y - h / 2
                    class_ids.append(class_id)
                    confidences.append(float(confidence))
                    boxes.append([x, y, w, h])

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

        ''' # there can be more than one class detectedin an image
        for i in indices:
            label = str(classes[class_ids[i]])
        '''

        return classes[class_ids[indices[0][0]]]

    def get_output_layers(self, net):
        layer_names = net.getLayerNames()

        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers


# Callback for the "Encuentra objeto" button
def simulation():

    global photo
    global cv_img

    # Create a window
    window = tkinter.Tk()
    window.title("CIRCUITO")

    # Load an image using OpenCV
    cv_img = cv2.cvtColor(cv2.imread("./objects/pasillo.jpeg"), cv2.COLOR_BGR2RGB)

    # Get the image dimensions (OpenCV stores image data as NumPy ndarray)
    height, width, no_channels = cv_img.shape

    # Create a canvas that can fit the above image
    canvas = tkinter.Canvas(window, width=width, height=height)
    canvas.pack()

    # Use PIL (Pillow) to convert the NumPy ndarray to a PhotoImage
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(cv_img))

    # Add a PhotoImage to the Canvas
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

    # Button that lets the user blur the image
    btn_detect = tkinter.Button(window, text="Encuentra objeto", width=80, command=detected_object)
    btn_detect.pack(anchor=tkinter.CENTER, expand=True)

    # Run the window loop
    window.mainloop()



    def get_output_layers(net):
        layer_names = net.getLayerNames()

        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

        return output_layers

    def draw_prediction(img, class_id, confidence, x, y, x_plus_w, y_plus_h):
        label = str(classes[class_id])

        color = COLORS[class_id]

        cv2.rectangle(img, (x, y), (x_plus_w, y_plus_h), color, 2)

        cv2.putText(img, label, (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    files = glob.glob("./objects/*")
    file = random.choice(files)

    image = cv2.imread(file, 1)

    Width = image.shape[1]
    Height = image.shape[0]
    scale = 0.00392

    classes = None

    with open(CLASSES_FILE, 'r') as f:
        classes = [line.strip() for line in f.readlines()]

    COLORS = np.random.uniform(0, 255, size=(len(classes), 3))

    net = cv2.dnn.readNet(WEIGHTS_FILE, CONFIG_FILE)

    blob = cv2.dnn.blobFromImage(image, scale, (416, 416), (0, 0, 0), True, crop=False)

    net.setInput(blob)

    outs = net.forward(get_output_layers(net))

    class_ids = []
    confidences = []
    boxes = []
    conf_threshold = 0.5
    nms_threshold = 0.4

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                center_x = int(detection[0] * Width)
                center_y = int(detection[1] * Height)
                w = int(detection[2] * Width)
                h = int(detection[3] * Height)
                x = center_x - w / 2
                y = center_y - h / 2
                class_ids.append(class_id)
                confidences.append(float(confidence))
                boxes.append([x, y, w, h])

    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        x = box[0]
        y = box[1]
        w = box[2]
        h = box[3]
        draw_prediction(image, class_ids[i], confidences[i], round(x), round(y), round(x + w), round(y + h))

        print(classes[class_ids[i]])
        label = str(classes[class_ids[i]])

    height = 512
    width = 512
    dim = (width, height)

    destRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resize = cv2.resize(destRGB, dim, cv2.INTER_AREA)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(image_resize))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)

