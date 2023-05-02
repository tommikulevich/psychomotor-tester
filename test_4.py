import time

from PySide2 import QtGui
from PySide2.QtCore import QTimer, Qt, QPointF, Signal
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QGraphicsView, QGraphicsScene, QGroupBox
from PySide2.QtGui import QPen, QBrush

import random
random.seed(time.perf_counter())


class Test4(QWidget):
    testFinished = Signal()  # Signal that is emitted after the end of the test

    def __init__(self, parent=None):
        super().__init__(parent)
        self.testName = 'Object Tracking Test'
        self.settingsTab = parent.settingsTab

        # Test parameters
        self.circle1Dir = 1 * 2
        self.circle2Dir = (-1) * 2
        self.startTimes = []
        self.endTimes = []
        self.intersectClicks = 0
        self.nonIntersectClicks = 0
        self.unnecessaryClicks = 0

        # Window elements creation and configuration
        self.infoLabel = QLabel("INSTRUCTION: Press the 'Click' button when two circles intersect.")
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
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.clickButton = QPushButton("Click")
        self.clickButton.clicked.connect(self.onButtonClick)
        self.clickButton.setEnabled(False)

        self.testGroupBox = QGroupBox("Test")
        testLayout = QVBoxLayout(self.testGroupBox)
        testLayout.addWidget(self.graphicsView)
        testLayout.addWidget(self.clickButton)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.infoGroupBox)
        self.layout.addWidget(self.testGroupBox)
        self.setLayout(self.layout)

    def startTest(self):
        # Configure buttons
        self.startButton.setEnabled(False)
        self.clickButton.setEnabled(True)

        # Get parameters from settings
        self.trainTrials = self.settingsTab.trainTrialsSpinbox.value()
        self.trainTrialsLeft = self.trainTrials
        self.testTrials = self.settingsTab.testTrialsSpinbox.value()
        self.testTrialsLeft = self.testTrials
        self.prepareTrial()

    def prepareTrial(self):
        self.graphicsScene = QGraphicsScene()
        self.graphicsView.setScene(self.graphicsScene)

        # Reset animation timer
        if hasattr(self, 'animationTimer'):
            self.animationTimer.stop()
            self.animationTimer.timeout.disconnect()

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

        self.startTrial()

    def startTrial(self):
        self.generateMovingObjects()
        self.firstIntersectTime = None

    def generateMovingObjects(self):
        # Generate 2 circles
        self.circle1 = self.graphicsScene.addEllipse(0, 0, 100, 100, QPen(Qt.black), QBrush(QtGui.QColor('blue')))
        self.circle2 = self.graphicsScene.addEllipse(0, 0, 100, 100, QPen(Qt.black), QBrush(QtGui.QColor('red')))

        self.circle1.setPos(QPointF(self.graphicsView.width() / 2 - 150, self.graphicsView.height() / 2))
        self.circle2.setPos(QPointF(self.graphicsView.width() / 2 + 150, self.graphicsView.height() / 2))

        # Start animation
        self.animationTimer = QTimer(self)
        self.animationTimer.setInterval(20)
        self.animationTimer.timeout.connect(self.moveObjects)
        self.animationTimer.start()

    def moveObjects(self):
        # Move circles
        self.circle1.moveBy(self.circle1Dir, 0)
        self.circle2.moveBy(self.circle2Dir, 0)

        # Check for circle collision and set flags
        if self.circle1.collidesWithItem(self.circle2):
            self.intersecting = True
            if self.firstIntersectTime is None:
                self.firstIntersectTime = time.perf_counter()  # Remember time after collision
        else:
            self.intersecting = False
            self.firstIntersectTime = None

        # Change circle directions
        if self.circle1.x() + self.circle1.rect().width() > self.graphicsView.width() or self.circle1.x() < 0:
            self.circle1Dir = -self.circle1Dir

        if self.circle2.x() + self.circle2.rect().width() > self.graphicsView.width() or self.circle2.x() < 0:
            self.circle2Dir = -self.circle2Dir

    def onButtonClick(self):
        # Check if circles are not intersecting
        if not self.intersecting:
            self.nonIntersectClicks += 1
            return

        # Update flags. Get time of the end. Calculate the difference between start and end time
        self.endTime = time.perf_counter()
        if self.firstIntersectTime is not None:
            self.startTimes.append(self.endTime - self.firstIntersectTime)

        if self.trainTrialsLeft > 0:    # Train phase
            self.trainTrialsLeft -= 1
        else:   # Test phase
            self.intersectClicks += 1
            self.testTrialsLeft -= 1

            if self.testTrialsLeft == 0:
                self.endTest()
                return

        self.prepareTrial()

    def endTrial(self):
        self.animationTimer.stop()
        self.graphicsScene.clear()
        self.prepareTrial()

    def endTest(self):
        # Summarizing results
        self.endTimes = self.startTimes[self.trainTrials:]
        self.averageTime = sum(self.endTimes) / len(self.endTimes)
        self.startButton.setEnabled(True)
        self.clickButton.setEnabled(False)

        # Emit a signal of finishing (to switch to the next tab)
        self.testFinished.emit()

        # Update test section in the results tab
        mainWindow = self.window()
        mainWindow.resultsTab.updateResultsTest4(self.averageTime, self.intersectClicks, self.nonIntersectClicks, self.endTimes)
