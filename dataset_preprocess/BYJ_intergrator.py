#==============================================================================================================================#
"""서로 다른 json 통합, 고려해야 할것
  1. images의 id 0부터 시작
  2. annotations의 id 1부터 시작
  3. annotations의 image_id 1부터 시작
"""
import json


#with open('/home/bang2/code/make_samplebbox/instances_train_real1fake.json', 'r') as f:
with open('E:/EVlegacy/archive/ForTest/BoltEV_White_2019_Rainy_Time(20200722)_Morning_OutsideA_DC_Off/instances_default_main_Edited_Color.json', 'r') as f:
    json_data = json.load(f)

#with open('/home/bang2/code/make_samplebbox/instances_fake2.json', 'r') as f:
with open('E:/EVlegacy/archive/ForTest/BoltEV_White_2019_Rainy_Time(20200722)_Morning_OutsideB_DC_Off/instances_default_main_Edited_Color.json', 'r') as f:
    json_data1 = json.load(f)
#==============================================================================================================================#
"image id 바꾸기"
Ori_images = json_data["images"]
New_images = json_data1["images"]
Ori_images_count = len(Ori_images)
for i in range(0, len(New_images)):
    New_images[i]["id"] = New_images[i]["id"] + len(Ori_images)

print(New_images[0]["id"])

Ori_images.extend(New_images)
print(len(Ori_images))
#==============================================================================================================================#
"annot id, annot image_id 바꾸기"
Ori_annot = json_data["annotations"]
New_annot = json_data1["annotations"]
print(len(Ori_annot))


for i in range(0, len(New_annot)):
    New_annot[i]["id"] = New_annot[i]["id"] + len(Ori_annot)
    New_annot[i]["image_id"] = New_annot[i]["image_id"] + Ori_images_count
print(New_annot[0]["id"])
print(New_annot[0]["image_id"])

Ori_annot.extend(New_annot)
print(len(Ori_annot))

json_data["images"] = Ori_images
json_data["annotations"] = Ori_annot

with open('C:/Users/User/Desktop/annotation_test/BYJ_test.json', 'w', encoding='utf-8') as make_file:

    json.dump(json_data, make_file, indent="\t")

#==============================================================================================================================#