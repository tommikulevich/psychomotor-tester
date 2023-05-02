from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QSpinBox, QGridLayout, QGroupBox


class SettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.trainTrialsSpinbox = QSpinBox()
        self.trainTrialsSpinbox.setRange(1, 20)
        self.trainTrialsSpinbox.setValue(3)

        self.testTrialsSpinbox = QSpinBox()
        self.testTrialsSpinbox.setRange(1, 20)
        self.testTrialsSpinbox.setValue(5)

        self.timeTrialsSpinbox = QSpinBox()
        self.timeTrialsSpinbox.setRange(1, 60)
        self.timeTrialsSpinbox.setValue(3)

        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startTests)

        self.trialsGroupBox = QGroupBox("Number of trials")
        trialsLayout = QGridLayout(self.trialsGroupBox)
        trialsLayout.addWidget(QLabel("Train [1-20]:"), 0, 0)
        trialsLayout.addWidget(self.trainTrialsSpinbox, 0, 1)
        trialsLayout.addWidget(QLabel("Test [1-20]:"), 1, 0)
        trialsLayout.addWidget(self.testTrialsSpinbox, 1, 1)

        self.timeGroupBox = QGroupBox("Maximum time between trials")
        timeLayout = QGridLayout(self.timeGroupBox)
        timeLayout.addWidget(QLabel("Time in sec [1-60]:"), 0, 0)
        timeLayout.addWidget(self.timeTrialsSpinbox, 0, 1)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.trialsGroupBox)
        self.layout.addWidget(self.timeGroupBox)
        self.layout.addWidget(self.startButton)
        self.setLayout(self.layout)

    def startTests(self):
        mainWindow = self.window()

        mainWindow.tabWidget.setTabEnabled(1, True)
        mainWindow.tabWidget.setCurrentIndex(1)
        mainWindow.tabWidget.setTabEnabled(0, False)

        mainWindow.resultsTab.updateResultsMain()
