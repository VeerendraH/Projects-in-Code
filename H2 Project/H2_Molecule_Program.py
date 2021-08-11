########################################################################################
##            ##########        ###               ###      ###          ###           ##
##            ###     ###        ###             ###       ###          ###           ##
##            ###     ###         ###           ###        ###          ###           ##
##            ###    ##            ###         ###         ###          ###           ##
##            ########              ###       ###          ################           ##
##            ###    ###             ###     ###           ################           ##
##            ###     ###             ###   ###            ###          ###           ##
##            ###    ###               #######             ###          ###           ##
##            #########                 #####              ###          ###           ##
########################################################################################
#                                  File Details
# Project Find BornOppenheimer Potential of H2 Molecule
# Purpose
# Description

print("Monte Carlo Solution of H2 Molecule")
print("Finds Born-Oppenheimer Potential of H2 Molecuule")
print("Using Variational and Path-Integral Monte Carlo Methods")
print("To solve the two-center two-electron problem")
print("Lengths in Angstroms and Energies in eV")


########################################################################################
#                                     Importer
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pl
import matplotlib.gridspec as gridspec
# ######################################################################################
#                                      Input

hbm = 7.6359
e2 = 14.409
a0 = hbm/e2
print('Bohr radius is',a0)
s = 2
s2 = s/2
alpha = 2*a0
beta = 0.25
ngroup = 10
nensem = 10
dt = 0.005

hbmdt = hbm*dt
sqdt = hbmdt**2

ngroup = 20
size = 20
freq = 5

print("Calculating Energy")
print('The number of groups: ',ngroup)
print('The number of samples per group: ',size)
print('The sampling Frequency: ',freq)


print("Enter 1 for Variational, 2 for PIMC methods")
method = int(input())


print("Current Ensemble Size",nensem)
nensem = 5

if (nensem>50):
    nensem = 50

delta = 0.1
print('Current Delta or Metropolis Step Size: ',delta)

ntherm = 40
print('Current number of Thermalization Steps: ',ntherm)

########################################################################################
#                                    Functions

# Useful and repetitive Arithmetic Functions
def dist(x,y,z):
    return np.sqrt(x**2 + y**2 + z**2)

def fnchi(r):
    return np.exp(-r/a)

def fnchip(r):
    return -fnchi(r)/a

def fnchipp(r):
    return fnchi(r)/(a*a)

def fnd2chi(r):
    return fnchipp(r) + 2*fnchip(r)/r

def fnf(r):
    return np.exp(r/(alpha*(1 + beta*r)))

def fnfp(r):
    return fnf(r)/(alpha*((1 + beta*r)**2))

def fnfpp(r):
    return (fnfp(r)**2)/fnf(r) - 2*beta*fnf(r)/(alpha*(1+beta*r)**3)

def fnd2f(r):
    return fnfpp(r) + 2*fnfp(r)/r

def fndist(x,y,z):
    return np.sqrt(x**2+y**2+z**2,dtype = np.float)

# Generate an initial Configuration of the pair of electrons
def gen_config():
    delta = 1.5*a
    config = a*(np.random.rand(6,1)-0.5)
    config[2] = config[2] + s2
    config[5] = config[5] + s2
    return config

# Calculaate the Wave Function and Probability Amplitude of a Configuration
def calc_config(config):
    #print(config,'here')
    x1 = config[0]
    y1 = config[1]
    z1 = config[2]
    x2 = config[3]
    y2 = config[4]
    z2 = config[5]

    r1l = fndist(x1,y1,z1+s2)
    r1r = fndist(x1,y1,z1-s2)
    r2l = fndist(x2,y2,z2+s2)
    r2r = fndist(x2,y2,z2-s2)
    r12 = fndist(x1-x2,y1-y2,z1-z2)

    f = fnf(r12)
    chi1r = fnchi(r1r)
    chi1l = fnchi(r1l)
    chi2r = fnchi(r2r)
    chi2l = fnchi(r2l)
    phi = (chi1r + chi1l)*(chi2l + chi2r)*f
    w = phi*phi
    return w

# Perform a Metropolis Step over a given Configuration  
def metropolis_step(config):
    w = calc_config(config)
    csave = config
    config = config + delta*(np.random.rand(6,1) - 0.5)
    wtry = calc_config(config)
    if wtry < w*np.random.rand(1):
        w = wtry
    else:
        config = csave
    return config

# Generate an Ensemble for the PIMC Method 
def gen_ensemble():
	delta = 1.5*a
	config = gen_config()
	ensemble = np.zeros((nensem,6))
	for i in range(0,20):
		config = metropolis_step(config)

	for i in range(0,10*nensem):
		config = metropolis_step(config)
	
		if(i%10 == 0):
			Iensem = int(i/10)
			ensemble[Iensem,:] = config.flatten()
			
	weight = np.ones(len(ensemble))
	return [ensemble,weight]

# Calculate the Epsilon Value for a given Configuration
def calc_epsilon(config):
    x1 = config[0]
    y1 = config[1]
    z1 = config[2]
    x2 = config[3]
    y2 = config[4]
    z2 = config[5]

    r1l = fndist(x1,y1,z1+s2)
    r1r = fndist(x1,y1,z1-s2)
    r2l = fndist(x2,y2,z2+s2)
    r2r = fndist(x2,y2,z2-s2)
    r12 = fndist(x1-x2,y1-y2,z1-z2)

    f = fnf(r12)
    chi1r = fnchi(r1r)
    chi1l = fnchi(r1l)
    chi2r = fnchi(r2r)
    chi2l = fnchi(r2l)
    phi = (chi1r + chi1l)*(chi2l + chi2r)*f
    w = phi*phi

    r1dotr12 = x1*(x1-x2) + y1*(y1-y2) + z1*(z1-z2)
    sr12z = s*(z1-z2)
    r1ldotr12 = r1dotr12 + sr12z/2
    r1rdotr12 = r1dotr12 - sr12z/2
    r2ldotr12 = r1ldotr12 - r12**2
    r2rdotr12 = r1rdotr12 - r12**2

    tpop = 2*fnd2f(r12)/f
    temp = fnd2chi(r1r) + fnd2chi(r1l)
    tpop = tpop + temp/(chi1r + chi1l)
    temp = fnd2chi(r2r) + fnd2chi(r2l)
    tpop = tpop + temp/(chi2r + chi2l)
    temp = fnchip(r1l)*r1ldotr12/r1l
    cross = (temp + fnchip(r1r)*r1rdotr12/r1r)/(chi1l + chi1r)
    temp = -fnchip(r2r)*r2rdotr12/r2r
    temp = temp - fnchip(r2l)*r2ldotr12/r2l
    cross = cross + temp/(chi2l + chi2r)
    tpop = tpop + 2*(fnfp(r12)/f)*cross/r12
    tpop = -0.5*hbm*tpop

    vpop = -e2*(1/r1l + 1/r1r +1/r2l + 1/r2r - 1/r12)

    epsilon = tpop + vpop
    
    return epsilon

# Calculate the Drift for a Configuration
def calc_drift(config):

	drift = np.zeros((6,1))
	x1 = config[0]
	y1 = config[1]
	z1 = config[2]
	x2 = config[3]
	y2 = config[4]
	z2 = config[5]

	r1l = fndist(x1,y1,z1+s2)
	r1r = fndist(x1,y1,z1-s2)
	r2l = fndist(x2,y2,z2+s2)
	r2r = fndist(x2,y2,z2-s2)
	r12 = fndist(x1-x2,y1-y2,z1-z2)
	
	f = fnf(r12)
	chi1r = fnchi(r1r)
	chi1l = fnchi(r1l)
	chi2r = fnchi(r2r)
	chi2l = fnchi(r2l)
	phi = (chi1r + chi1l)*(chi2l + chi2r)*f
	w = phi*phi
	facta = hbmdt*(fnchip(r1l)/r1l + fnchip(r1r)/r1r)/(chi1l + chi1r)
	factb = hbmdt*(fnchip(r1l)/r1l - fnchip(r1r)/r1r)/(chi1l + chi1r)
	facte = hbmdt*fnfp(r12)/(f*r12)

	drift[0] = facta*x1+facte*(x1-x2)
	drift[1] = facta*y1+facte*(y1-y2)
	drift[2] = facta*z1 + factb*s2+facte*(z1-z2)

	facta = hbmdt*(fnchip(r2l)/r2l + fnchip(r2r)/r2r)/(chi2l + chi2r)
	factb = hbmdt*(fnchip(r2l)/r2l - fnchip(r2r)/r2r)/(chi2l + chi2r)


	drift[3] = facta*x2-facte*(x1-x2)
	drift[4] = facta*y2-facte*(y1-y2)
	drift[5] = facta*z2 + factb*s2-facte*(z1-z2)




	return drift

# Perform a Time Step Evolution in the Path Integral Method
def time_step(ensemble,weight):
	ebar = 0
	wbar = 0
	#print(ensemble,'Check for zeros')
	for i in range(0,nensem):
		config = ensemble[i]
		drift = calc_drift(config)
		rnd_num = 12*np.random.rand(1)-6
		config = config + drift.flatten() + rnd_num*sqdt
	
		epsilon = calc_epsilon(config)
		weight[i] = weight[i]*np.exp(-epsilon*dt)
		ebar = ebar + weight[i]*epsilon
		wbar = wbar + weight[i]

		ensemble[i] = config

	epsilon = ebar/wbar
	norm = nensem/wbar
	weight = norm*weight
	return [ensemble,weight,epsilon]

    


########################################################################################
#                                       Body

# Obtain Wave Function Parameter a
a = a0
aold = 0
while(abs(a-aold)>0.000001):
    aold = a
    a = a0/(1+np.exp(-s/aold))

print("Parameter a is",a)

# Generate a working ensemble or config
if (method==1):
    config = gen_config()
elif(method==2):
    [ensemble,weight] = gen_ensemble()

# Perform Thermalisation over some turns
for i in range(1,ntherm):
    if(method==1):
        config = metropolis_step(config)
    elif(method==2):
    	[ensemble,weight,epsilon] = time_step(ensemble,weight)

# Calc Stuff
# Initialising the Indices and Storage variables

more = ngroup
sume = 0
sume2 = 0
sumsig = 0
suma = 0

group_arr = np.zeros((ngroup,2))
sample_arr = np.zeros((ngroup*size,1))

print('The Variational calculation with Metropolis Step',delta)
print('Interproton Separation',s)
print('Wavefunction Parameter beta',beta)
print('Wavefunction Prameter a',a)
print('Sampling Freq ', freq)

# Loop for Group Iteration
for i in range(ngroup-more+1,ngroup+1):
	groupe = 0
	groupe2 = 0
	accpt = 0

# Loop for Samples
	for j in range(1,freq*size+1):
#   If Loop to redirect to appropriate evolution 
		if(method==1):    
			config = metropolis_step(config)
		elif(method==2):
			[ensemble,weight,epsilon] = time_step(ensemble,weight)
#   Perform Observation at some frequency			
		if(j%freq==0):
			if(method==1):# method 2 is already covered
				epsilon = calc_epsilon(config)
      
#     Arithmetic to make measurements out of observations
			groupe = groupe + epsilon
			groupe2 = groupe2 + epsilon**2

			sige = np.sqrt(groupe2/size)
			sumsig = sumsig+groupe2/size

			print('Sample',j/freq,'of',size)
			print('In groups of',i,'E=+',epsilon)
			print(i,j,'here')
			sample_arr[(i-1)*size+round(j/freq)-1] = epsilon


# Sum up Sample and Group Contributions     
	sume = sume + groupe
	sume2 = sume2 + groupe2


	sige = np.sqrt(groupe2/size)
	sumsig = sumsig + groupe2/size

	print('Group ',i,'of ',ngroup)
	print('Eigenvalue = +',groupe,'+-',sige)
	group_arr[i-1] = [groupe,sige]

	
	
#   Perform Observations on U
	avge = sume/(i*size)
	sige1 = np.sqrt((sume2/(i*size)-avge**2)/(i*size))
	sige2 = np.sqrt(sumsig/i**2)
	if (s>0.1):
	    U = avge+e2/s + e2/a0
	else:
	    U = 0
	print('The Simulated Born-OppenHeimer Potential is: ',U)
	    
	



########################################################################################
#                                   Visualisation
# Create 2x2 sub plots
gs = gridspec.GridSpec(2, 2)
Methods = ['null','Variational Monte Carlo','Path Integral Monte Carlo']
pl.figure()
pl.suptitle('Results of the H2 Quantum Molecule by '+Methods[method])
ax = pl.subplot(gs[0, 0]) # row 0, col 0
ax.title.set_text('Evolution of Electronic Eigenvalue of  with Group')
pl.plot(group_arr[:,0])

ax = pl.subplot(gs[0, 1]) # row 0, col 1
ax.title.set_text('Evolution of Intermolecular Potential with Group')
pl.plot(group_arr[:,1])

ax = pl.subplot(gs[1, :]) # row 1, span all columns
ax.title.set_text('Evolution of epsilon or Local Variational Energy with Sample')
pl.plot(sample_arr)

pl.show()
########################################################################################
#                                      Output
filenames = ['Groupwise Data using '+Methods[method]+'.csv','Samplewise Data using '+Methods[method]+'.csv']
np.savetxt(filenames[0], group_arr, delimiter=",", header="Electronic Eigenvalue,Intermolecular Potential",fmt="%i", comments='')
np.savetxt(filenames[1], sample_arr, delimiter=",", header="Local Variational Energy",fmt="%i", comments='')

########################################################################################
#                        AUTHOR: VEERENDRA HARSHAL BUDHI
########################################################################################
