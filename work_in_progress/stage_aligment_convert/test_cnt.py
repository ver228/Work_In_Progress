#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 21:38:46 2017

@author: ajaver
"""

from tierpsy.analysis.contour_orient.correctVentralDorsal import switchCntSingleWorm

from tierpsy.analysis.contour_orient.correctVentralDorsal import isBadVentralOrient

skeletons_file = '/Volumes/behavgenom_archive$/single_worm/finished/mutants/egl-12(n602)V@MT1232/food_OP50/XX/30m_wait/anticlockwise/egl-12 (n602)V on food R_2010_07_16__12_06_45___4___6_skeletons.hdf5'
switchCntSingleWorm(skeletons_file)