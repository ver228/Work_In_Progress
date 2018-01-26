import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.backends.backend_pdf import PdfPages
import os
from collect_data import read_light_data, get_exp_data, read_file_data


if __name__ == '__main__':
    _is_debug = True
    mask_dir = '/Volumes/behavgenom_archive$/Lidia/MaskedVideos'
    
    save_dir = './lidia_data'
    save_dir_r = './lidia_data_r'
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    if not os.path.exists(save_dir_r):
        os.makedirs(save_dir_r)
    
    exp_df = get_exp_data(mask_dir)
    
    #correct some issues
    wrongly_named_stains = {'HRB222':'HBR222'}
    bad_strains = ['AZ46', 'AZ60']
    exp_df['strain'].replace( wrongly_named_stains)
    exp_df = exp_df[~exp_df['strain'].isin(bad_strains)]
    exp_df.index = np.arange(len(exp_df))
    
    #%%
    feats2plot = ['speed', 'angular_velocity',
       'relative_speed_midbody', 'relative_radial_velocity_head_tip',
       'relative_angular_velocity_head_tip', 'relative_radial_velocity_neck',
       'relative_angular_velocity_neck', 'relative_radial_velocity_hips',
       'relative_angular_velocity_hips', 'relative_radial_velocity_tail_tip',
       'relative_angular_velocity_tail_tip', 'length', 
       'width_head_base', 'width_midbody', 'width_tail_base', 'curvature_head',
       'curvature_hips', 'curvature_midbody', 'curvature_neck',
       'curvature_tail'
    ]  
    
    feats2plot_r = ['speed', 'length', 'width_midbody', 'curvature_head',
       'curvature_hips', 'curvature_midbody'] 
     #%% 
    all_data = pd.DataFrame()
    for irow, row in exp_df.iterrows():
        print(irow+1, len(exp_df))
        mask_file = row['mask_file']
        feat_file = mask_file.replace('MaskedVideos', 'Results').replace('.hdf5', '_featuresN.hdf5')
        
        light_on = read_light_data(mask_file)
        
        output = read_file_data(mask_file, feat_file)
        if output is None:
            continue
        else:
            timeseries_data, blob_features, fps, region_size = output
        
        #%%
        dd = timeseries_data[['timestamp'] + feats2plot].groupby('timestamp').agg('median')
        dd = dd.rolling(round(fps*1)).median()
        #%%
        base_name = os.path.basename(row['mask_file'])[:-5]
        
        save_name = os.path.join(save_dir, base_name + '.pdf')
        save_name_r = os.path.join(save_dir_r, base_name + '.pdf')
        
        with PdfPages(save_name) as pdf, PdfPages(save_name_r) as pdf_r:
            
            for ff in feats2plot:
                ff_s = ff[:]
                yy = dd[ff].values
                xx = dd.index/fps
                
                if 'curvature' in ff_s:
                    yy = np.abs(yy)
                    ff_s += '_abs'
                    
                
                
                fig = plt.figure(figsize=(24, 5))
                plt.plot(xx, yy)
                
                xx = np.arange(light_on.size)/fps
                
                d_ylim = plt.ylim()
                d_r = d_ylim[1] - d_ylim[0]
                l_r = light_on*d_r + d_ylim[0]
                
                plt.plot(xx, l_r)
                plt.title(ff_s)    
                pdf.savefig(fig)
                if ff in feats2plot_r:
                    pdf_r.savefig(fig)
                plt.close()
        