########################################################################
########################################################################

#Author: Rebecca Miko 
#Date: 12/12/18
#Model modified from Izhikevich Neuron Model 
# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1257420

#Izhikevich Model: 
# dv/dt=0.04*v^2+5*v+140-u+I 
# du/dt=a*(b*v-u)

########################################################################

#USAGE
#python Iz_Replications.py [-h] [--plot-figure] [--debug DEBUG] simulator

#ARGUMENTS:
#simulator choice: neuron, nest or brian

#OPTIONAL ARGUMENTS:
#  -h, --help     Show help message
#  --plot-figure  Plot the simulation results
#  --debug DEBUG  Print debugging information

########################################################################

#Neuron types:
#RS: regular spiking
#IB: intrinsically bursting
#CH: chattering
#FS: fast spiking
#TC1/2: thalamo-cortical
#RZ: resonator
#LTS: low threshold spiking

#See the paper for more details

########################################################################
########################################################################
#imports
from numpy import arange
import os
import numpy as np
import matplotlib.pyplot as plt
from pyNN.utility import get_simulator,init_logging,normalized_filename

#configure simulation
sim,options=get_simulator(
	("--plot-figure","Plot the simulation results to a file.",
					{"action":"store_true"}), 
	("--debug","Print debugging information"))

#optional argument --debug
if options.debug: 
    init_logging(None,debug=True)

#Izhikevich neurons
izhikevich_values =[	
   {'name':'RS','a':0.02,'b':0.2,'c':-65,'d':8,'v':-70,'tstart':10.0,'c1':0.01}, 
   {'name':'IB','a':0.02,'b':0.2,'c':-55,'d':4,'v':-70,'tstart':10.0,'c1':0.01}, 
   {'name':'CH','a':0.02,'b':0.2,'c':-50,'d':2,'v':-70,'tstart':10.0,'c1':0.01}, 
   {'name':'FS','a':0.1,'b':0.2,'c':-65,'d':2,'v':-70,'tstart':10.0,'c1':0.01}, 
   {'name':'TC1','a':0.02,'b':0.25,'c':-65,'d':0.05,'v':-63,'tstart':50.0,'c1':0.001}, 
   {'name':'TC2','a':0.02,'b':0.25,'c':-65,'d':0.05,'v':-87,'tstart':10.0,'c1':-0.6}, 
   {'name':'RZ','a':0.1,'b':0.26,'c':-65,'d':0.05,'v':-70,'tstart':0.5, 'tstart2':110.0,'c1':0.000143, 'c2':0.001}, 
   {'name':'LTS','a':0.02,'b':0.25,'c':-65,'d':2,'v':-70, 'u':-14, 'tstart':10.0, 'c1':0.01}]

selected_value=raw_input("Please enter the Izhikevich neuron type: ")
my_dict=next((iz_dict for iz_dict in izhikevich_values if 
				iz_dict['name']==selected_value), None)

#sim parameters
sim_duration=200.0 #ms

#simulation
sim.setup(timestep=0.01,min_delay=1.0)
num_neurons=1

#neurons
neurons=sim.Population(num_neurons,sim.Izhikevich(a=my_dict.get('a'), b=my_dict.get('b'), c=my_dict.get('c'), d=my_dict.get('d')))

#input
src=sim.DCSource(start=my_dict.get('tstart'),stop=sim_duration,amplitude=my_dict.get('c1'))
step_current=sim.StepCurrentSource(times=[0.0,my_dict.get('tstart')],amplitudes=[my_dict.get('c1'),0.0])

if selected_value in ('RS','IB','CH','FS','LTS','TC1'):
	src.inject_into(neurons[0:1])
if selected_value in ('RZ'):
	src.inject_into(neurons[0:1])
	src2=sim.DCSource(start=my_dict.get('tstart2'),stop=160,amplitude=my_dict.get('c2'))
	src2.inject_into(neurons[0:1])
if selected_value in ('TC2'):
	step_current.inject_into(neurons[0:1])

neurons.record(['v','u']) 
neurons.initialize(v=my_dict.get('v'),u=-14.0) 

#RUN
sim.run(sim_duration)

#save and plot
directory="Iz_plots/"
filename=my_dict.get('name')
extension=".eps"
#optional argument --plot-figure
if options.plot_figure: 
	data=neurons.get_data().segments[0]
	v=data.filter(name='v')[0]
	#u=data.filter(name="u")[0]
	fig = plt.figure()
	plt.plot(v.times, v)
	if my_dict.get('name') !='TC2':
		plt.ylim(-80, 0)
	else:
		plt.ylim(-200, 0)
	plt.ylabel("Membrane potential (mV)")
	plt.xlabel("Time (ms)")
	plt.title(my_dict.get('name'))
	plt.savefig(os.path.join(directory, filename+extension), dpi=300)

#end sim
sim.end()

###############################################################################################################
###############################################################################################################


