'''
Functions used for computing mechanism RMS.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

# External libraries
import numpy as np

def mech_rms(mech_df,cluster_df,p_dict):
	'''
	Computes the mechanism RMS for each cluster
	'''
	cluster_df['mech_rms']=0.

	# Converts strike,dip,rake to radians
	strike_r=np.deg2rad(mech_df['ddir'].values-90)
	dip_r=np.deg2rad(mech_df['dip'].values)
	rake_r=np.deg2rad(mech_df['rake'].values)

	# Gets fault norm and slip vector
	fnorm,slip=vector_from_sdr(strike_r,dip_r,rake_r)

	if not('mech_count' in cluster_df.columns):
		cluster_df=cluster_df.merge(mech_df['cluster_id'].value_counts().rename('mech_count'),on='cluster_id',how='left')

	# Determines which clusters have mechanisms
	consider_cluster_ind=cluster_df[cluster_df['mech_count']>0].index.values

	# Loops over each cluster with mechs, considering the mechanisms from each
	group_mech_df=mech_df.groupby(by='cluster_id')
	for cluster_x in consider_cluster_ind:
		tmp_mech_df=group_mech_df.get_group(cluster_df.loc[cluster_x,'cluster_id'])
		mech_index=tmp_mech_df.index.values

		# Computes the average mechanism
		norm1_avg,norm2_avg=average_mech(fnorm[:,mech_index],slip[:,mech_index])

		# Finds the min angle between the avg mech and mech population
		rota,norm2,slip2=mech_rotation(norm1_avg,fnorm[:,mech_index],norm2_avg,slip[:,mech_index])

		# Computes mechanism RMS
		cluster_df.loc[cluster_x,'mech_rms']=np.sqrt(np.mean(rota**2))

	cluster_df['mech_rms']=cluster_df['mech_rms'].round(p_dict['angle_precision'])

	return cluster_df

def vector_from_sdr(strike_r,dip_r,rake_r):
	'''
	Gets fault normal vector (fnorm) and slip vector (slip) from [strike,dip,rake] (in radians).
	Uses (x,y,z) coordinate system with x=north, y=east, z=down
		Reference:  Aki and Richards, p. 115
	Based on code from HASH (Hardebeck & Shearer, 2002) and SKHASH (Skoumal et al., 2024)
	'''
	fnorm=np.zeros((3,len(strike_r)))
	slip=np.zeros((3,len(strike_r)))

	fnorm[0,:]=-np.sin(dip_r)*np.sin(strike_r)
	fnorm[1,:]=np.sin(dip_r)*np.cos(strike_r)
	fnorm[2,:]=-np.cos(dip_r)
	slip[0,:]=np.cos(rake_r)*np.cos(strike_r)+np.cos(dip_r)*np.sin(rake_r)*np.sin(strike_r)
	slip[1,:]=np.cos(rake_r)*np.sin(strike_r)-np.cos(dip_r)*np.sin(rake_r)*np.cos(strike_r)
	slip[2,:]=-np.sin(rake_r)*np.sin(dip_r)

	return fnorm,slip

def average_mech(norm1in,norm2in):
	'''
	Computes the average mech of the solutions.

	Inputs:
		norm1in: normal to fault plane, array(3,nf)
		norm2in: slip vector, array(3,nf)
	Output:
		norm1_avg: normal to average of plane 1
		norm2_avg: normal to average of plane 2

	Based on code from SKHASH (Skoumal et al., 2024)
	'''
	if norm1in.shape != norm2in.shape:
		raise ValueError('***Error in average_mech: shape of norm1in and norm2in must be the same')
	if len(norm1in.shape)!=2:
		raise ValueError('***Error in average_mech: norm1in and norm2in must each be an array of shape n-by-3')
	if norm1in.shape[0]!=3:
		raise ValueError('***Error in average_mech: norm1in and norm2in must each be an array of shape n-by-3')

	norm1=norm1in.copy()
	norm2=norm2in.copy()

	# If there is only one mechanism, return that mechanism
	if norm1.shape[1]==1:
		return norm1[:,0],norm2[:,0]

	norm1_ref=norm1in[:,0].copy()
	norm2_ref=norm2in[:,0].copy()

	rota,temp1,temp2=mech_rotation(norm1_ref,norm1[:,1:],norm2_ref,norm2[:,1:])

	norm1_avg=np.sum(np.hstack((norm1[:,[0]],temp1)),axis=1)
	norm2_avg=np.sum(np.hstack((norm2[:,[0]],temp2)),axis=1)
	ln_norm1=np.sqrt(np.sum(norm1_avg**2))
	ln_norm2=np.sqrt(np.sum(norm2_avg**2))
	norm1_avg=norm1_avg/ln_norm1
	norm2_avg=norm2_avg/ln_norm2

	# Determine the RMS observed angular difference between the average
	# Normal vectors and the normal vectors of each mechanism
	rota,temp1,temp2=mech_rotation(norm1_avg,norm1,norm2_avg,norm2)
	d11=temp1[0,:]*norm1_avg[0]+temp1[1,:]*norm1_avg[1]+temp1[2,:]*norm1_avg[2]
	d22=temp2[0,:]*norm2_avg[0]+temp2[1,:]*norm2_avg[1]+temp2[2,:]*norm2_avg[2]

	d11[d11>1]=1
	d11[d11<-1]=-1
	d22[d22>1]=1
	d22[d22<-1]=-1

	a11=np.arccos(d11)
	a22=np.arccos(d22)

	avang1=np.sqrt(np.sum(a11**2)/len(a11))
	avang2=np.sqrt(np.sum(a22**2)/len(a22))

	# the average normal vectors may not be exactly orthogonal (although
	# usually they are very close) - find the misfit from orthogonal and
	# adjust the vectors to make them orthogonal - adjust the more poorly
	# constrained plane more
	if (avang1+avang2)>=0.0001:
		maxmisf=0.01
		fract1=avang1/(avang1+avang2)
		for icount in range(100):
			dot1=norm1_avg[0]*norm2_avg[0]+norm1_avg[1]*norm2_avg[1]+norm1_avg[2]*norm2_avg[2]
			misf=90-np.rad2deg(np.arccos(dot1))
			if abs(misf)<=maxmisf:
				break
			else:
				theta1=np.deg2rad(misf*fract1)
				theta2=np.deg2rad(misf*(1-fract1))
				temp=norm1_avg
				norm1_avg=norm1_avg-norm2_avg*np.sin(theta1)
				norm2_avg=norm2_avg-temp*np.sin(theta2)
				ln_norm1=np.sqrt(np.sum(norm1_avg*norm1_avg))
				ln_norm2=np.sqrt(np.sum(norm2_avg*norm2_avg))
				norm1_avg=norm1_avg/ln_norm1
				norm2_avg=norm2_avg/ln_norm2
	return norm1_avg,norm2_avg

def mech_rotation(norm1_in,norm2_in,slip1_in,slip2_in):
	'''
	Finds the minimum rotation angle between two mechanisms.
	Does not assume that the normal and slip vectors are matched.
	Input:
		norm1_in: normal to fault plane 1
		norm2_in: normal to fault plane 2
		slip1_in: slip vector 1
		slip2_in: slip vector 2
	Output:
		rota: rotation angle
		norm2: normal to fault plane, best combination
		slip2: slip vector, best combination

	Based on code from SKHASH (Skoumal et al., 2024)
	'''
	if norm1_in.shape != slip1_in.shape:
		raise ValueError('***Error in mech_rotation: shape of norm1_in and slip1_in must be the same')
	if norm2_in.shape != slip2_in.shape:
		raise ValueError('***Error in mech_rotation: shape of norm2_in and slip2_in must be the same')
	if len(norm1_in.shape)!=1:
		raise ValueError('***Error in mech_rotation: norm1_in and slip1_in must each be an array of length 3')
	if norm1_in.shape[0]!=3:
		raise ValueError('***Error in mech_rotation: norm1_in and slip1_in must each be an array of length 3')
	if len(norm2_in.shape)!=2:
		raise ValueError('***Error in mech_rotation: norm2_in and slip2_in must each be an array of shape 3-by-n')
	if norm2_in.shape[0]!=3:
		raise ValueError('***Error in mech_rotation: norm2_in and slip2_in must each be an array of shape 3-by-n')

	norm1=norm1_in.copy()
	norm2=norm2_in.copy().T
	slip1=slip1_in.copy()
	slip2=slip2_in.copy().T

	num_vect=norm2.shape[0]
	rotemp=np.zeros((num_vect,4))
	for iter_x in range(0,4): # Iteration over the 4 possibilities
		if iter_x<2:
			norm2_temp=norm2.copy()
			slip2_temp=slip2.copy()
		else:
			norm2_temp=slip2.copy()
			slip2_temp=norm2.copy()
		if (iter_x==1) | (iter_x==3):
			norm2_temp=-norm2_temp
			slip2_temp=-slip2_temp

		B1=np.cross(slip1,norm1)*-1
		B2=np.cross(slip2_temp,norm2_temp)*-1

		phi=np.zeros((num_vect,3))
		phi[:,0]=norm1[0]*norm2_temp[:,0]+norm1[1]*norm2_temp[:,1]+norm1[2]*norm2_temp[:,2]
		phi[:,1]=slip1[0]*slip2_temp[:,0]+slip1[1]*slip2_temp[:,1]+slip1[2]*slip2_temp[:,2]
		phi[:,2]=B1[0]*B2[:,0]+B1[1]*B2[:,1]+B1[2]*B2[:,2]
		phi[phi>1]=1
		phi[phi<-1]=-1
		phi=np.arccos(phi)

		phi_flag=(phi<(1e-3))
		# if the mechanisms are very close, rotation = 0. Otherwise, calculate the rotation
		rot_ind=np.where(np.any(~phi_flag,axis=1))[0]

		# if one vector is the same, it is the rotation axis
		tmp_ind=rot_ind[np.where(phi_flag[rot_ind,2])[0]]
		rotemp[tmp_ind,iter_x]=(phi[tmp_ind,0])
		tmp_ind=rot_ind[np.where(phi_flag[rot_ind,0])[0]]
		rotemp[tmp_ind,iter_x]=(phi[tmp_ind,1])
		tmp_ind=rot_ind[np.where(phi_flag[rot_ind,1])[0]]
		rotemp[tmp_ind,iter_x]=(phi[tmp_ind,2])

		# find difference vectors - the rotation axis must be orthogonal to all three vectors
		rot_ind=np.where(np.all(~phi_flag,axis=1))[0]

		if len(rot_ind)==0:
			continue

		n=np.zeros((len(rot_ind),3,3))
		n[:,:,0]=norm1-norm2_temp[rot_ind,:]
		n[:,:,1]=slip1-slip2_temp[rot_ind,:]
		n[:,:,2]=B1-B2[rot_ind,:]
		scale=np.sqrt(n[:,0,:]**2+n[:,1,:]**2+n[:,2,:]**2)
		n=n/scale[:,np.newaxis,:]

		qdot=np.zeros((len(rot_ind),3))
		qdot[:,2]=n[:,0,0]*n[:,0,1]+n[:,1,0]*n[:,1,1]+n[:,2,0]*n[:,2,1]
		qdot[:,1]=n[:,0,0]*n[:,0,2]+n[:,1,0]*n[:,1,2]+n[:,2,0]*n[:,2,2]
		qdot[:,0]=n[:,0,1]*n[:,0,2]+n[:,1,1]*n[:,1,2]+n[:,2,1]*n[:,2,2]

		# use the two largest difference vectors, as long as they aren't orthogonal
		iout=np.zeros(len(rot_ind),dtype=int)-1
		qdot_flag=np.any(qdot>0.9999,axis=1)
		tmp_row=np.where(qdot_flag)[0]
		if len(tmp_row)>0:
			iout[tmp_row]=np.argmax(qdot[tmp_row,:],axis=1)
		tmp_row=np.where(~qdot_flag)[0]
		if len(tmp_row)>0:
			iout[tmp_row]=np.argmin(scale[tmp_row,:],axis=1)

		n1=np.zeros((len(rot_ind),3))
		n2=np.zeros((len(rot_ind),3))
		k=np.ones(len(rot_ind),dtype=bool)
		for j in range(3):
			tmp_ind=np.where(j!=iout)[0]
			tmp_ind_1=tmp_ind[k[tmp_ind]==True]
			tmp_ind_2=tmp_ind[k[tmp_ind]==False]

			if len(tmp_ind_1)>0:
				n1[tmp_ind_1,:]=n[tmp_ind_1,:,j]
				k[tmp_ind_1]=False
			if len(tmp_ind_2)>0:
				n2[tmp_ind_2,:]=n[tmp_ind_2,:,j]

		#  find rotation axis by taking cross product
		R=np.cross(n2,n1)*-1
		scaleR=np.sqrt(np.sum(R**2,axis=1))

		if np.any(scaleR==0):
			tmp_ind=np.where(scaleR==0)[0]
			rotemp[rot_ind[tmp_ind],iter_x]=9999
			rot_ind=np.delete(rot_ind,tmp_ind)
			scaleR=np.delete(scaleR,tmp_ind)
			R=np.delete(R,tmp_ind,axis=0)

		R=R/scaleR[:,np.newaxis]
		theta=np.zeros((len(rot_ind),3))
		theta[:,0]=norm1[0]*R[:,0]+norm1[1]*R[:,1]+norm1[2]*R[:,2]
		theta[:,1]=slip1[0]*R[:,0]+slip1[1]*R[:,1]+slip1[2]*R[:,2]
		theta[:,2]=B1[0]*R[:,0]+B1[1]*R[:,1]+B1[2]*R[:,2]
		theta[theta>1]=1
		theta[theta<-1]=-1
		theta=np.arccos(theta)

		iuse=np.argmin(np.abs(theta-(np.pi/2)),axis=1)
		tmp_ind=np.arange(len(iuse))

		tmp_rotemp=(np.cos(phi[rot_ind,iuse])-np.cos(theta[tmp_ind,iuse])**2)/(np.sin(theta[tmp_ind,iuse])**2)
		tmp_rotemp[tmp_rotemp>1]=1
		tmp_rotemp[tmp_rotemp<-1]=-1
		tmp_rotemp=np.arccos(tmp_rotemp)
		rotemp[rot_ind,iter_x]=tmp_rotemp

	rotemp=np.rad2deg(rotemp)
	rotemp=np.abs(rotemp)
	irot=np.argmin(rotemp,axis=1)

	tmp_ind=np.arange(len(irot))
	rota=rotemp[tmp_ind,irot]

	tmp_ind=np.where(irot>=2)[0]
	qtemp=slip2[tmp_ind,:]
	slip2[tmp_ind,:]=norm2[tmp_ind,:]
	norm2[tmp_ind,:]=qtemp

	tmp_ind=np.where( (irot==1) | (irot==3) )[0]
	norm2[tmp_ind,:]*=-1
	slip2[tmp_ind,:]*=-1

	return rota,norm2.T,slip2.T
