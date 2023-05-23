# UiAnalyzer
## Language
python

## How to use
#### 1. Run FindSimilarPage.py to find similar UIs for the target UI. 
Input the path of the target UI, then the program will find UIs which are similar to the target UI from the UI repository folder, and output a file folder containing the target UI and its similar UIs.
#### 2. Run CreateWireframe.py to create wireframes for the similar UIs and the target UI.
After obtaining the folder outputted by FindSimilarPage.py, the program is used to create wireframes for the target UI and its similar UIs in the folder.

#### 3. Run FindAbnormal.py to judge whether target UI has the risk of violating the design conventions
The program is used to analyze the wireframes of the target UI and its similar UIs, and output whether target UI has the risk of violating the design conventions.

## Data
The APK files are available at https://pan.quark.cn/s/ba256c4eab80

The way to download APK files is as follows:
![1](https://github.com/Hylance1224/UiAnalyzer/assets/39308424/bb70ca7d-fa30-48f6-9b1c-3c42b3b62e74)
