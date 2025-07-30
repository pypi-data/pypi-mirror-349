from typing import Optional, override

from PySide6.QtGui import QResizeEvent, QShowEvent, Qt
from PySide6.QtWidgets import QLabel, QSizePolicy


class ElidedLabelWidget(QLabel):
    def __init__(
        self,
        text: Optional[str] = None,
        text_elide_mode: Qt.TextElideMode = Qt.TextElideMode.ElideRight,
    ) -> None:
        super().__init__(text)

        self._text_elide_mode = text_elide_mode

        self.setWordWrap(False)
        self.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

    def _handle(self, width: int) -> None:
        q_string = self.fontMetrics().elidedText(
            self.text(), self._text_elide_mode, width
        )
        self.setText(q_string)

    def text_elide_mode(self) -> Qt.TextElideMode:
        return self._text_elide_mode

    def set_text_elide_mode(self, mode: Qt.TextElideMode) -> None:
        self._text_elide_mode = mode
        self._handle(self.width())

    @override
    def showEvent(self, event: QShowEvent, /) -> None:
        self._handle(self.width())
        return super().showEvent(event)

    @override
    def resizeEvent(self, event: QResizeEvent, /) -> None:
        self._handle(event.size().width())
        return super().resizeEvent(event)
