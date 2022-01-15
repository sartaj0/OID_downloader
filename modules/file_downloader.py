version = {
	"v6": {
		"train": "https://storage.googleapis.com/openimages/v6/oidv6-train-annotations-bbox.csv", 
		"validation": "https://storage.googleapis.com/openimages/v5/validation-annotations-bbox.csv", 
		"test": "https://storage.googleapis.com/openimages/v5/test-annotations-bbox.csv"
		},
	}


import os 
from multiprocessing.dummy import Pool as ThreadPool
from tqdm import tqdm 

threads = 5
pool = ThreadPool(threads)


download_dir = "dataset"
image_dir = "test"
image = "000026e7ee790996"
path = image_dir + '/' + str(image) + '.jpg ' + '"' + download_dir + '"'
command = 'aws s3 --no-sign-request --only-show-errors cp s3://open-images-dataset/' + path


commands = [command for i in range(20)]

list(tqdm(pool.imap(os.system, commands), total = len(commands) ))