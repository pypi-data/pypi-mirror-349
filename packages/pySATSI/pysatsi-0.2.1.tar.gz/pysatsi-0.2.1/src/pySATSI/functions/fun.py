'''
Functions for use in pySATSI.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''
# External libraries
import numpy as np
import pandas as pd

def az_diff_360(az1,az2):
	'''
	Given two azimuths (0-360), calculates the azimuthal difference between them.
	'''
	_az1=np.min([az1,az2],axis=0)
	_az2=np.max([az1,az2],axis=0)
	tmp_az1=_az2-_az1
	tmp_az2=np.abs(_az2-(_az1+360))
	return np.min([tmp_az1,tmp_az2],axis=0)

def az_diff_180(az1,az2,signed=False):
	'''
	Calculates the difference between two azimuths considering 0/180 edges.
	If signed==True, the sign between az2 and az1 will be preserved with + values = clockwise rotation
	'''
	az1=az1 % 180
	az2=az2 % 180
	if signed==False:
		diff_1=180-np.abs(np.abs(az1-az2)-180)
		diff_2=180-np.abs(np.abs(az1+180-az2)-180)
		difference=np.min((diff_1,diff_2),axis=0)
	else:
		difference = (az2-az1)%180
		# Convert to clockwise difference
		if difference>90:
			difference-=180
	return difference

def aux_plane_ddir(ddir, dip, rake):
	'''
	Converts the aux plane considering the dip direction, dip, and rake angles.

	Args:
		ddir: Dip direction in degrees (float).
		dip: Dip angle in degrees (float).
		rake: Rake angle in degrees (float).

	Returns:
		ddir2: Output array for dip direction
		dip2: Output array for dip angle
		rake2: Output array for rake angle
	'''

	rake[rake==-180]=180

	z=np.radians(ddir)
	dip[dip==90]=89.99999
	z2=np.radians(dip)
	z3=np.radians(rake)

	# Slick vector in plane 1
	s1=-np.cos(z3)*np.cos(z)-np.sin(z3)*np.sin(z)*np.cos(z2)
	s2=np.cos(z3)*np.sin(z)-np.sin(z3)*np.cos(z)*np.cos(z2)
	s3=np.sin(z3)*np.sin(z2)

	# Normal vector to plane 1
	n1=np.sin(z)*np.sin(z2)
	n2=np.cos(z)*np.sin(z2)
	n3=np.cos(z2)

	# Strike vector of plane 2
	h1=-s2
	h2=s1

	z,z2=find_strike_dip(s2,s1,s3)

	z+=90
	ddir2=z
	ddir2[ddir2<0]+=360
	ddir2[ddir2>=360]-=360
	dip2=z2

	z=h1*n1+h2*n2
	z/=np.sqrt(h1**2+h2**2)
	z=np.arccos(z)
	rake2=z
	rake2[s3<0]*=-1
	rake2=np.degrees(rake2)

	tmp_ind=np.where(dip2<0)[0]
	dip2[tmp_ind]*=-1
	ddir2[tmp_ind]+=180
	rake2[tmp_ind]*=-1

	tmp_ind=np.where(dip2>90)[0]
	dip2[tmp_ind]=180-dip2[tmp_ind]
	ddir2[tmp_ind]+=180
	rake2[tmp_ind]*=-1

	ddir2[ddir2>360]-=360
	ddir2[ddir2<0]+=360

	rake2[rake2>360]-=360
	rake2[rake2<0]+=360

	return ddir2,dip2,rake2

def find_strike_dip(n_in, e_in, u_in):
	'''
	Calculates strike and dip angles from a plane's normal vector.

	Args:
		n: North component of normal vector (float).
		e: East component of normal vector (float).
		u: Up component of normal vector (float).

	Returns:
		(strike, dip) in degrees (north of east, dip).
	'''

	n=n_in.copy()
	e=e_in.copy()
	u=u_in.copy()

	# Ensure positive normal vector components
	negu_flag=u<0
	n[negu_flag]*=-1
	e[negu_flag]*=-1
	u[negu_flag]*=-1

	# Strike angle (north of east)
	strike=np.degrees(np.arctan2(e, n))-90

	# Wrap strike angle to 0-360 degrees
	strike%=360

	# Dip angle
	horizontal_magnitude=np.sqrt(n**2 + e**2)
	dip=np.degrees(np.arctan2(horizontal_magnitude, u))

	return strike, dip

def tp2xyz(tr,pl,r):
	'''
	Converts trend (tr) and plunge (pl) to xyz.
	'''
	x=r*np.cos(pl)*np.cos(tr)
	y=r*np.cos(pl)*np.sin(tr)
	z=r*np.sin(pl)
	return x,y,z

def avg_von_mises(azimuth):
	'''
	Computes avg azimuth using von Mises method.
	'''
	rad_azimuth=np.radians(azimuth)
	avg_azimuth=np.degrees(np.arctan(np.sum(np.sin(rad_azimuth))/np.sum(np.cos(rad_azimuth))))
	return avg_azimuth

def calc_shmax_uncert(boot_stress_df,stress_df,p_dict):
	'''
	Calculates SHmax given a dataframe containing the azimuth and plunge
	for S1,S2,S3 and the corresponding min/max values.
	'''
	# If no bootstrapping was done, no uncertainties need to be calculated
	if boot_stress_df['boot'].max()==0:
		shape_ratio=1-stress_df['phi'].values.astype(float)
		stress_df['shmax']=calc_shmax(stress_df[['az1','az2','az3']].values,
								stress_df[['pl1','pl2','pl3']].values,
								shape_ratio)
	else: # Calculates uncertainties
		shape_ratio=1-boot_stress_df['phi'].values.astype(float)
		boot_stress_df['shmax']=calc_shmax(boot_stress_df[['az1','az2','az3']].values,
								boot_stress_df[['pl1','pl2','pl3']].values,
								shape_ratio)
		group_boot_stress_df=boot_stress_df.groupby(by='cluster_id')

		for cluster_x in range(stress_df.shape[0]):
			# Computes avg Shmax
			shmax_azimuth=group_boot_stress_df.get_group(stress_df.loc[cluster_x,'cluster_id'])['shmax'].values
			avg_shmax_azimuth=avg_von_mises(shmax_azimuth)
			stress_df.loc[cluster_x,'shmax']=avg_shmax_azimuth

			# Determine the uncertainty
			n_measurements=shmax_azimuth.shape[0]
			j=int(np.floor((n_measurements-1)*((100.-p_dict['confidence'])/100.)))
			diff_mean=az_diff_180(avg_shmax_azimuth,shmax_azimuth)
			shmax_uncert=diff_mean[np.argsort(np.abs(diff_mean))[::-1][j]]
			stress_df.loc[cluster_x,'shmax_uncert']=shmax_uncert

	# Rounds shmax azimuths
	stress_df['shmax']=np.round(stress_df['shmax'],p_dict['angle_precision'])
	if 'shmax_uncert' in stress_df.columns:
		stress_df['shmax_uncert']=np.round(stress_df['shmax_uncert'],p_dict['angle_precision'])

	return stress_df

def calc_shmax(tr,pl,phi):
	'''
	Given trends and plunges of S1, S2, and S3, calculates SHmax azimuths.
	Input:
		tr: trends, array of [n,3]
		pl: plunges, array of [n,3]
		phi: phi, array of [n]
	output:
		tr_shmax: trend of shmax, array of [n]
	'''
	R=1-phi

	# Converts [trend,plunge] to [x,y].
	x,y,_=tp2xyz(np.radians(tr),np.radians(pl),np.ones(tr.shape))

	# Calculates SHmax following Lund & Townend (2007)
	Y=2.0*(x[:,0]*y[:,0]+(1.0-R)*(x[:,1]*y[:,1]))
	X=x[:,0]**2-y[:,0]**2+(1.0-R)*(x[:,1]**2-y[:,1]**2)
	zero_flag=np.abs(X)<1e-8

	# Handle zero denominator case
	alpha=np.where(zero_flag,np.pi/4.0,np.arctan(Y/X)/2.0)
	special_case_1=np.logical_and(zero_flag,np.abs(x[:,1]*y[:,1])<1e-8)
	alpha=np.where(special_case_1&(np.abs(x[:,0]*y[:,0])<1e-8),-999.,alpha)

	# Handle condition where R is close to 1 + s1Ns1E/s2Ns2E
	if ((x[:,1]==0).any()):
		x[x[:,1]==0,1]=1e-8
	if ((y[:,1]==0).any()):
		y[y[:,1]==0,1]=1e-8
	cond_A=np.abs(R-(1.0+x[:,0]*y[:,0]/(x[:,1]*y[:,1])))<1e-8
	alpha=np.where(cond_A&zero_flag,-999.,alpha)

	# Second derivative and min check
	dev2=-2.0*X*np.cos(2.0*alpha)-2.0*Y*np.sin(2.0*alpha)
	alpha=np.where(dev2>0,alpha+np.pi/2.0,alpha)

	# Ensure alpha is between 0 and 2*pi
	alpha=alpha%(2*np.pi)

	# Converts back to deg
	tr_shmax=np.rad2deg(alpha)

	return tr_shmax

def calc_Aphi(stress_df,p_dict):
	'''
	Uses the orientations of the principal stresses and Phi to quantify the Anderson faulting types
	'''
	# Faulting type characterization following Table 3 from Zoback (1992)
	fault_type_n=np.zeros(stress_df.shape[0]);fault_type_n[:]=np.nan
	fault_type_n[(stress_df['pl1']>=52) & (stress_df['pl3']<=35)]=0
	fault_type_n[(stress_df['pl1']>=40) & (stress_df['pl1']<52) & (stress_df['pl3']<=20)]=0
	fault_type_n[(stress_df['pl1']<40) & (stress_df['pl2']>=45) & (stress_df['pl3']<=20)]=1
	fault_type_n[(stress_df['pl1']<=20) & (stress_df['pl2']>=45) & (stress_df['pl3']<40)]=1
	fault_type_n[(stress_df['pl1']<=20) & (stress_df['pl3']>=40) & (stress_df['pl3']<52)]=2
	fault_type_n[(stress_df['pl1']<=35) & (stress_df['pl3']>=52)]=2

	if np.any(np.isnan(fault_type_n)):
		print('\t*Warning: unable to determine the faulting type needed to compute AΦ for {} cluster(s) using the Zoback (1992) fault regime classification.'.format(np.sum(np.isnan(fault_type_n))))

	# Calculate A_phi following Eq 2 from Simpson (1997)
	Aphi=(fault_type_n+0.5)+((-1)**fault_type_n)*(stress_df['phi']-0.5)
	stress_df.insert(loc=1,column='Aphi',value=Aphi)
	stress_df['Aphi']=stress_df['Aphi'].round(p_dict['vector_precision'])
	stress_df.loc[stress_df['Aphi']<0,'Aphi']=np.nan

	return stress_df


def convert_cluster_ind(mech_df,cluster_df,damp_df,p_dict):
	'''
	Checks p_dict['dimension_names'] and then converts it to [cluster_id]
	'''
	if len(damp_df):
		# If cluster_id is in the mech dataframe, it is required in the damp dataframe too
		if ('cluster_id' in mech_df.columns)!=(('cluster_id1' in damp_df.columns) & ('cluster_id2' in damp_df.columns)):
			raise ValueError(('When using cluster_ids, expecting \'cluster_id\' in the mech file and '+\
					 			'\'cluster_id1\' and \'cluster_id2\' in the damp file.'))

	# If no cluster info is available, then put all mechs in one cluster
	if not(mech_df.columns.isin(p_dict['dimension_names']).any()):
		mech_df['cluster_id']=0
		return mech_df,cluster_df,damp_df

	if not('cluster_id' in mech_df.columns):
		# Ensures the mech and damp dataframes have the same dimension columns
		dim_names=np.asarray(p_dict['dimension_names'])
		mech_dim_names=dim_names[np.isin(dim_names,mech_df.columns)]

		# Converts the dim columns to [cluster_id]
		mech_df=mech_df.sort_values(by=list(mech_dim_names)).reset_index(drop=True)
		cluster_df=mech_df[mech_dim_names].drop_duplicates().reset_index(drop=True)
		cluster_df['cluster_id']=np.arange(len(cluster_df))
		mech_df=mech_df.merge(cluster_df,on=list(mech_dim_names),how='left')

		# Ensures cluster_id is the first column
		cluster_df.insert(0, 'cluster_id', cluster_df.pop('cluster_id'))
		mech_df.insert(0, 'cluster_id', mech_df.pop('cluster_id'))

		if len(damp_df):
			damp_dim_names1=dim_names[np.isin(np.char.add(dim_names,'1'),damp_df.columns)]
			damp_dim_names2=dim_names[np.isin(np.char.add(dim_names,'2'),damp_df.columns)]
			if not(np.array_equal(damp_dim_names1,damp_dim_names2)):
				raise ValueError('Damp file contains unmatching dimension column names.\n\t1: {}\n\t2: {}'.format(damp_dim_names1,damp_dim_names2))
			if not(np.array_equal(mech_dim_names,damp_dim_names1)):
				raise ValueError('Mech and damp files contains columns unmatching dimension names.\n\tMechs: {}\n\tDamp: {}'.format(mech_dim_names,damp_dim_names1))

			tmp_names1=list(np.char.add(mech_dim_names,'1'))
			damp_df=damp_df.merge(cluster_df.add_suffix('1'),on=tmp_names1,how='left')
			damp_df=damp_df.drop(columns=tmp_names1)

			tmp_names2=list(np.char.add(mech_dim_names,'2'))
			damp_df=damp_df.merge(cluster_df.add_suffix('2'),on=tmp_names2,how='left')
			damp_df=damp_df.drop(columns=tmp_names2)

			# Ignore any damping relationships for bins with no mechs
			damp_df=damp_df.drop(damp_df[damp_df.isnull().any(axis=1)].index).reset_index(drop=True).astype(int)
			# Sorts r values for each row
			damp_df[:]=np.sort(damp_df.values,axis=1)
	else:
		cluster_df=pd.DataFrame(columns=['cluster_id'])

	return mech_df,cluster_df,damp_df

def merge_stress_cluster_info(stress_df,cluster_df,p_dict):
	'''
	Combines information from the stress and cluster dataframes together
	'''
	if len(cluster_df):
		merge_col_names=cluster_df.columns[
							cluster_df.columns.isin(['cluster_id','mech_count']) |
							cluster_df.columns.isin(p_dict['dimension_names']) |
							cluster_df.columns.str.startswith('lon') |
							cluster_df.columns.str.startswith('lat') |
							cluster_df.columns.str.startswith('time')
						]
		stress_df=stress_df.merge(cluster_df[merge_col_names],on='cluster_id')
		stress_df.insert(0, 'cluster_id', stress_df.pop('cluster_id'))

	return stress_df