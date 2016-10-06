import json
import numpy as np

def normalizeEvolutiveData(data, fitness,dimensions_boundaries=None, fitness_boundaries=None):

	"""
	Normalize all values based in each dimension values

	Parametters:

	- data:
	Numpy array with individuals values in each epoch in the shape (E, I, D), where E = number of epochs, I = number of individuals, D = number of dimensions

	- fitness:
	Numpy array with all the fitness of each individual in each epoch, with shape (E,I) [letters same meaning in the last item described here]

	- dimensions_boundaries:

	Default is none, so the values considered as min and max for each dimension are the values in data and fitness, if is given, should have the following format: [{'min': <VALUE>, 'max': <VALUE>}, ...], one dict like these for each dimension

	- fitness_boundaries:

	Same idea that the last parameter, but is only one dict in the form {'min': <VALUE>, 'max': <VALUE>}
	"""

	E = data.shape[0]
	I = data.shape[1]
	D = data.shape[2]

	data_norm = np.zeros(data.shape)
	fitness_norm = np.zeros(fitness.shape)

	#Normalize fitnesss
	if fitness_boundaries is None:
		minFitness = fitness.min()
		maxFitness = fitness.max()
	else:
		minFitness = fitness_boundaries['min']
		maxFitness = fitness_boundaries['max']

	fitness_norm = (fitness- minFitness)/(maxFitness-minFitness)

	#normalize data
	for e in range(E):
		for d in range(D):

			if dimensions_boundaries is None:
				minInD = data[:,:,d].min()
				maxInD = data[:,:,d].max()
			else:
				minInD = dimensions_boundaries[d]['min']
				maxInD = dimensions_boundaries[d]['max']

			data_norm[:,:,d] = (data[:,:,d]-minInD)/(maxInD-minInD)

	return data_norm, fitness_norm

def evolutiveReader(filename):

	with open(filename,'r') as dotswarm:
		json_str = dotswarm.read()
		swarm_json = json.loads(json_str)

	data = np.array(swarm_json['data'])
	fitness = np.array(swarm_json['fitness'])

	return data,fitness
 
"""

Class for creat log of the optimization algorithm


"""

class EvolutiveLogger:

	def __init__(self):
		self.data = []
		self.fitness = []
		self.current_epoch = 0

		#epochs control
		self.data_acc = []
		self.fitness_acc = []
	
	def append_individual(self, features, fitness, epoch):

		if epoch > self.current_epoch:

			#salva dados da epoca passada
			self.data.append(self.data_acc)
			self.fitness.append(self.fitness_acc)

			#prepara para nova epoca
			self.data_acc = []
			self.fitness_acc = []

			self.current_epoch = epoch

		#salva dados de entrada de novo individuo
		self.data_acc.append(list(features))
		self.fitness_acc.append(fitness)

	def save_log(self, filename, data_only=False):

		log = {}
		if not data_only:
			header = {
				'dimension': len(self.data[0][0]),
				'epochs': len(self.data[0])
			}
			log['header'] = header

		log["data"] = np.array(self.data).tolist()
		log["fitness"] = np.array(self.fitness).tolist()

		if not filename.endswith('.swarm'):
			filename = filename +'.swarm'

		with open(filename,'w') as log_file:
			json_log = json.dumps(log)
			log_file.write(json_log)

		print('Log saved successfully as:', filename)


