"""
Estilos CSS para la aplicación PyQt6
Define la apariencia visual minimalista y moderna
"""

DARK_STYLESHEET = """
QMainWindow, QDialog {
    background-color: #1e1e1e;
    color: #ffffff;
}

QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
}

QLabel {
    color: #ffffff;
    font-size: 12px;
}

QPushButton {
    background-color: #0d47a1;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
    font-weight: bold;
    font-size: 12px;
}

QPushButton:hover {
    background-color: #1565c0;
}

QPushButton:pressed {
    background-color: #0d3a87;
}

QPushButton#primaryBtn {
    background-color: #2196f3;
    padding: 10px 20px;
    font-size: 13px;
}

QPushButton#primaryBtn:hover {
    background-color: #42a5f5;
}

QPushButton#dangerBtn {
    background-color: #d32f2f;
}

QPushButton#dangerBtn:hover {
    background-color: #f44336;
}

QPushButton#successBtn {
    background-color: #388e3c;
}

QPushButton#successBtn:hover {
    background-color: #4caf50;
}

QLineEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 8px;
    font-size: 12px;
}

QLineEdit:focus {
    border: 2px solid #2196f3;
    background-color: #2d2d2d;
}

QTextEdit {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 8px;
    font-size: 12px;
}

QTextEdit:focus {
    border: 2px solid #2196f3;
}

QComboBox {
    background-color: #2d2d2d;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 4px;
    padding: 8px;
    font-size: 12px;
}

QComboBox:focus {
    border: 2px solid #2196f3;
}

QComboBox::drop-down {
    border: none;
    padding-right: 4px;
}

QComboBox QAbstractItemView {
    background-color: #2d2d2d;
    color: #ffffff;
    selection-background-color: #2196f3;
}

QTableWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    gridline-color: #404040;
    border: 1px solid #404040;
    border-radius: 4px;
}

QTableWidget::item {
    padding: 4px;
}

QTableWidget::item:selected {
    background-color: #2196f3;
}

QHeaderView::section {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 8px;
    border: none;
    border-right: 1px solid #404040;
    border-bottom: 1px solid #404040;
    font-weight: bold;
}

QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 12px;
    border: none;
}

QScrollBar::handle:vertical {
    background-color: #404040;
    border-radius: 6px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background-color: #505050;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    border: none;
    background: none;
}

QFrame {
    background-color: #1e1e1e;
    color: #ffffff;
    border: none;
}

QMessageBox {
    background-color: #1e1e1e;
}

QMessageBox QLabel {
    color: #ffffff;
}

QMessageBox QPushButton {
    min-width: 60px;
}

QTabWidget::pane {
    border: 1px solid #404040;
}

QTabBar::tab {
    background-color: #2d2d2d;
    color: #ffffff;
    padding: 8px 16px;
    border: 1px solid #404040;
}

QTabBar::tab:selected {
    background-color: #1e1e1e;
    border-bottom: 2px solid #2196f3;
}
"""
