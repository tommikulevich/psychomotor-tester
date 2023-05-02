import time

from PySide2 import QtGui
from PySide2.QtCore import QTimer, Qt, QRectF, QPointF, Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QGraphicsView, QGraphicsScene, QGroupBox, \
    QHBoxLayout
from PySide2.QtGui import QPen, QBrush

import random
random.seed(time.perf_counter())


class Test2(QWidget):
    testFinished = Signal()  # Signal that is emitted after the end of the test

    def __init__(self, parent=None):
        super().__init__(parent)
        self.testName = 'Touch Test'
        self.settingsTab = parent.settingsTab

        # Test parameters
        self.colors = ['black', 'blue', 'green', 'orange', 'purple', 'red']
        self.correctColor = random.choice(self.colors)
        self.startTimes = []
        self.endTimes = []
        self.wrongClicks = 0
        self.correctClicks = 0
        self.unnecessaryClicks = 0
        self.stimulusShown = False

        # Window elements creation and configuration
        self.infoLabel = QLabel(f"INSTRUCTION: Press the 'Click' button when you see the {self.correctColor} rectangle"
                                f"or the 'No Click' button when not.")
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

        self.graphicsView = QGraphicsView()
        self.clickButton = QPushButton("Click")
        self.clickButton.clicked.connect(self.onButtonClick)
        self.clickButton.setEnabled(False)
        self.noClickButton = QPushButton("No Click")
        self.noClickButton.clicked.connect(self.onNoClickButton)
        self.noClickButton.setEnabled(False)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.addWidget(self.clickButton)
        buttonsLayout.addWidget(self.noClickButton)

        self.testGroupBox = QGroupBox("Test")
        testLayout = QVBoxLayout(self.testGroupBox)
        testLayout.addWidget(self.graphicsView)
        testLayout.addLayout(buttonsLayout)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.infoGroupBox)
        self.layout.addWidget(self.testGroupBox)
        self.setLayout(self.layout)

    def countdown(self):
        # Counting from value in timeTrialsSpinbox to 0 (start)
        if self.remainingTime > 0:
            self.graphicsView.scene().clear()

            font = QtGui.QFont()
            font.setPointSize(20)
            self.graphicsView.setFont(font)
            text = self.graphicsView.scene().addText(f"{self.remainingTime}")
            text.setPos(self.graphicsView.width() / 2 - text.boundingRect().width() / 2, self.graphicsView.height() / 2 - text.boundingRect().height() / 2)

            self.remainingTime -= 1
        else:
            self.timer.stop()
            self.graphicsView.scene().clear()

            text = self.graphicsView.scene().addText("Start")
            text.setPos(self.graphicsView.width() / 2 - text.boundingRect().width() / 2, self.graphicsView.height() / 2 - text.boundingRect().height() / 2)
            QTimer.singleShot(1000, self.showStimulus)  # Wait for 1000 ms

    def startTest(self):
        # Configure buttons
        self.startButton.setEnabled(False)
        self.clickButton.setEnabled(True)
        self.noClickButton.setEnabled(True)

        # Get parameters from settings
        self.trainTrials = self.settingsTab.trainTrialsSpinbox.value()
        self.trainTrialsLeft = self.trainTrials
        self.testTrials = self.settingsTab.testTrialsSpinbox.value()
        self.testTrialsLeft = self.testTrials
        self.prepareTrial()

    def prepareTrial(self):
        self.clearLayout()

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

        # Show stimulus (rectangle) with random color
        color = random.choice(self.colors)
        rect = QRectF(0, 0, 100, 100)
        rect.moveCenter(QPointF(self.graphicsView.width() / 2, self.graphicsView.height() / 2))
        self.graphicsScene.addRect(rect, QPen(Qt.black), QBrush(QtGui.QColor(color)))
        self.currentColor = color

        # Get time of start and update flag
        self.startTime = time.perf_counter()
        self.stimulusShown = True

        # Start auto continue timer
        self.autoContinueTimer = QTimer(self)
        self.autoContinueTimer.setSingleShot(True)
        self.autoContinueTimer.timeout.connect(self.autoContinueTrial)
        self.autoContinueTimer.start(self.settingsTab.timeTrialsSpinbox.value() * 1000)

    def autoContinueTrial(self):
        # Check if there is no stimulus
        if not self.stimulusShown:
            return

        # Update flags. Get time of the end. Calculate the difference between start and end time
        self.endTime = time.perf_counter()
        self.clearLayout()
        self.stimulusShown = False
        self.startTimes.append(self.endTime - self.startTime)

        if self.trainTrialsLeft > 0:    # Train phase
            self.trainTrialsLeft -= 1
        else:   # Test phase
            self.testTrialsLeft -= 1

            if self.testTrialsLeft == 0:
                self.endTest()
                return

        self.prepareTrial()

    def showStimulus(self):
        self.graphicsScene = QGraphicsScene()
        self.graphicsView.setScene(self.graphicsScene)
        self.startTrial()

    def onButtonClick(self):
        # Check if there is no stimulus
        if not self.stimulusShown:
            self.unnecessaryClicks += 1
            return

        # Update flags. Get time of the end. Calculate the difference between start and end time
        self.endTime = time.perf_counter()
        self.autoContinueTimer.stop()
        self.clearLayout()
        self.stimulusShown = False
        self.startTimes.append(self.endTime - self.startTime)

        if self.trainTrialsLeft > 0:    # Train phase
            self.trainTrialsLeft -= 1
        else:   # Test phase
            if self.currentColor == self.correctColor:  # ==
                self.correctClicks += 1
            else:
                self.wrongClicks += 1

            self.testTrialsLeft -= 1

            if self.testTrialsLeft == 0:
                self.endTest()
                return

        self.prepareTrial()

    def onNoClickButton(self):
        # Check if there is no stimulus
        if not self.stimulusShown:
            return

        # Update flags. Get time of the end. Calculate the difference between start and end time
        self.endTime = time.perf_counter()
        self.autoContinueTimer.stop()
        self.clearLayout()
        self.stimulusShown = False
        self.startTimes.append(self.endTime - self.startTime)

        if self.trainTrialsLeft > 0:    # Train phase
            self.trainTrialsLeft -= 1
        else:   # Test phase
            if self.currentColor != self.correctColor:  # !=
                self.correctClicks += 1
            else:
                self.wrongClicks += 1

            self.testTrialsLeft -= 1

            if self.testTrialsLeft == 0:
                self.endTest()
                return

        self.prepareTrial()

    def clearLayout(self):
        # Clear scene
        self.graphicsView.setScene(None)
        self.graphicsView.setScene(QGraphicsScene())

    def endTest(self):
        # Summarizing results
        self.endTimes = self.startTimes[self.trainTrials:]
        self.averageTime = sum(self.endTimes) / len(self.endTimes)
        self.startButton.setEnabled(True)
        self.clickButton.setEnabled(False)
        self.noClickButton.setEnabled(False)

        # Reset parameters and emit a signal of finishing (to switch to the next tab)
        self.stimulusShown = False
        self.clearLayout()
        self.testFinished.emit()

        # Update test section in the results tab
        mainWindow = self.window()
        mainWindow.resultsTab.updateResultsTest2(self.averageTime, self.correctClicks, self.wrongClicks, self.endTimes)
