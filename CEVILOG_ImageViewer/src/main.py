from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPalette, QIcon
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout, QVBoxLayout, \
                            QGridLayout, QFileDialog, QMessageBox, QPushButton, \
                            QComboBox, QTextEdit
import image_processing as image_processing
import numpy as np
import cv2
import sys
import os


class CevilogUI(QtWidgets.QWidget):
    """
    Main Window of the Cevilog Image Viewer UI
    The whole interface is built using vertical or horizontale layouts
    """
    def __init__(self):
        super().__init__()
        self.setGeometry(500, 200, 1200, 640)  #(xpos, ypos, w, h)
        self.setWindowTitle("CEVILOG image viewer")
        self.setWindowIcon(QIcon("ressources/SquareLogo.png"))

        #Main H-Layout
        outerLayout = QHBoxLayout()

        ##Left V-Layout
        leftLayout = QVBoxLayout()
        ###Top image H-Layout
        topImageHLayout = QHBoxLayout()
        openFolder = QPushButton("Image folder")
        openFolder.clicked.connect(self.open_folder) 
        openFolder.setMaximumSize(128, 24)
        topImageHLayout.addWidget(openFolder)
        self.folderPath = QTextEdit()
        self.folderPath.setReadOnly(True)
        self.folderPath.setMaximumSize(480, 24)
        topImageHLayout.addWidget(self.folderPath)
        leftLayout.addLayout(topImageHLayout)

        ##Image layout
        self.imageLabel = QLabel()
        self.imageLabel.setStyleSheet("border-width: 3px; border-style: outset")
        self.imageLabel.setMaximumSize(640, 480)
        leftLayout.addWidget(self.imageLabel)
        ###Button H-Layout
        buttonLayout = QHBoxLayout()
        self.inspectButton = QPushButton("Inspect")
        self.inspectButton.setDisabled(True)
        self.inspectButton.clicked.connect(self.inspect)
        buttonLayout.addWidget(self.inspectButton)
        self.nextButton = QPushButton("Next")
        self.nextButton.setDisabled(True)
        self.nextButton.clicked.connect(self.next_image)
        buttonLayout.addWidget(self.nextButton)
        leftLayout.addLayout(buttonLayout)

        ##Right V-Layout
        rightLayout = QVBoxLayout()
        ###Right middle V-Layout
        rightLayout2 = QVBoxLayout()
        modelLoadedTxt = QLabel("Model Loaded")
        modelLoadedTxt.setMaximumHeight(18)
        rightLayout2.addWidget(modelLoadedTxt)
        self.modelSelect = QComboBox()
        self.modelSelect.addItem("YOLOv7_TireDetection")
        rightLayout2.addWidget(self.modelSelect)
        rightLayout2.addSpacing(350)
        rightLayout2.setContentsMargins(50, 10, 10, 10)
        rightLayout.addLayout(rightLayout2)

        #Collate everything
        outerLayout.addLayout(leftLayout)
        outerLayout.addLayout(rightLayout)
        self.setLayout(outerLayout)
        
 
    def open_folder(self):
        """
        Open image folder button click event
        """
        dialog = QFileDialog()
        self.folder_path = dialog.getExistingDirectory(None, "Select Folder")
        self.list_of_images = os.listdir(self.folder_path)
        self.list_of_images = sorted(self.list_of_images)
        #print("Number of images in the selected foler: {}".format(len(self.list_of_images)))
        fileName = os.path.join(self.folder_path, self.list_of_images[0])

        #Update the self.folderPath text box with the name of the folder path
        self.folderPath.setText(str(self.folder_path))

        #Try to display the current image
        if fileName:
            image = QImage(fileName)
            #Cope with possible non-ascii characters in image path
            self.cv_image = cv2.imdecode(np.fromfile(fileName, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
            self.nextButton.setEnabled(True)
            self.inspectButton.setEnabled(True)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." %fileName)
                return
            self.imageLabel.setPixmap(QPixmap.fromImage(image).scaled(
                                      self.imageLabel.frameGeometry().width()- 6, 
                                      self.imageLabel.frameGeometry().height(), 
                                      Qt.KeepAspectRatio, 
                                      Qt.SmoothTransformation)
                                      )
            self.scaleFactor = 1.0
            self.i = 0
        

    def next_image(self):
        """
        Next image button click event
        """
        total_images = len(self.list_of_images)
        if self.list_of_images:
            try:
                self.i = (self.i + 1) % total_images
                fileName = os.path.join(self.folder_path, self.list_of_images[self.i])
                if fileName:
                    image = QImage(fileName)
                    #Cope with possible non-ascii characters in image path
                    self.cv_image = cv2.imdecode(np.fromfile(fileName, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
                    if image.isNull():
                        QMessageBox.information(self, "Image Viewer", "Cannot load %s." %fileName)
                        return
                    self.imageLabel.setPixmap(QPixmap.fromImage(image).scaled(
                                            self.imageLabel.frameGeometry().width()- 6, 
                                            self.imageLabel.frameGeometry().height(), 
                                            Qt.KeepAspectRatio, 
                                            Qt.SmoothTransformation)
                                            )
                    self.scaleFactor = 1.0
            except ValueError as e:
                print("The selected folder does not contain any images")


    def inspect(self):
        """
        Function called when inspect button pressed
        """
        im2 = image_processing.changeBrightness(self.cv_image, 50)
        cv2.imshow("brightness_change", im2)


# Main method
def window():
    app = QApplication(sys.argv)
    ceviUI = CevilogUI()
    ceviUI.show()
    sys.exit(app.exec_())

window()