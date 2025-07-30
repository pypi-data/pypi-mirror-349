'''
Functions for computing stresses.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

# Standard libraries
from timeit import default_timer as timer

# External libraries
import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.preprocessing import LabelEncoder

def slickenside(select_mech_df,damp_df_in, damp_param, p_dict,
			  G=np.asarray([]),D=np.asarray([]),slick=np.asarray([]),boot_x=-1,iter_x=-1,
			  case='stresstensor'):
	'''
	Computes stress inversions.
	case: 'stresstensor','misfit','mech_misfit', 'slick'
	'''
	stress_tic=timer()

	damp_df=damp_df_in.copy()
	num_clusters=1

	if not(case in ['stresstensor','misfit','mech_misfit','slick']):
		raise ValueError('Unknown case ({})'.format(case))

	if not('cluster_id' in select_mech_df.columns):
		select_mech_df['cluster_id']=0
	else:
		# If not sorted, sort values
		select_mech_df=select_mech_df.sort_values(by='cluster_id').reset_index(drop=True)

		# Encodes mech cluster ids
		le = LabelEncoder()
		if (len(damp_df)>0) and p_dict['damp_smoothing']:
			le.fit(np.hstack((select_mech_df['cluster_id'].values,damp_df['cluster_id1'],damp_df['cluster_id2'])))
		else:
			le.fit(select_mech_df['cluster_id'].values)
		select_mech_df['cluster_id_i']=le.transform(select_mech_df['cluster_id'].values)

		# Encodes damp cluster ids
		if len(damp_df):
			if not(p_dict['damp_smoothing']):
				# Considers only the damp pairs that have mechs
				if {'cluster_id1','cluster_id2'}.issubset(damp_df.columns):
					damp_df=damp_df.loc[damp_df['cluster_id1'].isin(select_mech_df['cluster_id']) & damp_df['cluster_id2'].isin(select_mech_df['cluster_id'])].reset_index(drop=True)

					# Selects unique damps
					damp_df=damp_df.drop_duplicates(subset=['cluster_id1','cluster_id2']).reset_index(drop=True)

			damp_df['cluster_id1_i']=le.transform(damp_df['cluster_id1'].values)
			damp_df['cluster_id2_i']=le.transform(damp_df['cluster_id2'].values)

		# Determines the number of clusters
		if (p_dict['report_empty_clusters']==True) & (len(damp_df)>0):
			num_clusters=np.max([select_mech_df['cluster_id_i'].max(),damp_df[['cluster_id1_i','cluster_id2_i']].max().max()])+1
		else:
			num_clusters=select_mech_df['cluster_id_i'].max()+1

	nobs_t=len(select_mech_df)
	num_damps=damp_df.shape[0]

	if ( (case=='slick') | (G.shape[0]==0) | (D.shape[0]==0) | (slick.shape[0]==0) ):
		# Degrees to radians
		z=np.radians(select_mech_df['ddir'].values)
		z2=np.radians(select_mech_df['dip'].values)
		z3=np.radians(select_mech_df['rake'].values)

		# Normal vector to fault plane
		n1=np.sin(z)*np.sin(z2)
		n2=np.cos(z)*np.sin(z2)
		n3=np.cos(z2)

		# Slickenside vector calculation
		slick=np.zeros((nobs_t*3))
		slick[::3]=-np.cos(z3)*np.cos(z)-np.sin(z3)*np.sin(z)*np.cos(z2)
		slick[1::3]=np.cos(z3)*np.sin(z)-np.sin(z3)*np.cos(z)*np.cos(z2)
		slick[2::3]=np.sin(z3)*np.sin(z2)

		# Creates data kernel matrix
		Gtmp=np.zeros((nobs_t*3,5))
		Gtmp[::3,0]=n1-n1*n1*n1+n1*n3*n3
		Gtmp[::3,1]=n2-2.*n1*n1*n2
		Gtmp[::3,2]=n3-2.*n1*n1*n3
		Gtmp[::3,3]=-n1*n2*n2+n1*n3*n3
		Gtmp[::3,4]=-2.*n1*n2*n3

		Gtmp[1::3,0]=-n2*n1*n1+n2*n3*n3
		Gtmp[1::3,1]=n1-2.*n1*n2*n2
		Gtmp[1::3,2]=-2.*n1*n2*n3
		Gtmp[1::3,3]=n2-n2*n2*n2+n2*n3*n3
		Gtmp[1::3,4]=n3-2.*n2*n2*n3

		Gtmp[2::3,0]=-n3*n1*n1-n3+n3*n3*n3
		Gtmp[2::3,1]=-2.*n1*n2*n3
		Gtmp[2::3,2]=n1-2.*n1*n3*n3
		Gtmp[2::3,3]=-n3*n2*n2-n3+n3*n3*n3
		Gtmp[2::3,4]=n2-2.*n2*n3*n3
		if num_clusters>1:
			# Finds where to split the Gtmp array based on differing cluster_id indicies
			split_inds=np.where(np.diff(select_mech_df['cluster_id_i'].values))[0]+1
			G=sparse.block_diag(np.split(Gtmp,split_inds*3))
		else:
			G=Gtmp

		if num_damps: # Set up inversion with damping
			# Computes damps only between adjacent clusters
			row_ind=np.tile(np.arange(num_damps*5),2)
			col_ind1=[]
			col_ind2=[]
			for damp_x in range(num_damps):
				col_ind1.append(np.arange(damp_df.loc[damp_x,'cluster_id1_i']*5,(damp_df.loc[damp_x,'cluster_id1_i']+1)*5))
				col_ind2.append(np.arange(damp_df.loc[damp_x,'cluster_id2_i']*5,(damp_df.loc[damp_x,'cluster_id2_i']+1)*5))

			col_ind=np.hstack((np.hstack(col_ind1),np.hstack(col_ind2)))
			data=np.hstack((np.ones(num_damps*5),np.ones(num_damps*5)*-1))

			D=sparse.csr_array((data,(row_ind,col_ind)),shape=(5*damp_df.shape[0],5*(1+damp_df[['cluster_id1_i','cluster_id2_i']].max().max())))

			# Pads sparse G matrix to agree with D dimensions. This facilitates damp smoothing across empty cells
			G.resize(G.shape[0],D.shape[1])

	if case=='slick':
		return G,D,slick

	if num_damps: # Set up inversion with damping
		A=(G.T @ G)+(((damp_param**2)*(D.T)) @ ((damp_param**2)*(D)))
		b=G.T @ slick
	else: # Set up inversion with no damping
		A=G.T @ G
		b=G.T @ slick

	# Do inversion
	stress=sparse.linalg.lsmr(A,b)[0]

	if case=='misfit':
		# Computes RMS mechanism misfit
		slick_pre=(G @ stress)
		mech_misfit=np.sum((slick_pre-slick)**2)
		mech_misfit/=G.shape[0]
		mech_misfit=np.sqrt(mech_misfit)

		# Computes stress field model length (variance)
		if num_damps>0:
			stress_len=D @ stress
			mvar=np.sqrt(np.sum(stress_len**2)/(num_damps*5))
		else:
			mvar=0.

		return mech_misfit,mvar

	elif case=='mech_misfit':
		slick_pre=(G @ stress)
		ls1=np.sqrt(np.sum((slick**2).reshape(-1,3),axis=1))
		ls2=np.sqrt(np.sum((slick_pre**2).reshape(-1,3),axis=1))
		ls3=np.sum((slick*slick_pre).reshape(-1,3),axis=1)
		misfit=ls3/(ls1*ls2)
		misfit[misfit>1.]=1.
		misfit[misfit<-1.]=-1.
		misfit_angle=np.degrees(np.arccos(misfit))
		tau_mag=ls2

		return misfit_angle,tau_mag

	elif case=='stresstensor':
		stress_df=pd.DataFrame(index=np.arange(num_clusters),columns=['st00', 'st01', 'st02', 'st11', 'st12', 'st22', 'phi', 'az1', 'pl1', 'az2', 'pl2', 'az3', 'pl3','dev_stress'],dtype=float)
		if num_clusters>1:
			stress_df['cluster_id_i']=np.arange(num_clusters)

		for r in range(num_clusters):
			k=r*5
			strten = np.array([[stress[k], stress[k + 1], stress[k + 2]],
							[stress[k + 1], stress[k + 3], stress[k + 4]],
							[stress[k + 2], stress[k + 4], -(stress[k] + stress[k + 3])]])

			lam,vecs=np.linalg.eig(strten)

			# Sort eigenvalues
			sort_ind=lam.argsort()
			lam=lam[sort_ind]
			vecs=vecs[:,sort_ind]

			dev_stress=lam[2]-lam[0]
			strten/=dev_stress
			stress_df.loc[r,['st00', 'st01', 'st02', 'st11', 'st12', 'st22','dev_stress']]=strten[0,0],strten[0,1],strten[0,2],strten[1,1],strten[1,2],strten[2,2],np.round(dev_stress,p_dict['vector_precision'])

			stress_df.loc[r,'cluster_id_i']=r
			if lam[0]!=lam[2]:
				phi=(lam[1]-lam[2])/(lam[0]-lam[2])
				stress_df.loc[r,'phi']=phi

			# Determine stress directions
			z, z2 = dirplg(vecs[0, 0], vecs[1, 0], vecs[2, 0])
			stress_df.loc[r,'az1']=z
			stress_df.loc[r,'pl1']=z2
			z, z2 = dirplg(vecs[0, 1], vecs[1, 1], vecs[2, 1])
			stress_df.loc[r,'az2']=z
			stress_df.loc[r,'pl2']=z2
			z, z2 = dirplg(vecs[0, 2], vecs[1, 2], vecs[2, 2])
			stress_df.loc[r,'az3']=z
			stress_df.loc[r,'pl3']=z2

		# Converts azimuths to a value between 0-360
		stress_df[['az1','az2','az3']]%=360

		# Rounds results to the specified precision
		stress_df[['az1','pl1','az2','pl2','az3','pl3']]=stress_df[['az1','pl1','az2','pl2','az3','pl3']].round(p_dict['angle_precision'])
		stress_df[['st00','st01','st02','st11','st12','st22','phi']]=stress_df[['st00','st01','st02','st11','st12','st22','phi']].round(p_dict['vector_precision'])

		# Decodes cluster values
		if num_clusters>1:
			stress_df['cluster_id']=le.inverse_transform(stress_df['cluster_id_i'].values)
		else:
			stress_df['cluster_id']=select_mech_df.loc[0,'cluster_id']
		stress_df=stress_df.drop(columns=['cluster_id_i'])

		stress_df['boot']=boot_x

		if p_dict['print_runtime']:
			if iter_x<1:
				print('\tBootstrap: {}/{}\n\t\tStress runtime: {:.2f} sec'.format(boot_x,p_dict['nboot']-1,timer()-stress_tic),flush=True)
			else:
				print('\tIteration: {}/{},\tBootstrap: {}/{}\n\t\tStress runtime: {:.2f} sec'.format(iter_x,p_dict['niterations']-1,boot_x,p_dict['nboot']-1,timer()-stress_tic),flush=True)
		return stress_df

def dirplg(e, n, u):
	'''
	Calculates the direction and plunge of a 3D vector.

	Input:
		e: Easting component of the vector.
		n: Northing component of the vector.
		u: Upward component of the vector.
	Output:
		pdir: Plunge direction (degrees east of north).
		pplg: Plunge amount (degrees from horizontal).
	'''
	# Calculate horizontal magnitude
	z=np.sqrt(e**2 + n**2)

	# Plunge angle (degrees from horizontal)
	pplg=np.degrees(np.arctan2(-u, z))
	if pplg < 0: # Re-orient vector if plunge is negative
		pplg=-pplg
		e=-e
		n=-n

	# Determine azimuth
	pdir=np.degrees(np.arctan2(e, n))

	return pdir,pplg



def misfit_stability(select_mech_df,tau):
	nobs_t=len(select_mech_df)
	num_clusters=len(select_mech_df['cluster_id'].unique())

	select_mech_df=select_mech_df.sort_values(by='cluster_id').reset_index(drop=True)

	# Degrees to radians
	z=np.radians(select_mech_df['ddir'].values)
	z2=np.radians(select_mech_df['dip'].values)
	z3=np.radians(select_mech_df['rake'].values)

	# Normal vector to fault plane
	n1=np.sin(z)*np.sin(z2)
	n2=np.cos(z)*np.sin(z2)
	n3=np.cos(z2)

	# Slickenside vector calculation
	slick=np.zeros((nobs_t*3))
	slick[::3]=-np.cos(z3)*np.cos(z)-np.sin(z3)*np.sin(z)*np.cos(z2)
	slick[1::3]=np.cos(z3)*np.sin(z)-np.sin(z3)*np.cos(z)*np.cos(z2)
	slick[2::3]=np.sin(z3)*np.sin(z2)

	# Creates data kernel matrix
	Gtmp=np.zeros((nobs_t*3,5))
	Gtmp[::3,0]=n1-n1*n1*n1+n1*n3*n3
	Gtmp[::3,1]=n2-2.*n1*n1*n2
	Gtmp[::3,2]=n3-2.*n1*n1*n3
	Gtmp[::3,3]=-n1*n2*n2+n1*n3*n3
	Gtmp[::3,4]=-2.*n1*n2*n3

	Gtmp[1::3,0]=-n2*n1*n1+n2*n3*n3
	Gtmp[1::3,1]=n1-2.*n1*n2*n2
	Gtmp[1::3,2]=-2.*n1*n2*n3
	Gtmp[1::3,3]=n2-n2*n2*n2+n2*n3*n3
	Gtmp[1::3,4]=n3-2.*n2*n2*n3

	Gtmp[2::3,0]=-n3*n1*n1-n3+n3*n3*n3
	Gtmp[2::3,1]=-2.*n1*n2*n3
	Gtmp[2::3,2]=n1-2.*n1*n3*n3
	Gtmp[2::3,3]=-n3*n2*n2-n3+n3*n3*n3
	Gtmp[2::3,4]=n2-2.*n2*n3*n3
	if num_clusters>1:
		# Finds where to split the Gtmp array based on differing cluster_id indicies
		split_inds=np.where(np.diff(select_mech_df['cluster_id'].values))[0]+1
		G=sparse.block_diag(np.split(Gtmp,split_inds*3))
	else:
		G=Gtmp

	slick_pre=(G @ tau)
	ls1=np.sqrt(np.sum((slick**2).reshape(-1,3),axis=1))
	ls2=np.sqrt(np.sum((slick_pre**2).reshape(-1,3),axis=1))
	ls3=np.sum((slick*slick_pre).reshape(-1,3),axis=1)
	misfit=ls3/(ls1*ls2)
	misfit[misfit>1.]=1.
	misfit[misfit<-1.]=-1.
	misfit_angle=np.degrees(np.arccos(misfit))
	tau_mag=ls2

	return misfit_angle,tau_mag