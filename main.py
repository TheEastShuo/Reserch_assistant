import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

import MainWin

if __name__ == '__main__':

    app = QApplication([])
    app.setWindowIcon(QIcon('图标.ico'))
    stat = MainWin.Status()

    stat.ui.show()
    app.exec()




