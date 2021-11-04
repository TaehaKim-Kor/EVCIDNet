import json
from glob import glob
import shutil
import os
from dataset import coco_json_integrator

data_type = "train"
file_type = ".json"
input_path = "C:\\Users\\User\\Desktop\\annotation_test\\"
coco_json_integrator(data_type,file_type,input_path)
