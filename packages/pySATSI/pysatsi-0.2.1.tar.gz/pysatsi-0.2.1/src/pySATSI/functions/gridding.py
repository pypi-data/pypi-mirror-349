'''
Functions for clustering data.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

# Standard libraries
import itertools
from timeit import default_timer as timer

# External libraries
import numpy as np
import pandas as pd
from sklearn.utils.extmath import weighted_mode
from sklearn.preprocessing import LabelEncoder

# Local libraries
import functions.checkerboard as checkerboard


def grid(mech_df,p_dict):
	'''
	Produces (non)uniform spatial and/or temporal grids.

	Input:
		mech_df: DataFrame with columns: ['cluster_id','strike','dip','rake']
		p_dict: Parameter dictionary
	Output:
		cluster_df: DataFrame with columns ['cluster_id','lon1','lon2','lat1','lat2']
	'''
	if ((not(p_dict['do_temporal_gridding'])) &
		(not(p_dict['do_vertical_gridding'])) &
		(not(p_dict['do_horizontal_gridding'])) &
		(not(mech_df.columns.isin(p_dict['dimension_names']).any()))):

		cluster_df=pd.DataFrame(data={'cluster_id':[0],'mech_count':[len(mech_df)]},dtype=int)
		return mech_df,cluster_df,pd.DataFrame(),p_dict

	flag_deg_to_km=False
	flag_cluster_x=False
	flag_cluster_y=False

	mech_df['cluster_id']=-999
	cluster_col=[]
	if len(p_dict['xspace']):
		flag_cluster_x=True
		mech_df['x']=-1
		cluster_col.append('x')
	if len(p_dict['yspace']):
		flag_cluster_y=True
		mech_df['y']=-1
		cluster_col.append('y')
	if p_dict['do_vertical_gridding']:
		mech_df['z']=-1
		cluster_col.append('z')
	if (len(p_dict['xspace'])>1) | (len(p_dict['yspace'])>1):
		mech_df['l']=-1
		cluster_col.append('l')
	if p_dict['do_temporal_gridding']:
		mech_df['t']=-1
		cluster_col.append('t')

	# Temporally clusters mechanisms
	if p_dict['do_temporal_gridding']:
		num_tbreaks=len(p_dict['time_breaks'])
		if not(pd.api.types.is_datetime64_any_dtype(mech_df['time'])):
			mech_df['time']=pd.to_datetime(mech_df['time'])

		mech_df.loc[mech_df['time']<p_dict['time_breaks'][0],'t']=0
		mech_df.loc[mech_df['time']>=p_dict['time_breaks'][-1],'t']=len(p_dict['time_breaks'])
		for t_x in range(1,len(p_dict['time_breaks'])):
			mech_df.loc[(mech_df['time']>=p_dict['time_breaks'][t_x-1]) &
						(mech_df['time']<p_dict['time_breaks'][t_x]),'t']=t_x

		time_cluster_df=pd.DataFrame(index=np.arange(len(p_dict['time_breaks'])+1),columns=['t','time1','time2'])
		time_cluster_df['time1']=time_cluster_df['time1'].astype('datetime64[ns]')
		time_cluster_df['time2']=time_cluster_df['time2'].astype('datetime64[ns]')
		time_cluster_df['t']=np.arange(time_cluster_df.shape[0])
		time_cluster_df.loc[1:,'time1']=p_dict['time_breaks']
		time_cluster_df.loc[:(time_cluster_df.shape[0]-2),'time2']=p_dict['time_breaks']
		time_cluster_df.loc[0,'time1']=p_dict['earliest_event_time']
		time_cluster_df.loc[time_cluster_df.index[-1],'time2']=p_dict['latest_event_time']

		# Fills empty times with default time values
		time_cluster_df['time1']=time_cluster_df['time1'].fillna(pd.Timestamp('1700-01-01'))
		time_cluster_df['time2']=time_cluster_df['time2'].fillna(pd.Timestamp('2200-01-01'))

	# Vertically clusters mechanisms
	if p_dict['do_vertical_gridding']:
		num_zbreaks=len(p_dict['depth_breaks'])
		mech_df.loc[mech_df['depth']<p_dict['depth_breaks'][0],'z']=0
		mech_df.loc[mech_df['depth']>=p_dict['depth_breaks'][-1],'z']=len(p_dict['depth_breaks'])
		for z_x in range(1,len(p_dict['depth_breaks'])):
			mech_df.loc[(mech_df['depth']>=p_dict['depth_breaks'][z_x-1]) &
						(mech_df['depth']<p_dict['depth_breaks'][z_x]),'t']=z_x

		depth_cluster_df=pd.DataFrame(index=np.arange(len(p_dict['depth_breaks'])+1),columns=['z','depth1','depth2'],dtype='float',data=-999)
		depth_cluster_df['z']=np.arange(depth_cluster_df.shape[0]).astype(int)
		depth_cluster_df.loc[1:,'depth1']=p_dict['depth_breaks']
		depth_cluster_df.loc[:(depth_cluster_df.shape[0]-2),'depth2']=p_dict['depth_breaks']
		depth_cluster_df.loc[0,'depth1']=p_dict['min_depth']
		depth_cluster_df.loc[depth_cluster_df.index[-1],'depth2']=p_dict['max_depth']

	# Horizontally clusters mechanisms
	if p_dict['do_horizontal_gridding']:
		if 'lon' in mech_df.columns:
			if not(np.isfinite(p_dict['min_lon'])):
				p_dict['min_lon']=mech_df['lon'].min()
			if not(np.isfinite(p_dict['max_lon'])):
				p_dict['max_lon']=mech_df['lon'].max()
		if 'lat' in mech_df.columns:
			if not(np.isfinite(p_dict['min_lat'])):
				p_dict['min_lat']=mech_df['lat'].min()
			if not(np.isfinite(p_dict['max_lat'])):
				p_dict['max_lat']=mech_df['lat'].max()
			if not(np.isfinite(p_dict['base_lat'])):
				# If study area is provided, takes the avg lat of the study area
				if np.isfinite([p_dict['min_lat'],p_dict['max_lat']]).all():
					p_dict['base_lat']=np.abs(np.mean([p_dict['min_lat'],p_dict['max_lat']]))
				# Otherwise determine the avg lat of the mechanisms
				elif 'lat' in mech_df.columns:
					p_dict['base_lat']=mech_df['lat'].mean()

		horizontal_tmp_col=[]
		if flag_cluster_x:
			horizontal_tmp_col.append('_xn')
		if flag_cluster_y:
			horizontal_tmp_col.append('_yn')

		# Converts deg to km
		if flag_cluster_x:
			if not('x_km' in mech_df.columns) and ('lon' in mech_df.columns):
				lonmult=111.1*np.cos(np.pi*p_dict['base_lat']/180.0)
				mech_df['x_km']=(mech_df['lon']-p_dict['min_lon'])*lonmult
				flag_deg_to_km=True
		if flag_cluster_y:
			if not('y_km' in mech_df.columns) and ('lat' in mech_df.columns):
				latmult=111.1
				mech_df['y_km']=(mech_df['lat']-p_dict['min_lat'])*latmult
				flag_deg_to_km=True

		if not(p_dict['do_temporal_gridding']):
			num_tbreaks=0
		if not(p_dict['do_vertical_gridding']):
			num_zbreaks=0

		# Rotates points
		if p_dict['rotate_deg']!=0:
			mech_df[['x_km','y_km']]=rotate_points([0,0],mech_df[['x_km','y_km']].values,p_dict['rotate_deg'])

		num_hspace=np.max([len(p_dict['xspace']),len(p_dict['yspace'])])
		if num_hspace==1:
			print('\tHorizontal spacing: {} km'.format(np.max([p_dict['xspace'],p_dict['yspace']])))
		for t_ind in range(num_tbreaks+1):
			for z_ind in range(num_zbreaks+1):
				for h_ind in range(num_hspace):
					print_hspace=0
					if flag_cluster_x:
						xspace=p_dict['xspace'][h_ind]
						print_hspace=xspace
					if flag_cluster_y:
						yspace=p_dict['yspace'][h_ind]
						print_hspace=yspace

					tmp_mech_df=mech_df.loc[(mech_df['cluster_id']<-1)].copy()
					if num_hspace>1:
						print('\tHorizontal {}/{}: [{} km]'.format(h_ind,num_hspace-1,print_hspace))
					if p_dict['do_vertical_gridding']:
						if not(np.isfinite(depth_cluster_df.loc[z_ind,'depth1'])):
							print('\tVertical {}/{}: [<{} km]'.format(z_ind,num_zbreaks,depth_cluster_df.loc[z_ind,'depth2']))
						elif not(np.isfinite(depth_cluster_df.loc[z_ind,'depth2'])):
							print('\tVertical {}/{}: [>{} km]'.format(z_ind,num_zbreaks,depth_cluster_df.loc[z_ind,'depth1']))
						else:
							print('\tVertical {}/{}: [{} - {} km]'.format(z_ind,num_zbreaks,depth_cluster_df.loc[z_ind,'depth1'],depth_cluster_df.loc[z_ind,'depth2']))
						tmp_mech_df=tmp_mech_df.loc[(tmp_mech_df['z']==z_ind)]
					if p_dict['do_temporal_gridding']:
						print('\tTemporal {}/{}: [{} - {}]'.format(t_ind,num_tbreaks,time_cluster_df.loc[t_ind,'time1'],time_cluster_df.loc[t_ind,'time2']))
						tmp_mech_df=tmp_mech_df.loc[(tmp_mech_df['t']==t_ind)]

					# Determines which grid cell the considered events fall into
					if flag_cluster_x:
						tmp_mech_df['_xn']=np.floor((tmp_mech_df['x_km'].values)/(xspace)).astype(int)
					if flag_cluster_y:
						tmp_mech_df['_yn']=np.floor((tmp_mech_df['y_km'].values)/(yspace)).astype(int)

					# Selects only the clusters with >= $minenv
					tmp_mech_df=tmp_mech_df.loc[tmp_mech_df.groupby(horizontal_tmp_col).transform('size').ge(p_dict['minev'])]

					# Records the grid cell each selected earthquake falls into
					if flag_cluster_x:
						mech_df.loc[tmp_mech_df.index,'x']=tmp_mech_df['_xn']
					if flag_cluster_y:
						mech_df.loc[tmp_mech_df.index,'y']=tmp_mech_df['_yn']
					if num_hspace>1:
						mech_df.loc[tmp_mech_df.index,'l']=h_ind

					mech_df.loc[tmp_mech_df.index,'cluster_id']=-1 # Signifies mech is clustered, but no id yet

	rm_index=mech_df[(mech_df.filter(['x','y','z','l','t'])==-1).any(axis=1)].index
	if len(rm_index):
		mech_df=mech_df.drop(rm_index).reset_index(drop=True)
		print('\tDiscarding {}/{} mechanisms ({}%) due to not being in a cluster with at least {} events.'.format(len(rm_index),len(mech_df),np.round(len(rm_index)/len(mech_df)*100,1),p_dict['minev']))

	# Determines cluster ids for each event
	sort_col=list(mech_df.filter(p_dict['dimension_names']).columns)
	mech_df=mech_df.sort_values(sort_col).reset_index(drop=True)
	mech_df['cluster_id']=mech_df.groupby(sort_col).ngroup()

	# Drops any unclustered earthquakes
	tmp_counts_df=mech_df['cluster_id'].value_counts()
	rm_index=tmp_counts_df.loc[tmp_counts_df<p_dict['minev']].index
	if len(rm_index):
		discard_ind=mech_df[mech_df['cluster_id'].isin(rm_index)].index
		print('\tDiscarding {}/{} mechanisms ({}%) due to not being in a cluster with at least {} events.'.format(len(discard_ind),len(mech_df),np.round(len(discard_ind)/len(mech_df)*100,1),p_dict['minev']))
		mech_df=mech_df.drop(discard_ind).reset_index(drop=True)

	if len(mech_df)==0:
		return pd.DataFrame(),pd.DataFrame(),pd.DataFrame(),p_dict

	# Remove unneeded spatial columns
	if flag_deg_to_km:
		mech_df=mech_df.drop(columns=mech_df.filter(['x_km','y_km']))

	# Creates cluster information
	cluster_df=mech_df.filter(np.hstack(['cluster_id',p_dict['dimension_names']])).drop_duplicates(subset=['cluster_id'])
	cluster_df=cluster_df.sort_values(by='cluster_id').reset_index(drop=True)

	if p_dict['do_damping'] and (not(len(p_dict['damp_file']))):
		cluster_df,damp_df=damp_connect(cluster_df,p_dict)
	else:
		damp_df=pd.DataFrame(columns=['cluster_id1','cluster_id2'])
	if len(damp_df)==0:
		if p_dict['do_damping']:
			p_dict['do_damping']=False
			print('\t\tNo damping needed.')

	# Determines the lon coords of the clusters
	if flag_cluster_x:
		if 'x' in cluster_col:
			lonmult=111.1*np.cos(np.pi*p_dict['base_lat']/180.0)
			if 'l' in cluster_col:
				cluster_df['x1']=cluster_df['x']*p_dict['xspace'][cluster_df['l']]
				cluster_df['x2']=(cluster_df['x']+1)*p_dict['xspace'][cluster_df['l']]
			else:
				cluster_df['x1']=cluster_df['x']*p_dict['xspace'][0]
				cluster_df['x2']=(cluster_df['x']+1)*p_dict['xspace'][0]
		elif 'y' in cluster_col:
			cluster_df['lon1']=mech_df['lon'].min()
			cluster_df['lon2']=mech_df['lon'].max()

	# Determines the lat coords of the clusters
	if flag_cluster_y:
		if 'y' in cluster_col:
			latmult=111.1
			if 'l' in cluster_col:
				cluster_df['y1']=cluster_df['y']*p_dict['yspace'][cluster_df['l']]#/latmult+p_dict['min_lat']
				cluster_df['y2']=(cluster_df['y']+1)*p_dict['yspace'][cluster_df['l']]#/latmult+p_dict['min_lat']
			else:
				cluster_df['y1']=cluster_df['y']*p_dict['yspace'][0]
				cluster_df['y2']=(cluster_df['y']+1)*p_dict['yspace'][0]
		elif 'x' in cluster_col:
			cluster_df['lat1']=mech_df['lat'].min()
			cluster_df['lat2']=mech_df['lat'].max()

	# Converts grid x,y coords to lon,lat
	if p_dict['rotate_deg']==0:
		if flag_cluster_x:
			if ('x1' in cluster_df.columns) & ('lon' in mech_df.columns):
				cluster_df[['lon1','lon2']]=cluster_df[['x1','x2']]/lonmult+p_dict['min_lon']
				cluster_df[['lon1','lon2']]=cluster_df[['lon1','lon2']].round(p_dict['coordinate_precision'])
		if flag_cluster_y:
			if ('y1' in cluster_df.columns) & ('lat' in mech_df.columns):
				cluster_df[['lat1','lat2']]=cluster_df[['y1','y2']]/latmult+p_dict['min_lat']
				cluster_df[['lat1','lat2']]=cluster_df[['lat1','lat2']].round(p_dict['coordinate_precision'])
	else:
		# Rotates the grid back
		cluster_df[['x1_r','y1_r']]=rotate_points([0,0],cluster_df[['x1','y1']].values,-p_dict['rotate_deg'])
		cluster_df[['x2_r','y2_r']]=rotate_points([0,0],cluster_df[['x2','y2']].values,-p_dict['rotate_deg'])
		cluster_df[['x3_r','y3_r']]=rotate_points([0,0],cluster_df[['x1','y2']].values,-p_dict['rotate_deg'])
		cluster_df[['x4_r','y4_r']]=rotate_points([0,0],cluster_df[['x2','y1']].values,-p_dict['rotate_deg'])
		cluster_df[['lon1','lon2','lon3','lon4']]=cluster_df[['x1_r','x2_r','x3_r','x4_r']]/lonmult+p_dict['min_lon']
		cluster_df[['lat1','lat2','lat3','lat4']]=cluster_df[['y1_r','y2_r','y3_r','y4_r']]/latmult+p_dict['min_lat']
		cluster_df[['lon1','lat1','lon2','lat2']]=cluster_df[['lon1','lat1','lon2','lat2']].round(p_dict['coordinate_precision'])
		cluster_df[['lon3','lat3','lon4','lat4']]=cluster_df[['lon3','lat3','lon4','lat4']].round(p_dict['coordinate_precision'])

		# Removes unneeded columns
		cluster_df=cluster_df.drop(columns=cluster_df.filter(['x1_r','y1_r','x2_r','y2_r','x3_r','y3_r','x4_r','y4_r']))

	if p_dict['do_vertical_gridding']:
		if 'z' in cluster_col:
			cluster_df=cluster_df.merge(depth_cluster_df,on='z',how='left')

	if p_dict['do_temporal_gridding']:
		if 't' in cluster_col:
			cluster_df=cluster_df.merge(time_cluster_df,on='t',how='left')

	# Ensures all the clustering went appropriately
	if cluster_df.isnull().values.any():
		raise ValueError('Null value(s) present in cluster records.')

	# Counts the number of mechanisms in each cluster
	cluster_df=cluster_df.merge(mech_df['cluster_id'].value_counts().rename('mech_count'),on='cluster_id',how='left')
	cluster_df['mech_count']=cluster_df['mech_count'].fillna(0).astype(int)

	if len(p_dict['checkerboard_type']):
		# Finds the grid interval for the checkerboard
		eq_grid_ind=np.where(p_dict['checkerboard_hspace']==p_dict['xspace'])[0]
		lt_grid_ind=np.where((p_dict['checkerboard_hspace'] % p_dict['xspace'])==0)[0]

		if len(eq_grid_ind):
			grid_ind=eq_grid_ind[0]
		elif len(lt_grid_ind):
			grid_ind=lt_grid_ind[0]
		else:
			raise ValueError('Checkerboard spacing ($checkerboard_hspace={}) must be both >= than and a factor of the horizontal grid spacing ($xspace={})'.format(p_dict['checkerboard_hspace'],p_dict['xspace']))

		if len(eq_grid_ind) | len(lt_grid_ind):
			grid_spacing=int(p_dict['checkerboard_hspace']/p_dict['xspace'][grid_ind])
		else:
			grid_spacing=int(p_dict['xspace'][grid_ind]/p_dict['checkerboard_hspace'])

		min_x=np.min([mech_df['x'].min(),cluster_df['x'].min()])
		min_y=np.min([mech_df['y'].min(),cluster_df['y'].min()])

		# Determines traditional grid Shmax
		if p_dict['checkerboard_type']=='traditional':

			x_grid_flag=(((mech_df['x'].values-min_x) / grid_spacing).astype(int) % 2).astype(bool)
			y_grid_flag=(((mech_df['y'].values-min_y) / grid_spacing).astype(int) % 2).astype(bool)
			grid_flag=(x_grid_flag & ~y_grid_flag) | (~x_grid_flag & y_grid_flag)

			cluster_x_grid_flag=(((cluster_df['x'].values-min_x) / grid_spacing).astype(int) % 2).astype(bool)
			cluster_y_grid_flag=(((cluster_df['y'].values-min_y) / grid_spacing).astype(int) % 2).astype(bool)
			cluster_grid_flag=(cluster_x_grid_flag & ~cluster_y_grid_flag) | (~cluster_x_grid_flag & cluster_y_grid_flag)

			mech_df['synth_shmax']=p_dict['checkerboard_shmax1']
			mech_df.loc[~grid_flag,'synth_shmax']=p_dict['checkerboard_shmax2']

			cluster_df['synth_shmax']=p_dict['checkerboard_shmax1']
			cluster_df.loc[~cluster_grid_flag,'synth_shmax']=p_dict['checkerboard_shmax2']

		# Creates gradient checkerboard
		elif p_dict['checkerboard_type']=='gradient':

			x_grid=((mech_df['x'].values-min_x) / grid_spacing).astype(int)
			y_grid=((mech_df['y'].values-min_y) / grid_spacing).astype(int)
			mech_df['synth_shmax']=p_dict['checkerboard_shmax_start']+p_dict['checkerboard_gradient']*np.max(np.vstack((x_grid,y_grid)),axis=0)

			cluster_x_grid=((cluster_df['x'].values-min_x) / grid_spacing).astype(int)
			cluster_y_grid=((cluster_df['y'].values-min_y) / grid_spacing).astype(int)
			cluster_df['synth_shmax']=p_dict['checkerboard_shmax_start']+p_dict['checkerboard_gradient']*np.max(np.vstack((cluster_x_grid,cluster_y_grid)),axis=0)
		else:
			raise ValueError('Unknown checkerboard_type ({})'.format(p_dict['checkerboard_type']))

		# Determine synthetic rake
		group_mech_df=mech_df.groupby(by='synth_shmax')
		for synth_shmax_value in list(group_mech_df.groups.keys()):
			tmp_df=group_mech_df.get_group(synth_shmax_value)
			tmp_index=tmp_df.index
			tau=checkerboard.determine_stress_tensor(p_dict['shape_ratio'],synth_shmax_value,0,p_dict['theta'])
			mech_df.loc[tmp_index,'rake']=checkerboard.synth_rake(mech_df.loc[tmp_index,'ddir'].values-90,mech_df.loc[tmp_index,'dip'].values,tau)

	if p_dict['discard_undamped_clusters']:
		discard_cluster_index=cluster_df[~(cluster_df['cluster_id'].isin(damp_df.values.ravel()))].index
		if len(discard_cluster_index):
			discard_cluster_id=cluster_df.loc[discard_cluster_index,'cluster_id'].values
			discard_mech_index=mech_df[mech_df['cluster_id'].isin(discard_cluster_id)].index
			print('Discarding {}/{} ({}%) clusters, representing {}/{} ({}%) of the events, for not having any damped relationships.'.format(
				len(discard_cluster_index),len(cluster_df),np.round(len(discard_cluster_index)/len(cluster_df)*100,1),
				len(discard_mech_index),len(mech_df),np.round(len(discard_mech_index)/len(mech_df)*100,1)))
			cluster_df=cluster_df.drop(discard_cluster_index).reset_index(drop=True)
			mech_df=mech_df.drop(discard_mech_index).reset_index(drop=True)

			le = LabelEncoder()
			le.fit(mech_df['cluster_id'].values)
			mech_df['cluster_id']=le.transform(mech_df['cluster_id'].values)
			damp_df['cluster_id1']=le.transform(damp_df['cluster_id1'].values)
			damp_df['cluster_id2']=le.transform(damp_df['cluster_id2'].values)
			cluster_df['cluster_id']=le.transform(cluster_df['cluster_id'].values)

	return mech_df,cluster_df,damp_df,p_dict


def damp_connect(cluster_df,p_dict):
	'''
	Finds adjacent grid cells, handling non-spatiotemporally uniform results.

	For simple cases (i.e. 2D), this could be done faster. It could also be done faster for complex,
	non-uniform cases with indexing, but the logic may be tougher to follow.
	'''
	print('\tDetermining damping relationships...')
	tic_damping=timer()

	cluster_col=cluster_df.filter(p_dict['dimension_names']).columns.values

	flag_uniform=True
	if 'l' in cluster_col:
		flag_uniform=False

	if flag_uniform:
		# Finds DataFrame of all grid cells contained within domain
		cluster_max=(cluster_df[cluster_col].max().values+1)
		cluster_min=(cluster_df[cluster_col].min().values)
		list_index=[np.arange(min_x,max_x) for min_x,max_x in zip(cluster_min,cluster_max)]
		cluster_ind_dim=[(x.shape[0]) for x in list_index]

		all_cell_coord=np.asarray(list(itertools.product(*list_index)))
		all_cell_coord_df=pd.DataFrame(data=all_cell_coord,columns=cluster_col)

		# Relates the cluster_ids, creating new cluster_ids for empty clusters
		all_cell_coord_df=all_cell_coord_df.merge(cluster_df[np.hstack(('cluster_id',cluster_col))],on=list(cluster_col),how='left').fillna(-1)
		all_cell_coord_df=all_cell_coord_df.astype(int)
		unclustered_index=all_cell_coord_df[all_cell_coord_df['cluster_id']<0].index
		num_unclustered=len(unclustered_index)
		max_cluster_id=all_cell_coord_df['cluster_id'].max()
		new_cluster_id=np.arange(max_cluster_id+1,max_cluster_id+1+num_unclustered)
		all_cell_coord_df.loc[unclustered_index,'cluster_id']=new_cluster_id

		# Applies cluster_ids to the corresponding array location
		cluster_ind=np.zeros(cluster_ind_dim,dtype=int)-1
		## Unpacking operator doesn't work in early python versions. Using tuple for now.
		# cluster_ind[*(all_cell_coord_df[cluster_col].values-all_cell_coord_df[cluster_col].min().values).T]=all_cell_coord_df.index
		cluster_ind[tuple((all_cell_coord_df[cluster_col].values-all_cell_coord_df[cluster_col].min().values).T)]=all_cell_coord_df.index
	else:
		if not({'x','y'}.issubset(cluster_df.columns)):
			raise ValueError('Unable to form nonuniform damping relationships without x and y info')

		l_cluster_df=cluster_df.sort_values(by='l',ascending=False).reset_index(drop=True)
		l_cluster_df['dist']=2**(l_cluster_df['l'])
		l_cluster_df['x']*=l_cluster_df['dist']
		l_cluster_df['y']*=l_cluster_df['dist']
		l_cluster_df['x2']=l_cluster_df['x']+l_cluster_df['dist']
		l_cluster_df['y2']=l_cluster_df['y']+l_cluster_df['dist']

		cluster_col2=['x2','y2']
		if 'z' in cluster_col:
			cluster_col2.append('z')
		if 't' in cluster_col:
			cluster_col2.append('t')
		cluster_ind_dim=l_cluster_df[cluster_col2].max().values+1

		dist_mode=int(np.floor(weighted_mode(l_cluster_df['dist'].values,l_cluster_df['dist'].values)[0][0]))
		if not(dist_mode in l_cluster_df['dist']):
			unique_dist=l_cluster_df['dist'].unique()
			dist_mode=unique_dist[np.argmin(np.abs(unique_dist-dist_mode))]

		# Ensures the x,y dimensions are on the interval dist_mode
		cluster_ind_dim[0]=int(np.ceil(cluster_ind_dim[0]/dist_mode)*dist_mode)
		cluster_ind_dim[1]=int(np.ceil(cluster_ind_dim[1]/dist_mode)*dist_mode)

		# Create the base background grid (cluster_ind)
		cluster_ids_dim=cluster_ind_dim.copy()
		cluster_ids_dim[0]/=dist_mode
		cluster_ids_dim[1]/=dist_mode
		max_cluster_id=l_cluster_df['cluster_id'].max()
		max_base_id=cluster_ids_dim[0]*cluster_ids_dim[1]
		base_background_ids=np.arange(max_cluster_id+1,max_cluster_id+1+max_base_id)
		base_background_ids2d=base_background_ids.reshape((cluster_ids_dim[0],cluster_ids_dim[1]),order='F')
		cluster_ind=np.repeat(base_background_ids2d,dist_mode,1).repeat(dist_mode,0)

		# If 3 or 4 dimensions, expand the background grid, increasing the ind each time
		if len(cluster_col2)==3:
			cluster_ind=np.repeat(cluster_ind[:, :, np.newaxis], cluster_ind_dim[2], axis=2)
			for dim_3 in range(1,cluster_ind_dim[2]):
				cluster_ind[:,:,dim_3]+=(max_base_id*(dim_3))
		elif len(cluster_col2)==4:
			cluster_ind=np.repeat(cluster_ind[:, :, np.newaxis], cluster_ind_dim[2], axis=2)
			cluster_ind=np.repeat(cluster_ind[:, :, :, np.newaxis], cluster_ind_dim[3], axis=3)
			for dim_3 in range(0,cluster_ind_dim[2]):
				for dim_4 in range(0,cluster_ind_dim[3]):
					cluster_ind[:,:,dim_3,dim_4]+=(max_base_id*(dim_3*cluster_ind_dim[3]+dim_4))
		elif len(cluster_col2)>4:
			raise ValueError('Unexpected number of dimensions when determining background grid')

		background_cluster_id=np.arange(max_cluster_id+1,cluster_ind.max()+1)
		background_cell_coord_df=pd.DataFrame(columns=np.hstack(('cluster_id',cluster_col)),index=np.arange(len(background_cluster_id)),dtype=int)
		background_cell_coord_df['cluster_id']=background_cluster_id
		background_cell_coord_df['l']=l_cluster_df.loc[l_cluster_df['dist'].eq(dist_mode).idxmax(),'l']
		background_cell_coord_df['x']=np.tile(np.arange(cluster_ids_dim[0]),np.prod(cluster_ids_dim[1:]))
		background_cell_coord_df['y']=np.tile(np.repeat(np.arange(cluster_ids_dim[1]),cluster_ids_dim[0]),np.prod(cluster_ids_dim[2:]))
		if ('z' in cluster_col) & ('t' in cluster_col):
			background_cell_coord_df['z']=np.tile(np.repeat(np.arange(cluster_ids_dim[2]),cluster_ids_dim[0]*cluster_ids_dim[1]),cluster_ids_dim[3])
			background_cell_coord_df['t']=np.repeat(np.arange(cluster_ids_dim[3]),cluster_ids_dim[0]*cluster_ids_dim[1]*cluster_ids_dim[2])
		elif ('z' in cluster_col):
			background_cell_coord_df['z']=np.repeat(np.arange(cluster_ids_dim[2]),cluster_ids_dim[0]*cluster_ids_dim[1])
		elif ('t' in cluster_col):
			background_cell_coord_df['t']=np.repeat(np.arange(cluster_ids_dim[2]),cluster_ids_dim[0]*cluster_ids_dim[1])

		for cluster_i in range(l_cluster_df.shape[0]):
			if not(('t' in cluster_col) | ('z' in cluster_col)):
				cluster_ind[l_cluster_df.loc[cluster_i,'x']:l_cluster_df.loc[cluster_i,'x2'],
							l_cluster_df.loc[cluster_i,'y']:l_cluster_df.loc[cluster_i,'y2']]=l_cluster_df.loc[cluster_i,'cluster_id']
			elif ('t' in cluster_col) & ('z' in cluster_col):
				cluster_ind[l_cluster_df.loc[cluster_i,'x']:l_cluster_df.loc[cluster_i,'x2'],
							l_cluster_df.loc[cluster_i,'y']:l_cluster_df.loc[cluster_i,'y2'],
							l_cluster_df.loc[cluster_i,'z'],
							l_cluster_df.loc[cluster_i,'t']]=l_cluster_df.loc[cluster_i,'cluster_id']
			elif ('t' in cluster_col):
				cluster_ind[l_cluster_df.loc[cluster_i,'x']:l_cluster_df.loc[cluster_i,'x2'],
							l_cluster_df.loc[cluster_i,'y']:l_cluster_df.loc[cluster_i,'y2'],
							l_cluster_df.loc[cluster_i,'t']]=l_cluster_df.loc[cluster_i,'cluster_id']
			elif ('z' in cluster_col):
				cluster_ind[l_cluster_df.loc[cluster_i,'x']:l_cluster_df.loc[cluster_i,'x2'],
							l_cluster_df.loc[cluster_i,'y']:l_cluster_df.loc[cluster_i,'y2'],
							l_cluster_df.loc[cluster_i,'z']]=l_cluster_df.loc[cluster_i,'cluster_id']
			else:
				raise ValueError('Unable to assign cluster_id to nonuniform grid')

		# Merge the clustered and background clusters together
		all_cell_coord_df=pd.concat([cluster_df,background_cell_coord_df]).reset_index(drop=True)

	# Finds adjacent grid cells
	cluster1_ind=[]
	cluster2_ind=[]
	for dim_i in range(cluster_ind.ndim):
		ind1=np.vstack(np.where(cluster_ind.take(np.arange(1,cluster_ind.shape[dim_i]),axis=dim_i) !=
								cluster_ind.take(np.arange(0,cluster_ind.shape[dim_i]-1),axis=dim_i)))
		ind2=ind1.copy()
		ind2[dim_i]+=1
		## Unpacking operator doesn't work in early python versions. Using tuple for now.
		# cluster1_ind.append(cluster_ind[*ind1])
		# cluster2_ind.append(cluster_ind[*ind2])
		cluster1_ind.append(cluster_ind[tuple(ind1)])
		cluster2_ind.append(cluster_ind[tuple(ind2)])
	cluster1_ind=np.hstack(cluster1_ind)
	cluster2_ind=np.hstack(cluster2_ind)

	damp_df=pd.DataFrame(columns=['cluster_id1','cluster_id2'],index=np.arange(cluster1_ind.shape[0]))
	damp_df['cluster_id1']=all_cell_coord_df.loc[cluster1_ind,'cluster_id'].values
	damp_df['cluster_id2']=all_cell_coord_df.loc[cluster2_ind,'cluster_id'].values

	# Removes any clusters that are not present
	drop_index=all_cell_coord_df[~(all_cell_coord_df['cluster_id'].isin(np.unique(damp_df.values)))].index
	all_cell_coord_df=all_cell_coord_df.drop(drop_index).reset_index(drop=True)

	# Sorts by cluster_id, and puts cluster_id as the first column
	all_cell_coord_df=all_cell_coord_df.sort_values(by='cluster_id').reset_index(drop=True)
	damp_df=damp_df.sort_values(by=['cluster_id1','cluster_id2']).reset_index(drop=True)
	tmp_col=all_cell_coord_df.pop('cluster_id')
	all_cell_coord_df.insert(0, tmp_col.name, tmp_col)

	if len(damp_df):
		print('\t\t{} damped relationships created.'.format(len(damp_df)))
		print('\t\tDamp creation runtime: {0:.2f} sec'.format(timer()-tic_damping))
		return all_cell_coord_df,damp_df
	else:
		return cluster_df,damp_df


def rotate_points(origin, points, angle):
	'''
	Rotates points clockwise by a given angle around a given origin.
	'''
	angle_r=np.radians(-angle)
	cos_angle_r=np.cos(angle_r)
	sin_angle_r=np.sin(angle_r)

	rotated_points=np.zeros(points.shape)
	rotated_points[:,0]=origin[0]+cos_angle_r*(points[:,0]-origin[0])-sin_angle_r*(points[:,1]-origin[1])
	rotated_points[:,1]=origin[1]+sin_angle_r*(points[:,0]-origin[0])+cos_angle_r*(points[:,1]-origin[1])

	return rotated_points