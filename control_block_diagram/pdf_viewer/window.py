from PyQt5 import QtCore, QtWebEngineWidgets


class Window(QtWebEngineWidgets.QWebEngineView):
    """
        Window used by the PDF Viewer
    """
    def __init__(self, pdf, size=(800, 600)):
        """Initializes a Window"""
        super(Window, self).__init__()

        # Settings of the window
        self.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.PluginsEnabled, True)
        self.settings().setAttribute(
            QtWebEngineWidgets.QWebEngineSettings.PdfViewerEnabled, True)
        self.load(QtCore.QUrl.fromUserInput(pdf))
        self.setWindowTitle('Control Block Diagram')
        self.setGeometry(100, 50, size[0], size[1])
