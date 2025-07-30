from io import StringIO
from typing import TextIO

import pygments
from pygments.formatters import HtmlFormatter
from pygments.lexers.python import PythonTracebackLexer
from PySide6 import QtWidgets


class StdRedirect(StringIO):

    def __init__(
        self,
        initial_value: str | None = "",
        newline: str | None = "\n",
    ) -> None:
        super().__init__(initial_value, newline)
        self.text_edits: list[QtWidgets.QTextEdit] = []
        self.orig_stream: TextIO | None = None
        self.text = ""

    def write(self, s: str) -> int:
        self.text += s
        if self.orig_stream is not None:
            self.orig_stream.write(s)
        for text_edit in self.text_edits:

            html = pygments.highlight(
                self.text,
                lexer=PythonTracebackLexer(),
                formatter=HtmlFormatter(nobackground=True, noclasses=True, full=True),
            )
            text_edit.setHtml(html)
        return super().write(s)
