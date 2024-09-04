from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QSpinBox, QLabel, QPushButton, QDialogButtonBox
)
from PySide6.QtCore import Qt, QThread, Signal, QObject
from PySide6.QtGui import QMovie
import sys
from PySide6.QtWidgets import QApplication

from src.web.Scraper.scraper import Scraper

class LoadProxyDialog(QDialog):
    """
    Modal dialog class to open when user is prompted to begin scraping
    """
    def __init__(self, scraper: Scraper = None):
        super().__init__()

        self.setWindowTitle("Scraping Selection")

        self.scraper = scraper

        layout = QVBoxLayout(self)

        # Spinbox for number selection
        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(1, 500)
        layout.addWidget(self.spin_box)

        # Buttons
        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Ok, self)
        button_box.button(QDialogButtonBox.Cancel).setText("Cancel")
        button_box.button(QDialogButtonBox.Ok).setText("Start")
        button_box.rejected.connect(self.reject)
        button_box.accepted.connect(self.start_loading)
        layout.addWidget(button_box)

        # Loading animation and label (initially hidden)
        self.loading_layout = QHBoxLayout()
        self.loading_label = QLabel("Loading...", self)
        self.loading_label.setVisible(False)

        self.loading_gif = QLabel(self)
        self.movie = QMovie("loading.gif")  # KopiteCowboy, CC BY-SA 4.0 <https://creativecommons.org/licenses/by-sa/4.0>, via Wikimedia Commons
        self.loading_gif.setMovie(self.movie)
        self.loading_gif.setVisible(False)

        self.loading_layout.addWidget(self.loading_gif)
        self.loading_layout.addWidget(self.loading_label)
        layout.addLayout(self.loading_layout)

    def start_loading(self):
        # Hide the spinbox and buttons, show loading animation
        self.spin_box.setEnabled(False)
        self.findChild(QDialogButtonBox).setEnabled(False)
        self.loading_label.setVisible(True)
        self.loading_gif.setVisible(True)
        self.movie.start()

        # Start the loading thread
        self.get_proxy()

    def get_spinbox_value(self):
        return self.spin_box.value()

    def get_proxy(self):
        self.scraper.initiate_proxy()

