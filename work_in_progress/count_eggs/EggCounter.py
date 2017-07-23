import sys
import os
import numpy as np
import time
import pandas as pd

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QPointF
from tierpsy.gui.HDF5VideoPlayer import HDF5VideoPlayerGUI

mask_file = '/Users/ajaver/OneDrive - Imperial College London/optogenetics/Arantza/MaskedVideos/control_pulse/pkd2_5min_Ch1_11052017_121414.hdf5'
assert os.path.exists(mask_file)


MIN_DIST = 5
TIME_BTW_PRESS_RELEASE = 0.5
MARKER_DIAMETER = 3
class EggCounterGUI(HDF5VideoPlayerGUI):
    def __init__(self):
        super().__init__()
        #self._canvas_enter_event = self.mainImage._canvas.enterEvent
        #self.mainImage._scene.enterEvent = self.enter_event


        self._canvas_press_event = self.mainImage._canvas.mousePressEvent
        self.mainImage._canvas.mousePressEvent = self.press_event
        
        self._canvas_release_event = self.mainImage._canvas.mouseReleaseEvent
        self.mainImage._scene.mouseReleaseEvent = self.release_event

        self.eggs = {}

        self.updateVideoFile(mask_file)
    
    def updateImage(self):
        super().updateImage()
        
        if not self.h5path in self.eggs or \
            not self.frame_number in self.eggs[self.h5path]:
            return

        current_list = self.eggs[self.h5path][self.frame_number]

        painter = QPainter()
        painter.begin(self.frame_qimg)
        pen = QPen()
        
        pen.setWidth(2)
        pen.setColor(Qt.red)
        painter.setPen(pen)
        
        for (x,y) in current_list:
            center = QPointF(x, y)
            painter.drawEllipse(center, MARKER_DIAMETER, MARKER_DIAMETER)
        painter.end()
        
        self.mainImage.setPixmap(self.frame_qimg)

    
    def release_event(self, event):
        self._canvas_release_event(event)
        #if the delay between the release and the press is too large it means that the user is dragging
        #in that case do not add the coordinate
        if time.time() - self.enter_time > TIME_BTW_PRESS_RELEASE:
            return

        self._add_coordinate(self.m_x, self.m_y)
        self.updateImage()

    def press_event(self, event):
        self.enter_time = time.time()
        self.m_x = event.pos().x()
        self.m_y = event.pos().y()
        self._canvas_press_event(event)
    

    def _add_coordinate(self, x, y):
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

    def _eggs_to_table(self):
        data = []
        for gg, frame_data in self.eggs.items():
            for frame, coords in frame_data.items():
                data += [(gg, frame, x,y) for x,y in coords]
        
        return pd.DataFrame(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = EggCounterGUI()
    ui.show()

    sys.exit(app.exec_())
