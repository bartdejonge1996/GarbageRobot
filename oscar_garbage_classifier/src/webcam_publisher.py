#!/usr/bin/env python

from __future__ import print_function
import rospy
import sys
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def main(args):
    pub = rospy.Publisher('image_topic', Image, queue_size=1)
    rospy.init_node('webcam', anonymous=True)
    rate = rospy.Rate(10)
    cam = cv2.VideoCapture(1)
    cv_bridge = CvBridge()
    while not rospy.is_shutdown(): 
        ret, frame = cam.read()
        if ret: 
            try: 
                pub.publish(cv_bridge.cv2_to_imgmsg(frame))
            except CvBridgeError as e: 
                print('error: %s' % e)
        rate.sleep()
    cam.release()



# Main
if __name__ == "__main__": 
    try: 
        main(sys.argv)
    except rospy.ROSInterruptException(): 
        pass
