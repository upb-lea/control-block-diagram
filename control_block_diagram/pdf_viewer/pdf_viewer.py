import sys
from PyQt5 import QtWidgets
from multiprocessing import Process
from .window import Window


class PDFViewer:
    def __init__(self, pdf):
        self._pdf = pdf
        self._process = None

    def open_pdf(self):
        self._process = Process(target=self._show_pdf, args=[self._pdf], name='ControlBlockDiagram')
        self._process.start()

    def close_pdf(self):
        self._process.kill()

    @staticmethod
    def _show_pdf(pdf):
        app = QtWidgets.QApplication(sys.argv)
        window = Window(pdf)
        window.show()
        app.exec_()

    def show_pdf(self):
        app = QtWidgets.QApplication(sys.argv)
        window = Window(self._pdf)
        window.show()
        app.exec_()
