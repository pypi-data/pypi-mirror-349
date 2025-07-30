'''
Functions used for creating synthetic checkerboards.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

# External libraries
import numpy as np

def synth_rake(strike,dip,tau):
	'''
	Computes synthetic rakes given a tau value and catalog of strike,dip.
	'''
	num_events=len(strike)
	strike_radians=np.radians(strike)
	dip_radians=np.radians(dip)
	dip_radians[dip_radians==0]=0.00001

	# Fault normals
	n=np.zeros((num_events,3))
	n[:,0]=-np.sin(dip_radians)*np.sin(strike_radians)
	n[:,1]=np.sin(dip_radians)*np.cos(strike_radians)
	n[:,2]=-np.cos(dip_radians)

	term1=np.zeros((num_events,3))
	term2=np.zeros((num_events,3))
	shear_traction=np.zeros((num_events,3))
	shear_trac_1=np.zeros((num_events))
	shear_trac_2=np.zeros((num_events))
	shear_trac_3=np.zeros((num_events))

	for k in range(0,num_events):
		for i in range(0,3):
			for j in range(0,3):
				term1[k,i]=term1[k,i]+tau[i,j]*n[k,j]
				for l in range(0,3):
					term2[k,i]=term2[k,i]+tau[j,l]*n[k,j]*n[k,l]*n[k,i]
			shear_traction[k,i]=term1[k,i]-term2[k,i]
	shear_traction[(shear_traction==0).all(axis=1),2]=0.0000001

	# Normalization
	for k in range(0,num_events):
		shear_trac_1[k]=shear_traction[k,0]/np.linalg.norm(shear_traction[k,:],ord=2)
		shear_trac_2[k]=shear_traction[k,1]/np.linalg.norm(shear_traction[k,:],ord=2)
		shear_trac_3[k]=shear_traction[k,2]/np.linalg.norm(shear_traction[k,:],ord=2)

	tmp=-shear_trac_3/np.sin(dip_radians)
	tmp[tmp>1]=1
	tmp[tmp<-1]=-1
	synth_rake=np.degrees(np.arcsin(tmp))

	# Determining the quadrant
	cos_rake=shear_trac_1*np.cos(strike_radians)+shear_trac_2*np.sin(strike_radians)
	tmp_flag=cos_rake<0
	synth_rake[tmp_flag]=180-synth_rake[tmp_flag]
	synth_rake[synth_rake<-180]+=360
	synth_rake[synth_rake>180]-=360
	synth_rake=np.round(synth_rake,2)

	return synth_rake

def determine_stress_tensor(shape_ratio,sigma1_az,sigma2_az,theta):
	'''
	Based on code written by Patricia Martínez-Garzón. For more info, see:
		Martínez-Garzón, P., Heidbach, O., & Bohnhoff, M. (2020). Contemporary stress
			and strain field in the Mediterranean from stress inversion of focal mechanisms
			and GPS data. Tectonophysics, 774, 228286.
	'''
	sigma1_az=sigma1_az%360
	sigma2_az=sigma2_az%360

	theta_radians=np.radians(90-theta)
	sigma1_az_radians=np.radians(sigma1_az)
	sigma2_az_radians=np.radians(sigma2_az)

	# Calculate deviatoric stress magnitudes
	sigma_1=-1
	sigma_2=sigma_1*(1-2*shape_ratio)/(1+shape_ratio)
	sigma_3=-sigma_1-sigma_2

	# Normalize
	sigma_dev=sigma_3-sigma_1
	sigma_1=2*sigma_1/sigma_dev
	sigma_2=2*sigma_2/sigma_dev
	sigma_3=2*sigma_3/sigma_dev

	sigma_1=sigma_1-sigma_3
	sigma_2=sigma_2-sigma_3
	sigma_3=0

	# Calculate rotated eigenvectors S1, S2, S3 and deviatoric stress tensor (tau)
	sigma_vector_1=np.zeros((3,1))
	sigma_vector_2=np.zeros((3,1))
	sigma_vector_3=np.zeros((3,1))

	sigma_vector_1[0]=np.sin(theta_radians)*np.cos(sigma1_az_radians)
	sigma_vector_1[1]=np.sin(theta_radians)*np.sin(sigma1_az_radians)
	sigma_vector_1[2]=np.cos(theta_radians)

	sigma_vector_2[0]=-(np.cos(sigma1_az_radians)*np.cos(sigma2_az_radians)*np.cos(theta_radians)+\
					np.sin(sigma1_az_radians)*np.sin(sigma2_az_radians))
	sigma_vector_2[1]=np.cos(sigma1_az_radians)*np.sin(sigma2_az_radians)-\
					np.cos(sigma2_az_radians)*np.cos(theta_radians)*np.sin(sigma1_az_radians)
	sigma_vector_2[2]=np.cos(sigma2_az_radians)*np.sin(theta_radians)

	sigma_vector_3[0]=np.cos(sigma1_az_radians)*np.cos(theta_radians)*np.sin(sigma2_az_radians)-\
					np.cos(sigma2_az_radians)*np.sin(sigma1_az_radians)
	sigma_vector_3[1]=np.cos(sigma1_az_radians)*np.cos(sigma2_az_radians)+\
					np.cos(theta_radians)*np.sin(sigma1_az_radians)*np.sin(sigma2_az_radians)
	sigma_vector_3[2]=-np.sin(sigma2_az_radians)*np.sin(theta_radians)

	tau=sigma_1*sigma_vector_1*sigma_vector_1.T+sigma_2*sigma_vector_2*sigma_vector_2.T+\
		sigma_3*sigma_vector_3*sigma_vector_3.T

	return tau