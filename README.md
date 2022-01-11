## EVCIDNet
# Electric Vehicle Charge Inlet Detection Network
Model : DetectoRS with MMdetection

Camera : Azure Kinect DK

Language : C++(Kinect) , Python(DetectoRS)

Communication : Pymodbus(TCP/IP Modbus)

If you want to use this project, you should add or install these libraries.
> OpenCV, At least 4.3.0, opencv_world4{xx}d.dll, opencv_world4{xx}d.dll should be in the ./x64/Release/
>> If you install OpenCV 4.5.0 in your Windows, it will work.
>
> Pytorch Parameter Model File. [Download Link, to be announced](tobeannoucned.com)
>> Default file name : best_model.pth

# Main Libraries
> Pytorch
> 
> MMdetection
> 
> DetectoRS
> 
> Azure Kinect DK SDK
> 
> Pymodbus
> 
> OpenCV

# Demonstration System Specification
> CPU - Intel Core i7 8700
>
> RAM - 16GB
>
> GPU - NVIDIA Geforce RTX 2080Ti
>
> mmdet - 2.17.0
>
> mmcv - 1.3.8
>
> CUDA - 10.1
>
> OpenCV(Visual Studio) - 4.3.0
>
> OpenCV(Python) - 4.5.3
>
> Pytorch - 1.8.0+cu101
>> Torchvision - 0.9.0+cu101
>>
>> Torchaudio - 0.8.0


# Released System Specification
> CPU - Intel Core i7 11700
>
> RAM - 16GB
>
> GPU - NVIDIA Geforce GTX 1080Ti
>
> mmdet - 2.6.0
>
> mmcv - 1.3.9
>
> CUDA - 10.1
>
> OpenCV(Visual Studio) - 4.5.0
>
> OpenCV(Python) - 4.5.5
>
> Pytorch - 1.8.1+cu101
>> Torchvision - 0.9.1+cu101
>>
>> Torchaudio - 0.8.1

# Tips for Reproducing
> 1. Be careful while installing the entire libraries you need.
>
> That is because there is a complicate requirements between Pytorch, MMdet, and MMCV.
>
> And if you want to use another nerual network models in MMCV directly, you should check that model's MMCV, MMdet version too.
>
> 2. If you use Windows 10, you should check Visual Studio's version carefully while installing MMCV and MMdet.
>
> When I tried to install MMCV in my virtual environment, installing MMCV failed that was because I used Visual Studio 2022.
>
> You should use Visual Studio 2015 or [2019](https://docs.microsoft.com/en-us/visualstudio/releases/2019/release-notes).
>
> Our system was working in the Visual Studio 2019.
>
> If you get the error message
>
>> ModuleNotFoundError: No module named 'mmcv._ext'.
>
> you should doubt MMCV installtion is finished correctly or not.
>
> 3. OpenCV should be installed in the Visual Studio and Python too.
>
> For the correct working on the system, you should modify all of path related OpenCV in the visual studio.
>
> If you modify all of the path, then please release the visual studio again.
>
> No matter what version you use, it will works I think.
>
> I used OpenCV 4.3.0 for the Demostration system, and 4.5.0 for the Released system.
> 
> 4. When you run the code, please follow this type.
>> python infer.py {Path for RGB image from Kinect} {Path for MMdetection configuration file} {Path for Pytorch Parameter Model File}


# Command for running system
> python infer.py AzureKinectDK/output/color.png configs/config_demo.py best_model.pth

# Contributors for this vision system
> Taeha Kim
>> Seoul National University of Science and Technology
>> 
>> Department of Electrical and Information Engineering
>> 
>> Main contribution : Camera Application, Neural Network Training and Test, System Research and Development
>
> Yeonjun Bang
>> Seoul National University of Science and Technology
>> 
>> Department of Electronic and IT Media Engineering
>> 
>> Main contribution : Dataset Creation, Dataset Augmentation, Neural Network Training and Test
>
> Jinyeong Lee
>> Seoul National University of Science and Technology
>> 
>> Department of Electrical and Information Engineering
>> 
>> Main contribution : Dataset Creation, System Maintenance

# Reference
> [MMdetection](https://github.com/open-mmlab/mmdetection)
>
> [Azure Kinect DK](https://docs.microsoft.com/en-us/azure/kinect-dk/)
>
> [DetectoRS](https://github.com/joe-siyuan-qiao/DetectoRS)
