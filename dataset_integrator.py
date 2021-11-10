import json
from glob import glob
import shutil
import os
from dataset_preprocess.dataset import dataset_maker, coco_json_integrator
from dataset_preprocess.myval import *

#Prototype Integration function
#coco_json_integrator(data_type, file_type, input_path)

#Main Fucntion for Dataset Integration
dataset_maker(input_path, output_folder, researcher, data_type, file_type)
