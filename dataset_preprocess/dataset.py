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

def json_caller(json_add):
    with open(json_add, 'r') as f:
        json_data = json.load(f)
    return json_data

def annotated_image_id_caller(json_data):
    length = len(json_data["annotations"])
    id_list = []
    for i in range(length):
        id_list.append(json_data["annotations"][i]["image_id"])
    return str(set(id_list))[1:-1].split(", ")

def segmentation_return(json_data):
    xmin = json_data["annotations"][i]["bbox"][0]
    ymin = json_data["annotations"][i]["bbox"][1]
    xmax = xmin+json_data["annotations"][i]["bbox"][2]
    ymax = ymin+json_data["annotations"][i]["bbox"][3]
    segmentation = [xmin,ymin,xmax,ymin,xmin,ymax,xmax,ymax]
    return segmentation

def segmentation_return_from_annolist(anno_data):
    xmin = anno_data["bbox"][0]
    ymin = anno_data["bbox"][1]
    xmax = xmin+anno_data["bbox"][2]
    ymax = ymin+anno_data["bbox"][3]
    segmentation = [xmin,ymin,xmax,ymin,xmin,ymax,xmax,ymax]
    return segmentation

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

def annotation_caller(json_data, image_id):
    count = 0
    anno_list = []
    for i in range(len(json_data["annotations"])):
        if int(json_data["annotations"][i]["image_id"]) == int(image_id):
            anno_list.append(json_data["annotations"][i])
            count += 1
            if count >= 3: break
    return anno_list

def images_caller(json_data, image_id):
    for i in range(len(json_data["images"])):
        if int(json_data["images"][i]["id"]) == int(image_id):
            return json_data["images"][i]

def json_cleaner(json_data, temp_add):
    id_count = 1
    anno_count = 1
    clean_json = open(temp_add, 'w', encoding='utf-8')
    annotated_id_list = annotated_image_id_caller(json_data)
    image_info_list = []
    anno_info_list = []
    for id in annotated_id_list:
        anno_info = annotation_caller(json_data, id)
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

def json_integrator(json_output_addr, json_adder_addr, json_temp_addr):
    try:
        shutil.copyfile(json_output_addr,json_temp_addr)
        json_output = json_caller(json_temp_addr)
        json_adder = json_caller(json_adder_addr)
        print(len(json_output["images"]))
        for k in range(0,len(json_adder["images"])):
            json_adder["images"][k]['id'] += len(json_output['images'])
        json_output["images"].extend(json_adder["images"])
        print(len(json_adder['images']))
        print(len(json_output["images"]))
        for k in range(0,len(json_adder["annotations"])):
            json_adder["annotations"][k]["id"] += len(json_output["annotations"])
            json_adder["annotations"][k]["image_id"] += len(json_output['images'])
        json_output["annotations"].extend(json_adder["annotations"])
        output = open(json_output_addr, 'w', encoding='utf-8')
        json.dump(json_output, output, indent="\t")
        output.close()
    except:
        print(json_output_addr+" is not existed json file.")
        shutil.copyfile(json_adder_addr, json_output_addr)

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
    if trigger: print("Integration dataset code successfully works.")

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
