# Test output of deepseek V4 model from hugging face

#!/usr/bin/env python3
"""
Modern Calculator Application
Built with PySide6 and Python
Features: Basic & Scientific modes, History, Memory, Themes, Keyboard Support
Lines: 1000+
"""

import sys
import math
import re
import json
import os
from datetime import datetime
from functools import partial
from typing import Union, Optional, List, Dict, Any

from PySide6.QtCore import (
    Qt, QSize, QTimer, QPropertyAnimation, QEasingCurve,
    QPoint, Signal, Slot, QRect, QEvent
)
from PySide6.QtGui import (
    QFont, QIcon, QKeyEvent, QColor, QPainter, QPen,
    QBrush, QFontDatabase, QAction, QPalette, QLinearGradient,
    QRadialGradient, QMouseEvent, QPaintEvent
)
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLineEdit, QLabel, QScrollArea,
    QFrame, QSizePolicy, QSpacerItem, QMenu, QMenuBar, QDialog,
    QDialogButtonBox, QComboBox, QCheckBox, QTabWidget, QTextEdit,
    QListWidget, QListWidgetItem, QSplitter, QToolTip, QMessageBox,
    QStackedWidget, QButtonGroup, QRadioButton, QGroupBox, QSlider,
    QStatusBar, QToolBar, QStyle, QStyleFactory
)


# =============================================================================
# THEME MANAGEMENT
# =============================================================================

class ThemeManager:
    """Manages application themes and color schemes."""

    DARK_THEME = {
        "name": "Dark",
        "colors": {
            "bg_primary": "#1a1a2e",
            "bg_secondary": "#16213e",
            "bg_tertiary": "#0f3460",
            "bg_display": "#0a0a1a",
            "bg_button": "#1c2541",
            "bg_button_hover": "#2d3a5c",
            "bg_button_pressed": "#3a4a7a",
            "bg_button_operator": "#e94560",
            "bg_button_operator_hover": "#ff6b81",
            "bg_button_operator_pressed": "#c23152",
            "bg_button_equal": "#0f3460",
            "bg_button_equal_hover": "#1a5276",
            "bg_button_function": "#2c3e6b",
            "bg_button_function_hover": "#3d5691",
            "bg_button_memory": "#1e3a5f",
            "bg_history": "#111827",
            "bg_history_item": "#1f2937",
            "bg_scrollbar": "#2d3748",
            "bg_scrollbar_handle": "#4a5568",
            "text_primary": "#e2e8f0",
            "text_secondary": "#a0aec0",
            "text_display": "#00ff88",
            "text_button": "#e2e8f0",
            "text_operator": "#ffffff",
            "text_equal": "#00ff88",
            "text_function": "#a0c4ff",
            "text_memory": "#81e6d9",
            "text_history": "#94a3b8",
            "text_history_result": "#00ff88",
            "text_error": "#ff6b6b",
            "border_display": "#2d3748",
            "border_button": "#2d3748",
            "border_history": "#374151",
            "shadow": "rgba(0, 0, 0, 0.5)",
            "highlight": "#00ff8855",
            "accent": "#e94560",
            "gradient_bg_start": "#1a1a2e",
            "gradient_bg_end": "#16213e",
        },
        "border_radius": {
            "display": 15,
            "button": 12,
            "panel": 15,
            "history_item": 8,
        },
        "font_sizes": {
            "display": 32,
            "display_secondary": 14,
            "button": 16,
            "button_small": 13,
            "history": 12,
            "menu": 13,
        }
    }

    LIGHT_THEME = {
        "name": "Light",
        "colors": {
            "bg_primary": "#f8fafc",
            "bg_secondary": "#f1f5f9",
            "bg_tertiary": "#e2e8f0",
            "bg_display": "#ffffff",
            "bg_button": "#ffffff",
            "bg_button_hover": "#e2e8f0",
            "bg_button_pressed": "#cbd5e1",
            "bg_button_operator": "#3b82f6",
            "bg_button_operator_hover": "#60a5fa",
            "bg_button_operator_pressed": "#2563eb",
            "bg_button_equal": "#10b981",
            "bg_button_equal_hover": "#34d399",
            "bg_button_function": "#f0f9ff",
            "bg_button_function_hover": "#e0f2fe",
            "bg_button_memory": "#f0fdf4",
            "bg_history": "#ffffff",
            "bg_history_item": "#f8fafc",
            "bg_scrollbar": "#e2e8f0",
            "bg_scrollbar_handle": "#94a3b8",
            "text_primary": "#1e293b",
            "text_secondary": "#64748b",
            "text_display": "#0f172a",
            "text_button": "#1e293b",
            "text_operator": "#ffffff",
            "text_equal": "#ffffff",
            "text_function": "#3b82f6",
            "text_memory": "#059669",
            "text_history": "#475569",
            "text_history_result": "#059669",
            "text_error": "#ef4444",
            "border_display": "#e2e8f0",
            "border_button": "#cbd5e1",
            "border_history": "#e2e8f0",
            "shadow": "rgba(0, 0, 0, 0.1)",
            "highlight": "#3b82f622",
            "accent": "#3b82f6",
            "gradient_bg_start": "#f8fafc",
            "gradient_bg_end": "#e2e8f0",
        },
        "border_radius": {
            "display": 15,
            "button": 12,
            "panel": 15,
            "history_item": 8,
        },
        "font_sizes": {
            "display": 32,
            "display_secondary": 14,
            "button": 16,
            "button_small": 13,
            "history": 12,
            "menu": 13,
        }
    }

    @classmethod
    def get_theme(cls, theme_name: str = "Dark") -> Dict[str, Any]:
        """Get theme configuration by name."""
        if theme_name.lower() == "light":
            return cls.LIGHT_THEME.copy()
        return cls.DARK_THEME.copy()


# =============================================================================
# CALCULATOR ENGINE
# =============================================================================

class CalculatorEngine:
    """Core calculation engine handling all mathematical operations."""

    def __init__(self):
        self.reset_state()

    def reset_state(self):
        """Reset the calculator state."""
        self._current_input = "0"
        self._previous_input = ""
        self._operator = ""
        self._result = 0.0
        self._last_result = 0.0
        self._is_new_input = True
        self._last_was_operator = False
        self._has_decimal = False
        self._expression = ""
        self._memory = 0.0
        self._history: List[Dict[str, Any]] = []
        self._angle_mode = "DEG"  # DEG, RAD, GRAD
        self._precision = 10
        self._error_state = False

    # --- Memory Functions ---
    def memory_clear(self) -> None:
        self._memory = 0.0

    def memory_recall(self) -> float:
        return self._memory

    def memory_add(self, value: float) -> None:
        self._memory += value

    def memory_subtract(self, value: float) -> None:
        self._memory -= value

    def memory_store(self, value: float) -> None:
        self._memory = value

    # --- Input Handling ---
    def append_digit(self, digit: str) -> str:
        """Append a digit to current input."""
        if self._error_state:
            self._clear_entry()
            self._error_state = False

        if self._is_new_input or self._current_input == "0":
            if digit == ".":
                if not self._has_decimal:
                    self._current_input = "0."
                    self._has_decimal = True
                    self._is_new_input = False
            else:
                self._current_input = digit
                self._is_new_input = False
        else:
            if digit == ".":
                if not self._has_decimal:
                    self._current_input += "."
                    self._has_decimal = True
            else:
                if len(self._current_input) < 16:
                    self._current_input += digit

        self._last_was_operator = False
        return self._current_input

    def append_operator(self, operator: str) -> Optional[str]:
        """Handle operator input."""
        if self._error_state:
            self._error_state = False

        current_value = self._get_current_value()

        if self._operator and not self._last_was_operator:
            result = self._calculate()
            self._previous_input = str(result)
            self._current_input = str(result)
            self._result = result
        else:
            self._previous_input = self._current_input

        self._operator = operator
        self._is_new_input = True
        self._has_decimal = False
        self._last_was_operator = True
        self._expression = f"{self._previous_input} {self._operator}"
        return None

    def calculate(self) -> str:
        """Perform the calculation."""
        if self._error_state:
            return "Error"

        if not self._operator:
            return self._current_input

        current_value = self._get_current_value()
        self._expression = (
            f"{self._previous_input} {self._operator} {self._current_input}"
        )

        result = self._calculate()
        self._add_to_history(self._expression, result)

        self._last_result = result
        self._current_input = self._format_result(result)
        self._previous_input = ""
        self._operator = ""
        self._is_new_input = True
        self._has_decimal = "." in self._current_input
        self._last_was_operator = False
        self._result = result

        return self._current_input

    def _calculate(self) -> float:
        """Internal calculation method."""
        prev = self._safe_float(self._previous_input)
        curr = self._safe_float(self._current_input)

        try:
            if self._operator == "+":
                return prev + curr
            elif self._operator == "-":
                return prev - curr
            elif self._operator == "×":
                return prev * curr
            elif self._operator == "÷":
                if abs(curr) < 1e-15:
                    self._error_state = True
                    return float("nan")
                return prev / curr
            elif self._operator == "^":
                return math.pow(prev, curr)
            elif self._operator == "mod":
                if abs(curr) < 1e-15:
                    self._error_state = True
                    return float("nan")
                return prev % curr
            elif self._operator == "y√x":
                if abs(curr) < 1e-15:
                    self._error_state = True
                    return float("nan")
                return math.pow(prev, 1.0 / curr)
            else:
                return curr
        except (OverflowError, ValueError):
            self._error_state = True
            return float("nan")

    def _safe_float(self, value: str) -> float:
        """Safely convert string to float."""
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def _get_current_value(self) -> float:
        """Get current input as float."""
        return self._safe_float(self._current_input)

    def _format_result(self, value: float) -> str:
        """Format result for display."""
        if math.isnan(value):
            self._error_state = True
            return "Error"
        if math.isinf(value):
            self._error_state = True
            return "Infinity"

        if isinstance(value, float):
            if abs(value) >= 1e15 or (abs(value) < 1e-10 and value != 0):
                return f"{value:.{self._precision}e}"

            formatted = f"{value:.{self._precision}f}".rstrip("0").rstrip(".")

            if len(formatted) > 16:
                formatted = f"{value:.{self._precision}e}"

            return formatted

        return str(value)

    def _add_to_history(self, expression: str, result: float) -> None:
        """Add calculation to history."""
        entry = {
            "expression": expression,
            "result": self._format_result(result),
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        self._history.append(entry)
        if len(self._history) > 100:
            self._history.pop(0)

    # --- Scientific Functions ---
    def calculate_scientific(self, func: str) -> str:
        """Handle scientific calculator functions."""
        if self._error_state:
            self._error_state = True
            return "Error"

        value = self._get_current_value()

        try:
            if func == "sin":
                angle = self._to_radians(value)
                result = math.sin(angle)
            elif func == "cos":
                angle = self._to_radians(value)
                result = math.cos(angle)
            elif func == "tan":
                angle = self._to_radians(value)
                result = math.tan(angle)
            elif func == "asin":
                result = math.asin(value)
                result = self._from_radians(result)
            elif func == "acos":
                result = math.acos(value)
                result = self._from_radians(result)
            elif func == "atan":
                result = math.atan(value)
                result = self._from_radians(result)
            elif func == "sinh":
                result = math.sinh(value)
            elif func == "cosh":
                result = math.cosh(value)
            elif func == "tanh":
                result = math.tanh(value)
            elif func == "log":
                if value <= 0:
                    self._error_state = True
                    return "Error"
                result = math.log10(value)
            elif func == "ln":
                if value <= 0:
                    self._error_state = True
                    return "Error"
                result = math.log(value)
            elif func == "sqrt":
                if value < 0:
                    self._error_state = True
                    return "Error"
                result = math.sqrt(value)
            elif func == "cbrt":
                result = math.cbrt(value) if hasattr(math, "cbrt") else (
                    math.pow(abs(value), 1/3) * (-1 if value < 0 else 1)
                )
            elif func == "square":
                result = value * value
            elif func == "cube":
                result = value * value * value
            elif func == "reciprocal":
                if abs(value) < 1e-15:
                    self._error_state = True
                    return "Error"
                result = 1.0 / value
            elif func == "factorial":
                if value < 0 or value != int(value):
                    self._error_state = True
                    return "Error"
                result = math.factorial(int(value))
            elif func == "abs":
                result = abs(value)
            elif func == "floor":
                result = math.floor(value)
            elif func == "ceil":
                result = math.ceil(value)
            elif func == "exp":
                result = math.exp(value)
            elif func == "ten_power":
                result = math.pow(10, value)
            elif func == "percent":
                result = value / 100.0
            elif func == "negate":
                result = -value
            elif func == "pi":
                result = math.pi
            elif func == "e_const":
                result = math.e
            elif func == "deg_to_rad":
                result = math.radians(value)
            elif func == "rad_to_deg":
                result = math.degrees(value)
            else:
                return self._current_input

            self._add_to_history(f"{func}({value})", result)
            self._last_result = result
            self._current_input = self._format_result(result)
            self._is_new_input = True
            self._has_decimal = "." in self._current_input
            self._result = result

            return self._current_input

        except (OverflowError, ValueError, ArithmeticError):
            self._error_state = True
            return "Error"

    def _to_radians(self, value: float) -> float:
        """Convert angle to radians based on current mode."""
        if self._angle_mode == "DEG":
            return math.radians(value)
        elif self._angle_mode == "GRAD":
            return value * math.pi / 200.0
        return value

    def _from_radians(self, value: float) -> float:
        """Convert radians to current angle mode."""
        if self._angle_mode == "DEG":
            return math.degrees(value)
        elif self._angle_mode == "GRAD":
            return value * 200.0 / math.pi
        return value

    # --- Utility ---
    def clear_entry(self) -> str:
        """Clear current entry."""
        self._current_input = "0"
        self._is_new_input = True
        self._has_decimal = False
        self._last_was_operator = False
        self._error_state = False
        return self._current_input

    def clear_all(self) -> str:
        """Clear everything."""
        self.reset_state()
        return self._current_input

    def backspace(self) -> str:
        """Remove last character."""
        if self._error_state or self._is_new_input:
            return self._current_input

        if len(self._current_input) > 1:
            if self._current_input[-1] == ".":
                self._has_decimal = False
            self._current_input = self._current_input[:-1]
        else:
            self._current_input = "0"
            self._is_new_input = True
            self._has_decimal = False

        return self._current_input

    def toggle_sign(self) -> str:
        """Toggle positive/negative."""
        if self._error_state:
            return self._current_input

        if self._current_input.startswith("-"):
            self._current_input = self._current_input[1:]
        else:
            self._current_input = "-" + self._current_input

        return self._current_input

    def set_angle_mode(self, mode: str) -> None:
        """Set angle mode (DEG, RAD, GRAD)."""
        self._angle_mode = mode

    def get_history(self) -> List[Dict[str, Any]]:
        """Get calculation history."""
        return self._history

    def clear_history(self) -> None:
        """Clear calculation history."""
        self._history.clear()

    def load_from_history(self, index: int) -> str:
        """Load a value from history."""
        if 0 <= index < len(self._history):
            value = self._history[index]["result"]
            self._current_input = str(value)
            self._is_new_input = True
            self._has_decimal = "." in self._current_input
            return self._current_input
        return self._current_input

    # --- Constants ---
    @property
    def memory_value(self) -> float:
        return self._memory

    @property
    def current_input(self) -> str:
        return self._current_input

    @property
    def expression(self) -> str:
        return self._expression

    @property
    def angle_mode(self) -> str:
        return self._angle_mode

    @property
    def is_error(self) -> bool:
        return self._error_state


# =============================================================================
# CUSTOM WIDGETS
# =============================================================================

class CalculatorButton(QPushButton):
    """Custom styled calculator button with animations."""

    def __init__(
        self,
        text: str,
        button_type: str = "number",
        parent: Optional[QWidget] = None
    ):
        super().__init__(text, parent)
        self.button_type = button_type
        self._theme = {}
        self._animation = None
        self.setCursor(Qt.PointingHandCursor)
        self.setFocusPolicy(Qt.NoFocus)

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        """Apply theme to button."""
        self._theme = theme
        colors = theme["colors"]
        radius = theme["border_radius"]["button"]
        font_size = theme["font_sizes"]["button"]

        if self.button_type == "operator":
            bg = colors["bg_button_operator"]
            hover = colors["bg_button_operator_hover"]
            pressed = colors["bg_button_operator_pressed"]
            text_color = colors["text_operator"]
        elif self.button_type == "equal":
            bg = colors["bg_button_equal"]
            hover = colors["bg_button_equal_hover"]
            pressed = colors["bg_button_operator_pressed"]
            text_color = colors["text_equal"]
        elif self.button_type == "function":
            bg = colors["bg_button_function"]
            hover = colors["bg_button_function_hover"]
            pressed = colors["bg_button_pressed"]
            text_color = colors["text_function"]
        elif self.button_type == "memory":
            bg = colors["bg_button_memory"]
            hover = colors["bg_button_function_hover"]
            pressed = colors["bg_button_pressed"]
            text_color = colors["text_memory"]
            font_size = theme["font_sizes"]["button_small"]
        elif self.button_type == "clear":
            bg = colors["accent"]
            hover = colors["bg_button_operator_hover"]
            pressed = colors["bg_button_operator_pressed"]
            text_color = "#ffffff"
        else:
            bg = colors["bg_button"]
            hover = colors["bg_button_hover"]
            pressed = colors["bg_button_pressed"]
            text_color = colors["text_button"]

        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {bg};
                color: {text_color};
                border: 1px solid {colors['border_button']};
                border-radius: {radius}px;
                font-size: {font_size}px;
                font-weight: bold;
                padding: 5px;
                min-height: 40px;
            }}
            QPushButton:hover {{
                background-color: {hover};
                border-color: {colors['accent']};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
                padding-top: 7px;
                padding-bottom: 3px;
            }}
            QPushButton:disabled {{
                background-color: {colors['bg_tertiary']};
                color: {colors['text_secondary']};
            }}
        """)

    def enterEvent(self, event):
        """Handle mouse enter for tooltip."""
        super().enterEvent(event)

    def sizeHint(self) -> QSize:
        return QSize(60, 48)


class DisplayWidget(QFrame):
    """Custom display widget for showing calculations."""

    expressionChanged = Signal(str)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._theme = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the display UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(5)

        # Expression label (shows the calculation)
        self.expression_label = QLabel("")
        self.expression_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.expression_label.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.expression_label.setFixedHeight(22)

        # Main display
        self.display = QLineEdit("0")
        self.display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.display.setReadOnly(True)
        self.display.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Fixed
        )
        self.display.setFixedHeight(55)
        self.display.setFrame(False)

        # Memory indicator
        self.memory_label = QLabel("")
        self.memory_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.memory_label.setFixedHeight(18)

        # Angle mode indicator
        self.angle_label = QLabel("DEG")
        self.angle_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.angle_label.setFixedHeight(18)

        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(self.memory_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.angle_label)

        layout.addWidget(self.expression_label)
        layout.addWidget(self.display)
        layout.addLayout(bottom_layout)

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        """Apply theme to display."""
        self._theme = theme
        colors = theme["colors"]
        radius = theme["border_radius"]["display"]
        font_size = theme["font_sizes"]["display"]
        secondary_size = theme["font_sizes"]["display_secondary"]

        self.setStyleSheet(f"""
            DisplayWidget {{
                background-color: {colors['bg_display']};
                border: 2px solid {colors['border_display']};
                border-radius: {radius}px;
            }}
        """)

        self.display.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                color: {colors['text_display']};
                font-size: {font_size}px;
                font-weight: bold;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                border: none;
                padding: 5px 10px;
            }}
        """)

        self.expression_label.setStyleSheet(f"""
            QLabel {{
                color: {colors['text_secondary']};
                font-size: {secondary_size}px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                background: transparent;
                padding: 2px 10px;
            }}
        """)

        self.memory_label.setStyleSheet(f"""
            QLabel {{
                color: {colors['text_memory']};
                font-size: 11px;
                background: transparent;
                padding: 0 10px;
            }}
        """)

        self.angle_label.setStyleSheet(f"""
            QLabel {{
                color: {colors['text_function']};
                font-size: 11px;
                font-weight: bold;
                background: transparent;
                padding: 0 10px;
            }}
        """)

    def set_text(self, text: str) -> None:
        """Set display text."""
        self.display.setText(text)

    def set_expression(self, text: str) -> None:
        """Set expression text."""
        self.expression_label.setText(text)

    def set_memory_indicator(self, has_memory: bool) -> None:
        """Show/hide memory indicator."""
        self.memory_label.setText("M" if has_memory else "")

    def set_angle_mode(self, mode: str) -> None:
        """Set angle mode indicator."""
        self.angle_label.setText(mode)

    def get_text(self) -> str:
        """Get display text."""
        return self.display.text()


class HistoryPanel(QWidget):
    """History panel showing past calculations."""

    historyItemClicked = Signal(int)

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._theme = {}
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup the history panel UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        # Header
        header_layout = QHBoxLayout()
        self.title_label = QLabel("📋 History")
        self.title_label.setFont(QFont("Segoe UI", 13, QFont.Bold))

        self.clear_button = QPushButton("Clear")
        self.clear_button.setCursor(Qt.PointingHandCursor)
        self.clear_button.setFixedSize(60, 28)

        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.clear_button)
        layout.addLayout(header_layout)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFixedHeight(1)
        layout.addWidget(separator)

        # History list
        self.history_list = QListWidget()
        self.history_list.setCursor(Qt.PointingHandCursor)
        self.history_list.setVerticalScrollMode(
            QListWidget.ScrollPerPixel
        )
        self.history_list.setSpacing(3)
        layout.addWidget(self.history_list)

    def apply_theme(self, theme: Dict[str, Any]) -> None:
        """Apply theme to history panel."""
        self._theme = theme
        colors = theme["colors"]

        self.setStyleSheet(f"""
            HistoryPanel {{
                background-color: {colors['bg_history']};
                border: 1px solid {colors['border_history']};
                border-radius: {theme['border_radius']['panel']}px;
            }}
        """)

        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {colors['text_primary']};
                background: transparent;
            }}
        """)

        self.clear_button.setStyleSheet(f"""
            QPushButton {{
                background-color: {colors['bg_button']};
                color: {colors['text_secondary']};
                border: 1px solid {colors['border_button']};
                border-radius: 8px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {colors['accent']};
                color: white;
            }}
        """)

        self.history_list.setStyleSheet(f"""
            QListWidget {{
                background-color: transparent;
                border: none;
                outline: none;
            }}
            QListWidget::item {{
                background-color: {colors['bg_history_item']};
                color: {colors['text_history']};
                border-radius: {theme['border_radius']['history_item']}px;
                padding: 10px;
                margin: 2px 0;
                border: 1px solid transparent;
            }}
            QListWidget::item:hover {{
                border-color: {colors['accent']};
                background-color: {colors['bg_button_hover']};
            }}
            QListWidget::item:selected {{
                border-color: {colors['accent']};
                background-color: {colors['highlight']};
            }}
            QScrollBar:vertical {{
                background: {colors['bg_scrollbar']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {colors['bg_scrollbar_handle']};
                border-radius: 4px;
                min-height: 20px;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0;
            }}
        """)

    def update_history(self, history: List[Dict[str, Any]]) -> None:
        """Update history list."""
        self.history_list.clear()
        for i, entry in enumerate(reversed(history)):
            item_widget = QWidget()
            item_layout = QVBoxLayout(item_widget)
            item_layout.setContentsMargins(5, 3, 5, 3)
            item_layout.setSpacing(2)

            expr_label = QLabel(entry["expression"])
            expr_label.setStyleSheet("font-size: 11px; font-weight: bold;")

            result_label = QLabel(f"= {entry['result']}")
            result_label.setStyleSheet("font-size: 14px;")

            time_label = QLabel(entry["timestamp"])
            time_label.setStyleSheet("font-size: 9px; color: gray;")
            time_label.setAlignment(Qt.AlignRight)

            item_layout.addWidget(expr_label)
            item_layout.addWidget(result_label)
            item_layout.addWidget(time_label)

            list_item = QListWidgetItem()
            list_item.setSizeHint(item_widget.sizeHint())
            list_item.setData(Qt.UserRole, len(history) - 1 - i)
            self.history_list.addItem(list_item)
            self.history_list.setItemWidget(list_item, item_widget)


class SettingsDialog(QDialog):
    """Settings dialog for calculator configuration."""

    def __init__(
        self,
        current_theme: str,
        angle_mode: str,
        parent: Optional[QWidget] = None
    ):
        super().__init__(parent)
        self._current_theme = current_theme
        self._angle_mode = angle_mode
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup settings dialog UI."""
        self.setWindowTitle("Calculator Settings")
        self.setFixedSize(400, 350)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title = QLabel("⚙️ Settings")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Theme selection
        theme_group = QGroupBox("Appearance")
        theme_layout = QVBoxLayout(theme_group)

        self.dark_radio = QRadioButton("🌙 Dark Theme")
        self.light_radio = QRadioButton("☀️ Light Theme")

        if self._current_theme.lower() == "light":
            self.light_radio.setChecked(True)
        else:
            self.dark_radio.setChecked(True)

        theme_layout.addWidget(self.dark_radio)
        theme_layout.addWidget(self.light_radio)
        layout.addWidget(theme_group)

        # Angle mode
        angle_group = QGroupBox("Angle Unit")
        angle_layout = QVBoxLayout(angle_group)

        self.deg_radio = QRadioButton("📐 Degrees (DEG)")
        self.rad_radio = QRadioButton("🔄 Radians (RAD)")
        self.grad_radio = QRadioButton("📏 Gradians (GRAD)")

        if self._angle_mode == "RAD":
            self.rad_radio.setChecked(True)
        elif self._angle_mode == "GRAD":
            self.grad_radio.setChecked(True)
        else:
            self.deg_radio.setChecked(True)

        angle_layout.addWidget(self.deg_radio)
        angle_layout.addWidget(self.rad_radio)
        angle_layout.addWidget(self.grad_radio)
        layout.addWidget(angle_group)

        layout.addStretch()

        # Buttons
        button_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply")
        self.cancel_btn = QPushButton("Cancel")
        self.ok_btn = QPushButton("OK")

        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.apply_btn)
        button_layout.addWidget(self.ok_btn)
        layout.addLayout(button_layout)

        # Connections
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.apply_btn.clicked.connect(self._on_apply)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e293b;
                border-radius: 15px;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 13px;
                color: #e2e8f0;
                border: 1px solid #374151;
                border-radius: 10px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #a0c4ff;
            }
            QRadioButton {
                color: #cbd5e1;
                font-size: 13px;
                padding: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 9px;
                border: 2px solid #4a5568;
            }
            QRadioButton::indicator:checked {
                background-color: #3b82f6;
                border-color: #3b82f6;
            }
            QPushButton {
                padding: 8px 20px;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
            }
            QPushButton#apply_btn, QPushButton#ok_btn {
                background-color: #3b82f6;
                color: white;
            }
            QPushButton#cancel_btn {
                background-color: #374151;
                color: #e2e8f0;
            }
            QLabel {
                color: #e2e8f0;
            }
        """)

    def get_settings(self) -> Dict[str, str]:
        """Get selected settings."""
        theme = "Light" if self.light_radio.isChecked() else "Dark"
        if self.rad_radio.isChecked():
            angle = "RAD"
        elif self.grad_radio.isChecked():
            angle = "GRAD"
        else:
            angle = "DEG"
        return {"theme": theme, "angle_mode": angle}

    def _on_apply(self) -> None:
        """Handle apply button."""
        # Signal parent to apply settings immediately if needed
        pass


class AboutDialog(QDialog):
    """About dialog for the calculator."""

    def __init__(self, parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup about dialog."""
        self.setWindowTitle("About Calculator")
        self.setFixedSize(380, 280)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(10)

        title = QLabel("🧮 Modern Calculator")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        version = QLabel("Version 2.0.0")
        version.setAlignment(Qt.AlignCenter)
        version.setStyleSheet("color: #64748b; font-size: 13px;")
        layout.addWidget(version)

        layout.addSpacing(10)

        desc = QLabel(
            "A feature-rich calculator built with PySide6.\n"
            "Supports basic arithmetic, scientific functions,\n"
            "memory operations, calculation history, and more."
        )
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #94a3b8; font-size: 12px;")
        layout.addWidget(desc)

        layout.addSpacing(15)

        tech = QLabel("🛠️ Built with Python & PySide6 (Qt for Python)")
        tech.setAlignment(Qt.AlignCenter)
        tech.setStyleSheet("color: #a0c4ff; font-size: 11px;")
        layout.addWidget(tech)

        layout.addStretch()

        close_btn = QPushButton("Close")
        close_btn.setFixedSize(100, 35)
        close_btn.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1e293b;
                border-radius: 15px;
            }
            QLabel {
                color: #e2e8f0;
            }
            QPushButton {
                background-color: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: bold;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #60a5fa;
            }
        """)


# =============================================================================
# MAIN CALCULATOR WINDOW
# =============================================================================

class ModernCalculator(QMainWindow):
    """Main calculator application window."""

    def __init__(self):
        super().__init__()
        self.engine = CalculatorEngine()
        self._current_theme_name = "Dark"
        self._theme = ThemeManager.get_theme("Dark")
        self._history_visible = True
        self._scientific_mode = True

        self._setup_window()
        self._setup_menu_bar()
        self._setup_status_bar()
        self._setup_central_widget()
        self._apply_theme()
        self._connect_signals()

    def _setup_window(self) -> None:
        """Configure main window properties."""
        self.setWindowTitle("Modern Calculator")
        self.setMinimumSize(680, 580)
        self.resize(750, 620)
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        # Center on screen
        screen = QApplication.primaryScreen()
        if screen:
            center = screen.availableGeometry().center()
            geo = self.frameGeometry()
            geo.moveCenter(center)
            self.move(geo.topLeft())

    def _setup_menu_bar(self) -> None:
        """Setup application menu bar."""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")

        clear_history_action = QAction("Clear History", self)
        clear_history_action.setShortcut("Ctrl+Shift+H")
        clear_history_action.triggered.connect(self._clear_history)
        file_menu.addAction(clear_history_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # View menu
        view_menu = menubar.addMenu("&View")

        toggle_history_action = QAction("History Panel", self)
        toggle_history_action.setCheckable(True)
        toggle_history_action.setChecked(True)
        toggle_history_action.setShortcut("Ctrl+H")
        toggle_history_action.triggered.connect(self._toggle_history)
        view_menu.addAction(toggle_history_action)
        self._toggle_history_action = toggle_history_action

        toggle_scientific_action = QAction("Scientific Mode", self)
        toggle_scientific_action.setCheckable(True)
        toggle_scientific_action.setChecked(True)
        toggle_scientific_action.setShortcut("Ctrl+S")
        toggle_scientific_action.triggered.connect(self._toggle_scientific)
        view_menu.addAction(toggle_scientific_action)
        self._toggle_scientific_action = toggle_scientific_action

        view_menu.addSeparator()

        settings_action = QAction("Settings...", self)
        settings_action.setShortcut("Ctrl+,")
        settings_action.triggered.connect(self._open_settings)
        view_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu("&Help")

        shortcuts_action = QAction("Keyboard Shortcuts", self)
        shortcuts_action.triggered.connect(self._show_shortcuts)
        help_menu.addAction(shortcuts_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)

    def _setup_status_bar(self) -> None:
        """Setup status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Add permanent widgets
        self.status_theme_label = QLabel("🌙 Dark")
        self.status_bar.addPermanentWidget(self.status_theme_label)

    def _setup_central_widget(self) -> None:
        """Setup the central widget with all calculator components."""
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(8)

        # Calculator panel (display + buttons)
        calc_panel = QWidget()
        calc_layout = QVBoxLayout(calc_panel)
        calc_layout.setContentsMargins(0, 0, 0, 0)
        calc_layout.setSpacing(8)

        # Display
        self.display = DisplayWidget()
        calc_layout.addWidget(self.display)

        # Button area
        self.button_stack = QStackedWidget()

        # Basic mode buttons
        self.basic_buttons = self._create_basic_buttons()
        self.button_stack.addWidget(self.basic_buttons)

        # Scientific mode buttons
        self.scientific_buttons = self._create_scientific_buttons()
        self.button_stack.addWidget(self.scientific_buttons)

        self.button_stack.setCurrentIndex(1)  # Scientific mode default

        calc_layout.addWidget(self.button_stack)

        main_layout.addWidget(calc_panel, 3)

        # History panel
        self.history_panel = HistoryPanel()
        self.history_panel.setMinimumWidth(200)
        self.history_panel.setMaximumWidth(300)
        main_layout.addWidget(self.history_panel, 1)

        # Connect history signals
        self.history_panel.clear_button.clicked.connect(self._clear_history)
        self.history_panel.history_list.itemClicked.connect(
            self._on_history_item_clicked
        )

    def _create_basic_buttons(self) -> QWidget:
        """Create basic mode button layout."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        # Row 1: Memory operations
        mem_layout = QHBoxLayout()
        mem_layout.setSpacing(5)
        mem_buttons = [
            ("MC", "memory"), ("MR", "memory"),
            ("M+", "memory"), ("M-", "memory"), ("MS", "memory"),
        ]
        for text, btype in mem_buttons:
            btn = CalculatorButton(text, btype)
            btn.clicked.connect(partial(self._on_memory_button, text))
            mem_layout.addWidget(btn)
        layout.addLayout(mem_layout)

        # Row 2: Clear operations
        row2 = QHBoxLayout()
        row2.setSpacing(5)
        clear_buttons = [
            ("CE", "clear"), ("C", "clear"), ("⌫", "clear"),
            ("÷", "operator"),
        ]
        for text, btype in clear_buttons:
            btn = CalculatorButton(text, btype)
            if text in ("CE", "C", "⌫"):
                btn.clicked.connect(partial(self._on_clear_button, text))
            else:
                btn.clicked.connect(partial(self._on_operator_button, text))
            row2.addWidget(btn)
        layout.addLayout(row2)

        # Number pad rows
        number_layouts = [
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
        ]

        for row_data in number_layouts:
            row = QHBoxLayout()
            row.setSpacing(5)
            for text, btype in row_data:
                btn = CalculatorButton(text, btype)
                if btype == "number":
                    btn.clicked.connect(
                        partial(self._on_digit_button, text)
                    )
                else:
                    btn.clicked.connect(
                        partial(self._on_operator_button, text)
                    )
                row.addWidget(btn)
            layout.addLayout(row)

        # Last row
        last_row = QHBoxLayout()
        last_row.setSpacing(5)
        last_buttons = [
            ("±", "function"), ("0", "number"), (".", "number"), ("=", "equal"),
        ]
        for text, btype in last_buttons:
            btn = CalculatorButton(text, btype)
            if text == "=":
                btn.clicked.connect(self._on_equal_button)
            elif text == "±":
                btn.clicked.connect(self._on_sign_toggle)
            elif btype == "number":
                btn.clicked.connect(partial(self._on_digit_button, text))
            last_row.addWidget(btn)
        layout.addLayout(last_row)

        return widget

    def _create_scientific_buttons(self) -> QWidget:
        """Create scientific mode button layout."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Row 1: Memory
        mem_layout = QHBoxLayout()
        mem_layout.setSpacing(4)
        mem_buttons = [
            ("MC", "memory"), ("MR", "memory"),
            ("M+", "memory"), ("M-", "memory"), ("MS", "memory"),
        ]
        for text, btype in mem_buttons:
            btn = CalculatorButton(text, btype)
            btn.clicked.connect(partial(self._on_memory_button, text))
            mem_layout.addWidget(btn)
        layout.addLayout(mem_layout)

        # Row 2: Scientific functions
        sci_row1 = QHBoxLayout()
        sci_row1.setSpacing(4)
        sci_buttons1 = [
            ("sin", "function"), ("cos", "function"), ("tan", "function"),
            ("log", "function"), ("ln", "function"),
        ]
        for text, btype in sci_buttons1:
            btn = CalculatorButton(text, btype)
            btn.clicked.connect(
                partial(self._on_scientific_button, text)
            )
            sci_row1.addWidget(btn)
        layout.addLayout(sci_row1)

        # Row 3: More scientific
        sci_row2 = QHBoxLayout()
        sci_row2.setSpacing(4)
        sci_buttons2 = [
            ("√", "function"), ("x²", "function"), ("xʸ", "operator"),
            ("1/x", "function"), ("n!", "function"),
        ]
        for text, btype in sci_buttons2:
            btn = CalculatorButton(text, btype)
            if btype == "operator":
                btn.clicked.connect(
                    partial(self._on_operator_button, "^")
                )
            else:
                btn.clicked.connect(
                    partial(self._on_scientific_button, text)
                )
            sci_row2.addWidget(btn)
        layout.addLayout(sci_row2)

        # Row 4: Clear + basic ops
        row4 = QHBoxLayout()
        row4.setSpacing(4)
        row4_buttons = [
            ("CE", "clear"), ("C", "clear"), ("⌫", "clear"),
            ("÷", "operator"),
        ]
        for text, btype in row4_buttons:
            btn = CalculatorButton(text, btype)
            if text in ("CE", "C", "⌫"):
                btn.clicked.connect(partial(self._on_clear_button, text))
            else:
                btn.clicked.connect(partial(self._on_operator_button, text))
            row4.addWidget(btn)
        layout.addLayout(row4)

        # Number pad
        number_layouts = [
            [("7", "number"), ("8", "number"), ("9", "number"), ("×", "operator")],
            [("4", "number"), ("5", "number"), ("6", "number"), ("-", "operator")],
            [("1", "number"), ("2", "number"), ("3", "number"), ("+", "operator")],
        ]

        for row_data in number_layouts:
            row = QHBoxLayout()
            row.setSpacing(4)
            for text, btype in row_data:
                btn = CalculatorButton(text, btype)
                if btype == "number":
                    btn.clicked.connect(
                        partial(self._on_digit_button, text)
                    )
                else:
                    btn.clicked.connect(
                        partial(self._on_operator_button, text)
                    )
                row.addWidget(btn)
            layout.addLayout(row)

        # Last row
        last_row = QHBoxLayout()
        last_row.setSpacing(4)
        last_buttons = [
            ("±", "function"), ("0", "number"), (".", "number"), ("=", "equal"),
        ]
        for text, btype in last_buttons:
            btn = CalculatorButton(text, btype)
            if text == "=":
                btn.clicked.connect(self._on_equal_button)
            elif text == "±":
                btn.clicked.connect(self._on_sign_toggle)
            elif btype == "number":
                btn.clicked.connect(partial(self._on_digit_button, text))
            last_row.addWidget(btn)
        layout.addLayout(last_row)

        # Extra scientific row
        extra_row = QHBoxLayout()
        extra_row.setSpacing(4)
        extra_buttons = [
            ("π", "function"), ("e", "function"), ("|x|", "function"),
            ("10ˣ", "function"), ("mod", "operator"),
        ]
        for text, btype in extra_buttons:
            btn = CalculatorButton(text, btype)
            if btype == "operator":
                btn.clicked.connect(
                    partial(self._on_operator_button, "mod")
                )
            else:
                btn.clicked.connect(
                    partial(self._on_scientific_button, text)
                )
            extra_row.addWidget(btn)
        layout.addLayout(extra_row)

        return widget

    def _apply_theme(self) -> None:
        """Apply current theme to all widgets."""
        self._theme = ThemeManager.get_theme(self._current_theme_name)
        colors = self._theme["colors"]

        # Main window
        self.setStyleSheet(f"""
            QMainWindow {{
                background: qlineargradient(
                    x1: 0, y1: 0, x2: 0, y2: 1,
                    stop: 0 {colors['gradient_bg_start']},
                    stop: 1 {colors['gradient_bg_end']}
                );
            }}
            QMenuBar {{
                background-color: {colors['bg_secondary']};
                color: {colors['text_primary']};
                border-bottom: 1px solid {colors['border_display']};
                padding: 2px;
                font-size: {self._theme['font_sizes']['menu']}px;
            }}
            QMenuBar::item:selected {{
                background-color: {colors['bg_tertiary']};
                border-radius: 4px;
            }}
            QMenu {{
                background-color: {colors['bg_secondary']};
                color: {colors['text_primary']};
                border: 1px solid {colors['border_display']};
                border-radius: 8px;
                padding: 5px;
            }}
            QMenu::item {{
                padding: 6px 25px;
                border-radius: 4px;
            }}
            QMenu::item:selected {{
                background-color: {colors['bg_tertiary']};
            }}
            QStatusBar {{
                background-color: {colors['bg_secondary']};
                color: {colors['text_secondary']};
                border-top: 1px solid {colors['border_display']};
                font-size: 11px;
            }}
        """)

        # Apply to display
        self.display.apply_theme(self._theme)

        # Apply to all buttons
        for widget in self.findChildren(CalculatorButton):
            widget.apply_theme(self._theme)

        # Apply to history
        self.history_panel.apply_theme(self._theme)

        # Status bar theme indicator
        theme_emoji = "☀️" if self._current_theme_name == "Light" else "🌙"
        self.status_theme_label.setText(
            f"{theme_emoji} {self._current_theme_name}"
        )

        # Update angle mode display
        self.display.set_angle_mode(self.engine.angle_mode)

    def _connect_signals(self) -> None:
        """Connect all signals and slots."""
        # Keyboard input
        self.setFocusPolicy(Qt.StrongFocus)

    # --- Button Handlers ---
    def _on_digit_button(self, digit: str) -> None:
        """Handle digit button press."""
        result = self.engine.append_digit(digit)
        self._update_display(result)
        self.status_bar.showMessage(f"Input: {digit}", 1000)

    def _on_operator_button(self, operator: str) -> None:
        """Handle operator button press."""
        self.engine.append_operator(operator)
        self.display.set_expression(
            f"{self.engine.expression} ..."
        )
        self.status_bar.showMessage(f"Operator: {operator}", 1000)

    def _on_equal_button(self) -> None:
        """Handle equal button press."""
        result = self.engine.calculate()
        self._update_display(result)
        self.display.set_expression("")
        self._refresh_history()
        self.status_bar.showMessage("Calculated", 2000)

    def _on_clear_button(self, clear_type: str) -> None:
        """Handle clear button press."""
        if clear_type == "CE":
            result = self.engine.clear_entry()
        elif clear_type == "C":
            result = self.engine.clear_all()
            self.display.set_expression("")
        elif clear_type == "⌫":
            result = self.engine.backspace()
        self._update_display(result)

    def _on_sign_toggle(self) -> None:
        """Handle sign toggle."""
        result = self.engine.toggle_sign()
        self._update_display(result)

    def _on_scientific_button(self, func: str) -> None:
        """Handle scientific function button press."""
        func_map = {
            "sin": "sin", "cos": "cos", "tan": "tan",
            "log": "log", "ln": "ln", "√": "sqrt",
            "x²": "square", "1/x": "reciprocal", "n!": "factorial",
            "π": "pi", "e": "e_const", "|x|": "abs", "10ˣ": "ten_power",
        }
        actual_func = func_map.get(func, func)
        result = self.engine.calculate_scientific(actual_func)
        self._update_display(result)
        self._refresh_history()
        self.status_bar.showMessage(f"Function: {func}", 1500)

    def _on_memory_button(self, mem_op: str) -> None:
        """Handle memory operation button press."""
        current = self.engine._get_current_value()
        if mem_op == "MC":
            self.engine.memory_clear()
        elif mem_op == "MR":
            value = self.engine.memory_recall()
            self.engine._current_input = str(value)
            self.engine._is_new_input = True
            self._update_display(str(value))
        elif mem_op == "M+":
            self.engine.memory_add(current)
        elif mem_op == "M-":
            self.engine.memory_subtract(current)
        elif mem_op == "MS":
            self.engine.memory_store(current)

        has_mem = abs(self.engine.memory_value) > 1e-15
        self.display.set_memory_indicator(has_mem)
        self.status_bar.showMessage(
            f"Memory: {self.engine.memory_value}", 1500
        )

    # --- UI Updates ---
    def _update_display(self, text: str) -> None:
        """Update the main display."""
        if self.engine.is_error:
            self.display.set_text("Error")
        else:
            self.display.set_text(text)
        self.display.set_memory_indicator(
            abs(self.engine.memory_value) > 1e-15
        )

    def _refresh_history(self) -> None:
        """Refresh the history panel."""
        self.history_panel.update_history(self.engine.get_history())

    def _clear_history(self) -> None:
        """Clear calculation history."""
        self.engine.clear_history()
        self._refresh_history()
        self.status_bar.showMessage("History cleared", 2000)

    def _on_history_item_clicked(self, item: QListWidgetItem) -> None:
        """Handle clicking a history item."""
        index = item.data(Qt.UserRole)
        if index is not None:
            result = self.engine.load_from_history(index)
            self._update_display(result)
            self.status_bar.showMessage(
                f"Loaded from history: {result}", 2000
            )

    def _toggle_history(self, checked: bool) -> None:
        """Toggle history panel visibility."""
        self.history_panel.setVisible(checked)
        self._history_visible = checked

    def _toggle_scientific(self, checked: bool) -> None:
        """Toggle scientific mode."""
        self._scientific_mode = checked
        if checked:
            self.button_stack.setCurrentIndex(1)
        else:
            self.button_stack.setCurrentIndex(0)
        self.status_bar.showMessage(
            f"{'Scientific' if checked else 'Basic'} mode", 1500
        )

    def _open_settings(self) -> None:
        """Open settings dialog."""
        dialog = SettingsDialog(
            self._current_theme_name,
            self.engine.angle_mode,
            self
        )
        if dialog.exec() == QDialog.Accepted:
            settings = dialog.get_settings()
            if settings["theme"] != self._current_theme_name:
                self._current_theme_name = settings["theme"]
                self._apply_theme()
            self.engine.set_angle_mode(settings["angle_mode"])
            self.display.set_angle_mode(settings["angle_mode"])
            self.status_bar.showMessage("Settings applied", 2000)

    def _show_about(self) -> None:
        """Show about dialog."""
        dialog = AboutDialog(self)
        dialog.exec()

    def _show_shortcuts(self) -> None:
        """Show keyboard shortcuts dialog."""
        shortcuts = (
            "⌨️ Keyboard Shortcuts\n\n"
            "0-9, .       : Input digits and decimal\n"
            "+ - * /      : Arithmetic operators\n"
            "Enter, =     : Calculate result\n"
            "Backspace    : Delete last character\n"
            "Escape       : Clear all (C)\n"
            "Delete       : Clear entry (CE)\n"
            "Ctrl+H       : Toggle history panel\n"
            "Ctrl+S       : Toggle scientific mode\n"
            "Ctrl+,       : Open settings\n"
            "Ctrl+Q       : Exit application"
        )
        QMessageBox.information(self, "Keyboard Shortcuts", shortcuts)

    # --- Keyboard Handling ---
    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle keyboard input."""
        key = event.key()
        text = event.text()
        modifiers = event.modifiers()

        # Check for Ctrl combinations
        if modifiers & Qt.ControlModifier:
            if key == Qt.Key_H:
                checked = not self._history_visible
                self._toggle_history(checked)
                self._toggle_history_action.setChecked(checked)
                return
            elif key == Qt.Key_S:
                checked = not self._scientific_mode
                self._toggle_scientific(checked)
                self._toggle_scientific_action.setChecked(checked)
                return
            elif key == Qt.Key_Comma:
                self._open_settings()
                return
            elif key == Qt.Key_Q:
                self.close()
                return
            super().keyPressEvent(event)
            return

        # Digit keys
        if Qt.Key_0 <= key <= Qt.Key_9:
            self._on_digit_button(text)
            return

        # Decimal point
        if key == Qt.Key_Period:
            self._on_digit_button(".")
            return

        # Operators
        if key == Qt.Key_Plus:
            self._on_operator_button("+")
            return
        elif key == Qt.Key_Minus:
            self._on_operator_button("-")
            return
        elif key == Qt.Key_Asterisk:
            self._on_operator_button("×")
            return
        elif key == Qt.Key_Slash:
            self._on_operator_button("÷")
            return

        # Equal / Enter
        if key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Equal):
            self._on_equal_button()
            return

        # Clear operations
        if key == Qt.Key_Backspace:
            self._on_clear_button("⌫")
            return
        elif key == Qt.Key_Delete:
            self._on_clear_button("CE")
            return
        elif key == Qt.Key_Escape:
            self._on_clear_button("C")
            self.display.set_expression("")
            return

        super().keyPressEvent(event)

    def closeEvent(self, event) -> None:
        """Handle window close event."""
        # Could save settings here
        event.accept()


# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    app.setApplicationName("Modern Calculator")
    app.setOrganizationName("CalcApp")
    app.setApplicationVersion("2.0.0")

    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # Create and show the main window
    calculator = ModernCalculator()
    calculator.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()