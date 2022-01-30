import argparse
# python main.py download --classes Car --type_data train --annot_format yolo

'''
classes: List
type_data: Muliple or Single 'train test validation'
limit: Intger
annot_format: String - coco, yolo, voc

'''

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	subparser = parser.add_subparsers(dest='command')

	download = subparser.add_parser('download', help="To download the dataset")
	show = subparser.add_parser('show', help="To visualize the dataset")

	download.add_argument('--classes', type=str, required=True, nargs='+', help="Name of the classes")
	download.add_argument('--limit', type=int, required=False, default=None, help="Number of images per classes")
	download.add_argument('--type_data', type=str, required=True, choices=['train', 'test', 'validation'], nargs='+')
	download.add_argument('--annot_format', type=str, required=True, choices=['coco', 'yolo', 'voc'])
	download.add_argument('--down_dir', type=str, required=False, help="Download Dir")

	args = vars(parser.parse_args())

	print(args)
