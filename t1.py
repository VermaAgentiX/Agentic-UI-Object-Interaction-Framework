import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QMainWindow
from PySide6.QtGui import QPainter, QPen, QColor, QBrush, QConicalGradient
from PySide6.QtCore import Qt, QTimer, QRectF

class SciFiHUD(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle1 = 0
        self.angle2 = 360
        self.sweep_angle = 0
        
        # 30ms timer for ~33 FPS animation
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_angles)
        self.timer.start(30) 
        
        self.setMinimumSize(300, 300)
        # Allows it to float over other UI elements
        self.setAttribute(Qt.WA_TranslucentBackground) 

    def update_angles(self):
        # Different speeds for different elements
        self.angle1 = (self.angle1 + 2) % 360
        self.angle2 = (self.angle2 - 1.5) % 360
        self.sweep_angle = (self.sweep_angle + 3) % 360
        self.update() # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Center coordinates and dynamic radius
        cx = self.width() / 2
        cy = self.height() / 2
        radius = min(cx, cy) - 20

        # --- 1. Static Outer Ring ---
        pen = QPen(QColor(0, 255, 255, 80), 2) # Faint Cyan
        painter.setPen(pen)
        painter.drawEllipse(int(cx - radius), int(cy - radius), int(radius*2), int(radius*2))

        # --- 2. Rotating Outer Arcs ---
        pen.setWidth(4)
        pen.setColor(QColor(0, 255, 255, 200)) # Bright Cyan
        painter.setPen(pen)
        rect_outer = QRectF(cx - radius + 10, cy - radius + 10, (radius-10)*2, (radius-10)*2)
        
        # drawArc takes angles in 1/16ths of a degree
        painter.drawArc(rect_outer, self.angle1 * 16, 75 * 16)
        painter.drawArc(rect_outer, (self.angle1 + 180) * 16, 75 * 16)

        # --- 3. Counter-Rotating Inner Dashed Ring ---
        pen.setWidth(2)
        pen.setColor(QColor(255, 0, 150, 180)) # Neon Magenta
        pen.setStyle(Qt.DashLine)
        painter.setPen(pen)
        rect_inner = QRectF(cx - radius + 40, cy - radius + 40, (radius-40)*2, (radius-40)*2)
        
        # Rotate the painter for the dashed ring
        painter.save()
        painter.translate(cx, cy)
        painter.rotate(self.angle2)
        painter.drawEllipse(QRectF(-radius + 40, -radius + 40, (radius-40)*2, (radius-40)*2))
        painter.restore()

        # --- 4. Radar Sweep Gradient ---
        gradient = QConicalGradient(cx, cy, -self.sweep_angle)
        gradient.setColorAt(0.0, QColor(0, 255, 255, 120)) # Leading edge
        gradient.setColorAt(0.1, QColor(0, 255, 255, 0))   # Trail fades out
        gradient.setColorAt(1.0, QColor(0, 255, 255, 0))
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(int(cx - radius), int(cy - radius), int(radius*2), int(radius*2))

# --- Testing the Widget Standalone ---
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.resize(500, 500)
    window.setStyleSheet("background-color: #0A0A1A;") # Dark sci-fi background
    
    hud = SciFiHUD()
    window.setCentralWidget(hud)
    window.show()
    sys.exit(app.exec_())