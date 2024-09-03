import sys
import os
import pathlib
from twisted.internet import reactor

from PySide6.QtWidgets import QApplication, QStyleFactory, QStyle
from PySide6.QtWidgets import QMainWindow

from PySide6.QtCore import QTimer, Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

from src.qtgui.MainWindow.UI.MainUI import Ui_MainWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    # Main window of the application
    def __init__(self, reactor, parent=None):
        super(MainWindow, self).__init__(parent)
        print(QStyleFactory.keys())
        self.reactor = reactor

        self.setupUi(self)

        self.addSignals()
        
        relative_path = 'test_paper.pdf'
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), relative_path))
        print(abs_path)

        document = QPdfDocument(self)
        
        document.load(abs_path)
        self.pdfView.setPageMode(QPdfView.PageMode.MultiPage)
        self.pdfView.setDocument(document)
        print(self.pdfView.document().pageCount())

    def addSignals(self):
        self.pdfView.documentChanged.connect(lambda: self.queueGroupBox.setFixedWidth(self.pdfView.width() / 3))
    
    def resizeEvent(self, event):
        self.queueGroupBox.setFixedWidth(self.pdfView.width() / 3)
    
    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)
        print("Closing the application")
        event.accept()


def run_interface():

    # Make the event loop interruptable quickly
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication([])
    app.setAttribute(Qt.AA_ShareOpenGLContexts)
    app.setAttribute(Qt.AA_EnableHighDpiScaling)

    app.setStyle(QStyleFactory.create('Fusion'))

    if 'twisted.internet.reactor' in sys.modules:
        del sys.modules['twisted.internet.reactor']

    import ReactorCore

    ReactorCore.install()

    # DO NOT move the following import to the top!
    from twisted.internet import reactor

    # Show the main window
    mainwindow = MainWindow(reactor)

    mainwindow.show()

    timer = QTimer()
    timer.timeout.connect(lambda: None)
    timer.start(100)

    # No need to .exec_ - the reactor takes care of it.
    reactor.run()