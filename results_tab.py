from PySide2.QtCharts import QtCharts
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QVBoxLayout, QWidget, QLabel, QGroupBox, QScrollArea


class ResultsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mainWindow = parent

        self.resultsGroupBox = QGroupBox("Main Info")
        self.resultsLayout = QVBoxLayout()

        self.results1GroupBox = QGroupBox("Test #1: Stroop Test")
        self.chart1View = QtCharts.QChartView()
        self.chart1View.setMinimumHeight(300)
        self.results1Layout = QVBoxLayout()
        self.results1Layout.addWidget(self.chart1View)
        self.results1GroupBox.setLayout(self.results1Layout)

        self.results2GroupBox = QGroupBox("Test #2: Touch Test")
        self.chart2View = QtCharts.QChartView()
        self.chart2View.setMinimumHeight(300)
        self.results2Layout = QVBoxLayout()
        self.results2Layout.addWidget(self.chart2View)
        self.results2GroupBox.setLayout(self.results2Layout)

        self.results3GroupBox = QGroupBox("Test #3: Sound Test")
        self.chart3View = QtCharts.QChartView()
        self.chart3View.setMinimumHeight(300)
        self.results3Layout = QVBoxLayout()
        self.results3Layout.addWidget(self.chart3View)
        self.results3GroupBox.setLayout(self.results3Layout)

        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        scrollAreaWidget = QWidget()
        scrollAreaLayout = QVBoxLayout(scrollAreaWidget)
        scrollAreaLayout.addWidget(self.resultsGroupBox)
        scrollAreaLayout.addWidget(self.results1GroupBox)
        scrollAreaLayout.addWidget(self.results2GroupBox)
        scrollAreaLayout.addWidget(self.results3GroupBox)
        scrollArea.setWidget(scrollAreaWidget)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(scrollArea)
        self.setLayout(self.layout)

    def updateResultsMain(self):
        self.resultsLayout.addWidget(
            QLabel(f"Number of train trials: {self.mainWindow.settingsTab.trainTrialsSpinbox.value()}"))
        self.resultsLayout.addWidget(
            QLabel(f"Number of test trials: {self.mainWindow.settingsTab.testTrialsSpinbox.value()}"))
        self.resultsLayout.addWidget(
            QLabel(f"Max time between trials: {self.mainWindow.settingsTab.timeTrialsSpinbox.value()} s"))
        self.resultsGroupBox.setLayout(self.resultsLayout)

    def updateResultsTest1(self, averageTime, correctClicksPercentage, endTimes):
        self.results1Layout.addWidget(QLabel(f"Average time: {averageTime:.3f} [s]"))
        self.results1Layout.addWidget(QLabel(f"Correct clicks: {correctClicksPercentage:.1f}%"))

        barSet = QtCharts.QBarSet("Time [s]")
        for endTime in endTimes:
            barSet << endTime

        series = QtCharts.QBarSeries()
        series.append(barSet)

        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setTitle("Stroop Test Results")
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        categories = [f"Trial #{i + 1}" for i in range(len(endTimes))]
        axisX = QtCharts.QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QtCharts.QValueAxis()
        axisY.setRange(0, max(endTimes) * 1.1)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.chart1View.setChart(chart)

    def updateResultsTest2(self, averageTime, correctClicks, wrongClicks, endTimes):
        self.results2Layout.addWidget(QLabel(f"Average time: {averageTime:.3f} [s]"))
        self.results2Layout.addWidget(QLabel(f"Correct/wrong clicks: {correctClicks}/{wrongClicks}"))

        barSet = QtCharts.QBarSet("Time [s]")
        for endTime in endTimes:
            barSet << endTime

        series = QtCharts.QBarSeries()
        series.append(barSet)

        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setTitle("Touch Test Results")
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        categories = [f"Trial #{i + 1}" for i in range(len(endTimes))]
        axisX = QtCharts.QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QtCharts.QValueAxis()
        axisY.setRange(0, max(endTimes) * 1.1)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.chart2View.setChart(chart)

    def updateResultsTest3(self, averageTime, unnecessaryClicks, endTimes):
        self.results3Layout.addWidget(QLabel(f"Average time: {averageTime:.3f} [s]"))
        self.results3Layout.addWidget(QLabel(f"Unnecessary clicks: {unnecessaryClicks}"))

        barSet = QtCharts.QBarSet("Time [s]")
        for endTime in endTimes:
            barSet << endTime

        series = QtCharts.QBarSeries()
        series.append(barSet)

        chart = QtCharts.QChart()
        chart.addSeries(series)
        chart.setTitle("Sound Test Results")
        chart.setAnimationOptions(QtCharts.QChart.SeriesAnimations)

        categories = [f"Trial #{i + 1}" for i in range(len(endTimes))]
        axisX = QtCharts.QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignBottom)
        series.attachAxis(axisX)

        axisY = QtCharts.QValueAxis()
        axisY.setRange(0, max(endTimes) * 1.1)
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisY)

        self.chart3View.setChart(chart)
