import cv2
import numpy as np

def non_max_suppression(boxes, overlapThresh):
    if len(boxes) == 0:
        return []
    
    boxes = np.array(boxes, dtype="float")
    
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    
    areas = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(areas)[::-1]
    
    pick = []
    
    while len(idxs) > 0:
        last = idxs[0]
        pick.append(last)
        suppress = [0]
        
        for i in range(1, len(idxs)):
            xx1 = max(x1[last], x1[idxs[i]])
            yy1 = max(y1[last], y1[idxs[i]])
            xx2 = min(x2[last], x2[idxs[i]])
            yy2 = min(y2[last], y2[idxs[i]])
            
            w = max(0, xx2 - xx1 + 1)
            h = max(0, yy2 - yy1 + 1)
            
            overlap = float(w * h) / areas[idxs[i]]
            
            if overlap > overlapThresh:
                suppress.append(i)
        
        idxs = np.delete(idxs, suppress)
    
    return boxes[pick].astype("int")

image = cv2.imread("/home/user/test_canny/test_canny/test.png")
image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

template = cv2.imread("/home/user/test_canny/test_canny/template/template_test.jpeg")
template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
w, h = template.shape[::-1]

template1 = cv2.imread("/home/user/test_canny/test_canny/template/template.jpeg")
template1 = cv2.cvtColor(template1, cv2.COLOR_RGB2GRAY)
w1, h1 = template1.shape[::-1]

res = cv2.matchTemplate(image_gray, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.9
loc = np.where(res >= threshold)

res1 = cv2.matchTemplate(image_gray, template1, cv2.TM_CCOEFF_NORMED)
threshold1 = 0.7
loc1 = np.where(res1 >= threshold1)

boxes = []
for pt in zip(*loc[::-1]):
    boxes.append([pt[0], pt[1], pt[0] + w, pt[1] + h])

picked_boxes = non_max_suppression(boxes, overlapThresh=0.3)

for (x1, y1, x2, y2) in picked_boxes:
    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 2)
    print(f"좌표: ({x1}, {y1}) ~ ({x2}, {y2}), 면적: {(x2 - x1) * (y2 - y1)}")
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    robot_x = 320
    robot_y = 400
    cv2.circle(image, (center_x, center_y), 1, (0, 200, 200), 2)
    cv2.circle(image, (robot_x, robot_y), 1, (0, 0, 255), 2)
    distance = (((center_x - robot_x)**2 + (center_y - robot_y)**2)**0.5) * 0.258
    print(f"distance: {distance}")

boxes1 = []
for pt1 in zip(*loc1[::-1]):
    boxes1.append([pt1[0], pt1[1], pt1[0] + w1, pt1[1] + h1])

picked_boxes1 = non_max_suppression(boxes1, overlapThresh=0.3)

for (x3, y3, x4, y4) in picked_boxes1:
    cv2.rectangle(image, (x3, y3), (x4, y4), (0, 255, 255), 2)
    print(f"좌표: ({x3}, {y3}) ~ ({x4}, {y4}), 면적: {(x4 - x3) * (y4 - y3)}")
    center_x1 = (x3 + x4) // 2
    center_y1 = (y3 + y4) // 2
    cv2.circle(image, (center_x1, center_y1), 1, (0, 200, 0), 2)
    cv2.circle(image, (robot_x, robot_y), 1, (0, 255,0), 2)
    distance1 = (((center_x1 - robot_x)**2 + (center_y1 - robot_y)**2)**0.5) * 0.258
    print(f"distance1: {distance1}")

cv2.imshow('test', image)

cv2.waitKey()
cv2.destroyAllWindows()