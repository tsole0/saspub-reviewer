import sys
import os
import pathlib
import datetime
from twisted.internet import reactor

from PySide6.QtWidgets import QApplication, QStyleFactory, QStyle
from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QDialog

from PySide6.QtCore import QTimer, Qt
from PySide6.QtPdf import QPdfDocument
from PySide6.QtPdfWidgets import QPdfView

from src.qtgui.MainWindow.UI.MainUI import Ui_MainWindow

from src.web.Scraper.scraper import Scraper
from src.qtgui.ProxyDialog.LoadProxy import LoadProxyDialog

class MainWindow(QMainWindow, Ui_MainWindow):
    # Main window of the application
    def __init__(self, reactor, parent=None):
        super(MainWindow, self).__init__(parent)
        self.reactor = reactor

        self.setupUi(self)

        self.addSignals()
        self.initialize_ui()

        # Instance variables
        self.scraper = None
    
    def initialize_ui(self):
        """
        Initialize UI with values
        """
        current_year = datetime.datetime.now().year
        self.spinYear.setMaximum(current_year)
        self.spinYear.setValue(self.spinYear.maximum())

        #Clear queuebox
        for i in range(self.queueBox.count(), 0, -1):
            self.queueBox.removeItem(i - 1)

    def addSignals(self):
        self.pdfView.documentChanged.connect(lambda: self.queueGroupBox.setFixedWidth(self.pdfView.width() / 4))
        self.cmdScrape.clicked.connect(self.scrape)
        self.queueBox.currentChanged.connect(self.checkSetQueueDefault)

    def checkSetQueueDefault(self):
        """Add no papers in queue message if there are no papers to display"""
        if self.queueBox.count() == 0:
            default_item = QueueItem("", self.queueBox)
            self.queueBox.insertItem(0, default_item, "No papers in queue")
    
    def scrape(self):
        self.scraper = Scraper() if self.scraper is None else self.scraper
        proxyDialog = LoadProxyDialog(scraper=self.scraper)
        if proxyDialog.exec_() == QDialog.Accepted:
            amount_papers = proxyDialog.get_spinbox_value()
        else:
            return
        print(f"{amount_papers} papers to scrape")
        year = self.spinYear.value()
        self.scraper.searchYear(year)
    
    def setPaper(self, path):
        """Set paper displayed in pdfView"""
        document = QPdfDocument(self)
        document.load(path)
        self.pdfView.setDocument(document)

    ### EVENTS ###
    
    def resizeEvent(self, event):
        self.queueGroupBox.setFixedWidth(self.pdfView.width() / 3)
    
    def closeEvent(self, event):
        self.reactor.callFromThread(self.reactor.stop)
        print("Closing the application")
        event.accept()

class QueueItem(QWidget):
    def __init__(self, label_text='', parent=None):
        super().__init__(parent)
        
        # Create a QVBoxLayout to manage the widget's layout
        layout = QVBoxLayout(self)
        
        # Create a QLabel and set its text
        self.label = QLabel(label_text)
        
        # Add the QLabel to the layout
        layout.addWidget(self.label)


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