'''
Functions used to read/write files for pySATSI.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

# Standard libraries
import os
import multiprocessing
import argparse
import importlib.util
from timeit import default_timer as timer

# External libraries
import numpy as np
import pandas as pd

def read_command_line(p_dict):
	'''
	Reads user inputs provided on the command line.
	'''
	parser = argparse.ArgumentParser()
	parser.add_argument('control_file',nargs='?')
	for p_dict_var in p_dict.keys():
		parser.add_argument('--'+p_dict_var)
	args = vars(parser.parse_args())
	for p_dict_var in p_dict.keys():
		if args[p_dict_var] is not None:
			dtype=type(p_dict[p_dict_var])
			if dtype==bool:
				if args[p_dict_var].lower() in ['true','1']:
					p_dict[p_dict_var]=True
				elif args[p_dict_var].lower() in ['false','0']:
					p_dict[p_dict_var]=False
				else:
					raise ValueError(('Expected a boolean for the command-line declared variable \'{}\''+\
						'The provided value ({}) is not a boolean.').format(p_dict_var,args[p_dict_var]))
			else:
				p_dict[p_dict_var]=dtype(args[p_dict_var])
	return p_dict

def read_control_file(p_dict):
	'''
	Reads the user's control file.
	If the control file does not contain a variable, the default value in p_dict is used.
	If the control file contains an unexpected variable, it is ignored after printing a warning message.
	This file should follow the format:
		$var_name
		var_value
		...
	Where "$var_name" is the name of the variable with a "$" as the first non-whitespace character,
	and "var_value" is the value of the variable on the following line.

	User text on all other lines will be ignored, provided the first non-whitespace character on the line is not a "$".
	User text will also be ignored following a space (" ") after "$var_name"
	'''
	if not(os.path.exists(p_dict['control_file'])):
		raise ValueError('Control file ({}) does not exist.'.format(p_dict['control_file']))

	# Reads lines from the control file
	with open(p_dict['control_file']) as f:
		lines=f.read().splitlines()
		lines=[line.strip() for line in lines]

	# Removes any text following a '#'
	for line_x in range(len(lines)):
		if '#' in lines[line_x]:
			lines[line_x]=lines[line_x][:lines[line_x].find('#')].strip()

	# Identifies the variable names and their line numbers
	var_name=[]
	var_line=[]
	value_line=[]
	for line_x,line in enumerate(lines):
		if line: # If not empty
			if line[0]=='$':
				tmp_var_name=line.split()[0][1:]
				tmp_var_name=tmp_var_name.split('#')[0] # In case the user didn't put a space after the variable name.
				if tmp_var_name in p_dict.keys():
					var_name.append(tmp_var_name)
					var_line.append(line_x)
				else:
					raise ValueError('Unknown variable name ({}) in the control file on line {}:\n\t{}'.format(tmp_var_name,line_x,line))
			elif line[0]!='#':
				value_line.append(line_x)

	# Ensures there are not duplicate variables
	var_set=set()
	duplicate_var=[x for x in var_name if x in var_set or var_set.add(x)]
	if duplicate_var:
		raise ValueError('Duplicate variable name in control file: \"{}\"'.format(duplicate_var[0]))

	# Ensures that every value line corresponds with a variable
	corr_bool=np.isin( (np.asarray(value_line)-1),var_line)
	if not(np.all(corr_bool)):
		prob_ind=np.where(corr_bool==False)[0][0]
		raise ValueError('Unable to associate a value (\"{}\") on line {} with a variable in the control file. If this is a variable, start the line with a \'$\'. If this is intended to be ignored, start the line with a \'#\'.'.format(lines[value_line[prob_ind]],value_line[prob_ind]))

	if (var_line[-1]+1)==len(lines):
		raise ValueError('Unable to associate a value with the final variable in the control file.')

	# Determines the variable values that follow the variable name lines
	var_value=[]
	for line_x in var_line:
		tmp_var_value=lines[line_x+1].strip()

		if len(tmp_var_value)==0:
			raise ValueError('No value is provided for the variable on line {} in the control file.'.format(line_x+1))
		if tmp_var_value[0]=='#':
			raise ValueError('Value (\"{}\") on line {} in the control file starts with a \'#\'.'.format(tmp_var_value,line_x+1) )
		if tmp_var_value.isdigit(): # if int
			tmp_var_value=int(tmp_var_value)
		elif tmp_var_value.replace('.','',1).lstrip('-').isdigit(): # if float
			tmp_var_value=float(tmp_var_value)
		elif (tmp_var_value=='True'):
			tmp_var_value=True
		elif (tmp_var_value=='False'): # if bool
			tmp_var_value=False
		elif (',' in tmp_var_value): # list divided by commas
			if '[' in tmp_var_value:
				tmp_var_value=tmp_var_value.replace('[','',1)
			if ']' in tmp_var_value:
				tmp_var_value=tmp_var_value.replace(']','',1)
			tmp_var_value=tmp_var_value.split(',')
			tmp_var_value=[s.strip() for s in tmp_var_value] # Removes any whitespace
		elif (('\'' in tmp_var_value) or ('\"' in tmp_var_value)): # If variables are divided by quotation marks (' or ")
			tmp_var_value=tmp_var_value.replace('\"','\'')
			print(tmp_var_value)
			quote_ind=[i for i, letter in enumerate(tmp_var_value) if letter == '\'']
			if not((len(quote_ind) % 2)==0):
				raise ValueError('Unable to parse the variable line due to an odd number of quotations:\n\t{}'.format(tmp_var_value))
			tmp=[]
			for tmp_x in range(0,len(quote_ind),2):
				tmp.append(tmp_var_value[quote_ind[tmp_x]:quote_ind[tmp_x+1]])
			tmp_var_value=tmp
		var_value.append(tmp_var_value)

	# Assigns the variable values to the dictionary
	for name,value in zip(var_name,var_value):
		p_dict[name]=value

	# Some basic variable type fixing
	p_dict['hspace_values']=np.atleast_1d(p_dict['hspace_values']).astype(float)
	p_dict['damp_values']=np.atleast_1d(p_dict['damp_values']).astype(float)
	p_dict['xspace']=np.atleast_1d(p_dict['xspace']).astype(float)
	p_dict['yspace']=np.atleast_1d(p_dict['yspace']).astype(float)
	p_dict['depth_breaks']=np.atleast_1d(p_dict['depth_breaks']).astype(float)
	if type(p_dict['time_breaks'])!=list:
		p_dict['time_breaks']=list([p_dict['time_breaks']])
	p_dict['time_breaks']=[pd.Timestamp(t) for t in p_dict['time_breaks']]
	p_dict['plots']=np.atleast_1d(p_dict['plots'])

	return p_dict


def qc_params(p_dict):
	'''
	Does various quality control checks on the user parameters
	'''
	# Creates event filepaths
	if not(p_dict['event_outfile']):
		p_dict['event_outfile']=os.path.join(p_dict['project_dir'],'bin_mechs.csv') # binned mechanisms
	if not(p_dict['binloc_outfile']):
		p_dict['binloc_outfile']=os.path.join(p_dict['project_dir'],'bin_locations.csv') # locations of bins
	if not(p_dict['damp_outfile']):
		p_dict['damp_outfile']=os.path.join(p_dict['project_dir'],'damp_pairs.csv') # pairs of neighboring bins for damping
	if not(p_dict['tradeoff_outfile']):
		p_dict['tradeoff_outfile']=os.path.join(p_dict['project_dir'],'damp_tradeoff.csv')

	# Standard outfiles
	if not(p_dict['rawstress_outfile']):
		p_dict['rawstress_outfile']=os.path.join(p_dict['project_dir'],'raw_stress.csv')
	if not(p_dict['stress_outfile']):
		p_dict['stress_outfile']=os.path.join(p_dict['project_dir'],'stress.csv')

	# Requires inputs to be provided
	if not(p_dict['project_dir']):
		raise ValueError('A project directory ($project_dir) is required.')
	if not(p_dict['event_file']):
		raise ValueError('An event file ($event_file) is required.')

	# Ensures the input files exist
	if len(p_dict['event_file']):
		if not(os.path.exists(p_dict['event_file'])):
			raise ValueError('Event input file (event_file) not found: {}'.format(p_dict['event_file']))
	if len(p_dict['damp_file']):
		if not(os.path.exists(p_dict['damp_file'])):
			raise ValueError('Damp input file (damp_file) not found: {}'.format(p_dict['damp_file']))
	if len(p_dict['binloc_file']):
		if not(os.path.exists(p_dict['binloc_file'])):
			raise ValueError('Bin location file (binloc_file) not found: {}'.format(p_dict['binloc_file']))

	# Ensure the cluster file exists if the damp file exists
	if os.path.isfile(p_dict['binloc_file']):
		if not(os.path.isfile(p_dict['damp_outfile'])):
			raise ValueError('When providing a damp file ({}), the bin locations ({}) should also be provided'.format(p_dict['damp_outfile'],p_dict['binloc_file']))

	# Creates output folder(s), if needed
	for outfile in [p_dict['event_outfile'],p_dict['binloc_outfile'],p_dict['damp_outfile']]:
		if os.path.dirname(outfile):
			os.makedirs(os.path.dirname(outfile),exist_ok=True)

	# Ensures damp values are floats
	p_dict['damp_values']=np.asarray(p_dict['damp_values']).astype(float)

	# Ensures damp values are sorted
	if (len(np.unique(p_dict['damp_values']))!=len(p_dict['damp_values'])):
		raise ValueError('Damping values should be unique, but duplicates were found: {}'.format(p_dict['damp_values']))

	# There must be at least one boot
	if p_dict['nboot']<1:
		raise ValueError('There must be at least one iteration. Set nboot>=1.')

	# Determines the number of cores to use
	if p_dict['num_cpus']!=1:
		num_cpus_avail=multiprocessing.cpu_count()-1
		if (p_dict['num_cpus']==0): # Uses all available cores
			p_dict['num_cpus']=num_cpus_avail
		elif (p_dict['num_cpus']>num_cpus_avail): # If the num requested > available cores, use all available
			print('You requested {} cores, but only {} are available. Using all available cores instead.'.format(p_dict['num_cpus'],num_cpus_avail))
			p_dict['num_cpus']=num_cpus_avail

	# If there are five or fewer damp values, raise an error
	if p_dict['do_damping']:
		if len(p_dict['damp_values'])<5:
			raise ValueError('There should be at least 5 $damp_values, but there are currently {} value(s) provided: {}'.format(len(p_dict['damp_values']),p_dict['damp_values']))

	# Ensures depth breaks are increasing
	if len(p_dict['depth_breaks']):
		p_dict['depth_breaks']=np.sort(p_dict['depth_breaks'])

	if (p_dict['rotate_deg']<0) | (p_dict['rotate_deg']>90):
		raise ValueError('Grid rotations ($rotate_deg) should be 0-90°, but the provided value is: {}'.format(p_dict['rotate_deg']))

	if len(p_dict['hspace_values']):
		# If directly providing hspace values, ensures the other horizontal spacing variables are not provided
		for space_name in ['hspace_min','hspace_max','hspace']:
			print(p_dict[space_name])
			if np.isfinite(p_dict[space_name]):
				raise ValueError('When providing horizontal bin sizes ($hspace_values), the horizontal bin size variable (${}) is not necessary.'.format(space_name))
		for space_name in ['xspace','yspace']:
			if len(p_dict[space_name]):
				raise ValueError('When providing horizontal bin sizes ($hspace_values), the horizontal bin size variable (${}) is not necessary.'.format(space_name))

		# Ensures hspace values are a factor of 2 (allowing for skips)
		p_dict['hspace_values']=np.sort(p_dict['hspace_values'])
		if not(np.all((np.log2(p_dict['hspace_values']/p_dict['hspace_values'][0]) % 1)==0)):
			raise ValueError('$hspace_values must increase by a factor of 2')
		p_dict['xspace']=p_dict['hspace_values']
		p_dict['yspace']=p_dict['hspace_values']
		p_dict['hspace_values']=[]
	elif np.isfinite(p_dict['hspace']):
		# If providing a uniform hspace value, ensures the other horizontal spacing variables are not provided
		for space_name in ['hspace_min','hspace_max']:
			if np.isfinite(p_dict[space_name]):
				raise ValueError('When providing a uniform horizontal bin size ($hspace), the horizontal bin size variable (${}) is not necessary.'.format(space_name))
		for space_name in ['xspace','yspace']:
			if len(p_dict[space_name]):
				raise ValueError('When providing horizontal bin sizes ($hspace_values), the horizontal bin size variable (${}) is not necessary.'.format(space_name))

		p_dict['xspace']=np.asarray([p_dict['hspace']])
		p_dict['yspace']=np.asarray([p_dict['hspace']])
		p_dict['hspace']=np.inf
	elif np.isfinite(p_dict['hspace_min']) | np.isfinite(p_dict['hspace_max']):
		if not(np.isfinite(p_dict['hspace_min'])):
			raise ValueError('When providing a minimum horizontal bin size ($hspace_min), the maximum horizontal bin size ($hspace_max) must be provided.'.format(space_name))
		if not(np.isfinite(p_dict['hspace_max'])):
			raise ValueError('When providing a maximum horizontal bin size ($hspace_max), the minimum horizontal bin size ($hspace_min) must be provided.'.format(space_name))
		if (p_dict['hspace_min']<=0) & (p_dict['hspace_max']<=0):
			raise ValueError('Both the minimum ($hspace_min) and maximum ($hspace_max) horizontal bin sizes must be > 0')
		num_spacings=np.round((np.log2(p_dict['hspace_max'])-np.log2(p_dict['hspace_min']))+1,10)
		if (num_spacings).is_integer():
			num_spacings=int(num_spacings)
		else:
			potential_hspace_max=p_dict['hspace_min']*2**(int(np.round(num_spacings))-1)
			raise ValueError('hspace_max ({} km) and hspace_min ({} km) must be related by log2 (e.g., hspace_max={})'.format(p_dict['hspace_max'],p_dict['hspace_min'],potential_hspace_max))
		p_dict['xspace']=p_dict['hspace_min']*2**(np.arange(num_spacings))
		p_dict['yspace']=p_dict['xspace']

	# If multiple xspace and yspace values are being considered, they must have the same values
	if (len(p_dict['xspace'])>1) | (len(p_dict['yspace'])>1):
		if len(p_dict['xspace'])!=len(p_dict['yspace']):
			raise ValueError('$xspace ({}) and $yspace ({}) must be the same length. If you are considering multiple horizontal spacings, consider using the $hspace variable.'.format(p_dict['xspace'],p_dict['yspace']))
		# if len(p_dict['xspace'])>1:
		if not((p_dict['xspace']==p_dict['yspace']).all()):
			raise ValueError('When using multiple xspace ({}) and yspace ({}) values, they must be identical'.format(p_dict['xspace'],p_dict['yspace']))

	# Creates convinence flags to determine if spatial/temporal gridding is needed
	if len(p_dict['xspace']) | len(p_dict['yspace']):
		p_dict['do_horizontal_gridding']=True
	if len(p_dict['depth_breaks']):
		p_dict['do_vertical_gridding']=True
	if len(p_dict['time_breaks'])>0:
		p_dict['do_temporal_gridding']=True

	if p_dict['damp_smoothing']:
		if p_dict['discard_undamped_clusters']:
			print('Because $damp_smoothing==True, all clusters will be damped. Setting $discard_undamped_clusters==False')
			p_dict['discard_undamped_clusters']=False

	# Checks if the cluster type agrees with the expected data types
	if p_dict['cluster_type']=='grid':
		if len(p_dict['hspace_values'])>1:
			raise ValueError('When doing a \'grid\' cluster_type, only one grid spacing can be considered.')
	elif p_dict['cluster_type']=='quadroot':
		if len(p_dict['hspace_values'])<2:
			raise ValueError('Quadroot clustering expects multiple hspace values.')

	# Determine minimum grid interval
	if len(p_dict['checkerboard_type']):
		p_dict['min_grid_spacing']=np.min([p_dict['checkerboard_hspace'],p_dict['hspace_min']])
	else:
		p_dict['min_grid_spacing']=np.min(p_dict['hspace_min'])

	# Ensures friction values are an array of floats
	p_dict['friction']=np.atleast_1d(np.asarray(p_dict['friction'])).astype(float)

	# Ensures plot types are lowercase
	p_dict['plots']=[plot_type.lower() for plot_type in p_dict['plots']]
	# Only plots stereonets if the spacing is the same
	if 'stereonet' in p_dict['plots']:
		if np.isfinite(p_dict['hspace_min']):
			if p_dict['hspace_min']!=p_dict['hspace_max']:
				print('WARNING: Cannot plot stereonets when doing non-unfiform spatial grids.')
				p_dict['plots']=p_dict['plots'][p_dict['plots']!='stereonet']
	# Ensures the plots are a recognized type
	for plot_type in p_dict['plots']:
		if not(plot_type in ['stereonet','shmax','shmax_error','aphi','phi','damp_tradeoff']):
			raise ValueError('Unknown plot type: {}'.format(plot_type))

	if len(p_dict['plots']):
		if (spec := importlib.util.find_spec('matplotlib')) is None:
			raise ImportError('Unable to find the matplotlib module. Either install matplotlib (pip install \'pySATSI[plot]\') or remove the following plot requests: {}'.format(p_dict['plots']))

	return p_dict


def read_mech_file(p_dict):
	'''
	Reads in file containing earthquake focal mechanism

	Must always contain the columns:
		'dip' and 'rake'
	Must always contain either:
		'strike' or 'ddir'
	If considering horizontal event location, must contain the corresponding columns:
		'lat' and/or 'lon' (*or* 'x_km' and/or 'y_km')
	If considering vertical event location, must contain:
		'depth'
	If considering event timing, must contain:
		'time'
	If using pre-determined fault plane probability, must contain:
		'fault_probability'
	If using individual fault plane uncertainties, must contain:
		'fault_plane_uncertainty'
	If using individual aux plane uncertainties, must contain:
		'aux_plane_uncertainty'
	If using pre-clustered mechanisms, must contain:
		'cluster_id' (*or* some combination of 'x', 'y', 'z', 't', 'l')
	If selecting mechanisms based on qualities, must contain at least one of the following:
		'fault_plane_uncertainty', 'aux_plane_uncertainty', 'polarity_misfit', 'prob_mech', 'sta_distribution_ratio'
	'''
	mech_df=pd.read_csv(p_dict['event_file'])

	if 'latitude' in mech_df.columns:
		mech_df=mech_df.rename(columns={'latitude':'lat'})
	elif 'event_lat' in mech_df.columns:
		mech_df=mech_df.rename(columns={'event_lat':'lat'})
	if 'longitude' in mech_df.columns:
		mech_df=mech_df.rename(columns={'longitude':'lon'})
	elif 'event_lon' in mech_df.columns:
		mech_df=mech_df.rename(columns={'event_lon':'lon'})
	if 'event_depth' in mech_df.columns:
		mech_df=mech_df.rename(columns={'event_depth':'depth'})
	elif 'origin_depth_km' in mech_df.columns:
		mech_df=mech_df.rename(columns={'origin_depth_km':'depth'})

	if np.sum(mech_df.columns.isin(['lat']))>1:
		raise ValueError('Multiple latitude columns provided in event_file ({})'.format(p_dict['event_file']))
	if np.sum(mech_df.columns.isin(['lon']))>1:
		raise ValueError('Multiple longitude columns provided in event_file ({})'.format(p_dict['event_file']))
	if np.sum(mech_df.columns.isin(['depth']))>1:
		raise ValueError('Multiple depth columns provided in event_file ({})'.format(p_dict['event_file']))

	if not({'dip','rake'}.issubset(mech_df.columns)):
		raise ValueError('The binned mechanism file (event_outfile) must contain the columns: [cluster_id, dip, rake]')
	if not('ddir' in mech_df.columns):
		if not('strike' in mech_df.columns):
			raise ValueError('The binned mechanism file (event_outfile) must contain either the column [strike] or [ddir]')

	if (not(p_dict['do_horizontal_gridding'])) & (not(p_dict['do_vertical_gridding'])) & (not(p_dict['do_temporal_gridding'])):
		if (not(mech_df.columns.isin(p_dict['dimension_names']).any())):
			p_dict['do_damping']=False

	if (p_dict['mech_uncertainty']>0) and ('fault_plane_uncertainty' in mech_df.columns):
		raise ValueError('When individual fault plane uncertainties (\'fault_plane_uncertainty\' column) are present in the mechanism file, the constant $mech_uncertainty should be 0.')
	if ('aux_plane_uncertainty' in mech_df.columns) and (not('fault_plane_uncertainty' in mech_df.columns)):
		raise ValueError('When the \'aux_plane_uncertainty\' column is present in the mechanism file, the \'fault_plane_uncertainty\' column should be present too.')
	if (p_dict['mech_uncertainty']>0):
		mech_df['fault_plane_uncertainty']=p_dict['mech_uncertainty']
	if not('fault_plane_uncertainty' in	mech_df.columns):
		mech_df['fault_plane_uncertainty']=0

	if not(p_dict['randomize_nodalplane']):
		mech_df['fault_probability']=100
	if not('fault_probability' in mech_df.columns):
		mech_df['fault_probability']=p_dict['fracplane']

	# # If dip direction present, convert to strike
	# if 'ddir' in mech_df.columns:
	# 	mech_df['strike']=mech_df['ddir']-90
	# mech_df['strike']%=360

	# If strike direction present, convert to dip direction
	if 'strike' in mech_df.columns:
		mech_df['ddir']=mech_df['strike']+90
	mech_df['ddir']%=360

	# Ensures ddir, dip, and rake are floats
	mech_df[['ddir','dip','rake']]=mech_df[['ddir','dip','rake']].astype(float)

	# If dip is 0, sets to a small number instead
	mech_df.loc[mech_df['dip']==0,'dip']=0.00001

	if 'x' in mech_df.columns:
		mech_df['x']=mech_df['x'].astype(int)
	if 'y' in mech_df.columns:
		mech_df['y']=mech_df['y'].astype(int)
	if 'z' in mech_df.columns:
		mech_df['z']=mech_df['z'].astype(int)
	if 't' in mech_df.columns:
		mech_df['t']=mech_df['t'].astype(int)

	if 'fault_probability' in mech_df.columns:
		mech_df['fault_probability']=mech_df['fault_probability'].astype(float)

	# Ensures cluster_id is an integer
	if 'cluster_id' in mech_df.columns:
		mech_df['cluster_id']=mech_df['cluster_id'].astype(int)

	# Removes any earthquakes that fall outside of the selected study area
	drop_flag=np.zeros(len(mech_df),dtype=bool)
	if np.isfinite(p_dict['min_lon']) or np.isfinite(p_dict['max_lon']):
		if not('lon' in mech_df.columns):
			raise ValueError('When considering a min or max longitude ($min_lon, $max_lon), there must be a \'lon\' column in the mechanism file ({})'.
					format(p_dict['event_file']))
		drop_flag+=(mech_df['lon'].values<p_dict['min_lon'])+(mech_df['lon'].values>p_dict['max_lon'])
	if np.isfinite(p_dict['min_lat']) or np.isfinite(p_dict['max_lat']):
		if not('lon' in mech_df.columns):
			raise ValueError('When considering a min or max latitude ($min_lat, $max_lat), there must be a \'lat\' column in the mechanism file ({})'.
					format(p_dict['event_file']))
		drop_flag+=(mech_df['lat'].values<p_dict['min_lat'])+(mech_df['lat'].values>p_dict['max_lat'])
	if np.isfinite(p_dict['min_x']) or np.isfinite(p_dict['max_x']):
		if not('x_km' in mech_df.columns):
			raise ValueError('When considering a min or max horizontal x location ($min_x, $max_x), there must be a \'x_km\' column in the mechanism file ({})'.
					format(p_dict['event_file']))
		drop_flag+=(mech_df['x_km'].values<p_dict['min_x'])+(mech_df['x_km'].values>p_dict['max_x'])
	if np.isfinite(p_dict['min_y']) or np.isfinite(p_dict['max_y']):
		if not('y_km' in mech_df.columns):
			raise ValueError('When considering a min or max horizontal y location ($min_y, $max_y), there must be a \'y_km\' column in the mechanism file ({})'.
					format(p_dict['event_file']))
		drop_flag+=(mech_df['y_km'].values<p_dict['min_y'])+(mech_df['y_km'].values>p_dict['max_y'])
	if np.isfinite(p_dict['min_depth']) or np.isfinite(p_dict['max_depth']):
		if not('y_km' in mech_df.columns):
			raise ValueError('When considering a min or max depth ($min_depth, $max_depth), there must be a \'depth\' column in the mechanism file ({})'.
					format(p_dict['event_file']))
		drop_flag+=(mech_df['y_km'].values<p_dict['min_y'])+(mech_df['y_km'].values>p_dict['max_y'])

	if np.any(drop_flag):
		print('\tIgnoring {}/{} ({}%) mechanisms for being outside of the selected area'.
			format(np.sum(drop_flag),len(mech_df),np.round(np.sum(drop_flag)/len(mech_df)*100,1)))
		mech_df=mech_df.drop(mech_df.loc[drop_flag].index).reset_index(drop=True)

	# Drops focal mechanisms that don't meet the specified quality criteria
	if (~np.isnan([p_dict['max_fault_plane_uncertainty'],p_dict['max_polarity_misfit'],
			p_dict['min_prob_mech'],p_dict['min_sta_distribution_ratio']])).any():

		drop_flag=np.zeros(mech_df.shape[0],dtype=bool)
		if ~np.isnan(p_dict['max_fault_plane_uncertainty']):
			if not('fault_plane_uncertainty' in mech_df.columns):
				raise ValueError(('When setting a max fault plane uncertainty (max_fault_plane_uncertainty={}), there should be a \'fault_plane_uncertainty\' '+
					 '(and optionally an \'auxillary_plane_uncertainty\') column in the mechanism file.').format(p_dict['max_fault_plane_uncertainty']))
			# If aux plane uncertainties also provided, compute average fault plane uncertainty
			if 'aux_plane_uncertainty' in mech_df.columns:
				drop_flag[((mech_df['fault_plane_uncertainty']+mech_df['aux_plane_uncertainty'])/2)>p_dict['max_fault_plane_uncertainty']]=True
			else: # Otherwise, use just the fault plane uncertainty
				drop_flag[mech_df['fault_plane_uncertainty']>p_dict['max_fault_plane_uncertainty']]=True

		if ~np.isnan(p_dict['max_polarity_misfit']):
			if not('polarity_misfit' in mech_df.columns):
				raise ValueError(('When setting a max polarity misfit (max_polarity_misfit={}), there should be a \'polarity_misfit\' '+
					 'column in the mechanism file.').format(p_dict['max_polarity_misfit']))
			drop_flag[mech_df['polarity_misfit']>p_dict['max_polarity_misfit']]=True

		if ~np.isnan(p_dict['min_prob_mech']):
			if not('prob_mech' in mech_df.columns):
				raise ValueError(('When setting a min mechanism probability (prob_mech={}), there should be a \'prob_mech\' '+
					 'column in the mechanism file.').format(p_dict['min_prob_mech']))
			drop_flag[mech_df['prob_mech']<p_dict['min_prob_mech']]=True

		if ~np.isnan(p_dict['min_sta_distribution_ratio']):
			if not('sta_distribution_ratio' in mech_df.columns):
				raise ValueError(('When setting a min station distribution ratio (min_sta_distribution_ratio={}), there should be a \'sta_distribution_ratio\' '+
					 'column in the mechanism file.').format(p_dict['min_sta_distribution_ratio']))
			drop_flag[mech_df['sta_distribution_ratio']<p_dict['min_sta_distribution_ratio']]=True

		if drop_flag.any():
			print('\tIgnoring {}/{} ({}%) mechanisms for not meeting the mechanism quality criteria.'.
				format(np.sum(drop_flag),len(mech_df),np.round(np.sum(drop_flag)/len(mech_df)*100,1)))

	if p_dict['do_vertical_gridding']:
		# Ensures depth column exists if considering event depths
		if not('depth' in mech_df.columns):
			raise ValueError('When considering event depths, mechanisms must include a \'depth\' column.')

	if 'time' in mech_df.columns:
		mech_df['time']=pd.to_datetime(mech_df['time'])

	# If considering timing, the 'time' column must be present
	if len(p_dict['time_breaks']) or not(pd.isnull(p_dict['earliest_event_time'])) or not(pd.isnull(p_dict['latest_event_time'])):
		if not('time' in mech_df.columns):
			raise ValueError('When considering event times (with time_breaks, earliest_event_time, or latest_event_time), mechanisms must include a \'time\' column.')

		drop_index=mech_df[(mech_df['time']<p_dict['earliest_event_time']) | (mech_df['time']>p_dict['latest_event_time'])].index
		if len(drop_index):
			print('\tIgnoring {}/{} ({}%) mechanisms for falling outside of the selected time window ({} - {})'.format(\
				len(drop_index),len(mech_df),np.round(len(drop_index)/len(mech_df)*100,1),p_dict['earliest_event_time'],p_dict['latest_event_time']))
			mech_df=mech_df.drop(drop_index).reset_index(drop=True)

	# Selects only the columns of interest
	mech_df=mech_df.filter(['ddir','dip','rake','fault_probability','fault_plane_uncertainty', 'aux_plane_uncertainty',
						 	'lat','lon','x_km','y_km','depth','time','x', 'y', 'z', 't', 'l','cluster_id'])

	if len(mech_df)==0:
		print('There are no mechanisms in selected dataset. Quitting.')
		quit()

	return mech_df,p_dict


def read_damp_file(p_dict):
	'''
	Reads a .csv file containing damping relationships.

	Must contain the columns:
		'cluster_id1', 'cluster_id2'
	'''
	damp_df=pd.read_csv(p_dict['damp_file'])

	# If the cluster_id1 and cluster_id2 columns already exist, return those columns
	if set(['cluster_id1','cluster_id2']).issubset(damp_df.columns):
		damp_df=damp_df[['cluster_id1','cluster_id2']].astype(int)
		return damp_df

	# If individual dimension names are given, read those in
	found_dim_s=[]
	for dim_s in p_dict['dimension_names']:
		if (dim_s+'1') in damp_df.columns:
			if (dim_s+'2') in damp_df.columns:
				found_dim_s.append(dim_s)
			else:
				raise ValueError('In damp_file ({}), dimension {}1 was found but {}2 was missing.'.format(p_dict['damp_file'],dim_s,dim_s))
	if len(found_dim_s):
		use_dim_col=[]
		for dim_s in found_dim_s:
			use_dim_col.append(dim_s+'1')
		for dim_s in found_dim_s:
			use_dim_col.append(dim_s+'2')
		damp_df=damp_df[use_dim_col].astype(int)
		return damp_df

	raise ValueError(('In damp_file ({}), the following column names (with a \'1\' or \'2\' suffix) are acceptable but were not found:'+
					'\n\t\'cluster_id\'\n\t\t- OR -\n\t{}').format(p_dict['damp_file'],p_dict['dimension_names']))

def read_cluster_file(p_dict):
	'''
	Reads file of predetermined cluster locations
	'''
	if len(p_dict['binloc_file']):
		if os.path.exists(p_dict['binloc_file']):
			cluster_df=pd.read_csv(p_dict['binloc_file'])
			return cluster_df
	raise ValueError('The binloc file ({}) is empty'.format(p_dict['binloc_file']))

def write_misfit_file(mech_df,p_dict):
	'''
	Writes file containing the mechanism misfits
	'''
	misfit_mech_df=mech_df.copy()
	misfit_mech_df['strike']=(misfit_mech_df['ddir']-90)%360
	misfit_mech_df[['strike','dip','rake','misfit_angle']]=misfit_mech_df[['strike','dip','rake','misfit_angle']].round(p_dict['angle_precision'])
	if 'fault_probability' in misfit_mech_df.columns:
		misfit_mech_df['fault_probability']=misfit_mech_df['fault_probability'].round(p_dict['angle_precision']) # Using angle precision for %
	misfit_mech_df[['tau_mag']]=misfit_mech_df[['tau_mag']].round(p_dict['vector_precision'])
	misfit_mech_df=misfit_mech_df.filter(np.hstack([['strike','dip','rake','cluster_id'],p_dict['dimension_names'],['misfit_angle','tau_mag','fault_probability']]))
	misfit_mech_df.to_csv(p_dict['event_outfile'],index=False)
	return 0