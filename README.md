# 🧠 Psychomotor Tester

> ☣ **Warning:** This project was created during my studies for educational purposes only. It may contain non-optimal solutions.

### 📊 About

**A psychomotor performance tester** has been implemented. The application consisted of a series of different tests examining simple and complex response times to optical and acoustic stimuli. Each test is preceded by information about the test and a training phase, during which the person performs the same actions as during the test phase, but without evaluation. After performing a series of tests, the results of the tests are displayed in synthetic and analytical form using numerical values and graphical representation.

> The application is written in **Python 3.10.9**, using the Qt Framework (PySide2), in PyCharm 2023.1.1 (Professional Edition).

### 🔮 Functionality

- **Settings** tab - contains fields allowing to enter the number of trials in the training and test phase and the break time between them (countdown time). After pressing *Start*, the user will go to the first test (next tab).

<p align="center">
  <img src="/_readme-img/1-settings.png?raw=true" width="400" alt="Settings">
</p>

- **Stroop Test** tab - implementation of a test to test attention processes and reaction inhibition. It consists of an information field (instruction, current phase, trial number, *Start* button) and a proper test field that contains buttons with color names and a space where the colored word appears. Both word and color are randomized. Before starting the test, the field where the word appears will be showed a countdown from the value selected in the Settings tab to 1 (then the word will appear). The test execution time is measured from the moment the word appears to the moment button is clicked (as in all subsequent tests).

<p align="center">
  <img src="/_readme-img/2-test1.png?raw=true" width="400" alt="Stroop Test">
</p>

- **Touch Test** tab - another test that involves pressing the *Click* button when a square of a certain color appears or *No Click* when it does not. The color of the square is randomized. It allows you to test the speed of reaction and the ability to make quick decisions depending on the visual stimulus. In addition, this test automatically switches to the next trial after the time specified in the Settings tab.

<p align="center">
  <img src="/_readme-img/3-test2.png?raw=true" width="400" alt="Touch Test">
</p>

- **Sound Test** tab - a test consisting in pressing the *Click* button after hearing a sound that is played at a random point in time from 0 to the value specified in the Settings tab. This is a test that allows you to study the speed of response to a sound stimulus and the ability to make quick decisions depending on the auditory signal.

<p align="center">
  <img src="/_readme-img/4-test3.png?raw=true" width="400" alt="Sound Test">
</p>

- **Object Tracking Test** tab - involves pressing the *Click* button when two circles intersect each other. The time taken to try is measured from the moment the objects touch to click, but when the objects stop touching, the user must wait for the next intersection. It is a test that allows you to test the ability to track and process visual stimuli and the speed of reaction to changing situations.

<p align="center">
  <img src="/_readme-img/5-test4.png?raw=true" width="400" alt="Object Tracking Test">
</p>

- **Results** tab - contains the results of individual tests in the form of bar or point charts and text data (average response time, number of correct, incorrect and/or unnecessary clicks, etc.). The results can be scrolled.

<p align="center">
  <img src="/_readme-img/6-results.png?raw=true" width="400" alt="Results">
</p>
