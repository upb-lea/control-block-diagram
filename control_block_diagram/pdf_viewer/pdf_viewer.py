import sys
from PyQt5 import QtWidgets
from multiprocessing import Process
from .window import Window


class PDFViewer:
    """
        Viewer to show a PDF File
    """

    def __init__(self, pdf):
        """
        Initializes a pdf viewer for a certain pdf
            pdf: pdf to be shown
        """
        self._pdf = pdf
        self._process = None

    def open_pdf(self):
        """opens a window wiht the pdf in the background"""
        self._process = Process(target=self._show_pdf, args=[self._pdf], name='ControlBlockDiagram')
        self._process.start()

    def close_pdf(self):
        """closes the window"""
        self._process.kill()

    def show_pdf(self):
        """opens a window with the pdf file"""
        app = QtWidgets.QApplication(sys.argv)
        window = Window(self._pdf)
        window.show()
        app.exec_()

    @staticmethod
    def _show_pdf(pdf):
        """opens a window for a given pdf file"""
        app = QtWidgets.QApplication(sys.argv)
        window = Window(pdf)
        window.show()
        app.exec_()
