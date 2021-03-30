import cv2
import os

def checkinside(x1, y1, w,
              h, x, y) :
    x2 = x1 + w 
    y2 = y1 + h
    if (x > x1 and x < x2 and
        y > y1 and y < y2) :
        return True
    else :
        return False

def get_class_name():
    class_name = []
    with open("class_name.txt", "rt") as f:
        for i in f:
            class_name.append(i.rstrip())
    return class_name
     
def draw_class_name(img, size, step=70):
    class_name = get_class_name()
    img_h, img_w = size
    box_region = []
    for k, v in enumerate(class_name, 1):
        cv2.rectangle(img, (img_w + 20, k*step-50), (img_w + 100, k*step - 20), (0, 0, 255), 3)
        # cv2.putText(img, "Choose", (img_w + 20, k*step - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        cv2.putText(img, v, (img_w + 20, k*step - 55), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)
        box_region.append((img_w + 20, k*step-50, 80, 30))
    
    return img, class_name, box_region


def check_class(x, y, class_name, class_region, current_label):
    for c, r in zip(class_name, class_region):
        if(checkinside(r[0], r[1], r[2], r[3], x, y)):
            return c
    return current_label

def save_id_nclass(idnclass, filename, path=""):
    file = os.path.join(path, filename)
    with open(file, "wt") as f:
        for k, v in idnclass.items():
            f.write(str(k) + " " + str(v) + "\n")
             