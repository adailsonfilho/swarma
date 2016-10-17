import json
import numpy as np
import ipdb

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

	with open(filename,'r', encoding='utf-8') as dotswarm:
		json_str = dotswarm.read()
		swarm_json = json.loads(json_str)

	E = swarm_json['header']['epochs']
	I = swarm_json['header']['individuals']
	D = swarm_json['header']['dimension']

	print(type(swarm_json['data']))
	print(type(swarm_json['data'][0]))
	print(type(swarm_json['data'][0][0]))
	print(type(swarm_json['data'][0][0][0]))

	ipdb.set_trace()

	data = np.array(swarm_json['data'])
	fitness = np.array(swarm_json['fitness'])

	return data,fitness
 
"""

Class for creat log of the optimization algorithm


"""

class EvolutiveLogger:


	def __init__(self, name, objective):

		assert(objective == 'minimize' or 'maximize')

		self.name = name
		self.objective = objective
		self.data = []
		self.fitness = []
		self.current_epoch = 0

		self.data.insert(self.current_epoch,[])
		self.fitness.insert(self.current_epoch,[])

	
	def append_individual(self, features, fitness, epoch):

		#não pode setar valores de epocas passadas
		assert(epoch >= self.current_epoch)

		#se for nova epoca
		if epoch > self.current_epoch:

			self.data.insert(epoch,[])
			self.fitness.insert(epoch,[])
			self.current_epoch = epoch

		self.data[epoch].append([a.item() for a in features])
		self.fitness[epoch].append(fitness.item())

		# if epoch > self.current_epoch:

		# 	#salva dados da epoca passada
		# 	self.data.append(self.data_acc)
		# 	self.fitness.append(self.fitness_acc)

		# 	#prepara para nova epoca
		# 	self.data_acc = []
		# 	self.fitness_acc = []

		# 	self.current_epoch = epoch

		# #salva dados de entrada de novo individuo
		# self.data_acc.append(list(features))
		# self.fitness_acc.append(fitness)

	def save_log(self, filename, data_only=False):

		E = len(self.data)
		I = len(self.data[0])
		D = len(self.data[0][0])

		log = {}
		if not data_only:
			header = {
				'dimension': D,
				'individuals': I,
				'epochs': E,
				'objective':self.objective,
				'name':self.name

			}
			log['header'] = header

		

		log["data"] = np.array(self.data).tolist()
		log["fitness"] = np.array(self.fitness).tolist()

		#garantir que dados estão em formatos nativos de python
		# log['data'] = [[[e.item() for e in individual] for individual in epoch] for epoch in self.data]
		# log['fitness'] = [[e.item() for e  in epoch] for epoch in self.fitness]

		if not filename.endswith('.swarm'):
			filename = filename +'.swarm'

		with open(filename,'w', encoding='utf-8') as log_file:
			json_log = json.dumps(log)
			log_file.write(json_log)

		print('Log saved successfully as:', filename)


