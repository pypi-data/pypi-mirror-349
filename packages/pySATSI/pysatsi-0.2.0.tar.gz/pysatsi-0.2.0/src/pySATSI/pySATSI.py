'''
Python package for focal mechanism stress inversions.

Author: Robert J. Skoumal (rskoumal@usgs.gov)

This code is inspired by the SATSI algorithm created by Jeanne L. Hardebeck
and Andrew J. Michael. If you use this code, please cite the appropriate papers.
	Skoumal, R.J., Hardebeck, J.L., & Michael, A.J. (in prep). pySATSI: A Python
		package for computing focal mechansim stress inversions. Seismological Research Letters.
	Hardebeck, J.L., & Michael, A.J. (2006). Damped regional‐scale stress inversions:
		Methodology and examples for southern California and the Coalinga aftershock sequence.
		Journal of Geophysical Research: Solid Earth, 111(B11). https://doi.org/10.1029/2005JB004144
'''

# Standard libraries
import sys
from timeit import default_timer as timer

# Local libraries
import functions.bootmech as bootmech # Bootstrapped stress computation
import functions.file_io as file_io # Reads/writes files
import functions.fun as fun # General functions
import functions.gridding as gridding # Clustering events
import functions.knee as knee # Determining optimal damping parameter
import functions.mech as mech # Computes mechanism RMS
import functions.stress as stress # Stress computations

def pySATSI():
	tic=timer()

	from functions.default_params import p_dict # Default parameters

	# Checks Python version.
	if not((sys.version_info.major==3) & (sys.version_info.minor>=8)):
		print('***WARNING: pySATSI has only been tested on Python 3.8+. Refer to the documentation for supported versions.')

	'''
	Reads user arguments from the command line and control file. Note that if you use a control file,
	the control file variable will overwrite command line arguments.
	'''
	p_dict=file_io.read_command_line(p_dict)
	if p_dict['control_file']:
		p_dict=file_io.read_control_file(p_dict)

	# Cosmetic version information
	print(('='*25+'\npySATSI {} ({})\n'+'='*25).
		format(p_dict['version_string'],p_dict['version_date']))

	# Runs various QC checks on the parameters
	p_dict=file_io.qc_params(p_dict)

	'''
	Reads the focal mechanism file
	'''
	print('Reading mechanisms...')
	tic_readmech=timer()
	mech_df,p_dict=file_io.read_mech_file(p_dict)
	print('\tMechanism read runtime: {0:.2f} sec'.format(timer()-tic_readmech))

	'''
	Reads or creates the cluster and damping relationships
	'''
	print('Clustering mechanisms...')
	tic_gridding=timer()

	# Reads pre-determined damping file
	if len(p_dict['damp_file']):
		damp_df=file_io.read_damp_file(p_dict)
		print('\tDamping file read.')

	if len(p_dict['binloc_file']):
		# Reads pre-determined cluster file
		cluster_df=file_io.read_cluster_file(p_dict)
		print('\tMechanism cluster file read.')
	else:
		# Creates clusters
		mech_df,cluster_df,damp_df,p_dict=gridding.grid(mech_df,p_dict)
		print('\tMechanisms clustered.')

	if len(mech_df)==0:
		print('No mechanisms left to consider. Quitting.')
		quit()

	if not('cluster_id' in mech_df.columns):
		# Converts binned dimensions (i.e. [x,y,z,t,l]) into cluster_id
		mech_df,cluster_df,damp_df=fun.convert_cluster_ind(mech_df,cluster_df,damp_df,p_dict)
		print('\tCluster IDs assigned.')

	print('\tMechanism clustering runtime: {0:.2f} sec'.format(timer()-tic_gridding))

	'''
	Computes mechanism RMS for each cluster
	'''
	print('Computing mechanism RMS...')
	tic_mechrms=timer()
	cluster_df=mech.mech_rms(mech_df,cluster_df,p_dict)
	print('\tMechanism RMS runtime: {0:.2f} sec'.format(timer()-tic_mechrms))

	'''
	Writes cluster files
	'''
	if len(cluster_df):
		# Saves cluster locations
		cluster_df.to_csv(p_dict['binloc_outfile'],index=False)

		# Saves damped relationships
		if p_dict['do_damping'] and p_dict['write_damp_file']:
			damp_df.to_csv(p_dict['damp_outfile'],index=False)

	'''
	Invert damping parameter
	'''
	if p_dict['do_damping'] and (p_dict['damp_param']<0):
		tic_damping=timer()
		print('Identifying scalar damping parameter...')
		damp_misfit_df,p_dict['damp_param']=knee.find_damp(mech_df,damp_df,p_dict)
		print('\tDamping parameter runtime: {0:.1f} sec'.format(timer()-tic_damping))

	'''
	Perform bootstraps
	'''
	tic_bootstrap=timer()
	print('Computing stresses...')
	boot_stress_df,iteration_damp_misfit_df=bootmech.compute_boot(mech_df,damp_df,p_dict)
	if iteration_damp_misfit_df:
		damp_misfit_df=iteration_damp_misfit_df
	boot_stress_df.to_csv(p_dict['rawstress_outfile'],index=False)
	print('\tStress computation runtime: {:.2f} sec'.format(timer()-tic_bootstrap))

	'''
	Compute bootstrap uncertainties and SHmax
	'''
	tic_uncertainties=timer()
	print('Computing uncertainties...',flush=True)
	stress_df=bootmech.uncert(boot_stress_df,p_dict)
	stress_df=fun.calc_shmax_uncert(boot_stress_df,stress_df,p_dict)
	stress_df=fun.calc_Aphi(stress_df,p_dict)
	print('\tUncertainty computation runtime: {:.2f} sec'.format(timer()-tic_uncertainties),flush=True)

	'''
	Compute focal mechanism misfit
	'''
	tic_misfit=timer()
	print('Computing misfit...')
	mech_df['misfit_angle'],mech_df['tau_mag']=stress.slickenside(mech_df,damp_df,p_dict['damp_param'],p_dict,case='mech_misfit')
	file_io.write_misfit_file(mech_df,p_dict)
	print('\tMisfit computation runtime: {:.2f} sec'.format(timer()-tic_misfit),flush=True)

	'''
	Writes stress result file
	'''
	# Adds cluster location information to the stress dataframe
	if p_dict['merge_bin_info']:
		stress_df=fun.merge_stress_cluster_info(stress_df,cluster_df,p_dict)
	boot_stress_df=fun.merge_stress_cluster_info(boot_stress_df,cluster_df,p_dict)
	stress_df.to_csv(p_dict['stress_outfile'],index=False)

	'''
	Plots stress results
	'''
	if len(p_dict['plots']):
		import functions.plotting as plotting # Creates output plots
		tic_plot=timer()
		print('Creating plots...')
		for plot_type in p_dict['plots']:
			print(f'\tPlotting {plot_type} figure...')
			if plot_type=='damp_tradeoff':
				plotting.plot_tradeoff(damp_misfit_df,p_dict)
			else:
				plotting.plot_grid(stress_df,cluster_df,boot_stress_df,p_dict,plot_type)
		print('\tPlotting runtime: {:.2f} sec'.format(timer()-tic_plot))

	print('Total runtime: {0:.2f} sec'.format(timer()-tic))

def main():
	pySATSI()

if __name__ == "__main__":
	main()
