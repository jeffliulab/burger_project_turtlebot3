#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2


# package name: camera_processing
# script name: opencv_camera_node.py
# function: this file is to process the image of the usb camera on raspberry
#	    because usb_cam package in ROS does not support this camera's image

def camera_publisher():
    # initialize the ROS node
    rospy.init_node('opencv_camera_node',anonymous=True)
    # create a publisher to publish the image
    pub = rospy.Publisher('camera/image_processed', Image, queue_size=10)
    # initialize the CvBridge class to convert between ROS and OpenCV images
    bridge = CvBridge()
    # open the usb camera
    cap = cv2.VideoCapture(0)

    # set the camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        rospy.logerr("Cannot open camera")
        return

    # set the rate for publishing frames
    rate = rospy.Rate(10)


    while not rospy.is_shutdown():
        # capture a frame from the camera
        ret, frame = cap.read()

        if ret:
	    # convert the frame to a ROS Image message
            msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")

	    # publish the message
        pub.publish(msg)


	    # (optinal) display the frame in an opencv window for testing
        # CANNOT 
        # cv2.imshow("Camera Feed", frame)
        if cv2.waitKey(1)&0xFF == ord('q'):
            break
    else:
        rospy.logwarn("Failed to capture image")

    rate.sleep()


    # release the camera and close opencv windows when done
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        camera_publisher()
    except:
        rospy.ROSInterruptException
        pass

































    






