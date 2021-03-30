import cv2 
import os
import glob
import re
from collections import defaultdict
import random
from queue import Queue
import pandas as pd
import argparse
from annotate_utils import checkinside, draw_class_name, check_class, save_id_nclass
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-tp", "--txt_path", help="txt path", default="/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels")
ap.add_argument("-vp", "--video_path", help="video path", default="/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/May_10/2018-03-15")
ap.add_argument("-op", "--output_path", required = True)

args = vars(ap.parse_args())

# print(args)
# may10_path = "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/May_10/2018-03-15"
# may11_path = "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/May_11/2018-03-15"
# may10_annotation = "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels"
# may11_annotation = "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/EDSOLAB"


infor = ["name", "track_id", "frame", "type", "area", "coord", "is_occluded"]
infor_dict = {k:[] for k in infor}

digitP = r"[0-9]+"
def convert2video_path(name, video_path):
  txt_name = name.split("/")[-1]
  may, group, video_num = re.findall(digitP, txt_name)
  
  video_path = os.path.join(video_path, group, video_num +".mp4")
  return video_path

class Vehicle():
  def __init__(self, frame, track_id, coord, class_type, lost, occluded, generated):
    self.coord = list(map(int, coord))
    self.type = re.sub(r'\"',r'', class_type)
    self.frame = int(frame)
    self.track_id = int(track_id)
    self.lost = int(lost)
    self.occluded = int(occluded)
    self.generated = int(generated)
  #   self.class_dict = {
  #     'Human': 0,
  #     'Bicycle': 1,
  #     'Motorbike': 2,
  #     'Car': 3,
  #     'Bus': 4,
  #     'Truck': 5,
  #     'Container': 6
	# }
    self.area = None 
    
  def convert(self):
    # if(isinstance(xmin, str)):
    #   xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
      
    xmin, ymin, xmax, ymax = self.coord
    h, w = ymax-ymin, xmax-xmin
    
    self.area = h * w
    return xmin, ymin, w, h
  def get_area(self):
    return 
  
# train_path = "Dataset/train"
# test_path = "Dataset/test"

def create_folder(path):
  class_path = class_dict.keys()
  for c in class_path:
    c_path = os.path.join(path, c)
    if not os.path.exists(c_path):
      os.mkdir(c_path)
# create_folder(train_path)
# create_folder(test_path)

def clear_folder(path):
  for c in class_dict.keys():
    fpath = os.path.join(path, c)
    for file in os.listdir(fpath):
      os.remove(os.path.join(fpath, file))
      
# clear_folder(train_path)
# clear_folder(test_path)

def save_to_class_folder(img, folder, track_id, save_path, video_index):
  path = os.path.join(save_path, folder)
  if os.path.exists(path):
    sv_path = os.path.join(path, f"{folder}_{video_index}_{track_id}_{global_class_counter[folder]}.jpg")
    cv2.imwrite(sv_path, img)
    print("Finish saving!!!")
    return sv_path

target_new_path = ""
def save_new_file(id, class_name, file_name):
  file_create =  os.path.join(target_new_path,file_name + ".txt")
  if not os.path.isfile(file_create):
    with open(file_create, "wt") as f:
      f.write(str(id) + " " + class_name + "\n") 
  else:
    with open(file_create, "a") as f:
      f.write(str(id) + " " + class_name + "\n")
      
error_list = ["/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels/may10_01_01.txt", "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels/may10_01_00.txt",
              "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels/may10_01_04.txt", "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels/may10_01_03.txt", "/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels/may_10_01_02.txt"]
# for i in error_list:
#   print("/".join(i.split("/")[-5:]))

missing_labels = []


def click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
      print(x, y)
      if(coord_queue.full()):
        coord_queue.get()
      coord_queue.put((x, y))
    elif event == cv2.EVENT_RBUTTONDOWN:
      if(len(visited_id) != 0):
        val = visited_id.pop()
        del id2nclass[val]
        
        
# white_image = np.zeros([256,256,1],dtype=np.uint8)
# white_image.fill(255)

# def draw_text(event,x,y,flags,param):
#     if event == cv2.EVENT_LBUTTONDOWN:
#         i = 0
#         output = ""
#         clone = white_image.copy()
#         while True:
#             cv2.imshow('writeboard', clone) # to display the characters
#             k = cv2.waitKey(0)
#             cv2.putText(clone, chr(k) , (x+i,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 4, cv2.LINE_AA)
#             output += chr(k)
#             i+=10
#             # Press q to stop writing
#             if k == ord('q'):
#                 break
              
color_visited = (255, 0, 0)
color_not_visited = (0, 0, 255)

# for index, file_type in enumerate([train_video, test_video]):
#   save_path = train_path if index == 0 else test_path
file = glob.glob(args["txt_path"] + "/*.txt")

error_video = []
for video_idx in range(len(file)):
  vid = file[video_idx]
  if vid in error_list:
    print("Error video")
    continue
  # vid = '/home/son/trackingVehicle/DO_NOT_TOUCH/Video_nga_tu_QL48D_giao_QL1/annotations/labels/may10_01_04.txt'
  error_trigger = False


  id_counter = defaultdict(list)
  video_path_cv = convert2video_path(vid, args["video_path"])
  print("Process: ", vid)
  print("Process video: ", video_path_cv)
  
  vidcap = cv2.VideoCapture(video_path_cv)
  success,image = vidcap.read()

  with open(vid, "rt") as f:
      lines = f.readlines()    

  lines = list(map(lambda x:x.strip().split(" ")[:10], lines))
  # print(lines)
  vehicles = []
  for i in lines:
    if len(lines) != 11:
      vehicles.append(Vehicle(i[5], i[0], i[1:5], i[-1], i[6], i[7], i[8]))
    else:
      vehicles.append(Vehicle(i[5], i[0], i[1:5], i[-1] + i[-2], i[6], i[7], i[8]))

    
  vehicles = sorted(vehicles, key=lambda x:x.track_id)
  for v in vehicles:
    if not v.lost:
      id_counter[v.track_id].append(v.frame)
  
  max_image_per_id = 10
  for k, v in id_counter.items():
    get_num_images = min(max_image_per_id, len(v))
    id_counter[k] = random.sample(v, get_num_images)
  
  group_frame = defaultdict(list)
  for v in vehicles:
      group_frame[v.frame].append(v)
  new_vehicle = list(group_frame.values())
  new_vehicle = sorted(new_vehicle, key=lambda x: x[0].frame)
  
  valid_frame = []
  for v in new_vehicle:
    valid_frame.append(v[0].frame)
  
  current_frame = 0
  veh_idx = 0

  # id that we just rename the class
  
  # event 
  cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL | cv2.WINDOW_AUTOSIZE)
  cv2.setMouseCallback("image", click)
  # mapping new class to id 
  id2nclass = {}
  visited_id = []
  coord_queue = Queue(maxsize=2)
  print("Visited_id: ", visited_id)
  class_area_width = 200
  while success:
      rec_coord = []
      success,image = vidcap.read()
      if image is None:
        break
      image_h, image_w = image.shape[:2]
      class_choosing = np.zeros((image_h, class_area_width, 3), np.uint8)
      class_choosing.fill(255)
      vis_image = np.zeros((image_h, image_w+class_area_width,3), np.uint8)
      vis_image[:, :image_w] = image.copy()
      vis_image[:, image_w:] = class_choosing
      vis_image, temp_cls, box_region = draw_class_name(vis_image, (image_h, image_w))              
      # cv2.imshow("image", vis_image)
      # cv2.waitKey(0)
      # x, y = coord_queue.get()
      # check_class(x, y, temp_cls, box_region)
      
      try:
        if (current_frame == valid_frame[veh_idx]):
          for idx, v in enumerate(new_vehicle[current_frame]):
            if(v.frame != current_frame):
              raise ValueError("Frame mismatch")
            
            # or v.generated
            if v.lost:
              continue
            
            if v.track_id in visited_id:
              color_rec = color_visited
              v.type = id2nclass[v.track_id]
            else:
              color_rec = color_not_visited
              
            x, y, w, h = v.convert()
            rec_coord.append((x, y, w, h, v))
            
            cv2.rectangle(vis_image, (x-10, y), (x+w+10, y+h), color=color_rec, thickness=3)
            cv2.putText(vis_image, v.type , (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 1)
            
            
          # print('Read a new frame: ', success)
          if(success):
            cv2.imshow("image", vis_image)

          key = cv2.waitKey(0) & 0xFF
          if coord_queue.qsize() >= 2:
            print("hallo")
            x_check, y_check = coord_queue.get()
            x_check_class, y_check_class = coord_queue.get()
            assert x_check_class >= image_w, "Wrong position click"
            
            for info in rec_coord:
              coord = info[:-1]
              temp_id = info[-1].track_id
              if(temp_id in visited_id):
                continue
              print(x_check, y_check)
              if(checkinside(coord[0], coord[1], coord[2], coord[3], x_check, y_check)):
                visited_id.append(temp_id)
                new_class_type = check_class(x_check_class, y_check_class, temp_cls, box_region, info[-1].type)
                id2nclass[temp_id] = new_class_type
                
              else:
                continue
          print("")
          # if the 'c' key is pressed, next frame
          if key == ord("w"):
            # image = clone.copy()
            pass
          elif key == ord("x"):
            error_video.append(vid)
            error_trigger = True
            break
          elif key == ord("q"):
            break
          veh_idx += 1

          
      except IndexError as e:
        print("Error: ", e)
      
      current_frame += 1
  print(id2nclass)
  if(not error_trigger):
    save_id_nclass(id2nclass, vid.split("/")[-1], args["output_path"])
  
print("Error_video: ", error_video)
  
# # pd.DataFrame.from_dict(infor_dict).to_csv("data.csv", index=False)
          
