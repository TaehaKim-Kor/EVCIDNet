#pragma once
#pragma comment(lib, "k4a.lib")
#include <omp.h>
#include <Windows.h>
#include <k4a/k4a.h>
#include <k4arecord/playback.h>
#include <k4arecord/record.h>
#include <k4arecord/k4arecord_export.h>
#include <k4arecord/types.h>
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
// "C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4arecorder.exe" -l 10 -c 2160p -d WFOV_UNBINNED -r 15 "C:\Users\anstn\Desktop\output_2160p_3.mkv"
// "C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4aviewer.exe"
int MP_Sensor2Image()
{
	// getting the capture
	k4a_capture_t capture;
	k4a_calibration_t calibration;
	k4a_transformation_t transformation;
	k4a_image_t transformed_depth_image;
	k4a_image_t aligned_point_cloud_depth_image;
	const int32_t TIMEOUT_IN_MS = 10000;
	clock_t start, end;
	double result;
	char title_d[100];
	char title_c[100];
	char title_t[100];
	char title_pc[100];
	int max_frame = 41;
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
	config.color_resolution = K4A_COLOR_RESOLUTION_1536P;
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
		start = clock();
		k4a_device_get_capture(device, &capture, TIMEOUT_IN_MS);
		k4a_image_t color_image = k4a_capture_get_color_image(capture);
		uint8_t* color_buffer = k4a_image_get_buffer(color_image);
		int rows = k4a_image_get_height_pixels(color_image);
		int cols = k4a_image_get_width_pixels(color_image);
		k4a_image_t depth_image = k4a_capture_get_depth_image(capture);
		uint8_t* depth_buffer = k4a_image_get_buffer(depth_image);
		int depth_rows = k4a_image_get_height_pixels(depth_image);
		int depth_cols = k4a_image_get_width_pixels(depth_image);
#pragma omp parallel for
		for (int step = 0; step < 3; step++)
		{
			if (step == 0) //Align Depth & 3D Transform
			{
				transformation = k4a_transformation_create(&calibration);

				if (K4A_RESULT_SUCCEEDED != k4a_image_create(K4A_IMAGE_FORMAT_DEPTH16,
					cols,
					rows,
					cols * (int)sizeof(uint16_t),
					&transformed_depth_image))
				{
					cout << "Failed to create transformed depth image" << endl;
					//return false;
				}
				if (K4A_RESULT_SUCCEEDED != k4a_transformation_depth_image_to_color_camera(transformation, depth_image, transformed_depth_image))
				{
					cout << "Failed to compute transformed depth image" << endl;
					//return false;
				}
				uint8_t* buffer = k4a_image_get_buffer(transformed_depth_image);
				int transdepth_rows = k4a_image_get_height_pixels(transformed_depth_image);
				int transdepth_cols = k4a_image_get_width_pixels(transformed_depth_image);
				cv::Mat transdepth(transdepth_rows, transdepth_cols, CV_16UC1, (void*)buffer, cv::Mat::AUTO_STEP);
				sprintf_s(title_t, "C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output\\trans\\%03d.png", frame_count);
				cv::imwrite(title_t, transdepth);
				if (K4A_RESULT_SUCCEEDED != k4a_image_create(K4A_IMAGE_FORMAT_CUSTOM, cols, rows, cols * (int)sizeof(int16_t) * 3, &aligned_point_cloud_depth_image))
				{
					cout << "Failed to create aligned depth point_cloud" << endl;
					//return false;
				}
				if (K4A_RESULT_SUCCEEDED != k4a_transformation_depth_image_to_point_cloud(transformation, transformed_depth_image, K4A_CALIBRATION_TYPE_COLOR, aligned_point_cloud_depth_image))
				{
					cout << "Failed to compute aligned depth point_cloud" << endl;
					//return false;
				}
				uint8_t* point_cloud_buffer = k4a_image_get_buffer(aligned_point_cloud_depth_image);
				cv::Mat point_cloud(rows, cols, CV_16UC3, (void*)point_cloud_buffer, cv::Mat::AUTO_STEP);
				sprintf_s(title_pc, "C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output\\point\\%03d.png", frame_count);
				cv::imwrite(title_pc, point_cloud);
				k4a_image_release(transformed_depth_image);
				k4a_image_release(aligned_point_cloud_depth_image);
			}
			else if (step == 1) //Color
			{
				cv::Mat color(rows, cols, CV_8UC4, (void*)color_buffer, cv::Mat::AUTO_STEP);
				sprintf_s(title_c, "C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output\\color\\%03d.png", frame_count);
				cv::imwrite(title_c, color);
				k4a_image_release(color_image);
			}
			else                //Depth
			{
				cv::Mat depth(depth_rows, depth_cols, CV_16UC1, (void*)depth_buffer, cv::Mat::AUTO_STEP);
				sprintf_s(title_d, "C:\\Users\\anstn\\Desktop\\AzureKinectDK\\output\\depth\\%03d.png", frame_count);
				cv::imwrite(title_d, depth);
				k4a_image_release(depth_image);
			}
		}
		end = clock();
		result = (double)(end - start);
		cout << "Total Processing Time on Multi Processing : " << ((result) / CLOCKS_PER_SEC) << " seconds" << endl;
	}
	k4a_device_stop_cameras(device);
	k4a_device_close(device);
	return 0;
}
