#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:16:02 2017

@author: ajaver
"""
from tensorflow.contrib import keras
load_model = keras.models.load_model

load_model('unet_norm_w_no_bn-04249-0.3976.h5'),
load_model('unet_norm_w_no_bn_cnt-03499-1.1672.h5')