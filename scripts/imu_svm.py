#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64

from sklearn import svm
import sklearn
from sklearn.decomposition import PCA
from sklearn.externals import joblib

class Svm_pub:
	def __init__(self):
		self._sub = rospy.Subscriber("imu/data_raw", Imu, self.imu_callback)
		#self._pub = rospy.Publisher("stop_proba", Float64, queue_size=10)
		#self.m = 5
		clf = joblib.load("svc.pkl.cmp")
		pca = joblib.load('pca.pkl.cmp')

	def imu_callback(self, message):
		accel = message.linear_acceleration
		omega = message.angular_velocity
		print accel.z, omega.z

		#self.data = np.append(self.data, np.array([[accel.z]]), axis=0)
		#self.data = np.delete(self.data, 0, axis=0)

		#self._pub.publish(anomaly_score)

if __name__ == '__main__':
	print sklearn.__version__
	rospy.init_node('imu_svm')
	svm_pub = Svm_pub()
	rospy.spin()
