import cv2
import numpy as np

# Load Yolo
net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
# List Class Names From Coco File
classes = []
with open('coco.names', 'r') as f:
    classes = f.read().splitlines()

img = cv2.imread('images\dog.jpg')
height, width, _ = img.shape

# Detecting objects
blob = cv2.dnn.blobFromImage(img, 1 / 255, (416, 416), (0, 0, 0), swapRB=True, crop=False)
net.setInput(blob)
output_layers_names = net.getUnconnectedOutLayersNames()
layersOutputs = net.forward(output_layers_names)

boxes = []  # extract the bounding boxes
confidences = []
class_ids = []

for output in layersOutputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[1] * height)

            x = int(center_x - w / 2)
            y = int(center_y - h / 2)

            boxes.append([x, y, w, h])
            confidences.append((float(confidence)))
            class_ids.append(class_id)

# print(len(boxes))
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
# print(indexes.flatten())
font = cv2.FONT_HERSHEY_PLAIN
colors = np.random.uniform(0, 255, size=(len(boxes), 3))

for i in indexes.flatten():
    x, y, w, h = boxes[i]
    label = str(classes[class_ids[i]])
    confidence = str(round(confidences[i], 2))
    color = colors[i]
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
    cv2.putText(img, label + " " + confidence, (x, y + 20), font, 2, (255, 255, 255), 2)

cv2.imshow('Images', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
