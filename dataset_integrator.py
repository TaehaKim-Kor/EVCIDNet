import json
from glob import glob
import shutil
import os
from dataset_preprocess.dataset import dataset_maker, coco_json_integrator
from dataset_preprocess.myval import *

#Prototype Integration function
#coco_json_integrator(data_type, file_type, input_path)

#Main function
dataset_maker(data_type, file_type, input_path)
