########################################################################
########################################################################

#Author: Rebecca Miko 
#Date: 03/01/19
#Script based on the Izhikevich Neuron Model 
# https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1257420

#Izhikevich Model: 
# dv/dt=0.04*v^2+5*v+140-u+I 
# du/dt=a*(b*v-u)

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

#Output:
#pn: the iteration number
#s: total number of spikes
#v: membrane potential (mV)
#u : recovery variable

########################################################################
# Izhikevich neurons
izhikevich_values =[	
   {'name':'RS','a':0.02,'b':0.2,'c':-65,'d':8,'v':-70, 'u':-14}, 
   {'name':'IB','a':0.02,'b':0.2,'c':-55,'d':4,'v':-70, 'u':-14}, 
   {'name':'CH','a':0.02,'b':0.2,'c':-50,'d':2,'v':-70, 'u':-14}, 
   {'name':'FS','a':0.1,'b':0.2,'c':-65,'d':2,'v':-70, 'u':-14}, 
   {'name':'TC1','a':0.02,'b':0.25,'c':-65,'d':0.05,'v':-63, 'u':-14}, 
   {'name':'TC2','a':0.02,'b':0.25,'c':-65,'d':0.05,'v':-87, 'u':-14}, 
   {'name':'RZ','a':0.1,'b':0.26,'c':-65,'d':0.05,'v':-70, 'u':-14}, 
   {'name':'LTS','a':0.02,'b':0.25,'c':-65,'d':2,'v':-70, 'u':-14}]

selected_value=raw_input("Please enter the Izhikevich neuron type: ")
my_dict=next((iz_dict for iz_dict in izhikevich_values if 
				iz_dict['name']==selected_value), None)

#Variables
v=my_dict.get('v')
u=my_dict.get('u')
I=25

a=my_dict.get('a')
b=my_dict.get('b')
c=my_dict.get('c')
d=my_dict.get('d')

num_spikes=0

#Iterations
iterations = raw_input("Please enter the number of iterations (n): ")
iterations = range(0,int(iterations))

#option
op=raw_input("Choose which steps to see 'all', 'spikes' or 'last': ")

#print function
def print_func():
	print ("p" + str(i+1) + ":" + "\n" + 
		" v" + str(i) + "=" + str(v) + ", v'" + 
		str(i+1) + "=" + str(differential_v) + 
		", v" + str(i+1) + "=" + str(new_v)  + "\n" 
		+ " u" + str(i) + "=" + str(u) + ", u'" + str(i+1) + 
		"=" + str(differential_u) + ", u" + str(i+1) + "=" + 
		str(new_u)  + "\n" +  " s=" + str(num_spikes))

#loop through iterations
for i in iterations:
	#IZ equations
	differential_v=(0.04*(v**2))+(5*v)+140-u+I
	differential_u=a*((b*v)-u)

	#update v and u
	new_v=v+differential_v
	new_u=u+differential_u
	if new_v >=30:
		new_v=c
		new_u=new_u+d
		#update spike total
		num_spikes=num_spikes+1
	
	#print spike steps
	if op=="spike":
		if v==-65:
			print_func()

	#print all steps
	if op=="all":
		print_func()

	#update if its not the last iteration
	if i+1 !=len(iterations):
		v=new_v
		u=new_u

#print end result
if op=="last":
		print_func()

########################################################################

