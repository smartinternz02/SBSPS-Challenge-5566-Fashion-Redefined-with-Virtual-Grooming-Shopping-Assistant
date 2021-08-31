import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
global graph,preds
graph = tf.Graph()

from flask import Flask, request, render_template, redirect

from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
from os import listdir
from os.path import isfile, join
import cvzone
import cv2
import json
global payload
import base64



app = Flask(__name__,template_folder='Templates')
model = load_model("FashionF2.h5")


@app.route('/',methods = ["POST","GET"])
def main1():
	onlyfiles = []
	if request.method == "GET":
		return render_template('ex.html',onlyfiles=onlyfiles)
	if request.method == "POST":
		payload = request.json
		payload['name'] = 'Hii'
		key1 = 'wish'
		key2 = 'enquire'
		p = 0
		if key2 in payload:
			if payload['enquire'] == 'shirts':
				p = 5
				print("User wants shirts !!!")
			elif payload['enquire'] == 'Hoodies':
				p = 3
				print("User wants pants !!!")
			elif payload['enquire'] == 'pants':
				p = 4
				print("User wants pants !!!")
			elif payload['enquire'] == 'Full hand T-shirts':
				p = 2
				print("User wants pants !!!")
			elif payload['enquire'] == 'footwears':
				p = 6
				print("User wants pants !!!")
			elif payload['enquire'] == 'cap':
				p = 1
				print("User wants pants !!!")
			elif payload['enquire'] == 'Skirts':
				p = 8
				print("User wants pants !!!")
			elif payload['enquire'] == 'T-shirts':
				p = 9
				print("User wants pants !!!")
			elif payload['enquire'] == 'tops':
				p = 0
				print("User wants pants !!!")
			elif payload['enquire'] == 'Half hand T shirts':
				p = 9
				print("User wants pants !!!")
			elif payload['enquire'] == 'Shorts':
				p = 7
				print("User wants pants !!!")
		onlyfiles = [f for f in listdir('dress-1/' + str(p) + '/') if isfile(join('dress-1/' + str(p) + '/', f))]
		print(onlyfiles[0])
		with open('dress.txt', 'w') as f:
			for item in onlyfiles:
				f.write("%s\n" % item)
		return onlyfiles[0]

	else:
		print(request.data)
		return "200"

@app.route('/text',methods=["POST","GET"])
def main2():
	#file1 = open('myfile.txt', 'w')
	#file1.writelines((L))
	"""file1.close()
 
	# Using readline()
	file1 = open('dress.txt', 'r')
	count = 0
 
	while True:
		count += 1
		# Get next line from file
		line = file1.readline()
		# if line is empty
		# end of file is reached
		if not line:
			break
		files[i] = 
	file1.close()"""

	my_file = open("dress.txt", "r")
	content_list = my_file.readlines()
	print(content_list)

	return render_template('ex2.html',onlyfiles=content_list)

@app.route('/predict',methods = ['GET','POST'])
def main():
	if request.method == 'POST':

		f = request.files['file']
		print("current path")
		basepath = os.path.dirname(__file__)
		print("current path",basepath)
		filepath = os.path.join(basepath,'uploads',f.filename)
		print("uplaod folder is ",filepath)
		f.save(filepath)

		img = image.load_img(filepath,target_size = (64,64))
		x = image.img_to_array(img)
		x = np.expand_dims(x,axis = 0)

		preds = model.predict(x)
		preds = np.argmax(preds)
		print("prediction",preds)
		preds = str(preds)
		text = "the predoicted item is : " + preds
		onlyfiles = [f for f in listdir('dress-1/' + preds + '/') if isfile(join('dress-1/' + preds + '/', f))]
		return render_template('ex.html',preds=preds,onlyfiles=onlyfiles)
	else:
		print(request.data)
		return "200"

@app.route('/try-on', methods = ['GET','POST'])
def try_on():
	if request.method == 'GET':
		return render_template('base.html')
	if request.method == 'POST':
		f = request.files['file']
		print("current path")
		basepath = os.path.dirname(__file__)
		print("current path",basepath)
		filepath = os.path.join(basepath,'uploads',f.filename)
		print("uplaod folder is ",filepath)
		f.save(filepath)
		cap = cv2.VideoCapture(0)
		cap.set(3,1920)
		cap.set(4,1080)
		success, img = cap.read()
		print(f)
		imgFront = cv2.imread("uploads/" + f.filename, cv2.IMREAD_UNCHANGED)	
		imgFront = cv2.cvtColor(imgFront, cv2.COLOR_BGR2BGRA)

		print(imgFront.shape)

		hf, wf, cf = imgFront.shape
		hb, wb, cb = img.shape

		fpsReader = cvzone.FPS()

		while True:
			success, img = cap.read()
			imgResult = cvzone.overlayPNG(img, imgFront, [350, 200])
			_, imgResult = fpsReader.update(imgResult)
			cv2.imshow("Image", imgResult)
			key = cv2.waitKey(1)
			if key%256 == 27:
				break
		cap.release()
		cv2.destroyAllWindows()
		return render_template('ex.html')



if __name__ == '__main__':
	app.run(debug = True)

