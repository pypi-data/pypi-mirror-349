'''
Functions for identifying the knee of the tradeoff curve.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

# Standard libraries
import os

# External libraries
import numpy as np
import pandas as pd
from scipy.signal import argrelextrema

# Local libraries
import functions.stress as stress
import functions.fun as fun
# import functions.plotting as plotting


def find_damp(in_mech_df,damp_df,p_dict):
	'''
	Evaluates damp values and uses the variance vs length tradeoff curve to determine the optimal damp value.
	'''
	mech_df=in_mech_df.copy()
	if 'fault_probability' in mech_df.columns:
		if (mech_df['fault_probability']<50).any():
			use_aux_index=mech_df.loc[mech_df['fault_probability']<50].index
			mech_df.loc[use_aux_index,['ddir','dip','rake']]=np.vstack(fun.aux_plane_ddir(mech_df.loc[use_aux_index,'ddir'].values,mech_df.loc[use_aux_index,'dip'].values,mech_df.loc[use_aux_index,'rake'].values)).T

	G,D,slick=stress.slickenside(mech_df,damp_df,-1,p_dict,case='slick')

	# Computing damp misfit using precomputed G, D, slick
	damp_misfit_df=pd.DataFrame(index=np.arange(len(p_dict['damp_values'])),columns=['e','variance','length'],dtype=float)

	if p_dict['do_iterative']:
		num_damps=len(p_dict['damp_values'])
		damp_int=np.unique([0,int(np.floor(num_damps/3)),int(np.floor(num_damps/2)),int(np.floor(num_damps/3)*2),len(p_dict['damp_values'])-1])
		if len(damp_int)!=5:
			print('Unable to iteratively determine damping parameters. Considering all values.')
			p_dict['do_iterative']=False
		damp_misfit_df.loc[damp_int,'e']=p_dict['damp_values'][damp_int]

	if p_dict['do_iterative']: # Finds the knee using steps of damp values
		damp_int_all=damp_int
		break_next=False
		for R in range(p_dict['damp_iteration_max']):
			print('\tIteration {}'.format(R))
			for damp_x,damp_value in enumerate(p_dict['damp_values'][damp_int]):
				print('\t\t{}/{}: e={}'.format(damp_x,len(damp_int)-1,damp_value))
				damp_misfit_df.loc[damp_int[damp_x],['variance','length']]=stress.slickenside(mech_df,damp_df,damp_value,p_dict,G=G,D=D,slick=slick,case='misfit')
			damp_misfit_df.loc[damp_int,'e']=p_dict['damp_values'][damp_int]

			# Finds the knee
			knee_index=find_knee(damp_misfit_df['length'].dropna().values, damp_misfit_df['variance'].dropna().values)
			if break_next:
				break

			damp_int_all=damp_misfit_df['length'].dropna().index.values
			new_damp_int=[int(np.floor((damp_int_all[knee_index-1]+damp_int_all[knee_index])/2)),
						int(np.ceil((damp_int_all[knee_index]+damp_int_all[knee_index+1])/2))]
			if (new_damp_int[0]==(damp_int_all[knee_index]-1)) & (new_damp_int[1]==(damp_int_all[knee_index]+1)):
				break_next=True
			damp_int=new_damp_int

			if R==(p_dict['damp_iteration_max']-1):
				print('\tMaximum number of iterations reached.')

		damp_misfit_df=damp_misfit_df.dropna().reset_index(drop=True)

	else: # Finds the knee using all damp values
		damp_misfit_df['e']=p_dict['damp_values']
		for damp_x,damp_value in enumerate(p_dict['damp_values']):
			print('\t{}/{}: e={}'.format(damp_x,len(p_dict['damp_values'])-1,damp_value))
			damp_misfit_df.loc[damp_x,['variance','length']]=stress.slickenside(mech_df,damp_df,damp_value,p_dict,G=G,D=D,slick=slick,case='misfit')

	# Corrects any non-increasing lengths
	inc_index=damp_misfit_df[damp_misfit_df['length'].diff()>0].index
	if len(inc_index):
		trial_x=0
		while trial_x<10:
			damp_misfit_df.loc[inc_index-1,'length']=damp_misfit_df.loc[inc_index,'length'].values
			inc_index=damp_misfit_df[damp_misfit_df['length'].diff()>0].index
			if len(inc_index)==0:
				break
			trial_x+=1

	# Finds the knee
	knee_index=find_knee(damp_misfit_df['length'].values, damp_misfit_df['variance'].values)

	if knee_index is None:
		raise ValueError('Unable to find the optimal damp value. Increasing the number and range of damp_values may solve the issue.')
	damp_param=damp_misfit_df.loc[knee_index,'e']

	# Looks at damping parameters surrounding the knee
	if p_dict['num_additional_damp']>0:
		# Ensures there are samples with indicies above & below the knee
		if (knee_index<=(damp_misfit_df.shape[0]-2)) & (knee_index>=1):
			additional_damp_values=np.linspace(damp_misfit_df.loc[knee_index-1,'e'],damp_misfit_df.loc[knee_index+1,'e'],p_dict['num_additional_damp']+2)[1:-1]
			additional_damp_values=np.unique(np.round(additional_damp_values,5))

			# Finds the variance and length for the additional damping parameters
			add_damp_misfit_df=pd.DataFrame(index=np.arange(len(additional_damp_values)),columns=['e','variance','length'],dtype=float)
			add_damp_misfit_df['e']=additional_damp_values
			for damp_x,damp_value in enumerate(additional_damp_values):
				print('\t(additional) {}/{}: e={}'.format(damp_x,len(additional_damp_values)-1,damp_value))
				add_damp_misfit_df.loc[damp_x,['variance','length']]=stress.slickenside(mech_df,damp_df,damp_value,p_dict,G=G,D=D,slick=slick,case='misfit')
			damp_misfit_df=pd.concat([damp_misfit_df,add_damp_misfit_df]).sort_values(by=['e']).reset_index(drop=True)

			# Finds the knee
			knee_index=find_knee(damp_misfit_df['length'].values, damp_misfit_df['variance'].values)
			if knee_index is None:
				raise print('Unable to find the knee with the additional values. Using original damp parameter of e={}'.format(damp_param))
			damp_param=damp_misfit_df.loc[knee_index,'e']

	damp_misfit_df['knee_flag']=False
	damp_misfit_df.loc[knee_index,'knee_flag']=True
	print('\tSelected damp parameter of e={}'.format(damp_param))

	damp_misfit_df.round(6).to_csv(p_dict['tradeoff_outfile'],float_format='%f',index=False)

	return damp_misfit_df,damp_param

def find_knee(x_values,y_values):
	'''
	Given a curve of x_values and y_values, returns the index of the first knee found
	'''
	# Normalize values
	x_normalized=(x_values-np.min(x_values))/(np.max(x_values)-np.min(x_values))
	y_normalized=(y_values-np.min(y_values))/(np.max(y_values)-np.min(y_values))

	# Calculate the diff curve
	y_normalized=y_normalized.max()-y_normalized

	# Normalize diff curve
	y_difference=y_normalized-x_normalized
	x_difference=x_normalized.copy()

	# Find the local max
	maxima_indices=argrelextrema(y_difference, np.greater_equal)[0]
	y_difference_maxima=y_difference[maxima_indices]

	# Find the local min
	minima_indices=argrelextrema(y_difference, np.less_equal)[0]

	# Calculate thresholds
	Tmx=y_difference_maxima-(np.abs(np.diff(x_normalized).mean()))

	# If no max, no knee can be found
	if not maxima_indices.size:
		return None

	max_threshold_index=0
	knee=None

	# Iterate through the diff curve
	for x,_ in enumerate(x_difference):
		if x < maxima_indices[0]:
			continue

		# End of the curve and no knee found
		if x==(len(x_difference)-1):
			break

		# If at a local max, increment the max threshold index
		if (maxima_indices==x).any():
			threshold=Tmx[max_threshold_index]
			threshold_index=x
			max_threshold_index+=1
		# Now for local min
		if (minima_indices==x).any():
			threshold=0.0

		if y_difference[x+1]<threshold:
			knee=x_values[threshold_index]
			break

	# Return knee index
	if knee:
		return threshold_index
	else:
		return None

