#!/usr/bin/env python
#-*- coding:utf-8 -*-

#---------
# IMPORT
#---------
import sys, os

from PyQt4 import QtGui, QtCore

#---------
# DEFINE
#---------
class MyListWidget(QtGui.QListWidget):
    dropped = QtCore.pyqtSignal(list)

    def __init__(self, type, parent=None):
        super(MyListWidget, self).__init__(parent)

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()

        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

            filePaths = [
                str(url.toLocalFile())
                for url in event.mimeData().urls()
            ]

            self.dropped.emit(filePaths)

        else:
            event.ignore()

class MyWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.listWidgetFiles = MyListWidget(self)
        self.listWidgetFiles.dropped.connect(self.on_listWidgetFiles_dropped)

        self.layoutVertical = QtGui.QVBoxLayout(self)
        self.layoutVertical.addWidget(self.listWidgetFiles)

    @QtCore.pyqtSlot(list)
    def on_listWidgetFiles_dropped(self, filePaths):
        for filePath in filePaths:
            if os.path.exists(filePath):
                QtGui.QListWidgetItem(filePath, self.listWidgetFiles)

#---------
# MAIN
#---------
if __name__ == "__main__":        
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(333, 111)
    main.show()

    sys.exit(app.exec_())