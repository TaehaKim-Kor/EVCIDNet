import json
from glob import glob
import shutil
import os
from dataset_preprocess/dataset import dataset_maker

data_type = "train"
file_type = ".json"
input_path = "C:\\Users\\User\\Desktop\\annotation_test\\"
output_path = "E:\\annotation_integrated\\"
#data_type = "instances_default"
#file_type=".json"
#input_path="E:/EVlegacy/"
dataset_maker(data_type, file_type, input_path)
