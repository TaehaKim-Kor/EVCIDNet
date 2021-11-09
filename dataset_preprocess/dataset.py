from glob import glob
import json
import shutil
import os
from myval import json_dict


def io_address_caller(data_type, file_type, input_path):
    output_path = input_path + data_type + file_type
    json_list = glob(input_path + "*" + file_type)
    temp_path = [input_path + "temp" + str(i) + file_type for i in range(1,len(json_list)+1)]
    temp_path.append(input_path+"temp"+file_type)
    return output_path, json_list, temp_path
# 입출력 경로 확정 함수
# 프로토타입 결합 함수에서만 사용할 것(출력 경로를 자유롭게 지정할 수 없는 문제 발생)

#def output_address_caller(output_path, json_path)

def json_caller(json_add):
    with open(json_add, 'r') as f:
        json_data = json.load(f)
    return json_data
# json 파일 읽어오는 함수(쓰는 용도 아님)

def annotated_image_id_caller(json_data):
    length = len(json_data["annotations"])
    id_list = []
    for i in range(length):
        id_list.append(json_data["annotations"][i]["image_id"])
        #print(i, json_data["annotations"][i]["image_id"])
    #print(str(set(id_list))[1:-1].split(", "))
    return str(set(id_list))[1:-1].split(", ")
# Annotation이 존재하는 이미지만 포함된 리스트를 반환하는 함수

def segmentation_return(json_data):
    xmin = json_data["annotations"][i]["bbox"][0]
    ymin = json_data["annotations"][i]["bbox"][1]
    xmax = xmin+json_data["annotations"][i]["bbox"][2]
    ymax = ymin+json_data["annotations"][i]["bbox"][3]
    segmentation = [xmin,ymin,xmax,ymin,xmin,ymax,xmax,ymax]
    return segmentation
# Segmentation이 공란인 데이터를 처리하는 함수(미사용)

def segmentation_return_from_annolist(anno_data):
    xmin = anno_data["bbox"][0]
    ymin = anno_data["bbox"][1]
    xmax = xmin+anno_data["bbox"][2]
    ymax = ymin+anno_data["bbox"][3]
    segmentation = [xmin,ymin,xmax,ymin,xmin,ymax,xmax,ymax]
    return segmentation
# Segmentation이 공란인 데이터를 계산하여 채워주는 함수

def json_file_validation_checker(json_add_list, temp_add, output_add):
    try:
        json_add_list.remove(output_add)
    except:
        pass
    for addr in temp_add:
        try:
            json_add_list.remove(addr)
        except:
            pass
    return json_add_list
# 입력으로 쓰일 json파일의 리스트에서 출력과 임시 json파일 경로를 지움(경로최적화)
def annotation_caller(json_data, image_id):
    count = 0
    anno_list = []
    for i in range(len(json_data["annotations"])):
        if int(json_data["annotations"][i]["image_id"]) == int(image_id):
            anno_list.append(json_data["annotations"][i])
            count += 1
            if count >= 3: break
    if len(anno_list) == 0:
        return False
    else:
        return anno_list
# 대상 이미지 번호(Image_id)를 입력 받아 annotation 정보를 반환하는 함수
# False를 반환하는 경우 annotation 정보가 없는 경우(2111008 추가)

def images_caller(json_data, image_id):
    for i in range(len(json_data["images"])):
        if int(json_data["images"][i]["id"]) == int(image_id):
            return json_data["images"][i]
# 대상 이미지 번호(Image_id)를 입력 받아 image 정보를 반환하는 함수

def json_cleaner(json_data, temp_add):
    id_count = 1
    anno_count = 1
    clean_json = open(temp_add, 'w', encoding='utf-8')
    annotated_id_list = annotated_image_id_caller(json_data)
    image_info_list = []
    anno_info_list = []
    for id in annotated_id_list:
        anno_info = annotation_caller(json_data, id)
        if anno_info is not False:
            for i in range(len(anno_info)):
                if len(anno_info[i]["segmentation"]) == 0:
                    anno_info[i]["segmentation"] = segmentation_return_from_annolist(anno_info[i])
                anno_info[i]["id"] = anno_count
                anno_count += 1
                anno_info[i]["image_id"] = id_count
            image_info = images_caller(json_data, id)
            image_info["id"] = id_count
            id_count += 1
            image_info_list.append(image_info)
            for i in range(len(anno_info)):
                anno_info_list.append(anno_info[i])
    json_dict.update({"images":image_info_list,"annotations":anno_info_list})
    json.dump(json_dict,clean_json,indent="\t")
# json 파일을 입력받아 annotation 정보가 없는 image 정보를 제거하여 임시파일에 저장한 함수
# 기존엔 annotation 검사를 한번만 했으나 두 번 진행하는 것으로 수정(211108 추가)
# extend는 한번에 하는 것으로 수정(211108 추가)

def json_integrator(json_output_addr, json_adder_addr, json_temp_addr):
    try:
        shutil.copyfile(json_output_addr,json_temp_addr)
        json_output = json_caller(json_temp_addr)
        json_adder = json_caller(json_adder_addr)
        for k in range(len(json_adder["images"])):
            json_adder["images"][k]['id'] += len(json_output['images'])
        for k in range(len(json_adder["annotations"])):
            json_adder["annotations"][k]["id"] += len(json_output["annotations"])
            json_adder["annotations"][k]["image_id"] += len(json_output['images'])
        json_output["images"].extend(json_adder["images"])
        json_output["annotations"].extend(json_adder["annotations"])
        output = open(json_output_addr, 'w', encoding='utf-8')
        json.dump(json_output, output, indent="\t")
        output.close()
    except:
        print(json_output_addr+" is not existed json file.")
        shutil.copyfile(json_adder_addr, json_output_addr)
# 생성된 임시 json 파일을 입력받아 annotation/image정보를 합친 json파일을 반환하는 함수

def integration_validation_checker(json_list, output_addr):
    image_id_count = []
    anno_id_count = []
    trigger = True
    for addr in json_list:
        json_data=json_caller(addr)
        image_id_count.append(len(json_data["images"]))
        anno_id_count.append(len(json_data["annotations"]))
    output_data = json_caller(output_addr)
    if len(output_data["images"]) != sum(image_id_count):
        print("The number of image_id is not same between output and inputs")
        print("The number of image_id in output : "+ str(len(output_data["images"])))
        print("The number of image_id in input : "+ str(image_id_count))
        trigger = False
    if len(output_data["annotations"]) != sum(anno_id_count):
        print("The number of annotation_id is not same between output and inputs")
        print("The number of annotation_id in output : " + str(len(output_data["annotations"])))
        print("The number of annotation_id in input : " + str(anno_id_count))
        trigger = False
    unsafe_id = []
    for i in range(len(output_data["images"])):
        count = 0
        for j in range(len(output_data["annotations"])):
            if output_data["images"][i]["id"] == output_data["annotations"][j]["image_id"]:
                count += 1
        if count == 0 :
            trigger = False
            unsafe_id.append(output_data["images"][i]["id"])
    if bool(len(unsafe_id)):
        print("The image without annotation information is detected.")
        print("This is the image without annotation information list.")
        for i in unsafe_id:
            print(i)
    if trigger: print("Integration dataset code successfully works.")
# 생성된 임시 json 파일과 출력된 최종 json 파일의 유효성을 검사하는 함수
# 검사 내용
# 1. 임시 파일들의 image 정보의 갯수의 합이 출력 파일의 image 정보의 갯수와 같은지?
# 2. 임시 파일들의 annotation 정보의 갯수의 합이 출력 파일의 annotation 정보의 갯수와 같은지?
# 3. 임시 파일들의 image 정보 중 annotation 정보가 없는 것이 있는지?

def coco_json_integrator(data_type, file_type, input_path):
    output_add, json_list, temp_add = io_address_caller(data_type, file_type, input_path)
    json_list = json_file_validation_checker(json_list, temp_add, output_add)
    try:
        os.remove(output_add)
        print(output_add+" is detected. Legacy data was deleted!")
    except:
        pass
    for i in range(len(json_list)):
        json_data = json_caller(json_list[i])
        json_cleaner(json_data,temp_add[i])
        json_integrator(output_add, temp_add[i],temp_add[-1])
    integration_validation_checker(temp_add[0:len(json_list)], output_add)
    for temp in temp_add:
        try:
            os.remove(temp)
            print(temp + " is remained. Temporary data was deleted!")
        except:
            pass
# json 파일을 입력받아 결합하는 프로토타입 함수

def json_integrate_main(output_add, json_list, temp_add):
    json_list = json_file_validation_checker(json_list, temp_add, output_add)
    try:
        os.remove(output_add)
        print(output_add+" is detected. Legacy data was deleted!")
    except:
        pass
    for i in range(len(json_list)):
        print(output_add, temp_add[i], temp_add[-1])
        json_data = json_caller(json_list[i])
        json_cleaner(json_data,temp_add[i])
        json_integrator(output_add, temp_add[i],temp_add[-1])
    integration_validation_checker(temp_add[0:len(json_list)], output_add)
    for temp in temp_add:
        try:
            os.remove(temp)
            print(temp + " is remained. Temporary data was deleted!")
        except:
            pass
# json 파일을 입력받아 결합하는 메인 함수
# 사용 방법은 생성할 output/temp 파일 경로가 명확한지와 json_list 내 경로가 명확하게 존재하는지만 확인

def dataset_selector(dataset_addr, type):
    if type == "KTH":
        dataset_folder_list =glob(dataset_addr + "*/*")
        annotation_file_list = glob(dataset_folder_list + "/annotation/instance_default*.json")
        image_folder_list = glob(dataset_folder_list + "/color/*.png")
        return ()
    elif type == "BYJ":
        dataset_folder_list = glob(dataset_addr + "*/")

    else:
        print("Please define the researcher name.")
        raise NotImplementedError
# dataset 경로를 정리하는 함수
# 복잡한 데이터셋 구조로부터 json 파일과 image 파일 리스트를 정리해서 새로운 데이터셋을 정리하는데 사용
# 21.11.09 현재 개발 중


def dataset_maker(data_type, file_type, input_path):
    output_add, json_list, temp_add = io_address_caller(data_type, file_type, input_path)
    json_integrate_main(output_add, json_list, temp_add)