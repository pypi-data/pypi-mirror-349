'''
Plotting functions for use in pySATSI
'''

# External libraries
import copy
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap
from matplotlib.patches import Polygon,Rectangle,Wedge
from matplotlib.collections import PatchCollection,LineCollection
from matplotlib.ticker import MaxNLocator,StrMethodFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable

# Local libraries
import functions.fun as fun

params={'mathtext.default':'regular'}
plt.rcParams.update(params)
plt.rcParams['hatch.linewidth'] = 0.5

def plot_tradeoff(damp_misfit_df,p_dict,savepath='',damp_label=True):
	'''
	Plots the tradeoff curve
		damp_misfit_df: damping misfit dataframe. Contains ['e','variance','length','knee_flag'] columns
		savepath: filepath where figure will be saved
		damp_label: labels the damp values in the scatter plot
	'''
	if not(savepath):
		savepath=os.path.join(p_dict['project_dir'],'damp_tradeoff.png')

	plot_df=damp_misfit_df.loc[damp_misfit_df['e']>0,:].reset_index(drop=True)

	# Creates strings of the damping parameters to display
	plot_df['e_display']=plot_df['e'].astype(str)
	whole_ind=np.where((plot_df['e'].values % 1)==0)[0]
	for x_ind in whole_ind:
		plot_df.loc[x_ind,'e_display']=str(int(plot_df.loc[x_ind,'e']))

	# Finds the index of the knee
	if damp_misfit_df['knee_flag'].any():
		knee_index=damp_misfit_df.loc[damp_misfit_df['knee_flag']].index[0]
	else:
		knee_index=None

	fig,ax=plt.subplots(figsize=(8,6))
	s=ax.scatter(plot_df['length'],plot_df['variance'],c=plot_df['e'],s=30,lw=0.5,edgecolor='k', norm=colors.LogNorm(vmin=plot_df['e'].min(), vmax=plot_df['e'].max()),cmap='turbo',zorder=2);
	fig.colorbar(s, ax=ax,label='Damping parameter ($e$)')

	if knee_index:
		ax.scatter(damp_misfit_df.loc[knee_index,'length'],damp_misfit_df.loc[knee_index,'variance'],c='magenta',edgecolor='k',lw=0.5,marker='*',s=400)
	if damp_label:
		# Determines how to rotate damping parameter texts
		if damp_misfit_df.shape[0]>2:
			text_rotation=np.degrees(np.arctan2(np.diff(damp_misfit_df['variance']),np.diff(damp_misfit_df['length'])))-90
			text_rotation=np.hstack((text_rotation,text_rotation[-1]))

			text_rotation=(text_rotation[1:]+text_rotation[:-1])/2
			text_rotation=np.hstack((text_rotation,text_rotation[-1]))
			text_rotation=np.abs(text_rotation)
		else:
			text_rotation=np.zeros(damp_misfit_df.shape[0])
		for point_x in range(len(plot_df)):
			ax.text(plot_df.loc[point_x,'length'],plot_df.loc[point_x,'variance'],' '+(plot_df.loc[point_x,'e_display']),ha='left',va='center',rotation=text_rotation[point_x],rotation_mode='anchor')

	ax.set_axisbelow(True);ax.grid(color='gray', linestyle='dashed')
	ax.set_box_aspect(1)
	ax.set_xlabel('Model Length')
	ax.set_ylabel('Data Variance')
	plt.savefig(savepath, bbox_inches='tight',dpi=200);plt.close()


def plot_grid(stress_df,cluster_df,boot_stress_df, p_dict, plot_type,
			damp_df=[], mech_df=[],
			plot_gridlines=True,border=0,
			max_shmax_error=np.inf,shmax_vmin=np.nan,shmax_vmax=np.nan):
	'''
	Creates plots of the stress results.
	'''

	# Reads in custom colormaps
	function_path=os.path.dirname(__file__)
	try:
		with open(os.path.join(function_path,'colormaps/colorwheel.txt')) as f:
			cmap_colorwheel=f.read().splitlines()
	except:
		print('Warning: Unable to load local colormap \'colorwheel\'')
		cmap_colorwheel=[]
	try:
		with open(os.path.join(function_path,'colormaps/rainbow.txt')) as f:
			cmap_rainbow=f.read().splitlines()
	except:
		print('Warning: Unable to load local colormap \'rainbow\'')
		cmap_rainbow=[]

	# Colors for Sigma1-3
	c_s1='#e6194B'
	c_s2='#4363d8'
	c_s3='#3cb44b'

	if len(stress_df)==0:
		print('Stress results are empty. Skipping plotting.')
		return 0

	# Sets the color range of stresses
	if np.isnan(shmax_vmin):
		shmax_vmin=stress_df['shmax'].min()
	if np.isnan(shmax_vmax):
		shmax_vmax=stress_df['shmax'].max()
	if shmax_vmin>shmax_vmax:
		raise ValueError('shmax_vmin should be < shmax_vmax')
	if shmax_vmin==shmax_vmax:
		shmax_vmin-=0.1
		shmax_vmax+=0.1

	# Not plotting hlines and vlines if rotated
	if plot_gridlines & (('lat3' in cluster_df.columns) | ('lon3' in cluster_df.columns)):
		plot_gridlines=False

	# If no cluster info exists, make some placeholders
	if len(cluster_df)==1:
		cluster_df[['cluster_id','x','y','mech_count']]=np.asarray([[0,0,0,1]],dtype=int)

	rect_cluster_df=cluster_df.copy()
	if 'mech_count' in rect_cluster_df.columns:
		rect_cluster_df=rect_cluster_df.loc[rect_cluster_df['mech_count']>0].reset_index(drop=True)

	# Determines min/lon of the clusters (this can be handled much better)
	if {'lon1','lon2','lon3','lon4','lat1','lat2','lat3','lat4'}.issubset(rect_cluster_df.columns):
		min_lon_plot=rect_cluster_df[['lon1','lon2','lon3','lon4']].values.min()
		max_lon_plot=rect_cluster_df[['lon1','lon2','lon3','lon4']].values.max()
		min_lat_plot=rect_cluster_df[['lat1','lat2','lat3','lat4']].values.min()
		max_lat_plot=rect_cluster_df[['lat1','lat2','lat3','lat4']].values.max()
		plot_form='deg_rot'
	elif {'lon1','lon2','lat1','lat2'}.issubset(rect_cluster_df.columns):
		min_lon_plot=rect_cluster_df[['lon1','lon2']].values.min()
		max_lon_plot=rect_cluster_df[['lon1','lon2']].values.max()
		min_lat_plot=rect_cluster_df[['lat1','lat2']].values.min()
		max_lat_plot=rect_cluster_df[['lat1','lat2']].values.max()
		plot_form='deg'
	elif {'x','y'}.issubset(rect_cluster_df.columns):
		min_lon_plot=rect_cluster_df['x'].min()-0.5
		max_lon_plot=rect_cluster_df['x'].max()+0.5
		min_lat_plot=rect_cluster_df['y'].min()-0.5
		max_lat_plot=rect_cluster_df['y'].max()+0.5
		plot_form='xy'
	else:
		print('Cannot make plots without 2d horizontal bins.')
		return 0

	# Cosmetic buffer space around plotted results
	if border:
		border=np.max([(max_lon_plot-min_lon_plot),(max_lat_plot-min_lat_plot)])*border

	if plot_form=='deg':
		latmult=111.1
		lonmult=111.1*np.cos(np.pi*(min_lat_plot.min()+max_lat_plot.max())/2/180.0)
		aspect_ratio=latmult/lonmult
	elif plot_form=='xy':
		aspect_ratio=1
	else:
		raise ValueError('Unknown plot_form: {}'.format(plot_form))

	base_savepath=os.path.join(p_dict['project_dir'],plot_type)
	if 't' in cluster_df.columns:
		t_steps=cluster_df['t'].unique()
		num_t_steps=len(t_steps)
	else:
		num_t_steps=1

	for t in range(num_t_steps):
		if num_t_steps>1:
			t_step=t_steps[t]
			savepath=base_savepath+('_'+str(t_step)+'.png')
			if len(mech_df):
				plot_mech_df=mech_df.loc[mech_df['t']==t_step].reset_index(drop=True)
			else:
				plot_mech_df=mech_df
			plot_cluster_df=cluster_df.loc[cluster_df['t']==t_step].reset_index(drop=True)
			plot_stress_df=stress_df.loc[stress_df['t']==t_step].reset_index(drop=True)
			plot_boot_stress_df=boot_stress_df.loc[boot_stress_df['t']==t_step].reset_index(drop=True)
		else:
			savepath=base_savepath+'.png'
			plot_mech_df=mech_df
			plot_cluster_df=cluster_df
			plot_stress_df=stress_df
			plot_boot_stress_df=boot_stress_df

		rect_plot_cluster_df=plot_cluster_df.copy()
		rect_plot_cluster_df=rect_plot_cluster_df.merge(plot_stress_df[['cluster_id','shmax']],on='cluster_id')

		fig,ax=plt.subplots(figsize=(8,8))

		if len(plot_mech_df):
			# Plots mechanism epicenters
			if plot_form=='deg':
				ax.scatter(plot_mech_df['lon'],plot_mech_df['lat'],c='k',s=3,lw=0,zorder=3)
			else:
				raise ValueError('No set up to plot mechanisms when plot_form!=deg')

		if not('shmax_uncert' in plot_stress_df.columns):
			plot_stress_df['shmax_uncert']=0
		shmax_df=plot_stress_df[['cluster_id','shmax','shmax_uncert','Aphi','phi']].merge(plot_cluster_df,on='cluster_id')

		nomech_shmax_df=shmax_df.loc[shmax_df['mech_count']==0].reset_index()
		mech_shmax_df=shmax_df.loc[shmax_df['mech_count']!=0].reset_index()

		if len(shmax_df):
			mech_shmax_df['az_diff']=mech_shmax_df['shmax_uncert']*2
			drop_cluster_id=mech_shmax_df.loc[mech_shmax_df['shmax_uncert']>max_shmax_error,'cluster_id']
			if len(drop_cluster_id):
				mech_shmax_df=mech_shmax_df.loc[~mech_shmax_df['cluster_id'].isin(drop_cluster_id)].reset_index(drop=True)
				rect_plot_cluster_df=rect_plot_cluster_df.loc[~rect_plot_cluster_df['cluster_id'].isin(drop_cluster_id)].reset_index(drop=True)
				if len(plot_stress_df):
					plot_stress_df=plot_stress_df.loc[~plot_stress_df['cluster_id'].isin(drop_cluster_id)].reset_index(drop=True)

		if 'grid_dspace' in rect_plot_cluster_df.columns:
			rect_plot_cluster_df=rect_plot_cluster_df.sort_values(by='grid_dspace',ascending=False).reset_index(drop=True)

		rect_all=[]
		grey_rect_all=[]
		if plot_form=='deg':
			for cluster_x in range(len(rect_plot_cluster_df)):
				rect=Rectangle(xy=(rect_plot_cluster_df.loc[cluster_x,'lon1'], rect_plot_cluster_df.loc[cluster_x,'lat1']),
						width=(rect_plot_cluster_df.loc[cluster_x,'lon2']-rect_plot_cluster_df.loc[cluster_x,'lon1']),
						height=(rect_plot_cluster_df.loc[cluster_x,'lat2']-rect_plot_cluster_df.loc[cluster_x,'lat1']))
				if rect_plot_cluster_df.loc[cluster_x,'mech_count']>0:
					rect_all.append(rect)
				else:
					grey_rect_all.append(rect)
		elif plot_form=='deg_rot':
			for cluster_x in range(len(rect_plot_cluster_df)):
				rect=Polygon(np.vstack([rect_plot_cluster_df.loc[cluster_x,['lon1','lon3','lon2','lon4']].values,
										rect_plot_cluster_df.loc[cluster_x,['lat1','lat3','lat2','lat4']].values]).T)
				if rect_plot_cluster_df.loc[cluster_x,'mech_count']>0:
					rect_all.append(rect)
				else:
					grey_rect_all.append(rect)
		elif plot_form=='xy':
			for cluster_x in range(len(rect_plot_cluster_df)):
				rect=Rectangle(xy=(rect_plot_cluster_df.loc[cluster_x,'x']-0.5, rect_plot_cluster_df.loc[cluster_x,'y']-0.5),
						width=(1),
						height=(1))
				if rect_plot_cluster_df.loc[cluster_x,'mech_count']>0:
					rect_all.append(rect)
				else:
					grey_rect_all.append(rect)
		rect_all=np.asarray(rect_all)
		grey_rect_all=np.asarray(grey_rect_all)

		p1=PatchCollection(rect_all,lw=0.5,facecolor='None',edgecolor='k',zorder=4)
		ax.add_collection(p1)

		# If there are bins with no mechs, indicate with grey borders
		if p_dict['report_empty_clusters']:
			p1=PatchCollection(grey_rect_all,lw=0.5,facecolor='None',edgecolor='0.5',hatch='\\\\',zorder=2)
			ax.add_collection(p1)


		if (len(shmax_df)):
			if plot_form in ['deg','deg_rot']:
				x_mid=(shmax_df['lon1']+shmax_df['lon2'])/2
				y_mid=(shmax_df['lat1']+shmax_df['lat2'])/2
				wedge_length=(shmax_df['lat2']-shmax_df['lat1'])/2
			elif plot_form in ['xy']:
				x_mid=shmax_df['x']
				y_mid=shmax_df['y']
				wedge_length=np.zeros(shmax_df.shape[0])+0.5

			if plot_type=='stereonet':
				x1,y1,_=spherical_to_xyr(np.radians(plot_stress_df['az1'].values),np.radians(plot_stress_df['pl1'].values))
				x2,y2,_=spherical_to_xyr(np.radians(plot_stress_df['az2'].values),np.radians(plot_stress_df['pl2'].values))
				x3,y3,_=spherical_to_xyr(np.radians(plot_stress_df['az3'].values),np.radians(plot_stress_df['pl3'].values))

				if plot_form in ['deg','deg_rot']:
					rect_plot_cluster_df['center_x']=(rect_plot_cluster_df['lon1'].values+rect_plot_cluster_df['lon2'].values)/2
					rect_plot_cluster_df['center_y']=(rect_plot_cluster_df['lat1'].values+rect_plot_cluster_df['lat2'].values)/2
					circle_diameter=(rect_plot_cluster_df.loc[0,'lat2']-rect_plot_cluster_df.loc[0,'lat1'])*.9
				elif plot_form in ['xy']:
					rect_plot_cluster_df['center_x']=rect_plot_cluster_df['x'].values
					rect_plot_cluster_df['center_y']=rect_plot_cluster_df['y'].values
					circle_diameter=0.9
				circle_radius=circle_diameter/2

				# Creates unit circle borders
				A=np.radians(np.arange(0,360+5,5)) # Controls circles
				A2=np.radians(np.arange(0,180,30)) # Controls frequency of radial lines
				unit_circle=[]
				unit_interior_circle=[]
				interior_lines=[]

				for stress_x in range(len(plot_stress_df)):
					# Creates circle borders
					unit_circle.append(matplotlib.patches.Ellipse((x_mid[stress_x],y_mid[stress_x]),circle_diameter*aspect_ratio,circle_diameter))

					# Creates interior circles
					for R in np.arange(1/6,(1-1/6),1/6):
						interior_unit_x=(R*np.cos(A))*circle_radius*aspect_ratio+x_mid[stress_x]
						interior_unit_y=(R*np.sin(A))*circle_radius+y_mid[stress_x]
						unit_interior_circle.append(np.vstack((interior_unit_x,interior_unit_y)).T)

					# Creates interior radial lines
					for rad_az in A2:
						interior_line_x=[(np.sin(rad_az-np.pi))*circle_radius*aspect_ratio+x_mid[stress_x],
					   					(np.sin(rad_az))*circle_radius*aspect_ratio+rect_plot_cluster_df.loc[stress_x,'center_x']]
						interior_line_y=[(np.cos(rad_az-np.pi))*circle_radius+y_mid[stress_x],
					   					(np.cos(rad_az))*circle_radius+rect_plot_cluster_df.loc[stress_x,'center_y']]
						interior_lines.append(np.vstack((interior_line_x,interior_line_y)).T)

				unit_circle_collection=PatchCollection(copy.deepcopy(unit_circle),facecolor='white',zorder=8)
				unit_circle_collection_border=PatchCollection(unit_circle,facecolor='None',edgecolor='k',lw=1,zorder=10)
				unit_interior_circle_collection=LineCollection(unit_interior_circle, colors='0.5', linewidths=0.5,zorder=9)
				interior_line_collection=LineCollection(interior_lines, colors='0.5', linewidths=0.5,zorder=9)

				ax.add_collection(unit_circle_collection)
				ax.add_collection(unit_circle_collection_border)
				ax.add_collection(unit_interior_circle_collection)
				ax.add_collection(interior_line_collection)

				ax.scatter(x1*circle_radius*aspect_ratio+x_mid.values,y1*circle_radius+y_mid.values,c=c_s1,s=20,lw=0.5,ec='k',zorder=1000,label='$σ_{1}$')
				ax.scatter(x2*circle_radius*aspect_ratio+x_mid.values,y2*circle_radius+y_mid.values,c=c_s2,s=20,lw=0.5,ec='k',zorder=1000,label='$σ_{2}$')
				ax.scatter(x3*circle_radius*aspect_ratio+x_mid.values,y3*circle_radius+y_mid.values,c=c_s3,s=20,lw=0.5,ec='k',zorder=1000,label='$σ_{3}$')

				if len(plot_boot_stress_df):
					plot_boot_stress_df=plot_boot_stress_df.merge(rect_plot_cluster_df[['cluster_id','center_x','center_y']])
					all_x1,all_y1,_=spherical_to_xyr(np.radians(plot_boot_stress_df['az1'].values),np.radians(plot_boot_stress_df['pl1'].values))
					all_x2,all_y2,_=spherical_to_xyr(np.radians(plot_boot_stress_df['az2'].values),np.radians(plot_boot_stress_df['pl2'].values))
					all_x3,all_y3,_=spherical_to_xyr(np.radians(plot_boot_stress_df['az3'].values),np.radians(plot_boot_stress_df['pl3'].values))
					ax.scatter(all_x1*circle_radius*aspect_ratio+plot_boot_stress_df['center_x'],all_y1*circle_radius+plot_boot_stress_df['center_y'],c=c_s1,s=5,zorder=999)
					ax.scatter(all_x2*circle_radius*aspect_ratio+plot_boot_stress_df['center_x'],all_y2*circle_radius+plot_boot_stress_df['center_y'],c=c_s2,s=5,zorder=999)
					ax.scatter(all_x3*circle_radius*aspect_ratio+plot_boot_stress_df['center_x'],all_y3*circle_radius+plot_boot_stress_df['center_y'],c=c_s3,s=5,zorder=999)

				legend=ax.legend(loc='lower right',bbox_to_anchor=(0, 0),handletextpad=0)
				legend.get_frame().set_linewidth(1)
				legend.get_frame().set_edgecolor('k')
				legend.get_frame().set_facecolor('0.95')
				legend.get_frame().set_boxstyle('Square',pad=-0.1)
				for handle in legend.legend_handles:
					handle.set_sizes([100.0])

			elif not('l' in plot_cluster_df.columns):
				'''Plots SHmax uncertainty wedges'''
				shmax_err_patches=[]
				for x in range(len(x_mid)):
					shmax_min=shmax_df['shmax'][x]-shmax_df['shmax_uncert'][x]
					shmax_max=shmax_df['shmax'][x]+shmax_df['shmax_uncert'][x]
					shmax_err_patches.append(Wedge((x_mid[x],y_mid[x]),wedge_length[x],90-shmax_max,90-shmax_min))
					shmax_err_patches.append(Wedge((x_mid[x],y_mid[x]),wedge_length[x],90-shmax_max+180,90-shmax_min+180))
				shmax_err_patch_collection=PatchCollection(shmax_err_patches, alpha=1,facecolor='k',edgecolor='k',linewidth=.5,zorder=6)

				ax.add_collection(shmax_err_patch_collection)

			if len(rect_plot_cluster_df)>1:
				if plot_type=='shmax_error':
					az_diff=fun.az_diff_180(shmax_df['shmax'].values,shmax_df['synth_shmax'].values)
					rect_colors=az_diff
					use_cmap=matplotlib.colormaps['Reds']
					p2=PatchCollection(rect_all,lw=1,cmap=use_cmap,zorder=3)
					p2.set_clim(vmin=0,vmax=az_diff.max())
					p2.set_array(rect_colors)
					ax.add_collection(p2)

					if p_dict['report_empty_clusters']:
						nomech_az_diff=fun.az_diff_180(nomech_shmax_df['shmax'].values,nomech_shmax_df['synth_shmax'].values)
						nomech_rect_colors=nomech_az_diff
						p3=PatchCollection(grey_rect_all,lw=1,cmap=use_cmap,zorder=1)
						ax.add_collection(p3)
						p3.set_clim(vmin=0,vmax=az_diff.max())
						p3.set_array(nomech_rect_colors)
						ax.add_collection(p3)

					divider=make_axes_locatable(ax)
					cax=divider.append_axes('right', size='5%', pad=0)
					cbar=fig.colorbar(p2, cax=cax)
					cbar.ax.set_ylabel("$S_{Hmax}$ Error",rotation=-90,va='bottom')
				elif plot_type=='shmax':
					if (shmax_vmin==0) & (shmax_vmax==180):
						rect_colors=shmax_df['shmax'].values % 180
						if cmap_colorwheel:
							use_cmap=ListedColormap(cmap_colorwheel)
						else:
							use_cmap=matplotlib.colormaps['hsv']
					else:
						if np.isfinite(shmax_vmax) & np.isfinite(shmax_vmin):
							if not((shmax_vmin>=0) & (shmax_vmin<=180) & (shmax_vmax>=0) & (shmax_vmax<=180)):
								rect_colors=shmax_df['shmax'].copy().values
								if (shmax_vmin>=0):
									rect_colors[(rect_colors<shmax_vmin) | (rect_colors>shmax_vmax)]-=180
								elif (shmax_vmin<0):
									rect_colors[(rect_colors>90)]-=180
									rect_colors[(rect_colors>90)]-=180
							else:
								rect_colors=shmax_df['shmax'].values % 180

						if not(np.isfinite(shmax_vmin)):
							shmax_vmin=rect_colors.min()
						if not(np.isfinite(shmax_vmax)):
							shmax_vmax=rect_colors.max()
						if cmap_rainbow:
							use_cmap=ListedColormap(cmap_rainbow)
						else:
							use_cmap=matplotlib.colormaps['turbo']
					p2=PatchCollection(rect_all,lw=1,cmap=use_cmap,zorder=3)
					p2.set_clim(vmin=shmax_vmin,vmax=shmax_vmax)
					p2.set_array(rect_colors[mech_shmax_df['index'].values])
					ax.add_collection(p2)

					if p_dict['report_empty_clusters']:
						p3=PatchCollection(grey_rect_all,lw=1,cmap=use_cmap,zorder=1)
						p3.set_clim(vmin=shmax_vmin,vmax=shmax_vmax)
						p3.set_array(rect_colors[nomech_shmax_df['index'].values])
						ax.add_collection(p3)

					divider=make_axes_locatable(ax)
					cax=divider.append_axes('right', size='5%', pad=0)
					cbar=fig.colorbar(p2, cax=cax)
					cbar.ax.set_ylabel('$S_{Hmax}$',rotation=-90,va='bottom')

					cbar.ax.invert_yaxis()

					cbar.ax.yaxis.set_major_formatter(StrMethodFormatter(u"{x:03.0f}°"))

					# If colorbar tick labels have SHmax<0, change to 0-360 values
					cbar_yticks=cbar.ax.get_yticks()
					if (cbar_yticks<0).any():
						cbar.ax.yaxis.set_ticks(cbar_yticks)
						neg_cbar_ytick_ind=np.where(cbar_yticks<0)[0]
						cbar_ytick_labels=[item.get_text() for item in cbar.ax.get_yticklabels()]
						for tick_x in neg_cbar_ytick_ind:
							cbar_ytick_labels[tick_x]='%03.0f°' % (cbar_yticks[tick_x]+360)
						cbar.ax.set_yticklabels(cbar_ytick_labels)
					cbar.ax.set_ylim(shmax_vmin,shmax_vmax)
				elif plot_type=='phi':
					rect_colors=shmax_df['phi'].values

					if cmap_rainbow:
						use_cmap=ListedColormap(cmap_rainbow)
					else:
						use_cmap=matplotlib.colormaps['turbo']
					p2=PatchCollection(rect_all,lw=1,cmap=use_cmap,zorder=3)
					p2.set_clim(vmin=0,vmax=1)
					p2.set_array(rect_colors[mech_shmax_df['index'].values])
					ax.add_collection(p2)

					if p_dict['report_empty_clusters']:
						p3=PatchCollection(grey_rect_all,lw=1,cmap=use_cmap,zorder=1)
						p3.set_clim(vmin=0,vmax=1)
						p3.set_array(rect_colors[nomech_shmax_df['index'].values])
						ax.add_collection(p3)

					divider=make_axes_locatable(ax)
					cax=divider.append_axes('right', size='5%', pad=0)
					cbar=fig.colorbar(p2, cax=cax)
					cbar.ax.set_ylabel("Phi",rotation=-90,va='bottom')
				elif plot_type=='aphi':
					rect_colors=shmax_df['Aphi'].values

					if cmap_rainbow:
						use_cmap=ListedColormap(cmap_rainbow)
					else:
						use_cmap=matplotlib.colormaps['turbo']
					p2=PatchCollection(rect_all,lw=1,cmap=use_cmap,zorder=3)
					p2.set_clim(vmin=0,vmax=3)
					p2.set_array(rect_colors[mech_shmax_df['index'].values])
					ax.add_collection(p2)

					if p_dict['report_empty_clusters']:
						p3=PatchCollection(grey_rect_all,lw=1,cmap=use_cmap,zorder=1)
						p3.set_clim(vmin=0,vmax=3)
						p3.set_array(rect_colors[nomech_shmax_df['index'].values])
						ax.add_collection(p3)

					divider=make_axes_locatable(ax)
					cax=divider.append_axes('right', size='5%', pad=0)
					cbar=fig.colorbar(p2, cax=cax)
					cbar.ax.set_ylabel("$A_{Φ}$",rotation=-90,va='bottom')

		# Plots the web of buffer connections
		if len(damp_df):

			center_lon=(rect_plot_cluster_df['lon1']+rect_plot_cluster_df['lon2']).values/2
			center_lat=(rect_plot_cluster_df['lat1']+rect_plot_cluster_df['lat2']).values/2
			plot_damp_df=damp_df.loc[(damp_df['cluster_id1'].isin(rect_plot_cluster_df['cluster_id'])) & (damp_df['cluster_id2'].isin(rect_plot_cluster_df['cluster_id']))]
			plot_damp_df=plot_damp_df.sort_values(by=['cluster_id1','cluster_id2']).reset_index(drop=True)
			ax.plot(np.vstack((center_lon[plot_damp_df['cluster_id1'].values],center_lon[plot_damp_df['cluster_id2'].values])),
					np.vstack((center_lat[plot_damp_df['cluster_id1'].values],center_lat[plot_damp_df['cluster_id2'].values])),c='magenta',lw=.75,zorder=6)

		# Adds smallest grid intervals
		if plot_gridlines:
			# Recomputes the deg bins for the plots
			if 'grid_dspace' in rect_cluster_df.columns:
				min_dspace_ind=rect_cluster_df['grid_dspace'].argmin()
			else:
				min_dspace_ind=0

			if plot_form in ['deg','deg_rot']:
				min_dspace_lon=rect_cluster_df.loc[min_dspace_ind,'lon2']-rect_cluster_df.loc[min_dspace_ind,'lon1']
				min_dspace_lat=rect_cluster_df.loc[min_dspace_ind,'lat2']-rect_cluster_df.loc[min_dspace_ind,'lat1']
			elif plot_form=='xy':
				min_dspace_lon=1
				min_dspace_lat=1
			plot_lonbin=np.arange(min_lon_plot,max_lon_plot+min_dspace_lon/2,min_dspace_lon)
			plot_latbin=np.arange(min_lat_plot,max_lat_plot+min_dspace_lat/2,min_dspace_lat)
			ax.hlines(plot_latbin,plot_lonbin.min(),plot_lonbin.max(),color='k',lw=0.25,zorder=0,linestyle='--')
			ax.vlines(plot_lonbin,plot_latbin.min(),plot_latbin.max(),color='k',lw=0.25,zorder=0,linestyle='--')

		# Sets the limits and aspect ratio
		ax.set_xlim([min_lon_plot-border*aspect_ratio,max_lon_plot+border*aspect_ratio])
		ax.set_ylim([min_lat_plot-border,max_lat_plot+border])
		ax.set_aspect(aspect_ratio)

		# Makes xtick and ytick freq the same
		xtick_interval=np.diff(ax.get_xticks()).min()
		ytick_interval=np.diff(ax.get_yticks()).min()
		if xtick_interval<ytick_interval:
			ax.xaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=ytick_interval))
		if ytick_interval<xtick_interval:
			ax.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(base=xtick_interval))
		if plot_form in ['deg','deg_rot']:
			ax.set_xlabel('Longitude')
			ax.set_ylabel('Latitude')
		elif plot_form=='xy':
			if len(cluster_df)>1:
				ax.set_xlabel('X grid')
				ax.set_ylabel('Y grid')
				# Sets ticks to show only integer values
				ax.xaxis.set_major_locator(MaxNLocator(integer=True))
				ax.yaxis.set_major_locator(MaxNLocator(integer=True))
			else:
				ax.set_xticks([])
				ax.set_yticks([])

		if num_t_steps>1:
			if plot_cluster_df.loc[0,'time1']==np.datetime64('1700-01-01'):
				t_start_str='start'
			else:
				t_start_str=str(plot_cluster_df.loc[0,'time1'])
			if plot_cluster_df.loc[0,'time2']==np.datetime64('2200-01-01'):
				t_end_str='end'
			else:
				t_end_str=str(plot_cluster_df.loc[0,'time2'])
			ax.set_title(str(t_step)+': '+t_start_str+' to '+t_end_str)
		fig.tight_layout()
		plt.savefig(savepath, bbox_inches='tight',dpi=200);plt.close()

def spherical_to_xyr(azimuth, plunge):
	'''
	Convert spherical coordinates (azimuth, plunge) to cartesian coordinates (x,y,r).

	Args:
		azimuth: array of azimuth angles in radians.
		plunge:array of take-off angles in radians.

	Returns:
		x: array of x-coordinates.
		y: array of y-coordinates.
		r: array of radii.
	'''
	# Make consistent plunge
	plunge=np.pi/2-plunge

	# Handle angles > pi/2
	mask=plunge>np.pi/2
	azimuth[mask]+=np.pi
	plunge[mask]=np.pi-plunge[mask]

	# Project to cartesian coordinates
	r=np.sqrt(2)*np.sin(plunge/2)
	x=r*np.sin(azimuth)
	y=r*np.cos(azimuth)

	return x,y,r