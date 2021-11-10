import cv2
import json
from dataset_preprocess.dataset import json_caller
from glob import glob
import os
import numpy as np
addr = "C:/Users/User/Desktop/mmdetection/data/test_211018/train_additional/"
json_data = json_caller(addr+"annotations/train_additional.json")
image_addr = glob(addr+"*color*.png")
file_addr = [os.path.split(image_addr[i])[1] for i in range(len(image_addr))]
unsafe_list = []
for k in range(len(json_data["images"])):
    tgt = json_data["images"][k]["file_name"]
    image_id = json_data["images"][k]["id"]
    myindex = file_addr.index(tgt)
    tgtimg = cv2.imread(image_addr[myindex])
    count = 0
    print("==============================")
    print(tgt)
    for i in range(len(json_data["annotations"])):
        if json_data["annotations"][i]["image_id"] == image_id:
            bbox = json_data["annotations"][i]["bbox"]
            print(bbox)
            print(json_data["annotations"][i]["image_id"])
            tgtimg[int(bbox[1]):int(bbox[1]) + int(bbox[3]), int(bbox[0]):int(bbox[0]) + int(bbox[2]), 1:2] = 255
            count += 1
            if count == 3:
                break
    if count == 0:
        unsafe_list.append(json_data["images"][k]["file_name"])
    print("==============================")
    dst=cv2.resize(src=tgtimg, dsize=(0,0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)
    cv2.namedWindow("tgt image")
    cv2.imshow("tgt image",dst)
    cv2.waitKey(50)
print(len(json_data["images"]))
print(len(unsafe_list))