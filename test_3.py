import time
import winsound

from PySide2 import QtGui
from PySide2.QtCore import QTimer, Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QGroupBox

import random
random.seed(time.perf_counter())


class Test3(QWidget):
    testFinished = Signal()  # Signal that is emitted after the end of the test

    def __init__(self, parent=None):
        super().__init__(parent)
        self.testName = 'Sound Test'
        self.settingsTab = parent.settingsTab

        # Test parameters
        self.startTimes = []
        self.endTimes = []
        self.unnecessaryClicks = 0
        self.stimulusShown = False

        # Window elements creation and configuration
        self.infoLabel = QLabel("INSTRUCTION: Press the 'Click' button when you hear a sound.")
        self.phaseLabel = QLabel("Phase: -")
        self.trialLabel = QLabel("Trial: -")
        self.startButton = QPushButton("Start")
        self.startButton.clicked.connect(self.startTest)

        self.infoGroupBox = QGroupBox("Info")
        infoLayout = QVBoxLayout(self.infoGroupBox)
        infoLayout.addWidget(self.infoLabel)
        infoLayout.addWidget(self.phaseLabel)
        infoLayout.addWidget(self.trialLabel)
        infoLayout.addWidget(self.startButton)

        self.touchButton = QPushButton("Click")
        self.touchButton.clicked.connect(self.onButtonClick)
        self.touchButton.setEnabled(False)

        self.testGroupBox = QGroupBox("Test")
        testLayout = QVBoxLayout(self.testGroupBox)
        testLayout.addWidget(self.touchButton)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.infoGroupBox)
        self.layout.addWidget(self.testGroupBox)
        self.setLayout(self.layout)

    def countdown(self):
        # Counting from value in timeTrialsSpinbox to 0 (start)
        if self.remainingTime > 0:
            self.remainingTime -= 1
        else:
            self.timer.stop()
            QTimer.singleShot(1000, self.showStimulus)

    def startTest(self):
        # Configure buttons
        self.startButton.setEnabled(False)
        self.touchButton.setEnabled(True)

        # Get parameters from settings
        self.trainTrials = self.settingsTab.trainTrialsSpinbox.value()
        self.trainTrialsLeft = self.trainTrials
        self.testTrials = self.settingsTab.testTrialsSpinbox.value()
        self.testTrialsLeft = self.testTrials
        self.prepareTrial()

    def prepareTrial(self):
        # Create timer to count from value in timeTrialsSpinbox to 0 (start)
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.countdown)
        self.remainingTime = self.settingsTab.timeTrialsSpinbox.value()
        self.timer.start()

        # Update info labels
        if self.trainTrialsLeft > 0:
            self.phaseLabel.setText("Phase: train")
            font = QtGui.QFont()
            font.setBold(False)
            self.phaseLabel.setFont(font)
        else:
            self.phaseLabel.setText("Phase: test")
            font = QtGui.QFont()
            font.setBold(True)
            self.phaseLabel.setFont(font)

        trialNum = self.trainTrials - self.trainTrialsLeft + 1 if self.trainTrialsLeft > 0 else self.testTrials - self.testTrialsLeft + 1
        allTrials = self.trainTrials if self.trainTrialsLeft > 0 else self.testTrials
        self.trialLabel.setText(f"Trial: {trialNum}/{allTrials}")

    def startTrial(self):
        self.timer.stop()

        # Produce a simple beep sound
        winsound.Beep(440, 500)

        # Get time of start and update flag
        self.startTime = time.perf_counter()
        self.stimulusShown = True

    def showStimulus(self):
        # Sound will be turned on at random moment before maxWaitingTime
        maxWaitingTime = self.settingsTab.timeTrialsSpinbox.value() * 1000
        waitingTime = random.randint(0, maxWaitingTime)

        self.timer = QTimer(self)
        self.timer.setInterval(waitingTime)
        self.timer.timeout.connect(self.startTrial)
        self.timer.start()

    def onButtonClick(self):
        # Check if there is no stimulus
        if not self.stimulusShown:
            self.unnecessaryClicks += 1
            return

        # Update flags. Get time of the end. Calculate the difference between start and end time
        self.stimulusShown = False
        self.endTime = time.perf_counter()
        self.startTimes.append(self.endTime - self.startTime)

        if self.trainTrialsLeft > 0:    # Train phase
            self.trainTrialsLeft -= 1
        else:   # Test phase
            self.testTrialsLeft -= 1

            if self.testTrialsLeft == 0:
                self.endTest()
                return

        self.prepareTrial()

    def endTest(self):
        # Summarizing results
        self.endTimes = self.startTimes[self.trainTrials:]
        self.averageTime = sum(self.endTimes) / len(self.endTimes)
        self.unnecessaryClicksNum = self.unnecessaryClicks
        self.startButton.setEnabled(True)
        self.touchButton.setEnabled(False)

        # Reset parameters and emit a signal of finishing (to switch to the next tab)
        self.unnecessaryClicks = 0
        self.stimulusShown = False
        self.testFinished.emit()

        # Update test section in the results tab
        mainWindow = self.window()
        mainWindow.resultsTab.updateResultsTest3(self.averageTime, self.unnecessaryClicksNum, self.endTimes)
