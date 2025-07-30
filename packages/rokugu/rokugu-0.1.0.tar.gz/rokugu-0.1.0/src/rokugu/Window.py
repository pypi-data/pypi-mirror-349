from PySide6.QtGui import QKeySequence, QShortcut, Qt
from PySide6.QtWidgets import QApplication, QMainWindow


class Window(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        ctrl_q = QShortcut(
            QKeySequence(Qt.KeyboardModifier.ControlModifier, Qt.Key.Key_Q),
            self,
        )
        ctrl_q.activated.connect(QApplication.quit)
