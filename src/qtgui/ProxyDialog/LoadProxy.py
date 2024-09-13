import sys

from PySide6.QtWidgets import QDialog, QDialogButtonBox
from PySide6.QtGui import QMovie
from PySide6.QtCore import QSize

from twisted.internet import threads


from src.web.Scraper.scraper import Scraper
from src.qtgui.ProxyDialog.UI.ProxyDialogUI import Ui_LoadProxyDialog

class LoadProxyDialog(QDialog, Ui_LoadProxyDialog):
    """
    Modal dialog class to open when user is prompted to begin scraping
    """
    def __init__(self, scraper: Scraper = None, parent=None):
        super(LoadProxyDialog, self).__init__(parent)

        self.setupUi(self)

        self.parent = parent
        self.scraper = scraper

        self.lbl_loading.setVisible(True)

        self.addSignals()

    def addSignals(self):
        self.cmdCancel.clicked.connect(self.close)
        self.cmdScrape.clicked.connect(self.start_loading)

    def start_loading(self):
        # Hide the spinbox and buttons, show loading animation
        def disable():
            self.cmdCancel.setEnabled(False)
            self.cmdScrape.setEnabled(False)
            self.spinAmount.setEnabled(False)
            self.lbl_loading.setText("Initializing Scraper...")
        
        thread = threads.deferToThread(disable)
        thread.addCallback(lambda _: self.get_proxy())

    def get_spinbox_value(self):
        return self.spin_box.value()

    def get_proxy(self):
        sys.stdout = OutputRedirector(self.lbl_loading)
        self.scraper.initiate_proxy()
        sys.stdout = sys.__stdout__
        self.lbl_loading.setText(f'{self.lbl_loading.text()}. Closing window...')
        self.parent.scrapingStartSignal.emit(self.scraper, self.spinAmount.value())
        self.window().close()

class OutputRedirector:
    def __init__(self, label):
        self.label = label
        self.buffer = ""

    def write(self, text):
        self.buffer += text
        if "\n" in text:
            # Extract the line and update the label with it
            lines = self.buffer.split("\n")
            for line in lines[:-1]:  # Handle each complete line
                self.label.setText(line)
            self.buffer = lines[-1]  # Keep the rest in buffer for incomplete lines

    def flush(self):
        pass  # Required method for file-like behavior

