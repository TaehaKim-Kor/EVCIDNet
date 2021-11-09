import json
from glob import glob
import shutil
import os
#total_path = '/media/taeha/NVME2TB/ElectricCAR/ForTest/'
#json_add = glob(total_path + '*/*/instances_default_main_Edited_Color.json')
total_path = '/media/taeha/66A25289A2525E1D/Users/User/Desktop/mmdetection/data/archive/211013_output_annotated/211013_output/annotation_temp/'
json_add = glob(total_path + 'instances_default*.json')
json_add.sort()
#json_add = ['E:/EVlegacy/archive/ForTest/BoltEV_White_2019_Rainy_Time(20200722)_Morning_OutsideA_DC_Off/instances_default_main_Edited_Color.json','E:/EVlegacy/archive/ForTest/BoltEV_White_2019_Rainy_Time(20200722)_Morning_OutsideB_DC_Off/instances_default_main_Edited_Color.json']
output_add = total_path + 'train.json'
#output_add = 'C:/Users/User/Desktop/annotation_test/KTH_test.json'
temp_add = total_path + 'train_temp.json'
#temp_add = 'C:/Users/User/Desktop/annotation_test/KTH_test_temp.json'
shutil.copy(json_add[0],output_add)
for address in json_add[1:len(json_add)]:
    shutil.copy(output_add,temp_add)
    with open(address,'r') as f:
        json_data_add = json.load(f)
    with open(temp_add,'r') as f:
        json_data_output = json.load(f)
    print(len(json_data_add["images"]))
    print(len(json_data_output["images"]))
    for k in range(0,len(json_data_add["images"])):
        json_data_add["images"][k]['id']+=len(json_data_output['images'])
    for k in range(0,len(json_data_add["annotations"])):
        json_data_add["annotations"][k]["id"] += len(json_data_output["annotations"])
        json_data_add["annotations"][k]["image_id"] += len(json_data_output['images'])
    json_data_output["images"].extend(json_data_add["images"])
    json_data_output["annotations"].extend(json_data_add["annotations"])
    output=open(output_add,'w',encoding='utf-8')
    json.dump(json_data_output,output,indent="\t")
    output.close()
os.remove(temp_add)