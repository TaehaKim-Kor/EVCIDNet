import os
import json
from .val import *
import numpy as np
import cv2
from pymodbus.client.sync import ModbusTcpClient
import threading
import time
def flag_activator (flag_add):
    try:
        with open(flag_add,'w') as f:
            f.close()
        return True
    except:
        return False
def flag_remover(flag_add):
    if os.path.isfile(flag_add):
        os.remove(flag_add)

def json_fake_maker(output_addr):
    clean_json = open(output_addr, 'w', encoding='utf-8')
    image_info_list = [{"lincense" : 0, "date_captured" : 0, "width" : 2048, "flicker_url" : "", "file_name" : "color.png", "coco_url" : "", "height" : 1536, "id" : 1}]
    anno_info_list = [{"area" : 1, "iscrowd" : 0, "image_id" : 1, "category_id" : 1, "bbox" : [1,1,1,1], "id" : 1, "segmentation" : [[1,1,2,1,2,2,1,2]]}]
    json_dict.update({"images":image_info_list,"annotations":anno_info_list})
    json.dump(json_dict,clean_json,indent="\t")

def pixel_calculator(result_addr):
    f=open(result_addr, 'r')
    txt=f.readlines()
    if len(txt) is not 3:
        print("The number of object is not 3")
    tgt = [[] for i in range(3)]
    for i in range(3):
        tot = list(txt[i][1:-2].split(" "))
        for j in range(len(tot)):
            if tot[j] != "":
                tgt[i].append(float(tot[j]))
    return tgt
def nonzero_mean(nparray):
    nonzero_list = np.transpose(np.nonzero(nparray))
    arrsum = 0
    arrnum = len(nonzero_list)
    for nz in nonzero_list:
        arrsum += mytypecast(nparray[nz[0],nz[1]])
    return int(arrsum/arrnum)

def mytypecast(value):
    a = np.array(value, dtype=np.uint16)
    return int(a.view(np.int16))

def mean_coordinate_calculator(pc_addr, target):
    pc = np.array(cv2.imread(pc_addr, cv2.IMREAD_UNCHANGED), dtype=np.int16)
    coordinate_list = []
    for tgt in target:
        alpha = np.zeros(np.shape(pc))
        xmin = int(tgt[0])
        ymin = int(tgt[1])
        xmax = int(tgt[2])
        ymax = int(tgt[3])
        alpha[ymin:ymax, xmin:xmax, :] = 1
        temp = pc[:, :, 0] * alpha[:, :, 0]
        zmean = nonzero_mean(temp)
        temp = pc[:, :, 1] * alpha[:, :, 1]
        ymean = nonzero_mean(temp)
        temp = pc[:, :, 2] * alpha[:, :, 2]
        xmean = nonzero_mean(temp)
        coordinate_list.append([xmean,ymean,zmean])
    return coordinate_list
def center_coordinate_calculator(pc_addr, target):
    pc = np.array(cv2.imread(pc_addr, cv2.IMREAD_UNCHANGED), dtype=np.int16)
    temp = pc[:,:,0] + pc[:,:,1] + pc[:,:,2]
    coordinate_list = []
    for tgt in target:
        xmin = int(tgt[0])
        ymin = int(tgt[1])
        xmax = int(tgt[2])
        ymax = int(tgt[3])
        xcenter = int((xmin+xmax)/2)
        ycenter = int((ymin+ymax)/2)
        nonzero_list = np.nonzero(temp)
        ynonzero=(np.array(nonzero_list[0])-ycenter)**2
        xnonzero=(np.array(nonzero_list[1])-xcenter)**2
        dist_arr = (xnonzero+ynonzero)**0.5
        index=np.argmin(dist_arr)
        ty = nonzero_list[0][index]
        tx = nonzero_list[1][index]
        coordinate_list.append([mytypecast(pc[ty,tx,2]),mytypecast(pc[ty,tx,1]),mytypecast(pc[ty,tx,0])])
    #print(coordinate_list)
    return coordinate_list

def activate_client(addr, port):
    client = ModbusTcpClient(host=addr, port=port)
    return client

def transmit_coordinates(coordinates, client):
    distanceZ = coordinates[0][0] + offset
    distanceY = coordinates[0][1] + offset
    distanceX = coordinates[0][2] + offset
    client.write_register(address=regiaddrX1, value=distanceX, unit=255)
    client.write_register(address=regiaddrY1, value=distanceY, unit=255)
    client.write_register(address=regiaddrZ1, value=distanceZ, unit=255)
    print("Transmission success", coordinates[0])
    time.sleep(0.1)
    distanceZ = coordinates[1][0] + offset
    distanceY = coordinates[1][1] + offset
    distanceX = coordinates[1][2] + offset
    client.write_register(address=regiaddrX2, value=distanceX, unit=255)
    client.write_register(address=regiaddrY2, value=distanceY, unit=255)
    client.write_register(address=regiaddrZ2, value=distanceZ, unit=255)
    print("Transmission success", coordinates[1])
    time.sleep(0.1)
    distanceZ = coordinates[2][0] + offset
    distanceY = coordinates[2][1] + offset
    distanceX = coordinates[2][2] + offset
    client.write_register(address=regiaddrX3, value=distanceX, unit=255)
    client.write_register(address=regiaddrY3, value=distanceY, unit=255)
    client.write_register(address=regiaddrZ3, value=distanceZ, unit=255)
    print("Transmission success", coordinates[2])
    time.sleep(0.1)
    return True