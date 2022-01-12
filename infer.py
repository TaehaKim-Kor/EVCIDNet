import ctypes
import os
import subprocess
import time
import torch                # pytorch memory management
from infer_tools.func import *
from infer_tools.val import *
from glob import glob
import asyncio
from argparse import ArgumentParser

from mmdet.apis import (async_inference_detector, inference_detector,
                        init_detector, show_result_pyplot)
import numpy as np
import threading

def parse_args():       # add arguments
    parser = ArgumentParser()
    parser.add_argument('img', help='Image file')
    parser.add_argument('config', help='Config file')
    parser.add_argument('checkpoint', help='Checkpoint file')
    parser.add_argument(
        '--device', default='cuda:0', help='Device used for inference')
    parser.add_argument(
        '--score-thr', type=float, default=0.00001, help='bbox score threshold')
    parser.add_argument(
        '--async-test',
        action='store_true',
        help='whether to set async options for async inference.')
    
    args = parser.parse_args()
    
    return args
  
def initializer(args):          # remove color, point image file and allocate train model, client address
    try:
        os.remove(color_addr)
    except:
        pass
    
    try:
        os.remove(point_addr)
    except:
        pass
    
    model = init_detector(args.config, args.checkpoint, device=args.device)
    
    for addr in flag:
        flag_remover(addr)
    
    os.startfile(kinect_add)            # AzurekinectDK.exe
    client = activate_client(robot_addr, port_num)        # IP address, port number
    
    return model, client

def finisher():
    flag_activator(flag[2])
    time.sleep(2)
    
    for addr in flag:
        flag_remover(addr)
    
    try:
        os.remove(color_addr)
    except:
        pass
    
    try:
        os.remove(point_addr)         # initializer, finisher모두 color, point지우신게 비우고 시작하시기 위함이신지 질문드리기
    except:
        pass

def communicate_flag_activator(client, flag):       # get flag signal, response to signal and create flag
    while(True):
        #time.sleep(0.5)
        response = client.read_holding_registers(address = regiaddrC, unit = 255)
        
        if response.registers[0] == flag1_signal and not os.path.isfile(flag[0]): # create flag1, response to flag1 signal
            flag_activator(flag[0])
            inflag = 1      # image capture start
            break
        
        elif response.registers[0] == flag3_signal: # create flag3, response to flag3 signal
            flag_activator(flag[2])
            inflag = 0      # camera turn off and program terminate flag
            break
        
        else:               # image capture finish
            inflag = 2  # 혹시 inflag 번호와 flag번호를 다르게 주신 이유가 있으신지 질문드리기
    
    return inflag
    #return (inflag==1)

def vision_process_with_communication(model, client):
    #while (communicate_flag_activator(client, regiaddr, flag)):
    while(True):
        a = 3
        while(True):
            a = communicate_flag_activator(client, flag)      # a is inflag
            if (a == 2):
                time.sleep(0.1)
            else:
                break
        while not os.path.isfile(color_addr):
            time.sleep(0.1)
            
        if os.path.isfile(flag[0]):
            flag_remover(flag[1])       # store image and initialize flag
            
            if os.path.isfile(color_addr):
                time.sleep(0.5)
                result = inference_detector(model, args.img)
                class_detection_list = []
                
                if len(result[0]) is not 3:
                    print("The number of objects are detected is under the 3.")
                
                for i in range(len(result[0])):
                    tgt_list = [0 for i in range(5)]
                    
                    if len(result[0][i]) is not 1:
                        
                        for j in range(len(result[0][i])):
                            
                            if tgt_list[4] < result[0][i][j][4]:
                                tgt_list = result[0][i][j]
                    else:
                        tgt_list = result[0][i][0]
                    
                    class_detection_list.append(tgt_list)
                
                while(not os.path.isfile(point_addr)):
                    time.sleep(0.1)
                
                try:
                    pc_list=center_coordinate_calculator(point_addr, class_detection_list)
                except:
                    pc_list = [[0 for i in range(3)] for i in range(3)]
                # 여기까지하면 3차원좌표가 나옴.
                if transmit_coordinates(pc_list, client):
                    flag_remover(flag[0]) #이미지 캡처 시작 플래그 초기화
                    flag_remover(flag[1]) #이미지 캡처 완료 플래그 초기화
                    try: os.remove(color_addr)
                    except: pass
                    try: os.remove(point_addr)
                    except: pass
        elif os.path.isfile(flag[2]): break
        else:
            try: os.remove(color_addr)
            except: pass
            try: os.remove(point_addr)
            except: pass
    return True

if __name__ == "__main__":
    args = parse_args()
    model, client = initializer(args)
    #vision_process_with_communication(model, client)
    try:
        vision_process_with_communication(model, client)
        finisher()
    except:
        finisher()
    print("Program is finished.")
