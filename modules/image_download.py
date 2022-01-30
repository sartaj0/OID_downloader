import pandas as pd
import numpy as np

import os 
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm 


def extractImages(args):
	class_descr = pd.read_csv("Annotations/class-descriptions-boxable.csv", header=None)
	class_name = {}
	for classes in args['classes']:
		class_name[classes] = class_descr[class_descr.iloc[:, 1] == classes].iloc[0][0]
	class_name_inv = {v:k for k, v in class_name.items()}

	for folder in args['type_data']:
		bbox_annot = pd.read_csv(f"Annotations/{folder}-annotations-bbox.csv")


		bbox_annot = bbox_annot[bbox_annot['LabelName'].isin(list(class_name.values()))]
		print(class_name)
		print(bbox_annot.shape)

		if (args['limit'] is not None):
			images = select_images(bbox_annot, class_name_inv, args)
		else:
			images = np.unique(bbox_annot['ImageID'].values)
		print(len(images))

		with open(os.path.join("dataset", "classes.txt"), "w") as f:
			for classes in args['classes']:
				f.write(f"{str(classes)}\n")

		download_images(images, folder)
		create_annotations(images, bbox_annot, folder, class_name_inv, args)


def select_images(bbox_annot, class_name_inv, args):
	count = {classes: 0 for classes in args['classes']}
	classes_to_select = list(class_name_inv.keys())
	images = np.unique(bbox_annot['ImageID'].values)

	download_images = []
	for image in images:
		images_boxes = bbox_annot[bbox_annot['ImageID'] == image]
		if images_boxes['LabelName'].isin(classes_to_select).any():
			download_images.append(image)
			for classes in list(set(images_boxes['LabelName'].values)):
				count[class_name_inv[classes]] += 1
				if (count[class_name_inv[classes]] >= args['limit']) and (classes in classes_to_select):
					classes_to_select.remove(classes)
		elif classes_to_select == []:
			break
		# break

	print(count)
	return download_images


def download_images(images, folder, threads=5):

	pool = ThreadPool(threads)
	image_dir = folder
	download_dir = os.path.join("dataset", image_dir)

	commands = []


	for image in images:
		path = image_dir + '/' + str(image) + '.jpg ' + '"' + download_dir + '"'
		command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path
		commands.append(command)

	list(tqdm(pool.imap(os.system, commands), total = len(commands)))


def create_annotations(images, bbox_annot, folder, class_name_inv, args):
	for image in images:
		img_filename = os.path.sep.join(["dataset", folder, str(image)+".jpg"])
		if os.path.isfile(img_filename):
			# print(bbox_annot[bbox_annot['ImageID'] == image])
			# print(bbox_annot[bbox_annot['ImageID'] == image].rows)
			txt_filename = os.path.sep.join(["dataset", folder, f"{image}.txt"])
			with open(txt_filename, "w") as f:
				for i, row in bbox_annot[bbox_annot['ImageID'] == image].iterrows():
					xmin = row['XMin']
					ymin = row['YMin']
					xmax = row['XMax']
					ymax = row['YMax']

					x = (xmax + xmin) / 2
					y = (ymax + ymin) / 2

					w = (xmax - xmin)
					h = (ymax - ymin)
					label = args['classes'].index(class_name_inv[row['LabelName']])
					f.write(f"{label} {x} {y} {w} {h}\n")


if __name__ == '__main__':
	args = {
	'command': 'download',
	'classes' : ['Vehicle registration plate'],
	'limit': None, 
	'type_data': ['validation', 'test'], 
	'annot_format': 'yolo', 
	'down_dir': None, }

	extractImages(args)
