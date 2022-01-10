#pragma comment(lib, "k4a.lib")
#include <k4a/k4a.h>
#include <k4arecord/playback.h>
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
int Record2Image_test(const char input)
{
	k4a_playback_t playback_handle = NULL;
	if (k4a_playback_open(&input, &playback_handle) != K4A_RESULT_SUCCEEDED);
	//if (k4a_playback_open("C:\\Users\\anstn\\Desktop\\output_2160p_1.mkv", &playback_handle) != K4A_RESULT_SUCCEEDED);
	{
		cout << "Failed to open recording" << endl;
		return 1;
 	}
	uint64_t recording_length = k4a_playback_get_recording_length_usec(playback_handle);
	cout << "Recording length is " << recording_length / 1000000 << "seconds."<< endl;
	k4a_playback_close(playback_handle);
	k4a_capture_t capture = NULL;
	k4a_stream_result_t result = K4A_STREAM_RESULT_SUCCEEDED;
	while (result == K4A_STREAM_RESULT_SUCCEEDED)
	{
		result = k4a_playback_get_next_capture(playback_handle, &capture);
		if (result == K4A_STREAM_RESULT_SUCCEEDED)
		{
			k4a_capture_release(capture);
		}
		else if (result == K4A_STREAM_RESULT_EOF)
		{
			break;
		}
	}
	if (result == K4A_STREAM_RESULT_FAILED)
	{
		cout << "Failed to read entrie recording" << endl;
		return 1;
	}

}
// "C:\Program Files\Azure Kinect SDK v1.4.1\tools\k4arecorder.exe" - l 10 - c 2160p - d WFOV_UNBINNED - r 15 "C:\Users\anstn\Desktop\output_2160p_3.mkv"
