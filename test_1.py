import time
from functools import partial

from PySide2 import QtGui
from PySide2.QtCore import QTimer, Qt, Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QGroupBox, QHBoxLayout, QFrame

import random
random.seed(time.perf_counter())


class Test1(QWidget):
    testFinished = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.testName = 'Stroop Test'
        self.settingsTab = parent.settingsTab

        self.colorButtons = []
        self.startTimes = []
        self.endTimes = []
        self.correctClicks = 0
        self.testInProgress = False

        self.infoLabel = QLabel("INSTRUCTION: Click the button that corresponds to the text color.")
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

        self.colors = ['black', 'blue', 'green', 'orange', 'purple', 'red']
        self.colorButtonsLayout = QHBoxLayout()
        for color in self.colors:
            colorButton = QPushButton(color)
            colorButton.clicked.connect(partial(self.onButtonClick, colorButton, color))
            self.colorButtonsLayout.addWidget(colorButton)
            self.colorButtons.append(colorButton)
        self.setColorButtonsEnabled(False)

        self.testLabel = QLabel()
        self.testLabel.setFrameStyle(QFrame.Box | QFrame.Plain)
        self.testLabel.setAlignment(Qt.AlignCenter)
        font = self.testLabel.font()
        font.setPointSize(18)
        self.testLabel.setFont(font)

        self.testGroupBox = QGroupBox("Test")
        testLayout = QVBoxLayout(self.testGroupBox)
        testLayout.addWidget(self.testLabel)
        testLayout.addLayout(self.colorButtonsLayout)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.infoGroupBox)
        self.layout.addWidget(self.testGroupBox)
        self.setLayout(self.layout)

    def setColorButtonsEnabled(self, enabled):
        for button in self.colorButtons:
            button.setEnabled(enabled)

    def countdown(self):
        if self.remainingTime > 0:
            self.testLabel.setText(f"{self.remainingTime}")
            self.remainingTime -= 1
        else:
            self.timer.stop()
            self.testLabel.setText("Start")
            QTimer.singleShot(1000, self.startTrial)

    def startTest(self):
        self.startButton.setEnabled(False)
        self.setColorButtonsEnabled(True)

        self.trainTrials = self.settingsTab.trainTrialsSpinbox.value()
        self.trainTrialsLeft = self.trainTrials
        self.testTrials = self.settingsTab.testTrialsSpinbox.value()
        self.testTrialsLeft = self.testTrials
        self.prepareTrial()

    def prepareTrial(self):
        self.clearLayout()

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
        word = random.choice(self.colors)
        color = random.choice(self.colors)

        self.correctColor = color
        self.testLabel.setText(word)
        self.testLabel.setStyleSheet(f"color: {color}")

        self.startTime = time.perf_counter()
        self.testInProgress = True

    def prepareNextTrial(self):
        self.clearLayout()
        QTimer.singleShot(1000, self.prepareTrial)

    def onButtonClick(self, button, selectedColor):
        if not self.testInProgress:
            return

        self.testInProgress = False
        self.endTime = time.perf_counter()
        self.startTimes.append(self.endTime - self.startTime)

        correct = selectedColor == self.correctColor

        if self.trainTrialsLeft > 0:
            self.updateButtonColor(button, correct)
            QTimer.singleShot(1000, self.prepareNextTrial)
            self.trainTrialsLeft -= 1
        else:
            if correct:
                self.correctClicks += 1

            self.testTrialsLeft -= 1
            if self.testTrialsLeft == 0:
                self.endTest()
                return

            self.prepareNextTrial()

    @staticmethod
    def updateButtonColor(button, correct):
        if correct:
            button.setStyleSheet("background-color: green")
        else:
            button.setStyleSheet("background-color: red")

    def clearLayout(self):
        if hasattr(self, 'testLabel'):
            self.testLabel.setText("")
            self.testLabel.setStyleSheet("")

        for button in self.colorButtons:
            button.setStyleSheet("")

    def endTest(self):
        self.endTimes = self.startTimes[self.trainTrials:]
        self.averageTime = sum(self.endTimes) / len(self.endTimes)
        self.correctClicksPercentage = (self.correctClicks / self.testTrials) * 100
        self.startButton.setEnabled(True)

        self.correctClicks = 0
        self.testInProgress = False
        self.clearLayout()
        self.testFinished.emit()

        mainWindow = self.window()
        mainWindow.resultsTab.updateResultsTest1(self.averageTime, self.correctClicksPercentage, self.endTimes)
