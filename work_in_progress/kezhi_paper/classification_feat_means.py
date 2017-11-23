#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 13:21:59 2017

@author: ajaver
"""

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pylab as plt
import itertools
from matplotlib.backends.backend_pdf import PdfPages


#import matplotlib.pylab as plt
#from sklearn.preprocessing import normalize
#import seaborn as sns
#from sklearn.manifold import TSNE

np.random.seed(200)


valid_strains = ['CB4852', 'LSJ1', 'CB4856', 'ED3017', 'N2', 'MT9455', 'CB101']

train_df = pd.read_csv('train_feat_means.csv')
test_df = pd.read_csv('test_feat_means.csv')

test_df = test_df[test_df['strain'].isin(valid_strains)]
train_df = train_df[train_df['strain'].isin(valid_strains)]

bad_base_name = list(set(train_df['base_name']) & set(test_df['base_name']))
train_df = train_df[~train_df['base_name'].isin(bad_base_name)]
test_df = test_df[~test_df['base_name'].isin(bad_base_name)]
assert not len(set(train_df['base_name']) & set(test_df['base_name']))



strain_dict = {ss:ii for ii,ss in enumerate(train_df['strain'].unique())}

indexes_feats = train_df.columns[:8]

good_feats = [x for x in train_df.columns if x not in indexes_feats]
X_train = train_df.loc[:, good_feats]
Y_train, _ = pd.factorize(train_df['strain'].map(strain_dict))


frac_bad = X_train.isnull().mean()
good_feats = frac_bad.index[(frac_bad<0.05)]
X_train = X_train.loc[:, good_feats]

#frac_bad = X.isnull().mean(axis=1)
#good_index = frac_bad.index[(frac_bad<0.05)]
#X = X.loc[good_index]

t_mean = X_train.mean()
t_std = X_train.std()

X_train = X_train.apply(lambda x: x.fillna(x.mean()),axis=0) #replace with mean
X_train = (X_train - t_mean)/t_std


X_test = test_df.loc[:, good_feats]
X_test = X_test.apply(lambda x: x.fillna(x.mean()),axis=0) #replace with mean
X_test = (X_test - t_mean)/t_std

Y_test, _ = pd.factorize(test_df['strain'].map(strain_dict))

#%%
#pca = PCA(n_components=2)
#X_pca = pca.fit_transform(X_train)
#
#df = pd.DataFrame(X_pca, columns = ['x', 'y'])
#df['strain'] = train_df['strain']
#sns.lmplot('x', 
#           'y',
#           data=df,
#           hue="strain", 
#           fit_reg=False)
##%%
#
#model = TSNE(n_components=2, perplexity=5, random_state=0)
#pca = PCA(n_components=50)
#X_pca = pca.fit_transform(X_train)
#Xf = model.fit_transform(X_pca)
#
#df = pd.DataFrame(Xf, columns = ['x', 'y'])
#df['strain'] = train_df['strain']
#sns.lmplot('x', 
#           'y',
#           data=df,
#           hue="strain", 
#           fit_reg=False)

#%%

def _get_proba(clf, x_test, y_test):
    proba = clf.predict_proba(x_test)
    top_pred = np.argsort(proba, axis=1)[: ,::-1]
    preds = top_pred==y_test[:, np.newaxis]
    
    top1 = np.sum(preds[:, 0])/preds.shape[0]
    top2 = np.sum(preds[:, 0:2])/preds.shape[0]
    
    
    return top1, top2

def plot_confusion_matrix(clf, x_test, y_test, classes):
    y_pred = clf.predict(x_test)
    cm = confusion_matrix(y_test, y_pred)
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    fig = _plot_confusion_matrix(cm, classes)
    return fig


def _plot_confusion_matrix(cm, classes):
    #based on http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
    
    cmap=plt.cm.Blues
    fig = plt.figure(figsize=(7,7))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    np.set_printoptions(precision=2)
    
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, '%1.2f' % cm[i, j],
                 horizontalalignment="center",
                 fontsize =12,
                 color="white" if cm[i, j] > thresh else "black")
    #plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    return fig
#%%

def get_RF(count=None):
    clf_tree = RandomForestClassifier(n_estimators=10000)
    clf_tree.fit(X_train, Y_train)
    result = _get_proba(clf_tree, X_test, Y_test)
    
    if count is None:
        print('Random Forest')
        print('Top1', result[0])
        print('Top2', result[1])
    else:
        print(count, 'Random Forest')
    
    return clf_tree, result
#Top1 0.720812182741
#Top2 0.878172588832



#%%
def get_SVM(count=None):
    clf_svm = svm.SVC(kernel='linear', decision_function_shape='ovr', probability=True)
    clf_svm.fit(X_train, Y_train)
    result = _get_proba(clf_svm, X_test, Y_test)
    
    
    if count is None:
        print('SVM')
        print('Top1', result[0])
        print('Top2', result[1])
    else:
        print(count, 'SVM')
    
    return clf_svm, result
#Top1 0.736040609137
#Top2 0.903553299492

clf_tree, _ = get_RF()
clf_svm, _ = get_SVM()

names2change = {
        'MT9455':'tbh-1',
        'CB101':'unc-9',
        }
classes = sorted(strain_dict.keys(), key=lambda x: strain_dict[x])
classes = [x if not x in names2change else names2change[x] for x in classes]


fig_SVM = plot_confusion_matrix(clf_svm, X_test, Y_test, classes)
plt.title('SVM')

fig_RF = plot_confusion_matrix(clf_tree, X_test, Y_test, classes)
plt.title('Random Forest')

new_pred = pd.read_excel('nips_confusion_table.xlsx', names=['true','pred'])
cm = confusion_matrix(new_pred['true'], new_pred['pred'], labels=classes)
cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
fig_lstm = _plot_confusion_matrix(cm, classes)
plt.title('LSTM')


with PdfPages('confusion_matrix.pdf') as pdf:
    for fig in [fig_RF, fig_SVM, fig_lstm]:
        pdf.savefig(fig)
        
#%%
import multiprocessing as mp

def dum_svm(x):
    return get_SVM(x)[1]

def dum_rf(x):
    return get_RF(x)[1]

def print_results(dat_avg):
    np.set_printoptions(precision=5)
    d_mean = np.mean(dat_avg, axis=0)
    d_std = np.std(dat_avg, axis=0)
    for ii, (m,s) in enumerate(zip(d_mean, d_std)):
        print('T%i %2.3f ± %2.3f' % (ii, m*100,s*100))

    
p = mp.Pool()                         # Create a multiprocessing Pool
SVM_avg = p.map(dum_svm, range(100))
RF_avg = p.map(dum_rf, range(100))


print('SVM')
print_results(SVM_avg)

print('Random Forest')
print_results(RF_avg)


#%%
#pca = PCA(n_components=25)
#pca.fit(X_train)
#X_train_pca = pca.transform(X_train)
#X_test_pca = pca.transform(X_test)
#
#clf_svm_pca = svm.SVC(kernel='linear', decision_function_shape='ovr', probability=True)
#clf_svm_pca.fit(X_train_pca, Y_train)  
#print('SVM + PCA')
#_print_proba(clf_svm_pca, X_test_pca, Y_test)
#%%


#clf_lin = svm.LinearSVC()
#clf_lin.fit(X_train, Y_train)  
#preds = clf_lin.predict(X_test)
#print(np.sum(Y_test == preds)/Y_test.size)

#%%


strain_counts = pd.DataFrame()
strain_counts['train'] = train_df['strain'].value_counts()
strain_counts['test'] = test_df['strain'].value_counts()


#strain_counts.loc['Total', :] = np.sum(strain_counts)
print(strain_counts)