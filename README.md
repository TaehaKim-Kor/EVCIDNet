# EVCIDNet
Electric Vehicle Charge Inlet Detection Network

If you want to use this project, you should add or install these libraries.
> OpenCV, At least 4.3.0, opencv_world430d.dll should be in the /x64/Release/
> 
> Pytorch Parameter Model File. [Download Link, to be announced](tobeannoucned.com)

Reference
> [MMdetection](https://github.com/open-mmlab/mmdetection)
>
> [Azure Kinect DK](https://docs.microsoft.com/ko-kr/azure/kinect-dk/) 한국어
>
>[Azure Kinect DK](https://docs.microsoft.com/en-us/azure/kinect-dk/) English
>
> [DetectoRS](https://github.com/joe-siyuan-qiao/DetectoRS)

Demonstration System Specification
>CPU - Intel Core i7 8700
>
>RAM - 16GB
>
>GPU - NVIDIA Geforce RTX 2080Ti
>
>mmdet - 2.17.0
>
>mmcv - 1.3.8
>
>CUDA - 10.1
>
>Pytorch - 1.8.0+cu101
>>Torchvision - 0.9.0+cu101
>>
>>Torchaudio - 0.8.0


Released System Specification(To be announced)
>CPU - Intel Core i7 11700
>
>RAM - 16GB
>
>GPU - NVIDIA Geforce GTX 1080Ti
>
>mmdet - 
>
>mmcv -
>
>CUDA - 10.1
>
>Pytorch - 1.8.0+cu101
>>Torchvision - 0.9.0+cu101
>>
>>Torchaudio - 0.8.0

Tips for Reproducing
>1. Be careful while installing the entire libraries you need.
>That is because there is a complicate requirements between Pytorch, MMdet, and MMCV.
>And if you want to use another nerual network models in MMCV directly, you should check that model's MMCV, MMdet version too.
>
>2. If you use Windows 10, you should check Visual Studio's version carefully while installing MMCV and MMdet.
>When I installed MMCV in my virtual environment, sometimes installing was failed because I use Visual Studio 2022.
>You should use Visual Studio 2015 or 2019.
