from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow

from src.qtgui.MainWindow.UI import MainUI

class MainWindow(QMainWindow, MainUI):
    # Main window of the application
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setupUi(self)


def run_interface():

    # Make the event loop interruptable quickly
    import signal
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication([])

    import ReactorCore

    ReactorCore.install()

    # DO NOT move the following import to the top!
    from twisted.internet import reactor

    # Show the main SV window
    mainwindow = MainWindow()