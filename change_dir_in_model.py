import pickle
import os

# This is a script for converting paths for models donwloaded from the IIC github, 
# on a Python 3 system.
# Is to be run from root IIC directory.


# DOES NOT YET WORK FOR 
# the following models: ["544", "496", "482", "512", "521", "545", "555", "487"]:

assert os.path.exists("code") # assuming we're in iic after this ...

if not os.path.exists("out"):
	os.mkdir("out")

if not os.path.exists("datasets"):
	os.mkdir("datasets")

# pre-defined variables
external_storage = '/shared/users/daniesis/iic/'
if not os.path.isdir(external_storage) and os.path.exists(external_storage):
	external_storage = os.path.join(os.getcwd(), 'out')


for subdir, dirs, files in os.walk('models'):
	for direc in dirs:
		model_name = direc # might want to loop through models/ later..
		print(direc)
		if model_name in ["544", "496", "482", "512", "521", "545", "555", "487"]:
			print("Dropping "+model_name)
			continue

		with open(os.path.join('models', model_name, 'config.pickle'), 'rb') as conf_f:
			conf = pickle.load(conf_f, encoding='latin-1')

		try:
			dataset = conf.dataset

			dataset_dir = os.path.join(os.getcwd(), 'datasets', dataset)
			conf.dataset_root = dataset_dir
		except AttributeError:
			print(model_name+" has no attribute dataset")	

		conf.out_dir = os.path.join(os.getcwd(), 'out', model_name)
		conf.out_root = external_storage

		with open(os.path.join('models', model_name, 'config.pickle'), 'wb') as out:
			pickle.dump(conf, out)

		with open(os.path.join('models', model_name, 'config.txt'), 'w') as out:
			out.write('%s' % conf)

		# test
		with open(os.path.join('models', model_name, 'config.pickle'), 'rb') as conf_f:
			new_conf = pickle.load(conf_f)
			assert conf == new_conf

		print(model_name+" ok")
