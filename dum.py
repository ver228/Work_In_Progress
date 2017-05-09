#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 17:03:17 2017

@author: ajaver
"""
import os

ff = '''/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/no_waiting/unknown/N2 on food no wait_2012_04_03__12_17_01___8___1.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/mutants/unc-4(gk705)II@VC1528/food_OP50/XX/30m_wait/anticlockwise/unc-4 (gk705)II on food R_2011_08_11__12_20___3___8.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/anticlockwise/N2 on food R_2010_03_31__10_54___3___1.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/unknown/N2 L3 on food _2012_02_10__09_37___3___2.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/mutants/unc-40(n324)I@MT324/food_OP50/XX/30m_wait/clockwise/unc-40 (n324)I on food L_2010_04_13__14_38___3___10.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/unknown/N2 on food_2009_12_14__10_20_09___2___1.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/mutants/unc-104(e1265)II@CB1265/food_OP50/XX/30m_wait/clockwise/unc-101 (e1265) on food L_2010_09_17__16_05_25___2___8.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/mutants/trp-2(gk298)III@VC602/no_food/XX/30m_wait/unknown/trp-2 (ok298) off food_2010_04_30__13_08_25___2___7.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/mutants/unc-34(e566)V@CB566/food_OP50/XX/30m_wait/anticlockwise/unc-34on food R_2010_08_06__14_38_27___7___9.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/ED3054/food_OP50/XX/30m_wait/anticlockwise/507 ED3054 on food R_2011_03_22__13_07___3___6.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/unnamed/RB557 cam IL2 1 on food  R_2015_08_20__17_23_37___3___6.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/unnamed/Qt1084 unc-80 nRHO-1 nUNC-80 ttx GFP on food L_2012_09_25__12_21_26___8___6.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/PS312/food_N2-L4/XX/30m_wait/unknown/197 PS312 2 on N2-L4_2011_06_24__11_32_32___2___1.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/unknown/N2 on food_2011_04_11__17_03_36__2.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/ED3054/food_OP50/XX/30m_wait/anticlockwise/507 ED3054 on food R_2011_02_25__11_11_56__3.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/unknown/N2 on food _2011_04_11__16_43_04___7___1.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/JU440/food_OP50/XX/30m_wait/clockwise/575 JU440 on food L_2011_02_25__11_11_41___7___4.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/ED3054/food_OP50/XX/30m_wait/unknown/507 ED3059_2011_03_04__12_20_44___8___5.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/unknown/N2 on food_2011_07_13__15_32_21___8___1.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/unknown/N2 on food_2011_07_15__11_10_36___8___1.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/mutants/ocr-3(ok1559)X@RB1374/no_food/XX/30m_wait/unknown/ocr-3 (ok1557) off food _2010_04_28__11_01_12___2___3.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/mutants/trpa-1(ok999)IV@RB1052/no_food/XX/30m_wait/unknown/trpa-1 (ok999)off food _2010_04_28__14_50_29___2___6.hdf5
/Volumes/behavgenom_archive$/single_worm/unfinished/WT/N2/food_OP50/XX/30m_wait/unknown/N2 on food_2011_04_11__16_39_31___2___1.hdf5'''


fnames = ff.split('\n')

for fname in fnames:
    feat_file = fname.replace('.hdf5', '_features.hdf5')
    int_file = fname.replace('.hdf5', '_intensities.hdf5')
    
    if os.path.exists(feat_file):
        os.remove(feat_file)
    if os.path.exists(int_file):
        os.remove(int_file)

