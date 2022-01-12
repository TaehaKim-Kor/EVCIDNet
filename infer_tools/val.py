#Programming Part variables
#kinect_add = "./x64/Release/AzureKinectDK.exe"
kinect_add = "C:/Users/User/Desktop/EVCIDNet-master/x64/Release/AzureKinectDK.exe"
result_add = "./AzureKinectDK/output/result.txt"

flag1_add = "./AzureKinectDK/output/flag1.txt" #image capture start flag
flag2_add = "./AzureKinectDK/output/flag2.txt" #image capture finish flag
flag3_add = "./AzureKinectDK/output/flag3.txt" #camera turn off and program terminate flag
flag = [flag1_add, flag2_add, flag3_add]

color_addr = "./AzureKinectDK/output/color.png"
point_addr = "./AzureKinectDK/output/point.png"

json_addr = "./AzureKinectDK/output/demo.json"
json_dict = {"licenses": [{"name": "", "id": 0, "url": ""}],
             "info": {"contributor": "", "date_created": "", "description": "", "url": "", "version": "", "year": ""},
             "categories": [{"id": 1, "name": "HolePairLeft", "supercategory": ""},
                            {"id": 2, "name": "HolePairRight", "supercategory": ""},
                            {"id": 3, "name": "ACHole", "supercategory": ""}],
             "images": [], "annotations": []}

#Communication Part variables
regiaddrX1 = 8
regiaddrY1 = 9
regiaddrZ1 = 10

regiaddrX2 = 11
regiaddrY2 = 12
regiaddrZ2 = 13

regiaddrX3 = 14
regiaddrY3 = 15
regiaddrZ3 = 18

regiaddrC = 19
regiaddr = [regiaddrX1,regiaddrY1,regiaddrZ1,regiaddrX2,regiaddrY2,regiaddrZ2,regiaddrX3,regiaddrY3,regiaddrZ3,regiaddrC]

robot_addr = "192.168.137.100"
port_num = 502
offset = 32768 #int 16 max range

flag1_signal = 1
flag3_signal = 0
#confirm_signal = "C"
#terminate_signal = "D"