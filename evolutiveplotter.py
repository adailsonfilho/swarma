import numpy as np
import matplotlib.pyplot as plt
import os

def EvolutivePlotter(data2d,fitness,lims, folder='', id_label=False, save_format=".png"):
	
	if folder != '' and not os.path.exists(folder):
		os.makedirs(folder)


	vmin = fitness.min()
	vmax = fitness.max()

	for i,epoch in enumerate(data2d):

		print('Saving plots - Log 2D Epoch:',i,'of',len(data2d))

		cm = plt.cm.get_cmap('plasma')

		marker_size = 5

		fig = plt.figure()
		plt.xlim(lims[0]-marker_size, lims[1]+marker_size)
		plt.ylim(lims[0]-marker_size, lims[1]+marker_size)


		sc = plt.scatter(epoch[:,0],epoch[:,1], c = fitness[i], vmin = vmin, vmax = vmax, cmap = cm, edgecolors='face')
		plt.colorbar(sc)

		if(save_format == '.svg'):
			plt.axis('off')
			plt.gca().set_position([0, 0, 1, 1])

		if id_label:
			for counter,ind in enumerate(epoch):
				plt.text(ind[0], ind[1], str(counter+1))

		# plt.text(epoch[:,0],epoch[:,1],[str(counter) for counter in range(len(epoch))])

		id_int_size = len(str(len(data2d)))
		
		fig.suptitle('Epoch '+str(i+1), fontsize=20)
		plt.savefig(folder+'\\'+str(i).zfill(id_int_size)+'frame'+save_format)
		plt.clf()

def EvolutivePlotterFig(data2d,fitness,lims, id_label=False, epoch_index=0):

	vmin = fitness.min()
	vmax = fitness.max()

	epoch = data2d[epoch_index]

	cm = plt.cm.get_cmap('plasma')

	fig = plt.figure()
	plt.xlim(lims[0], lims[1])
	plt.ylim(lims[0], lims[1])

	sc = plt.scatter(epoch[:,0],epoch[:,1], c = fitness[epoch_index], vmin = vmin, vmax = vmax, cmap = cm, edgecolors='face')
	plt.colorbar(sc)

	if id_label:
		for counter,ind in enumerate(epoch):
			plt.text(ind[0], ind[1], str(counter+1))

	id_int_size = len(str(len(data2d)))
	
	fig.suptitle('Epoch '+str(epoch_index+1), fontsize=20)

	return fig