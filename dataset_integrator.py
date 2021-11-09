import json
from glob import glob
import shutil
import os
from dataset_preprocess.dataset import dataset_maker
from dataset_preprocess.myval import *

dataset_maker(data_type, file_type, input_path)
