'''
Default parameters used for pySATSI.

Author: Robert J. Skoumal (rskoumal@usgs.gov)
'''

import numpy as np
import pandas as pd

p_dict={
	# ------- File paths -------
	'control_file':'', # Path to control file
	'event_file':'', # Path to the mechanism file
	'damp_file':'', # Path to pre-determined damp relationships
	'binloc_file':'', # Path to pre-determined bin locations
	'project_dir':'', # The directory the output files will be saved

	# ------- Study area -------
	'min_lon':-np.inf, # Min longitude, deg
	'max_lon':np.inf, # Max longitude, deg
	'min_lat':-np.inf, # Min latitude, deg
	'max_lat':np.inf, # Max latitude, deg
	'min_x':-np.inf, # Min horizontal x location, kilometers
	'min_y':np.inf, # Min horizontal y location, kilometers
	'max_x':-np.inf, # Min horizontal x location, kilometers
	'max_y':np.inf, # Min horizontal y location, kilometers
	'min_depth':-np.inf, # Min vertical z location, kilometers
	'max_depth':np.inf, # Min vertical z location, kilometers
	'base_lat':np.nan, # Reference latitude for coordinate conversion
	'earliest_event_time':pd.Timestamp(''), # Earliest event time considered
	'latest_event_time':pd.Timestamp(''), # Earliest event time considered

	# ------- Clustering -------
	'minev':15, # Minimum number of mechanisms in a cell to be considered
	'cluster_type':'', # 'grid' or 'quadroot'
	'hspace':np.inf, # Grid cell size used when creating equally spaced grids, km
	'xspace':[], # Grid cell size for horizontal (x) grids
	'yspace':[], # Grid cell size for horizontal (y) grids
	'hspace_min':-np.inf, # Minimum horizontal grid size when producing quadroot clusters, km
	'hspace_max':np.inf, # Maximum horizontal grid size when producing quadroot clusters, km
	'hspace_values':[], # Rather than providing $hspace_min & $hspace_max, you can provide the grid size values directly, km
	'depth_breaks':[], # Depth intervals (km)
	'time_breaks':[], # List of times (strings) that will divide the study time. Example format: ['1990-04-01 01:02:03','2024-01-01 20:10:05']
	'rotate_deg':0, # Degrees counterclockwise to rotate horizontal grid cells

	# ------- Damping -------
	'do_damping':True,
	'write_damp_file':False, # If True, the file containing the damping relationships (damp_outfile) will be created
	'do_iterative':False, # If True, damp values will be iteratively sampled as the optimal knee is located. If False, every damp value is considered.
	'damp_iteration_max':50, # When iteratively sampling damping parameters, this sets the maximum number of iterations.
	'damp_smoothing':True, # If True, damping is 'smoothed' by considering cells without events
	'discard_undamped_clusters':False, # If True, clusters that are not damped with another cluster are discarded.
	'diag_buffer_flag':False, # If True, cells that are diagonal from one another are damped
	'damp_param':-1, # If >0, this damping parameter will be used instead of using the model length vs data variance tradeoff curve
	'damp_values':[0,0.02,0.05,0.1,0.2,0.3,0.4,0.6,0.8,1,1.2,1.4,1.6,1.8,2,2.25,2.5,2.75,3,3.5,4,5,6,7,8,9,10,15,20,50],# Damping parameters considered
	'num_additional_damp':0, # Additional number of measurements surrounding the knee e value
	'report_empty_clusters':False, # If True, damped estimates for clusters without mechanisms are reported

	# ------- Bootstrapping -------
	'nboot':30, # Number of bootstap resamplings for uncertainty estimates (>1000 recommended)
	'fracplane':50, # Percent chance that the nodal plane is the fault plane (50 if chosen randomly).
	'confidence':95, # Confidence level (e.g., 95 for 95%)
	'randomize_events':True, # If True, mechanisms will be randomly selected for each bootstrap iteration
	'randomize_nodalplane':True, # If True, the nodal plane that represents the fault plane will be randomly selected for each bootstrap iteration
	'mech_uncertainty':0, # The median of the normally distributed errors applied to the nodal planes.
	'num_cpus':1, # Number of cores to run the boostrapping in parallel. Set to 0 to use all available, or 1 to run in serial.

	# ------- Fault plane instability -------
	'niterations':0, # Number of instability iterations
	'iteration_weight':0.5, # Amount to weigh the fault probability for each iteration (0.5-1.0). 0.5 is equal weight, 1.0 doesn't consider previous weight.
	'instability_weight':0.5, # Amount to weigh relative instability calculation (0.0-1.0).
	'final_instability':False, # On the final iteration, an instability_weight and iteration_weight of 1.0 is used.
	'convergence_threshold':1.0, # Stops the iterations when the mean change in fault probability % is less than the convergence_threshold
	'iterative_damping':False, # If True, recomputes the damping parameter following an iteration.
	'friction':[0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1.0], # Friction values to consider

	# ------- Mechanism selection -------
	'max_fault_plane_uncertainty':np.nan, # Maximum fault plane uncertainty of mechs to consider.
	'max_polarity_misfit':np.nan, # Maximum polarity misfit of mechs to consider.
	'min_prob_mech':np.nan, # Minimum mechanism probably to consider.
	'min_sta_distribution_ratio':np.nan, # Minimum station distribution ratio of the mechanisms to consider.

	# ------- Checkerboard -------
	'checkerboard_type':'', # 'traditional' or 'gradient'. If empty, no checkerboard test is done.
	'shape_ratio':0.5,
	'theta':0, # dip of sigma1 for the checkerboard (0: horizontal, 90: vertical)
	'checkerboard_hspace':10, # length of checkerboard grid, km
	# -- Traditional checkerboard --
	'checkerboard_shmax1':0, # Shmax azimuth of one of the traditional checkerboard values, degrees
	'checkerboard_shmax2':45, # Shmax azimuth of the other traditional checkerboard value, degrees
	# -- Gradient checkerboard --
	'checkerboard_gradient':1, # rotation of shmax clockwise per gradient checkerboard_hspace, degrees
	'checkerboard_shmax_start':5, # Shmax value in the SW corner

	# ------- Output variables and measurement precision -------
	'coordinate_precision':6, # number of decimal places to round lon/lats
	'angle_precision':1, # number of decimal places to round measurements/solutions
	'vector_precision':6, # number of decimal places to round vector & phi results
	'merge_bin_info':True, # If True, the stress file will contain bin location/time information that is reported in $binloc_outfile

	# ------- Plotting -------
	'plots':[], # Can include 'stereonet', 'shmax', 'shmax_error', 'phi', 'aphi','damp_tradeoff'

	# ------- Cosmetic -------
	'print_runtime':True,

	# ------- Additional (hidden) variables -------
	# -- Filenames produced by pySATSI --
	'event_outfile':'', # Output path to the binned mechanism file
	'stress_outfile':'', # Output path to stress results
	'rawstress_outfile':'', # Output path to the raw boostrap stress results
	'binloc_outfile':'', # Output path to the bin locations
	'tradeoff_outfile':'', # Output path to the damp misfit results
	'damp_outfile':'', # Output path to the damping relationships. Created if write_damp_file==True
	# -- Cosmetic variables. Only used for printing version information --
	'version_string':'v0.2',
	'version_date':'2025-05-20',
	# -- Variables used internally. Don't modify these unless you know what you're doing. :)
	'dimension_names':['x','y','z','l','t'], # Allowed dimension names
	'min_grid_spacing':np.nan,
	'do_horizontal_gridding':False,
	'do_vertical_gridding':False,
	'do_temporal_gridding':False,
}