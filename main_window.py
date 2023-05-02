from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget, QApplication, QStyle

from settings_tab import SettingsTab
from test_1 import Test1
from test_2 import Test2
from test_3 import Test3
from test_4 import Test4
from results_tab import ResultsTab


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tester')
        self.setWindowIcon(QIcon(QApplication.instance().style().standardPixmap(QStyle.SP_FileDialogListView)))

        # Window elements creation and configuration
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.tabWidget = QTabWidget()
        self.layout = QVBoxLayout(self.centralWidget)
        self.layout.addWidget(self.tabWidget)

        # Add settings tab
        self.settingsTab = SettingsTab(self)
        self.tabWidget.addTab(self.settingsTab, "Settings")

        # Add tests tabs
        self.addTest(Test1(self))
        self.addTest(Test2(self))
        self.addTest(Test3(self))
        self.addTest(Test4(self))

        # Add results tab
        self.resultsTab = ResultsTab(self)
        self.tabWidget.addTab(self.resultsTab, "Results")

        # Disable all tabs except the first one
        for i in range(1, self.tabWidget.count()):
            self.tabWidget.setTabEnabled(i, False)

        self.adjustSize()

    def addTest(self, testWidget):
        self.tabWidget.addTab(testWidget, testWidget.testName)
        testWidget.testFinished.connect(self.switchToNext)

    def switchToNext(self):
        # Switch to the next tab
        currentIndex = self.tabWidget.currentIndex()
        if currentIndex + 1 < self.tabWidget.count():
            self.tabWidget.setTabEnabled(currentIndex, False)
            self.tabWidget.setCurrentIndex(currentIndex + 1)
            self.tabWidget.setTabEnabled(currentIndex + 1, True)
        else:
            self.tabWidget.setCurrentIndex(0)

        self.adjustSize()
