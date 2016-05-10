"""
CustomQtDialog.py - Example of how to create a custom Qt dialog in Deadline monitor
Copyright Thinkbox Software 2016
"""

import sys

from System.IO import *
from Deadline.Scripting import *

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.QtGui

########################################################################
# Globals
########################################################################
dialog = None

########################################################################
# Custom QDialog with some basic controls.
########################################################################


class CustomQtDialog(QDialog):

    def __init__(self, parent=None):
        super(CustomQtDialog, self).__init__(parent)

        # set the main layout as a vertical one
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        binDir = RepositoryUtils.GetBinDirectory()
        randomImage = Path.Combine(binDir, "/submission/MayaVRayDBR/Main/SubmitVRay.png")

        # display an image
        self.pixMap = QPixmap(randomImage)
        self.imageLabel = QLabel()
        self.imageLabel.setPixmap(self.pixMap)
        self.mainLayout.addWidget(self.imageLabel)

        # a label to display stuff
        self.displayLabel = QLabel("Click a button!")
        self.mainLayout.addWidget(self.displayLabel)

        # this horizontal layout will contain a bunch of buttons
        self.buttonLayout = QHBoxLayout()
        self.button1 = QPushButton("1")
        self.buttonLayout.addWidget(self.button1)

        self.button2 = QPushButton("2")
        self.buttonLayout.addWidget(self.button2)

        self.closeButton = QPushButton("Close")
        self.buttonLayout.addWidget(self.closeButton)

        self.mainLayout.addLayout(self.buttonLayout)

        # hook up the button signals to our slots
        self.button1.clicked.connect(self.button1Pressed)
        self.button2.clicked.connect(self.button2Pressed)
        self.closeButton.clicked.connect(self.closeButtonPressed)

    @pyqtSlot(bool)
    def button1Pressed(self, checked):
        self.displayLabel.setText("You pressed the first button!")

    @pyqtSlot(bool)
    def button2Pressed(self, checked):
        self.displayLabel.setText("You pressed the second button!")

    @pyqtSlot(bool)
    def closeButtonPressed(self, checked):
        self.done(0)

########################################################################
# Main Function Called By Deadline
########################################################################


def __main__():
    global dialog

    # Create an instance of our custom dialog, and show it
    dialog = CustomQtDialog()
    dialog.setVisible(True)
