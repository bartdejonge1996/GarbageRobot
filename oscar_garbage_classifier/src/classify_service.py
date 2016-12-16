#!/usr/bin/env python

from squeezenetv1_1 import SqueezeNet
import keras
import keras.backend.tensorflow_backend as K
import tensorflow as tf
from oscar_garbage_classifier.srv import ClassifyImage
from cv_bridge import CvBridge
import cv2
import numpy as np
import rospy
import time


classes = ['coca_cola_bottles', 'fanta_bottle', 'cola_cans', 'fanta_cans', 'paper_coffee_cups', 'water_bottles']
classes_mapping = {'coca_cola_bottles': 0, 'fanta_bottle': 0, 'cola_cans': 1, 'fanta_cans': 1, 'paper_coffee_cups': 2, 'water_bottles': 0}

my_graph = tf.Graph()
squeezenet = None

def load_squeezenet():
    with my_graph.as_default():
        global squeezenet
        if squeezenet is None: 
            squeezenet = SqueezeNet(6, input_shape=(227, 227, 3))
            print('Instantiated model')
            squeezenet.load_weights('./weights_v1.1.h5', by_name=True)
        return squeezenet

def load_image(img):
    # Load image with 3 channel colors
    # img = cv2.imread('/mnt/data/Development/ros/catkin_ws/images/cola_bottles_13.jpg', flags=1)
    # print(img.shape) 

    # Image needs to the resized to (227x227), but we want to maintain the aspect ratio.
    height = img.shape[0]
    width = img.shape[1]
    offset = int(round(max(height, width) / 2.0))

    # Add borders to the images.
    padded_img = cv2.copyMakeBorder(img, offset, offset, offset, offset, cv2.BORDER_CONSTANT)
    padded_height = padded_img.shape[0]
    padded_width = padded_img.shape[1]
    center_x = int(round(padded_width / 2.0))
    center_y = int(round(padded_height / 2.0))
    # Crop the square containing the full image.
    cropped_img = padded_img[center_y - offset: center_y + offset, center_x - offset: center_x + offset]

    # Resize image to 227, 227 as Squeezenet only accepts this format.
    resized_image = cv2.resize(cropped_img, (227, 227)).astype(np.float32)
    resized_image /= 255
    resized_image = np.expand_dims(resized_image, axis=0)
    return resized_image

def handle_service(request): 
    print('Classifying image')
    img = CvBridge().imgmsg_to_cv2(request.msg)
    img = load_image(img)
    sq = load_squeezenet()
    with my_graph.as_default():
        result = sq.predict(img)
    print('predicting')
    # result = squeezenet.predict(img2)
    print('result: %s' % zip(classes, result[0]))
    top = result[0].argsort()[-1::][0]
    print('Classified as %s' % classes[top])
    return top

def image_classify_service():
    rospy.init_node('image_classify_service')
    s = rospy.Service('image_classify', ClassifyImage, handle_service)
    print('Image classify service ready.')
    rospy.spin()


if __name__ == '__main__':
    image_classify_service()

