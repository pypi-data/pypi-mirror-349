from typing import Optional, Union, overload

from PySide6.QtCore import (
    QByteArray,
    QXmlStreamReader,
)
from PySide6.QtGui import Qt
from PySide6.QtSvgWidgets import QSvgWidget


class SvgWidget(QSvgWidget):

    def __init__(
        self,
        value: Optional[
            Union[
                QXmlStreamReader, str, QByteArray, bytes, bytearray, memoryview
            ]
        ] = None,
    ) -> None:
        super().__init__()

        self._q_svg_renderer = self.renderer()

        if value:
            self.load(value)

    @overload
    def load(self, value: QXmlStreamReader, /) -> bool: ...

    @overload
    def load(self, value: str, /) -> bool: ...

    @overload
    def load(
        self,
        value: QByteArray | bytes | bytearray | memoryview,
        /,
    ) -> bool: ...

    def load(self, value, /) -> bool:
        _ = self._q_svg_renderer.load(value)
        self._q_svg_renderer.setAspectRatioMode(
            Qt.AspectRatioMode.KeepAspectRatio
        )
        return _
