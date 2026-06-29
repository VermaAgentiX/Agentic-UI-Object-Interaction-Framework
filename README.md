

<p align="center">

<h1 align="center">🚀 Agentic UI Object Interaction (AUOI)</h1>

<h3 align="center">
A New Paradigm for AI-Native Desktop Systems
</h3>

<p align="center">
<b>Beyond Pixels. Beyond Clicks.</b><br>
Empowering AI Agents to interact directly with live UI objects instead of screenshots, OCR, or mouse automation.
</p>

</p>

---

## 📖 Overview
Introducing, An AI agent framework interacts directly with live UI objects through tools mehods instead of using pixels, OCR, or mouse automation.

**Agentic UI Object Interaction (AUOI)** is a new interaction paradigm where AI agents communicate directly with graphical user interface (GUI) objects rather than controlling applications through mouse movements, keyboard simulation, screenshots, or computer vision.

Instead of treating the GUI as an image, AUOI exposes the application's **live object tree** (buttons, labels, windows, tables, layouts, etc.) as structured tools that an AI agent can understand and manipulate safely.

This approach enables intelligent, deterministic, fast, and scalable desktop automation.

---

# Why AUOI?

Current AI desktop agents work like humans.

```
Screenshot
      │
      ▼
 Vision Model
      │
      ▼
 Mouse & Keyboard
      │
      ▼
 Application
```

This approach is:

* Slow
* Error-prone
* Resolution dependent
* OCR dependent
* Requires image understanding

---

AUOI works differently.

```
AI Agent
    │
    ▼
LangGraph Tools
    │
    ▼
UI Controller
    │
    ▼
Qt Widget Objects
```

No screenshots.

No OCR.

No pixel detection.

No mouse automation.

---

# AUOI Architecture

```text
                    ┌────────────────────────────┐
                    │        Human User          │
                    └─────────────┬──────────────┘
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │      LangGraph Agent       │
                    │        (LLM Brain)         │
                    └─────────────┬──────────────┘
                                  │
                         Tool Calling API
                                  │
                                  ▼
                    ┌────────────────────────────┐
                    │     AUOI Controller        │
                    └─────────────┬──────────────┘
                                  │
                    Widget Registry / Runtime
                                  │
      ┌───────────────────────────┼───────────────────────────┐
      ▼                           ▼                           ▼
 QPushButton                  QLabel                     QDial
 setText()                 setText()                 setValue()
 hide()                    show()                   hide()
 click()                   style()                  resize()
```

---

# Internal Architecture

```text
MainWindow
│
├── Widget Registry
│      │
│      ├── pushButton
│      ├── label
│      ├── dial
│      ├── table
│      ├── progressBar
│      └── ...
│
├── UI Controller
│      │
│      ├── execute(widget, action)
│      ├── validate()
│      ├── dispatch()
│      └── update()
│
└── LangGraph Tool
       │
       └── ui_action()
```

---

# Working Flow

```text
User

↓

"Make the application fullscreen."

↓

LLM

↓

Tool Call

↓

ui_action(
    widget="window",
    action="fullscreen"
)

↓

UI Controller

↓

window.showFullScreen()

↓

Qt Runtime

↓

Window Updated
```

---

# Example

## User

> Change the button text to **Start**

---

## Tool Call

```python
ui_action(
    widget="pushButton",
    action="set_text",
    value="Start"
)
```

---

## Controller

```python
controller.execute(
    "pushButton",
    "set_text",
    "Start"
)
```

---

## Qt Runtime

```python
pushButton.setText("Start")
```

---

## Result

```
PushButton

↓

Start
```

---

# Supported Operations

## Window

* Fullscreen
* Restore
* Maximize
* Minimize
* Close
* Show
* Hide

---

## Widgets

* Set Text
* Show
* Hide
* Enable
* Disable
* Move
* Resize
* Set Value
* Click
* Change Style
* Tooltip
* Geometry
* Alignment
* Colors

---

## Future Support

* Dynamic Layout Editing
* Drag & Drop
* Theme Switching
* Animation Control
* Camera Widgets
* Charts
* Tables
* Live Dashboards
* Custom Widgets

---

# Comparison

| Traditional GUI Agent | AUOI              |
| --------------------- | ----------------- |
| Screenshot-based      | Object-based      |
| OCR                   | Widget Properties |
| Mouse Clicks          | Method Calls      |
| Keyboard Simulation   | Direct API        |
| Vision Models         | Object Registry   |
| Pixel Coordinates     | Object Names      |
| Slow                  | Fast              |
| Error Prone           | Deterministic     |

---

# Advantages

✅ No OCR

✅ No Screenshots

✅ No Computer Vision

✅ No Mouse Automation

✅ Faster Execution

✅ Deterministic

✅ Safe Tool Execution

✅ Framework Extensible

✅ Runtime Widget Discovery

✅ Object-Level Intelligence

---

# Example Widget Registry

```python
{
    "window": QMainWindow,

    "pushButton": QPushButton,

    "labelStatus": QLabel,

    "progressCPU": QProgressBar,

    "dial": QDial,

    "tableLogs": QTableWidget,

    "terminal": QTextEdit
}
```

---

# Example Tool

```python
ui_action(
    widget="progressCPU",
    action="set_value",
    value="82"
)
```

---

# Framework Support (Planned)

* ✅ PySide6 / Qt
* ⏳ PyQt6
* ⏳ Tkinter
* ⏳ Kivy
* ⏳ Electron
* ⏳ Flutter
* ⏳ React
* ⏳ WPF
* ⏳ JavaFX

---

# Vision

AUOI aims to become a universal interface layer between AI agents and graphical applications.

Instead of interacting with pixels, future AI systems will communicate directly with structured UI objects through secure, framework-independent APIs.

This transforms traditional GUI applications into **AI-native applications**.

---

# Roadmap

* [ ] Qt Runtime Object Registry
* [ ] Universal UI Controller
* [ ] LangGraph Integration
* [ ] Dynamic Widget Discovery
* [ ] Safe Action Dispatcher
* [ ] Multi-Window Support
* [ ] Cross-Framework Support
* [ ] Open API Specification
* [ ] AUOI SDK
* [ ] Developer Documentation

---

# Author

**Abhishek Verma**

Software Engineer • AI/ML Engineer • Researcher

---

# License

MIT License

---

# Citation

If you use or build upon the AUOI concept in your work, please cite this repository.

---

<p align="center">

### ⭐ If you find AUOI interesting, consider giving this repository a Star!

**Agentic UI Object Interaction (AUOI)**

**Beyond Pixels. Beyond Clicks.**

</p>
