import sys
import os
import tables
import pandas as pd
import numpy as np
from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen, QColor
from PyQt5.QtCore import Qt

from image_labeler_ui import Ui_image_labeler

from MWTracker.GUI_Qt5.TrackerViewerAux import TrackerViewerAux_GUI
from MWTracker.GUI_Qt5.HDF5VideoPlayer import lineEditDragDrop, setChildrenFocusPolicy

class d_Ui_image_labeler(Ui_image_labeler):
	def __init__(self):
		super().__init__()

	def setupUi(self, image_labeler):
		#widgets that are not present in Ui_image_labeler, but are required by TrackerViewerAux_GUI.
		#we just create dummy objects here
		super().setupUi(image_labeler)
		self.playButton = QtWidgets.QPushButton()
		self.pushButton_skel = QtWidgets.QPushButton()
		self.lineEdit_skel = QtWidgets.QLineEdit()
		self.imageSlider = QtWidgets.QSlider()
		self.doubleSpinBox_fps = QtWidgets.QDoubleSpinBox()
		self.spinBox_step = QtWidgets.QDoubleSpinBox()
		self.spinBox_frame = QtWidgets.QDoubleSpinBox()

class image_labeler_GUI(TrackerViewerAux_GUI):

	def __init__(self, mask_file=''):
		super().__init__(d_Ui_image_labeler())
		
		self.btn_colors = {1:'red', 2:'green', 3:'yellow', 4:'blue'}
		self.buttons = {1:self.ui.pushButton_bad, 
						2:self.ui.pushButton_worm,
						3:self.ui.pushButton_worm_hard,
						4:self.ui.pushButton_aggregate}

		self._setup_buttons()
		self.ui.spinBox_samp_ord.valueChanged.connect(self.updateSampleNumber)

		self.sample_number = 0
		self.ui.spinBox_samp_ord.setValue(0)


		mask_file = '/Users/ajaver/OneDrive - Imperial College London/training_data/worm_ROI_samples.hdf5'
		if mask_file:
			self.updateVideoFile(mask_file)

	def updateVideoFile(self, vfilename):
		if self.fid != -1:
			self.fid.close()

		with pd.HDFStore(vfilename) as fid:
			self.sample_data = fid['/sample_data']

		if not 'resampled_index' in self.sample_data:
			self.sample_data['resampled_index'] = np.random.permutation(len(self.sample_data))
		self.sample_data['img_row_id'] = self.sample_data.index
		self.sample_data.index = self.sample_data['resampled_index'].values
		
		if not 'label_id' in self.sample_data:
			self.sample_data['label_id'] = 0

		#i want to use the father of TrackerViewerAux_GUI (i do not need the skeleton file updates)
		super(TrackerViewerAux_GUI, self).updateVideoFile(vfilename)
		self.ui.spinBox_samp_ord.setMaximum(self.tot_frames - 1)
		
	def updateImGroup(self):
		super().updateImGroup()
		self.updateSampleNumber()



	def keyPressEvent(self, event):
		if self.fid == -1:
			# break no file open, nothing to do here
			return

		key = event.key()

		# Move backwards when  are pressed
		if key == Qt.Key_Left:
			self.ui.spinBox_samp_ord.setValue(self.sample_number - 1)
		# Move forward when  are pressed
		elif key == Qt.Key_Right:
			self.ui.spinBox_samp_ord.setValue(self.sample_number + 1)
		
		elif key == Qt.Key_Minus:
			self.mainImage.zoom(-1)
		elif key == Qt.Key_Plus:
			self.mainImage.zoom(1)
		elif key == Qt.Key_1:
			self.ui.pushButton_bad.toggle()
		elif key == Qt.Key_2:
			self.ui.pushButton_worm.toggle()
		elif key == Qt.Key_3:
			self.ui.pushButton_worm_hard.toggle()
		elif key == Qt.Key_4:
			self.ui.pushButton_aggregate.toggle()

		else:
			print(key)
			QtWidgets.QMainWindow.keyPressEvent(self, event)


	def updateSampleNumber(self):
		self.sample_number = self.ui.spinBox_samp_ord.value()
		self.frame_number = int(self.sample_data.loc[self.sample_number, 'img_row_id'])
		
		self.updateImage()
		label_id = int(self.sample_data.loc[self.sample_number, 'label_id'])
		if label_id >0:
			self.buttons[label_id].setChecked(True)
		else:
			for btn in self.buttons.values():
				btn.setChecked(False)

	def _setup_buttons(self):
		stylesheet_str = "QPushButton:checked {border: 2px solid; border-radius: 6px; background-color: %s }"
		def _make_label(label_id, checked):
			if checked:
				for btn_id, btn in self.buttons.items():
					if btn_id != label_id:
						btn.setChecked(False)

			if self.fid != -1:
				if checked:
					#add label
					self.sample_data.loc[self.sample_number, 'label_id'] = label_id
				else:
					old_lab = self.sample_data.loc[self.sample_number, 'label_id']
					if old_lab == label_id:
						#if the labeld was unchecked remove the label
						self.sample_data.loc[self.sample_number, 'label_id'] = 0
				

		for btn_id, btn in self.buttons.items():
			btn.setCheckable(True)
			btn.setStyleSheet(stylesheet_str % self.btn_colors[btn_id])
			btn.toggled.connect(partial(_make_label, btn_id))

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	ui = image_labeler_GUI()
	ui.show()
	sys.exit(app.exec_())