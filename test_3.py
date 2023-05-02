import time
import winsound

from PySide2 import QtGui
from PySide2.QtCore import QTimer, Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QGroupBox

import random
random.seed(time.perf_counter())


class Test3(QWidget):
    testFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.testName = 'Sound Test'
        self.settingsTab = parent.settingsTab

        self.startTimes = []
        self.endTimes = []
        self.unnecessaryClicks = 0
        self.stimulusShown = False

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
        if self.remainingTime > 0:
            self.remainingTime -= 1
        else:
            self.timer.stop()
            QTimer.singleShot(1000, self.showStimulus)

    def startTest(self):
        self.startButton.setEnabled(False)
        self.touchButton.setEnabled(True)

        self.trainTrials = self.settingsTab.trainTrialsSpinbox.value()
        self.trainTrialsLeft = self.trainTrials
        self.testTrials = self.settingsTab.testTrialsSpinbox.value()
        self.testTrialsLeft = self.testTrials
        self.prepareTrial()

    def prepareTrial(self):
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.countdown)
        self.remainingTime = self.settingsTab.timeTrialsSpinbox.value()
        self.timer.start()

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

        winsound.Beep(440, 500)
        self.startTime = time.perf_counter()
        self.stimulusShown = True

    def showStimulus(self):
        maxWaitingTime = self.settingsTab.timeTrialsSpinbox.value() * 1000
        waitingTime = random.randint(0, maxWaitingTime)
        self.timer = QTimer(self)
        self.timer.setInterval(waitingTime)
        self.timer.timeout.connect(self.startTrial)
        self.timer.start()

    def onButtonClick(self):
        if not self.stimulusShown:
            self.unnecessaryClicks += 1
            return

        self.stimulusShown = False
        self.endTime = time.perf_counter()
        self.startTimes.append(self.endTime - self.startTime)

        if self.trainTrialsLeft > 0:
            self.trainTrialsLeft -= 1
        else:
            self.testTrialsLeft -= 1

            if self.testTrialsLeft == 0:
                self.endTest()
                return

        self.prepareTrial()

    def endTest(self):
        self.endTimes = self.startTimes[self.trainTrials:]
        self.averageTime = sum(self.endTimes) / len(self.endTimes)
        self.unnecessaryClicksNum = self.unnecessaryClicks
        self.startButton.setEnabled(True)
        self.touchButton.setEnabled(False)

        self.unnecessaryClicks = 0
        self.stimulusShown = False

        self.testFinished.emit()

        mainWindow = self.window()
        mainWindow.resultsTab.updateResultsTest3(self.averageTime, self.unnecessaryClicksNum, self.endTimes)
