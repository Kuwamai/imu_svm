#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import numpy as np
from sensor_msgs.msg import Imu
from std_msgs.msg import Float64
from imu_svm.msg import state_proba

from sklearn import svm
import sklearn
from sklearn.decomposition import PCA
from sklearn.externals import joblib
from pathlib import Path

class Svm_pub:
	def __init__(self):
		self._sub = rospy.Subscriber("imu/data_raw", Imu, self.imu_callback)
		self._pub = rospy.Publisher("state_proba", state_proba, queue_size=10)
		self.m = 5
		self.d = 6
		self.feature_num = 17
		p_svc = Path('./svc.pkl.cmp')
		p_pca = Path('./pca.pkl.cmp')
		self.clf = joblib.load(p_svc)
		self.pca = joblib.load(p_pca)

		self.a_x = np.zeros((1, self.m))
		self.a_y = np.zeros((1, self.m))
		self.a_z = np.zeros((1, self.m))
		self.o_x = np.zeros((1, self.m))
		self.o_y = np.zeros((1, self.m))
		self.o_z = np.zeros((1, self.m))

	def imu_callback(self, message):
		accel = message.linear_acceleration
		omega = message.angular_velocity

		self.a_x = np.delete(self.a_x, 0, axis=1)
		self.a_x = np.append(self.a_x, np.array([[accel.x]]), axis=1)

		self.a_y = np.delete(self.a_y, 0, axis=1)
		self.a_y = np.append(self.a_y, np.array([[accel.y]]), axis=1)

		self.a_z = np.delete(self.a_z, 0, axis=1)
		self.a_z = np.append(self.a_z, np.array([[accel.z]]), axis=1)

		self.o_x = np.delete(self.o_x, 0, axis=1)
		self.o_x = np.append(self.o_x, np.array([[omega.x]]), axis=1)

		self.o_y = np.delete(self.o_y, 0, axis=1)
		self.o_y = np.append(self.o_y, np.array([[omega.y]]), axis=1)

		self.o_z = np.delete(self.o_z, 0, axis=1)
		self.o_z = np.append(self.o_z, np.array([[omega.z]]), axis=1)

		data  = np.concatenate((self.a_x, self.a_y, self.a_z, self.o_x, self.o_y, self.o_z), axis=1)
		data  = self.pca.transform(data)
		proba = self.clf.predict_proba(data[:, 0:self.feature_num])

		st_proba = state_proba()

		st_proba.forward = proba[0][0]
		st_proba.crash   = proba[0][1]
		st_proba.turn_l  = proba[0][2]
		st_proba.turn_r  = proba[0][3]
		st_proba.stop    = proba[0][4]
		
		self._pub.publish(st_proba)

if __name__ == '__main__':
	rospy.init_node('imu_svm')
	svm_pub = Svm_pub()
	rospy.spin()
