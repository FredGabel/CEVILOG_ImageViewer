import numpy as np
import cv2

def changeBrightness(img,value):
		""" This function will take an image (img) and the brightness
			value. It will perform the brightness change using OpenCv
			and after split, will merge the img and return it.
		"""
		hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
		h,s,v = cv2.split(hsv)
		lim = 255 - value
		v[v>lim] = 255
		v[v<=lim] += value
		final_hsv = cv2.merge((h,s,v))
		img = cv2.cvtColor(final_hsv,cv2.COLOR_HSV2BGR)
		return img