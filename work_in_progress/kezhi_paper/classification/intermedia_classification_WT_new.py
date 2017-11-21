# -*- coding: utf-8 -*-
"""
Created on Tue Jun 06 16:16:01 2017

@author: kezhili
"""
import numpy as np
import tables
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

no_neuron = 1040  # step size in the mesh
no_fea = 30
fea_no = 30

names = ["Nearest Neighbors", "RBF SVM", "Gaussian Process",
         "Decision Tree", "Random Forest"]

if __name__ == '__main__':
    fdata = 'interm_LR_WTmemory_interm_result_30features_WT.hdf5'
    with tables.File(fdata, 'r') as fid:
        X = fid.get_node('/X3')[:]  
        Y = fid.get_node('/Y3')[:]  
        #because of the fix of a previous error in the dataset, 
        #where 'LSJ1' and 'L5J1' are actually the same class
        Y[97:107] = Y[107]  
    
    with open('result_30_features.txt') as f:
        lines = f.read().split('\n')
    X_ind = [x == 'True' for x in lines if x]    
    Xp = X[:,X_ind]
    
    
    cross_validation_fold = 5
    
    for n_estimators in [10, 100, 1000]:
        clf2 = RandomForestClassifier(n_estimators=n_estimators)
        c_val = cross_val_score(clf2, Xp, Y, cv = cross_validation_fold)
        print(np.mean(c_val), np.std(c_val))