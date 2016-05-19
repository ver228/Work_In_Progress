from PyQt4.QtGui import QApplication, QWidget
import sys

if __name__ == '__main__':
    print('HOLA')
    
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('Simple')
    w.show()
    
    print('HOLA')
    sys.exit(app.exec_()) 