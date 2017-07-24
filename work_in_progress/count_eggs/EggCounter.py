import sys
import os
import numpy as np
import time
import pandas as pd
import cv2

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from tierpsy.gui.HDF5VideoPlayer import HDF5VideoPlayerGUI

#mask_file = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/MaskedVideos/control_pulse/pkd2_5min_Ch1_11052017_121414.hdf5'
#mask_file = '/Users/ajaver/OneDrive - Imperial College London/aggregation/N2_1_Ch1_29062017_182108_comp3.hdf5'
mask_file = '/Volumes/behavgenom_archive$/RigRawVideos/PC1/Syngenta_Agar_Screening_003_210717_1/SYN_003_Egg_Set_1_P1.bmp'
assert os.path.exists(mask_file)


MIN_DIST = 2
TIME_BTW_PRESS_RELEASE = 0.2

def _updateUI(ui):
    ui.horizontalLayout_6.removeWidget(ui.pushButton_h5groups)
    ui.pushButton_h5groups.deleteLater()
    ui.pushButton_h5groups = None

    ui.horizontalLayout_3.removeWidget(ui.doubleSpinBox_fps)
    ui.doubleSpinBox_fps.deleteLater()
    ui.doubleSpinBox_fps = None


    ui.horizontalLayout_3.removeWidget(ui.label_fps)
    ui.label_fps.deleteLater()
    ui.label_fps = None

    ui.number_of_eggs = QLabel(ui.centralWidget)
    ui.horizontalLayout_3.addWidget(ui.number_of_eggs)
    ui.number_of_eggs.setText("0 Eggs")

    ui.save_push_button = QPushButton(ui.centralWidget)
    ui.horizontalLayout_3.addWidget(ui.save_push_button)
    ui.save_push_button.setText("Save")

    return ui


class EggCounterGUI(HDF5VideoPlayerGUI):
    def __init__(self):
        super().__init__()

        self.ui = _updateUI(self.ui)
        self.is_new_eggs = False #flag to know if there are new egg events to save
        
        #default expected groups in the hdf5
        self.ui.comboBox_h5path.setItemText(1, "/mask")
        self.ui.comboBox_h5path.setItemText(0, "/full_data")

        #self._canvas_enter_event = self.mainImage._canvas.enterEvent
        #self.mainImage._scene.enterEvent = self.enter_event


        #self._canvas_press_event = self.mainImage._canvas.mousePressEvent
        #self.mainImage._canvas.mousePressEvent = self.press_event
        #self._canvas_release_event = self.mainImage._canvas.mouseReleaseEvent
        #self.mainImage._scene.mouseReleaseEvent = self.release_event
        
        self.mainImage._canvas.mouseDoubleClickEvent = self.doubleclick_event

        self.eggs = {}

        self.ui.save_push_button.clicked.connect(self.save_eggs_table)

        self.updateVideoFile(mask_file)
        self.mainImage.zoomFitInView()



    def updateVideoFile(self, vfilename):

        self._ask_saving()

        if vfilename.endswith('.hdf5'):
            super().updateVideoFile(vfilename)
        else:
            
            img = cv2.imread(vfilename, cv2.IMREAD_GRAYSCALE)

            if img is not None:

                self.ui.lineEdit_video.setText(self.vfilename)
                self.image_height = img.shape[0]
                self.image_width = img.shape[1]

                self.h5path = 'img'
                self.vfilename = vfilename
                self.tot_frames = 1            

                self.ui.spinBox_frame.setMaximum(self.tot_frames - 1)
                self.ui.imageSlider.setMaximum(self.tot_frames - 1)

                self.frame_number = 0
                self.ui.spinBox_frame.setValue(self.frame_number)
                
                self.frame_img = img

            else:
                self.fid = None
                self.image_group = None
                QMessageBox.critical(
                    self,
                    '',
                    "The selected file is not a valid.",
                    QMessageBox.Ok)

        self.load_eggs_table()
        

        self.updateImage()
        

    def updateImage(self):
        if self.fid is not None:
            self.readCurrentFrame()
        else:
            self._normalizeImage()

        self.mainImage._canvas.setCursor(Qt.CrossCursor)

        if not self.h5path in self.eggs or \
            not self.frame_number in self.eggs[self.h5path]:
            self.mainImage.setPixmap(self.frame_qimg)
            return

        current_list = self.eggs[self.h5path][self.frame_number]

        painter = QPainter()
        painter.begin(self.frame_qimg)
        pen = QPen()
        
        pen.setWidth(2)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        painter.setBrush(Qt.red)

        
        for (x,y) in current_list:
            painter.drawEllipse(x,y, 1,1)
            #painter.drawPoint(x,y)
        painter.end()
        
        self.mainImage.setPixmap(self.frame_qimg)

        n_eggs_txt = "{} Eggs".format(len(self.eggs[self.h5path][self.frame_number]))
        self.ui.number_of_eggs.setText(n_eggs_txt)

    def doubleclick_event(self, event):
        self.m_x = event.pos().x()
        self.m_y = event.pos().y()
        self._add_coordinate(self.m_x, self.m_y)
        self.updateImage()

    # def release_event(self, event):
    #     self._canvas_release_event(event)
    #     #if the delay between the release and the press is too large it means that the user is dragging
    #     #in that case do not add the coordinate
    #     if time.time() - self.enter_time > TIME_BTW_PRESS_RELEASE:
    #         return

    #     self._add_coordinate(self.m_x, self.m_y)
    #     self.updateImage()

    # def press_event(self, event):
    #     self.enter_time = time.time()
    #     self.m_x = event.pos().x()
    #     self.m_y = event.pos().y()
    #     self._canvas_press_event(event)
    

    def _add_coordinate(self, x, y):
        self.is_new_eggs = True

        if not self.h5path in self.eggs:
            self.eggs[self.h5path] = {}

        if not self.frame_number in self.eggs[self.h5path]:
            self.eggs[self.h5path][self.frame_number] = []

        current_list = self.eggs[self.h5path][self.frame_number]
        
        if not current_list:
            #add the element if the list if empty
            current_list.append((x,y))
        else:
            V = np.array(current_list)
            dx = x - V[:, 0]
            dy = y - V[:, 1]

            rr = np.sqrt(dx*dx + dy*dy)

            ind = np.argmin(rr)
            if rr[ind] <= MIN_DIST:
                #delete it if there was a click almost over a previous point
                del current_list[ind]
            else:
                #otherwise add it
                current_list.append((x,y))




    def save_eggs_table(self):
        if self.vfilename is not None:
            save_name = self._get_save_name(self.vfilename)
            df = self._eggs_to_table()
            df.to_csv(save_name, index=False)

    def _eggs_to_table(self):
        data = []
        for gg, frame_data in self.eggs.items():
            for frame, coords in frame_data.items():
                data += [(gg, frame, x,y) for x,y in coords]
        
        return pd.DataFrame(data, columns=['group_name', 'frame_number', 'x', 'y'])

    def _get_save_name(self, vfilename):
        return os.path.splitext(vfilename)[0] + '_eggs.csv'

    def load_eggs_table(self):
        self.eggs = {}
        self.is_new_eggs = False

        if self.vfilename is not None:
            save_name = self._get_save_name(self.vfilename)
            
            if os.path.exists(save_name):
                df = pd.read_csv(save_name)
                
                
                for gg, g_dat in df.groupby('group_name'):
                    if not gg in self.eggs:
                        self.eggs[gg] = {}
                    for frame_number, f_dat in g_dat.groupby('frame_number'):
                        self.eggs[gg][frame_number] = [(f['x'], f['y']) for i,f in f_dat.iterrows()]

    def _ask_saving(self):
        if self.is_new_eggs:
            quit_msg = "Do you want to save the current progress?"
            reply = QMessageBox.question(self, 
                                                   'Message',
                                                   quit_msg, 
                                                   QMessageBox.No | QMessageBox.Yes,
                                                   QMessageBox.Yes)
            

            if reply == QMessageBox.Yes:
                self.save_eggs_table()

    def closeEvent(self, event):
        self._ask_saving()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = EggCounterGUI()
    ui.show()

    sys.exit(app.exec_())
