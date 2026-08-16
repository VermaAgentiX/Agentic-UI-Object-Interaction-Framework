'''import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl, Qt

class AnimatedSvgWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Animated SVG HUD")
        self.resize(600, 600)
        self.setWindowOpacity(0.9)  # Slightly transparent for a HUD effect

        # 1. Create the WebEngine View
        self.web_view = QWebEngineView(self)
        
        # 2. Make the background transparent (Great for Sci-Fi HUDs!)
        self.web_view.page().setBackgroundColor(Qt.transparent)
        
        # 3. Load the local SVG file
        # QWebEngineView requires an absolute path and a proper QUrl scheme
        svg_path = os.path.abspath("download.svg") 
        self.web_view.setUrl(QUrl.fromLocalFile(svg_path))

        self.setCentralWidget(self.web_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnimatedSvgWindow()
    window.show()
    sys.exit(app.exec())'''
    
# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py


from ui_form import Ui_MainWindow
class window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.form = Ui_MainWindow()
        self.form.setupUi(self)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = window()
    widget.show()
    sys.exit(app.exec())