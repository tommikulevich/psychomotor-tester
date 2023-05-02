import sys
from PySide2.QtWidgets import QApplication

from main_window import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainWindow()
    main_app.show()
    sys.exit(app.exec_())
