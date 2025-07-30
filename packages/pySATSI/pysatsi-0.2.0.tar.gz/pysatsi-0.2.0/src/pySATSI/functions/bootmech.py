'''
Functions used for bootstrapping and uncertainty computations.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

# Standard libraries
import multiprocessing

# External libraries
import pandas as pd
import numpy as np
import scipy.stats as st
rng=np.random.default_rng(123) # Used to produce reproducable bootstrapped results.

# Local libraries
import functions.stress as stress
import functions.fun as fun
import functions.knee as knee

def compute_boot(mech_df,damp_df,p_dict):
	'''
	nboot: Number of bootstrap iterations to perform.
		For nboot==1 or the first boostrap iteration, it will compute the stresses using the provided nodal planes and events.
		For nboot>1, it will randomize according to the $randomize_events and $randomize_nodalplane options.
	fracplane: Chance the nodal plane is the fault plane. Either a float or an array of floats
	'''

	num_iterations=p_dict['niterations']
	if num_iterations<1:
		num_iterations=1

	for iter_x in range(num_iterations):
		boot_stress_df=[]
		if p_dict['num_cpus']==1: # Runs bootstrapping in serial
			for boot_x in range(p_dict['nboot']):
				select_mech_df=mech_df.copy()
				if boot_x!=0:
					select_mech_df=randomize_mech(select_mech_df,p_dict)
				boot_stress_df.append(stress.slickenside(select_mech_df,damp_df,p_dict['damp_param'],p_dict,boot_x=boot_x,iter_x=iter_x))
		else: # Runs bootstrapping in parallel
			print('\tComputing bootstraps in parallel...')
			pool=multiprocessing.Pool(processes=p_dict['num_cpus'])
			async_results=[]
			for boot_x in range(p_dict['nboot']):
				select_mech_df=mech_df.copy()
				if boot_x!=0:
					select_mech_df=randomize_mech(select_mech_df,p_dict)
				async_results.append(pool.apply_async(stress.slickenside,
							(select_mech_df,damp_df,p_dict['damp_param'],p_dict),dict(boot_x=boot_x,iter_x=iter_x)))
			pool.close()
			pool.join()
			for result in async_results:
				boot_stress_df.append(result.get())

		boot_stress_df=pd.concat(boot_stress_df).reset_index(drop=True)

		# Use fault instability to inform fault plane
		if p_dict['niterations']>0:
			if (iter_x>=(num_iterations-2)) and (p_dict['final_instability']==True):
				instability_weight=1.
				iteration_weight=1.
				damp_df=pd.DataFrame(columns=['cluster_id1','cluster_id2'])
			else:
				instability_weight=p_dict['instability_weight']
				iteration_weight=p_dict['iteration_weight']

			mech_df['instability'],mech_df['aux_instability']=fault_instability(boot_stress_df,mech_df,p_dict)
			Idiff=mech_df['instability'].values**2-mech_df['aux_instability'].values**2
			abs_Idiff=np.abs(Idiff)

			# Determine the fault probability
			old_fault_probability=mech_df['fault_probability'].values
			mech_df['fault_probability']=100*(iteration_weight*
											(((Idiff/(instability_weight*abs_Idiff-instability_weight+1)+1)/2)-old_fault_probability/100) +
											old_fault_probability/100)

			# Checks for convergence
			mean_prob_diff=np.mean(np.abs(mech_df['fault_probability'].values-old_fault_probability))
			print('\t\tMean change of fault probability: {}%'.format(mean_prob_diff.round(2)))
			if mean_prob_diff<p_dict['convergence_threshold']:
				if iter_x<(num_iterations-1):
					print('\tReached the convergence threshold of {}%. Stopping iterations.'.format(p_dict['convergence_threshold']))
					break
			if p_dict['iterative_damping']:
				if iter_x<(num_iterations-1):
					iteration_damp_misfit_df,p_dict['damp_param']=knee.find_damp(mech_df,damp_df,p_dict)
	if p_dict['iterative_damping']:
		return boot_stress_df,iteration_damp_misfit_df
	else:
		return boot_stress_df,None

def randomize_mech(mech_df,p_dict):
	'''
	Randomizes the nodal plane for the mechanisms

	Input:
		mech_df: DataFrame of [ddir, ddir, dip, dip2, rake1, rake2, cluster_id]
		fracplane: Percentage that the nodal plane is the fault plane. Either a float or an array of floats
		randomize_events: Whether the selection of events are randomized, boolean.
		randomize_nodalplane: Whether the selection of nodal planes are randomized, boolean.
	Output:
		select_mech_df: DataFrame containing randomized nodal planes
	'''
	random_mech_df=mech_df.copy()
	nobs=len(random_mech_df)
	if p_dict['randomize_events']: # Randomizes which events are selected
		rand1=rng.choice(nobs,nobs)
		random_mech_df=random_mech_df.copy().loc[rand1,:].reset_index(drop=True)

	# Applies noise and randomizes which nodal plane is the fault plane
	if random_mech_df['fault_plane_uncertainty'].any():
		random_mech_df=mech_noise(random_mech_df)
	elif p_dict['randomize_nodalplane']:
		random_mech_df['ddir2'],random_mech_df['dip2'],random_mech_df['rake2']=fun.aux_plane_ddir(random_mech_df['ddir'].values,random_mech_df['dip'].values,random_mech_df['rake'].values)
		rand2=rng.uniform(size=nobs)*100
		if 'fault_probability' in random_mech_df:
			ind_rand2=np.where(rand2>random_mech_df['fault_probability'])[0]
		else:
			ind_rand2=np.where(rand2>p_dict['fracplane'])[0]
		random_mech_df.loc[ind_rand2,['ddir','dip','rake']]=random_mech_df.loc[ind_rand2,['ddir2','dip2','rake2']].values
		random_mech_df=random_mech_df.drop(columns=['ddir2','dip2','rake2'])

	return random_mech_df


def avguncert_azimuth_plunge(azimuth,plunge,round=1,confidence_thresh=95.):
	'''
	Given azimuths and plunges (in degrees), computes the eigenvectors of the
	covariance matrix and returns the mean azimuth in plunge (in degrees).
	'''

	# Converts plunge,azimuth (degrees) to lon,lat (radians)
	lat=np.radians(90-plunge)
	lon=0
	theta=np.radians(azimuth)

	# Converts lon,lat to xyz
	x=np.cos(lat)*np.cos(lon)
	y=np.cos(lat)*np.sin(lon)
	z=np.sin(lat)

	# Rotate lon,lat coords by theta degrees
	y_2=y*np.cos(theta)+z*np.sin(theta)
	z_2=-y*np.sin(theta)+z*np.cos(theta)
	r=np.sqrt(x**2+y_2**2+z_2**2)
	lat=np.arcsin(z_2/r)
	lon=np.arctan2(y_2,x)

	# Computes the antipodes
	x=np.cos(lat)*np.cos(lon)
	y=np.cos(lat)*np.sin(lon)
	z=np.sin(lat)
	r=np.sqrt(x**2+y**2+z**2)
	lat_antipode=np.arcsin(-z/r)
	lon_antipode=np.arctan2(-y,-x)

	# Concats the antipodes to the lon,lat arrays
	lon,lat=np.hstack([lon,lon_antipode]),np.hstack([lat,lat_antipode])
	xyz=np.zeros((len(lat),3))
	xyz[:,0]=np.cos(lat)*np.cos(lon)
	xyz[:,1]=np.cos(lat)*np.sin(lon)
	xyz[:,2]=np.sin(lat)

	# Computes eigenvectors
	cov=np.cov(xyz.T)
	eigvalues,eigvectors=np.linalg.eigh(cov)
	sort_index=eigvalues.argsort()
	vecs=eigvectors[:,sort_index]
	x,y,z=vecs[:,-1]

	# Calculate azimuth and plunge (in radians)
	azimuth_rads=np.arctan2(z,y)
	r=np.sqrt(x**2+y**2+z**2)
	if r==0:
		plunge_rads=np.arcsin(1)
	else:
		plunge_rads=np.arcsin(x/r)

	# Convert azimuth and plunge to degrees
	mean_plunge=np.degrees(plunge_rads)
	mean_azimuth=np.degrees(azimuth_rads)
	mean_azimuth=90-mean_azimuth
	if mean_azimuth<0:
		mean_azimuth+=360

	# If upwards plunge, get antipode
	if mean_plunge<0:
		mean_plunge*=-1
		mean_azimuth-=180
		if mean_azimuth<0:
			mean_azimuth+=360

	mean_azimuth=np.round(mean_azimuth,round)
	mean_plunge=np.round(mean_plunge,round)

	# Calculate confidence bounds
	n_measurements=len(azimuth)
	j=int(np.floor((n_measurements-1)*((100.-confidence_thresh)/100.)))
	dot_conf=np.dot(xyz[:int(xyz.shape[0]/2)],np.asarray([x,y,z]))
	ind_conf=np.argsort(np.abs(dot_conf))[j]
	conf_azimuth=azimuth[ind_conf]
	conf_plunge=plunge[ind_conf]

	if dot_conf[ind_conf]<0:
		conf_azimuth-=180

	uncert_azimuth=fun.az_diff_180(mean_azimuth,conf_azimuth)
	uncert_plunge=np.abs(mean_plunge-conf_plunge)

	# Round uncertainties
	uncert_azimuth=np.round(uncert_azimuth,round)
	uncert_plunge=np.round(uncert_plunge,round)

	return mean_azimuth,mean_plunge,uncert_azimuth,uncert_plunge

def uncert(boot_stress_df,p_dict):
	'''
	Calculates the average and variability range of the bootstrapped results
	'''
	# Group bootstrapped results by cluster_id
	boot_stress_df=boot_stress_df.sort_values(by=['cluster_id','boot'])

	# If no bootstrapping was done, no uncertainties need to be calculated
	if boot_stress_df['boot'].max()==0:
		boot_uncert_df=boot_stress_df[['cluster_id','phi','az1','pl1','az2','pl2','az3','pl3',]]
	else: # Calculates uncertainties
		group_boot_stress_df=boot_stress_df.groupby(by='cluster_id')
		r_keys=list(group_boot_stress_df.groups.keys())

		# Create empty uncert dataframe
		boot_uncert_df=pd.DataFrame(index=np.arange(len(r_keys)),
								columns=['cluster_id','phi','uncert_phi',
											'az1','az1_uncert','pl1','pl1_uncert',
											'az2','az2_uncert','pl2','pl2_uncert',
											'az3','az3_uncert','pl3','pl3_uncert'],
											dtype=float)
		boot_uncert_df['cluster_id']=r_keys
		boot_uncert_df['cluster_id']=boot_uncert_df['cluster_id'].astype(int)

		# Loop over each cluster
		for r_x,r_key in enumerate(r_keys):
			stress_df=group_boot_stress_df.get_group(r_key)

			# If there's only one record, no need to calculate uncertainties
			if len(stress_df)==1:
				boot_uncert_df.loc[r_x,['phi','az1','pl1','az2','pl2','az3','pl3']]=stress_df.iloc[0][['phi','az1','pl1','az2','pl2','az3','pl3']]
				continue

			# Computes mean azimuth/plunge using the eigenvectors of the covariance matrix
			boot_uncert_df.loc[r_x,['az1','pl1','az1_uncert','pl1_uncert']]=avguncert_azimuth_plunge(
					stress_df['az1'].values,stress_df['pl1'].values,
					round=p_dict['angle_precision'],confidence_thresh=p_dict['confidence'])
			boot_uncert_df.loc[r_x,['az2','pl2','az2_uncert','pl2_uncert']]=avguncert_azimuth_plunge(
					stress_df['az2'].values,stress_df['pl2'].values,
					round=p_dict['angle_precision'],confidence_thresh=p_dict['confidence'])
			boot_uncert_df.loc[r_x,['az3','pl3','az3_uncert','pl3_uncert']]=avguncert_azimuth_plunge(
					stress_df['az3'].values,stress_df['pl3'].values,
					round=p_dict['angle_precision'],confidence_thresh=p_dict['confidence'])

			# Computes phi stats
			boot_uncert_df.loc[r_x,'phi']=np.round(stress_df['phi'].mean(),p_dict['vector_precision'])
			if len(stress_df['phi'].unique())>1:
				tmp_interval=st.t.interval(p_dict['confidence']/100,stress_df.shape[0]-1,loc=boot_uncert_df.loc[r_x,['phi']],scale=st.sem(stress_df['phi'].values))
				boot_uncert_df.loc[r_x,'uncert_phi']=np.round(np.max(np.abs(boot_uncert_df.loc[r_x,'phi']-tmp_interval)),p_dict['vector_precision'])
			else:
				boot_uncert_df.loc[r_x,'uncert_phi']=0.

	return boot_uncert_df

def mech_noise(select_mech_df):
	'''
	Adds random noise to the mechanism solutions
	'''
	noise_mech_df=select_mech_df.copy()
	strike_r=np.radians(noise_mech_df['ddir'].values-90)
	dip_r=np.radians(noise_mech_df['dip'].values)
	rake_r=np.radians(noise_mech_df['rake'].values)

	num_mechs=len(strike_r)

	# Fault normals
	n=np.zeros((num_mechs,3))
	n[:,0]=-np.sin(dip_r)*np.sin(strike_r)
	n[:,1]=np.sin(dip_r)*np.cos(strike_r)
	n[:,2]=-np.cos(dip_r)

	# Slip direction
	u=np.zeros((num_mechs,3))
	u[:,0]=np.cos(rake_r)*np.cos(strike_r) + np.cos(dip_r)*np.sin(rake_r)*np.sin(strike_r)
	u[:,1]=np.cos(rake_r)*np.sin(strike_r) - np.cos(dip_r)*np.sin(rake_r)*np.cos(strike_r)
	u[:,2]=-np.sin(rake_r)*np.sin(dip_r)

	rand2=rng.uniform(size=num_mechs)*100
	if 'fault_probability' in noise_mech_df:
		tmp_bool=rand2<noise_mech_df['fault_probability'].values
	else:
		tmp_bool=rand2<50
	i0_ind=np.where(tmp_bool)[0]
	i1_ind=np.where(~tmp_bool)[0]

	b=np.zeros((len(strike_r),3))
	b[i0_ind]=np.cross(n[i0_ind],u[i0_ind])
	b[i1_ind]=np.cross(n[i1_ind],u[i1_ind])

	fault_plane_uncertainty=noise_mech_df['fault_plane_uncertainty'].values
	if 'aux_plane_uncertainty' in noise_mech_df.columns:
		fault_plane_uncertainty[i1_ind]=noise_mech_df['aux_plane_uncertainty'].values[i1_ind]

	# Random fault normal
	n_deviation_random=np.radians(fault_plane_uncertainty*np.random.randn(num_mechs))
	b_deviation_random=np.radians(fault_plane_uncertainty*np.random.randn(num_mechs))

	# Random noisy azimuth
	n_azimuth_random=np.pi*2*np.random.random(num_mechs)
	b_azimuth_random=np.pi*2*np.random.random(num_mechs)

	# Applies random noise to n
	n_perpendicular=u*np.sin(n_azimuth_random)[:,np.newaxis]+b*np.cos(n_azimuth_random)[:,np.newaxis]
	n_noise_component=n_perpendicular*np.sin(n_deviation_random)[:,np.newaxis]
	n_noisy=n+n_noise_component
	n_noisy=n_noisy/np.linalg.norm(n_noisy,2,axis=1)[:,np.newaxis]

	# Applies random noise to b
	b_perpendicular=n_noisy*np.sin(b_azimuth_random)[:,np.newaxis]+u*np.cos(b_azimuth_random)[:,np.newaxis]
	b_noise_component=b_perpendicular*np.sin(b_deviation_random)[:,np.newaxis]
	b_noisy=b+b_noise_component
	b_noisy=b_noisy/np.linalg.norm(b_noisy,2,axis=1)[:,np.newaxis]

	# Determines noisy slip direction
	u_noisy=np.cross(n_noisy,b_noisy)
	u_noisy*=np.sign(np.sum(u*u_noisy,axis=1))[:,np.newaxis]

	n=n_noisy.copy()
	u=u_noisy.copy()
	n[i1_ind]=u_noisy[i1_ind]
	u[i1_ind]=n_noisy[i1_ind]

	n1=n.copy()
	u1=u.copy()
	n2=u.copy()
	u2=n.copy()

	# Ensures vertical components are negative
	pos_n1_ind=np.where(n1[:,2]>0)[0]
	n1[pos_n1_ind]*=-1
	u1[pos_n1_ind]*=-1
	pos_n2_ind=np.where(n2[:,2]>0)[0]
	n2[pos_n2_ind]*=-1
	u2[pos_n2_ind]*=-1

	# Determine strike, dip, rake of noisy mech
	r_dip=np.arccos(-n1[:,2])
	r_strike=np.arcsin(-n1[:,0]/np.sqrt(n1[:,0]**2+n1[:,1]**2))
	dip=np.degrees(r_dip)
	strike=np.degrees(r_strike)
	rake=np.degrees(np.arcsin(-u1[:,2]/np.sin(r_dip)))

	# Determining quadrants
	n1_quad_ind=np.where(n1[:,1]<0)[0]
	strike[n1_quad_ind]=180-strike[n1_quad_ind]
	cos_rake=u1[:,0]*np.cos(np.radians(strike))+u1[:,1]*np.sin(np.radians(strike))
	u1_quad_ind=np.where(cos_rake<0)[0]
	rake[u1_quad_ind]=180-rake[u1_quad_ind]

	strike[strike<0]+=360
	rake[rake<-180]+=360
	rake[rake>180]-=360

	noise_mech_df['ddir']=(strike+90)%360
	noise_mech_df['dip']=dip
	noise_mech_df['rake']=rake

	return noise_mech_df

def fault_instability(boot_stress_df,mech_df,p_dict):
	'''
	Calculates the fault instability for the primary and auxiliary
	nodal planes following the instability parameter of Vavryčuk (2014).
	Takes the median instability considering the provided friction values.
	'''
	group_mech_df=mech_df.groupby(by='cluster_id')
	group_boot_stress_df=boot_stress_df.groupby(by='cluster_id')
	instability=np.zeros(mech_df.shape[0]);instability[:]=np.nan
	aux_instability=np.zeros(mech_df.shape[0]);aux_instability[:]=np.nan

	for cluster_id in list(group_mech_df.groups.keys()):
		cluster_mech_df=group_mech_df.get_group(cluster_id)
		cluster_boot_stress_df=group_boot_stress_df.get_group(cluster_id)

		ddir=cluster_mech_df['ddir'].values
		dip=cluster_mech_df['dip'].values
		rake=cluster_mech_df['rake'].values

		# Determines aux nodal plane
		aux_ddir,aux_dip,aux_rake=fun.aux_plane_ddir(ddir,dip,rake)

		# Converts ddir,dip to radians
		z=np.radians(ddir)
		dip[dip==90]=89.99999
		z2=np.radians(dip)

		# Converts aux ddir,dip to radians
		aux_z=np.radians(aux_ddir)
		aux_ddir[aux_ddir==90]=89.99999
		aux_z2=np.radians(aux_dip)

		# Normal vector to plane
		normal=np.zeros((len(z),3))
		normal[:,0]=np.sin(z)*np.sin(z2)
		normal[:,1]=np.cos(z)*np.sin(z2)
		normal[:,2]=np.cos(z2)

		# Normal vector to aux plane
		aux_normal=np.zeros((len(aux_z),3))
		aux_normal[:,0]=np.sin(aux_z)*np.sin(aux_z2)
		aux_normal[:,1]=np.cos(aux_z)*np.sin(aux_z2)
		aux_normal[:,2]=np.cos(aux_z2)

		# Determines stress tensor
		tau=np.zeros((len(cluster_boot_stress_df),3,3))
		tau[:,0,0]=cluster_boot_stress_df.loc[:,'st00']
		tau[:,0,1]=cluster_boot_stress_df.loc[:,'st01']
		tau[:,0,2]=cluster_boot_stress_df.loc[:,'st02']
		tau[:,1,1]=cluster_boot_stress_df.loc[:,'st11']
		tau[:,1,2]=cluster_boot_stress_df.loc[:,'st12']
		tau[:,2,2]=cluster_boot_stress_df.loc[:,'st22']
		tau[:,1,0]=tau[:,0,1]
		tau[:,2,0]=tau[:,0,2]
		tau[:,2,1]=tau[:,1,2]
		tau=np.sum(tau,axis=0)
		tau=tau/np.linalg.norm(tau,2)
		tau_rot=tau.copy()
		tau_rot[0,0]=tau[1,1]
		tau_rot[1,1]=tau[0,0]
		tau_rot[0,2]=tau[1,2]*-1
		tau_rot[1,2]=tau[0,2]*-1
		tau_rot[1,0]=tau_rot[0,1]
		tau_rot[2,0]=tau_rot[0,2]
		tau_rot[2,1]=tau_rot[1,2]
		tau=tau_rot.copy()

		lam,vecs=np.linalg.eig(tau)

		# Sort eigenvalues
		sort_ind=lam.argsort()
		lam=lam[sort_ind]
		vecs=vecs[:,sort_ind]

		# Shape ratio
		shape_ratio=(lam[0]-lam[1])/(lam[0]-lam[2])

		normal=normal[:,[1,0,2]]
		normal[:,2]*=-1
		aux_normal=aux_normal[:,[1,0,2]]
		aux_normal[:,2]*=-1

		# Fault and aux plane normals * principal stresses
		n=np.sum(normal[:,:,np.newaxis]*vecs,axis=1)
		aux_n=np.sum(aux_normal[:,:,np.newaxis]*vecs,axis=1)

		# Shear and normal traction along plane (Vavryčuk EQ 17,18)
		tau_shear=np.sqrt(n[:,0]**2+(1-2*shape_ratio)**2*n[:,1]**2.+n[:,2]**2-(n[:,0]**2+(1-2*shape_ratio)*n[:,1]**2-n[:,2]**2)**2)
		tau_normal=(n[:,0]**2+(1-2*shape_ratio)*n[:,1]**2-n[:,2]**2)

		# Shear and normal traction along aux plane (Vavryčuk EQ 17,18)
		aux_tau_shear=np.sqrt(aux_n[:,0]**2+(1-2*shape_ratio)**2*aux_n[:,1]**2.+aux_n[:,2]**2-(aux_n[:,0]**2+(1-2*shape_ratio)*aux_n[:,1]**2-aux_n[:,2]**2)**2)
		aux_tau_normal=(aux_n[:,0]**2+(1-2*shape_ratio)*aux_n[:,1]**2-aux_n[:,2]**2)

		# Computes instability for plane (Vavryčuk EQ 16)
		cluster_instability=(tau_shear[:,np.newaxis]-p_dict['friction']*(tau_normal[:,np.newaxis]-1))/(p_dict['friction']+np.sqrt(1+p_dict['friction']**2))
		cluster_instability=np.median(cluster_instability,axis=1)

		# Computes instability for aux plane (Vavryčuk EQ 16)
		cluster_aux_instability=(aux_tau_shear[:,np.newaxis]-p_dict['friction']*(aux_tau_normal[:,np.newaxis]-1))/(p_dict['friction']+np.sqrt(1+p_dict['friction']**2))
		cluster_aux_instability=np.median(cluster_aux_instability,axis=1)

		instability[cluster_mech_df.index]=cluster_instability
		aux_instability[cluster_mech_df.index]=cluster_aux_instability

	return instability, aux_instability