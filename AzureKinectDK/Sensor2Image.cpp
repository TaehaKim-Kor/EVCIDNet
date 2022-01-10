#pragma comment(lib, "k4a.lib")
#include <k4a/k4a.h>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <time.h>
using namespace std;
using namespace cv;
int Sensor2Image_test()
{
	// getting the capture
	k4a_capture_t capture;
	k4a_calibration_t calibration;
	k4a_transformation_t transformation;
	k4a_image_t transformed_depth_image;
	const int32_t TIMEOUT_IN_MS = 1000;
	clock_t start, end;
	double result;
	char title_d[100];
	char title_c[100];
	char title_t[100];
	int max_frame = 40;
	int frame_count = 0;
	
	
	uint32_t count = k4a_device_get_installed_count();
	if (count == 0)
	{
		printf("No k4a devices attached!\n");
		return 1;
	}
	// Open the first plugged in Kinect device
	k4a_device_t device = NULL;
	if (K4A_FAILED(k4a_device_open(K4A_DEVICE_DEFAULT, &device)))
	{
		printf("Failed to open k4a device!\n");
		return 1;
	}
	// Get the size of the serial number
	size_t serial_size = 0;
	k4a_device_get_serialnum(device, NULL, &serial_size);
	// Allocate memory for the serial, then acquire it
	char* serial = (char*)(malloc(serial_size));
	k4a_device_get_serialnum(device, serial, &serial_size);
	printf("Opened device: %s\n", serial);
	free(serial);
	// Configure a stream of 4096x3072 BRGA color data at 15 frames per second
	k4a_device_configuration_t config = K4A_DEVICE_CONFIG_INIT_DISABLE_ALL;
	config.camera_fps = K4A_FRAMES_PER_SECOND_15;
	config.color_format = K4A_IMAGE_FORMAT_COLOR_BGRA32;
	config.color_resolution = K4A_COLOR_RESOLUTION_720P;
	config.depth_mode = K4A_DEPTH_MODE_WFOV_UNBINNED;
	config.synchronized_images_only = true;
	if (K4A_RESULT_SUCCEEDED !=
		k4a_device_get_calibration(device, config.depth_mode, config.color_resolution, &calibration))
	{
		cout << "Failed to get calibration" << endl;
		return 0;
	}
	// Start the camera with the given configuration
	k4a_device_start_cameras(device, &config);
	for (frame_count; frame_count < max_frame; frame_count++)
	{
		k4a_device_get_capture(device, &capture, TIMEOUT_IN_MS);
		start = clock();
		k4a_image_t color_image = k4a_capture_get_color_image(capture);
		uint8_t* color_buffer = k4a_image_get_buffer(color_image);
		int rows = k4a_image_get_height_pixels(color_image);
		int cols = k4a_image_get_width_pixels(color_image);
		cv::Mat color(rows, cols, CV_8UC4, (void*)color_buffer, cv::Mat::AUTO_STEP);
		sprintf_s(title_c, "C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output\\color\\%03d.png", frame_count);
		cv::imwrite(title_c, color);
		end = clock();
		result = (double)(end - start);
		// 결과 출력
		cout << "Color result : " << ((result) / CLOCKS_PER_SEC) << " seconds" << endl;
		//cv::imshow("random", color);
		start = clock();
		k4a_image_t depth_image = k4a_capture_get_depth_image(capture);
		uint8_t* depth_buffer = k4a_image_get_buffer(depth_image);
		int depth_rows = k4a_image_get_height_pixels(depth_image);
		int depth_cols = k4a_image_get_width_pixels(depth_image);
		cv::Mat depth(depth_rows, depth_cols, CV_16UC1, (void*)depth_buffer, cv::Mat::AUTO_STEP);
		sprintf_s(title_d, "C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output\\depth\\%03d.png", frame_count);
		cv::imwrite(title_d, depth);
		//cv::imshow("depth image",depth);
		//cv::waitKey(0);
		end = clock();
		result = (double)(end - start);
		// 결과 출력
		cout << "Depth result : " << ((result) / CLOCKS_PER_SEC) << " seconds" << endl;
		start = clock();
		transformation = k4a_transformation_create(&calibration);
		if (K4A_RESULT_SUCCEEDED != k4a_image_create(K4A_IMAGE_FORMAT_DEPTH16,
			cols,
			rows,
			cols * (int)sizeof(uint16_t),
			&transformed_depth_image))
		{
			cout << "Failed to create transformed depth image" << endl;
			return false;
		}
		if (K4A_RESULT_SUCCEEDED != k4a_transformation_depth_image_to_color_camera(transformation, depth_image, transformed_depth_image))
		{
			cout << "Failed to compute transformed depth image" << endl;
			return false;
		}
		//std::cout << "width = " << width << std::endl;
		//std::cout << "height = " << height << std::endl;
		//cv::Mat frame;
		uint8_t* buffer = k4a_image_get_buffer(transformed_depth_image);
		int transdepth_rows = k4a_image_get_height_pixels(transformed_depth_image);
		int transdepth_cols = k4a_image_get_width_pixels(transformed_depth_image);
		cv::Mat transdepth(transdepth_rows, transdepth_cols, CV_16UC1, (void*)buffer, cv::Mat::AUTO_STEP);
		sprintf_s(title_t, "C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output\\trans\\%03d.png", frame_count);
		cv::imwrite(title_t, transdepth);
		end = clock();
		result = (double)(end - start);
		// 결과 출력
		cout << "Trans Depth result : " << ((result) / CLOCKS_PER_SEC) << " seconds" << endl;
		/*
		Mat befordepth = imread("transdepth.png");
		Mat depthcolor;
		applyColorMap(befordepth, depthcolor, COLORMAP_JET);
		cv::imwrite("transdepthcolor.png", depthcolor);
		*/
		/*
		Mat src1, src2, dst;
		src1 = imread("color.jpg");
		src2 = imread("transdepthcolor.png");
		double beta = 0.8, alpha = 0.2;
		addWeighted(src1, alpha, src2, beta, 0.0, dst);
		imwrite("blending image.png", dst);
		*/
	}
	k4a_device_stop_cameras(device);
	k4a_device_close(device);
	return 0;
}