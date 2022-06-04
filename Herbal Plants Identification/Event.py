# Importing necessary packages 
from ast import Str, While
from cProfile import label
from contextlib import nullcontext
from multiprocessing import connection
from pydoc import locate, text
import site
import sys


import random
import os
from tokenize import String
from types import new_class
from typing import Mapping
import cv2
from cv2 import waitKeyEx
from keras.backend import conv2d
from keras.models import load_model
from keras.preprocessing import image 
from keras.preprocessing.image import img_to_array, load_img
from matplotlib.pyplot import close
import numpy as np 

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import *
from AppUI import Ui_MainWindow


from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication

import Image

import sqlite3 #Imports to use use SQLite Database 


from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.uic import loadUi
import time


class MainForm(QMainWindow):
    
    def __init__(self):
        super(MainForm, self).__init__()
        
        self.userInterface = Ui_MainWindow()
        self.userInterface.setupUi(self) 
        
        self.imagepath="C:/Users/Dan/Desktop/Images/"
        self.userInterface.predictImage.setEnabled(False) 
        self.userInterface.viewLocatio.setEnabled(False) 
        self.userInterface.Capture_2.setEnabled(False) 
        self.userInterface.InsertImage.clicked.connect(self.browse_image)
        self.userInterface.predictImage.clicked.connect(self.predict_image)
        self.userInterface.viewLocatio.clicked.connect(self.locate)
        self.userInterface.Capture_2.clicked.connect(self.translate)
        self.userInterface.Capture.clicked.connect(self.openCam)
        
       
	    
        self.imageFile = ""
        self.filename=""
        self.fileNameDirectory = ""
        self.prediction = ""
        self.logic=0
        self.value=1
        self.indexer =0         #INDEX FOR MAPPING
        self.transpoint=0       #SWITCH LANGUGE
    
    
    def openCam(self):

        
        QMessageBox.warning(self, "Instruction ", "Please be reminded that to Capture a Plant just hit 'C' key on the keyboard.") 
        self.userInterface.Capture.setEnabled(False)
        self.userInterface.InsertImage.setEnabled(False)
        vid = cv2.VideoCapture(0)
  
    
        t_end = time.time() + 20
        while time.time() < t_end:  # Wait 5 seconds before window stops
 
         ret, frame = vid.read()

         cv2.imshow('Capture Plant', frame)
         if cv2.waitKey(1) & 0xFF == ord('C'):
            cv2.imwrite(self.imagepath +'This_Image.png',frame)
            vid.release()
            self.imageFile,_= QtWidgets.QFileDialog.getOpenFileName(self, "Captured Image: ", self.imagepath, "This_Image.png")

            if self.imageFile:  
                pngfile = QtGui.QPixmap(self.imageFile) # We create the image as a QPixmap widget, using your filename.
                pngfile = pngfile.scaled(self.userInterface.label_image.height(), self.userInterface.label_image.width(), QtCore.Qt.KeepAspectRatioByExpanding)
                self.userInterface.label_image.setPixmap(pngfile) 
                self.userInterface.label_image.setAlignment(QtCore.Qt.AlignCenter) 
                self.userInterface.predictImage.setEnabled(True)
                self.userInterface.label_plantName.setText("Classify This?")
                break

            else:
                cv2.destroyAllWindows()
                QMessageBox.warning(self, "Warning ", "No image selected.") 
                self.userInterface.label_plantName.setText("No Image Inserted")
                break
          
        

        #cv2.imwrite('C:/Users/Dan/Desktop/Images/%s.png'%(self.value),frame)
        
        cv2.destroyAllWindows()
        self.userInterface.Capture.setEnabled(True)
        self.userInterface.InsertImage.setEnabled(True)

    def browse_image(self):
        self.userInterface.Capture_2.setEnabled(False) 
        self.userInterface.label_plantName.setText("")
        self.userInterface.labe_benefits.setText("")
        self.imageFile, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load an image file: ", "", "Image Files (*.jpg *jpeg *.png)")
       
        if self.imageFile: 
            pixmap = QtGui.QPixmap(self.imageFile) 
            pixmap = pixmap.scaled(self.userInterface.label_image.height(), self.userInterface.label_image.width(), QtCore.Qt.KeepAspectRatioByExpanding) 
            self.userInterface.label_image.setPixmap(pixmap) 
            self.userInterface.label_image.setAlignment(QtCore.Qt.AlignCenter) 
            self.userInterface.predictImage.setEnabled(True)
            self.userInterface.label_plantName.setText("Classify This?")
        else:
         QMessageBox.warning(self, "Warning ", "No image selected.") 
         self.userInterface.label_plantName.setText("No Image Inserted")

    def locate(self):
        if self.userInterface.labe_benefits.text == "" or not self.imageFile:
            QMessageBox.warning(self, "Warning: ", "Please classify an image first, before locating.!") 
        else:
        
            self.window=QtWidgets.QMainWindow()
            self.ui = QWebEngineView() 
            self.ui.resize(750, 450)
            if self.indexer==0:self.ui.setWindowTitle("Aloe Vera Locations")
            if self.indexer==1:self.ui.setWindowTitle("Awoy-agkot Locations")
            if self.indexer==2:self.ui.setWindowTitle("Gabon Locations")
            if self.indexer==3:self.ui.setWindowTitle("Lagundi Locations")
            if self.indexer==4:self.ui.setWindowTitle("Luya Locations")
            if self.indexer==5:self.ui.setWindowTitle("Mayana Locations")
            if self.indexer==6:self.ui.setWindowTitle("Oregano Locations")
            if self.indexer==7:self.ui.setWindowTitle("Tawa-Tawa Locations")
            if self.indexer==8:self.ui.setWindowTitle("Tuba=Tuba Locations")
            if self.indexer==9:self.ui.setWindowTitle("Yerba Buena Locations")

            db =sqlite3.connect('herbal_database.db')  #OPEN DATABASE
            cursor=db.cursor()                         #MANIPULATE DATA FROM DATABASE
      
            if self.indexer==0: locate=cursor.execute("SELECT Site from Locations where id = 1").fetchall()
            if self.indexer==1: locate=cursor.execute("SELECT Site from Locations where id = 2").fetchall()
            if self.indexer==2: locate=cursor.execute("SELECT Site from Locations where id = 3").fetchall() 
            if self.indexer==3: locate=cursor.execute("SELECT Site from Locations where id = 4").fetchall() 
            if self.indexer==4: locate=cursor.execute("SELECT Site from Locations where id = 5").fetchall() 
            if self.indexer==5: locate=cursor.execute("SELECT Site from Locations where id = 6").fetchall() 
            if self.indexer==6: locate=cursor.execute("SELECT Site from Locations where id = 7").fetchall()                
            if self.indexer==7: locate=cursor.execute("SELECT Site from Locations where id = 8").fetchall() 
            if self.indexer==8: locate=cursor.execute("SELECT Site from Locations where id = 9").fetchall()                
            if self.indexer==9: locate=cursor.execute("SELECT Site from Locations where id = 10").fetchall() 
            
            for result in locate:
               self.ui.load(QUrl(str(result[0])))               
               self.ui.show()
            


            
    def predict_image(self):

        def classifyImage(image_path):
            self.userInterface.Capture_2.setEnabled(True)
            self.userInterface.viewLocatio.setEnabled(True)  
            self.newImage = image.load_img(image_path, target_size=(64, 64),color_mode='rgb')
            self.newImage = image.img_to_array(self.newImage)            
            self.newImage = self.newImage.astype("Float32")
            self.newImage /= 255.0
            self.newImage = np.expand_dims(self.newImage, axis=0)
            
            
            self.savedModel = load_model("C:/Users/Dan/Desktop/Capstone Projects/Computer Base/Herbal Plants Identification/Used_Model(current)/Mv.h5")  
                                
            # Classifying the image 
            pred = self.savedModel.predict(self.newImage)
            predct=np.argmax(pred, axis=1)
            
            return predct

         

        if not self.imageFile:
            QMessageBox.warning(self, "Warning: ", "Not a Herbal Plant. Try again!")
             
        else:
            self.userInterface.predictImage.setEnabled(False)
            self.userInterface.labe_benefits.setMargin(10)
            prediction = classifyImage(image_path = self.imageFile)
          
         
   
        db =sqlite3.connect('herbal_database.db')  #OPEN DATABASE
        cursor=db.cursor()                         #MANIPULATE DATA FROM DATABASE
      
        if prediction[0] ==   0: name=cursor.execute("SELECT Name from Plants where id = 1").fetchall()
        elif prediction[0] == 1: name=cursor.execute("SELECT Name from Plants where id = 2").fetchall()
        elif prediction[0] == 2: name=cursor.execute("SELECT Name from Plants where id = 3").fetchall()
        elif prediction[0] == 3: name=cursor.execute("SELECT Name from Plants where id = 4").fetchall()
        elif prediction[0] == 4: name=cursor.execute("SELECT Name from Plants where id = 5").fetchall()
        elif prediction[0] == 5: name=cursor.execute("SELECT Name from Plants where id = 6").fetchall()
        elif prediction[0] == 6: name=cursor.execute("SELECT Name from Plants where id = 7").fetchall()
        elif prediction[0] == 7: name=cursor.execute("SELECT Name from Plants where id = 8").fetchall()
        elif prediction[0] == 8: name=cursor.execute("SELECT Name from Plants where id = 9").fetchall()
        elif prediction[0] == 9: name=cursor.execute("SELECT Name from Plants where id = 10").fetchall()
        
        for result in name:
          self.userInterface.label_plantName.setText(str(result[0]))

        
        if prediction[0] ==   0: details=cursor.execute("SELECT English from Information where id = 1").fetchall();self.indexer=0
        elif prediction[0] == 1: details=cursor.execute("SELECT English from Information where id = 2").fetchall();self.indexer=1
        elif prediction[0] == 2: details=cursor.execute("SELECT English from Information where id = 3").fetchall();self.indexer=2
        elif prediction[0] == 3: details=cursor.execute("SELECT English from Information where id = 4").fetchall();self.indexer=3
        elif prediction[0] == 4: details=cursor.execute("SELECT English from Information where id = 5").fetchall();self.indexer=4
        elif prediction[0] == 5: details=cursor.execute("SELECT English from Information where id = 6").fetchall();self.indexer=5
        elif prediction[0] == 6: details=cursor.execute("SELECT English from Information where id = 7").fetchall();self.indexer=6
        elif prediction[0] == 7: details=cursor.execute("SELECT English from Information where id = 8").fetchall();self.indexer=7
        elif prediction[0] == 8: details=cursor.execute("SELECT English from Information where id = 9").fetchall();self.indexer=8
        elif prediction[0] == 9: details=cursor.execute("SELECT English from Information where id = 10").fetchall();self.indexer=9
    
        for res in details:
            self.userInterface.labe_benefits.setText(str(res[0]))

    

    def translate(self):
     
        if(self.transpoint==0):

            self.transpoint=1
            db =sqlite3.connect('herbal_database.db')  #OPEN DATABASE
            cursor=db.cursor()                         #MANIPULATE DATA FROM DATABASE
      
            if self.indexer==0: details=cursor.execute("SELECT Bisaya from Information where id = 1").fetchall()
            if self.indexer==1: details=cursor.execute("SELECT Bisaya from Information where id = 2").fetchall()
            if self.indexer==2: details=cursor.execute("SELECT Bisaya from Information where id = 3").fetchall() 
            if self.indexer==3: details=cursor.execute("SELECT Bisaya from Information where id = 4").fetchall() 
            if self.indexer==4: details=cursor.execute("SELECT Bisaya from Information where id = 5").fetchall() 
            if self.indexer==5: details=cursor.execute("SELECT Bisaya from Information where id = 6").fetchall() 
            if self.indexer==6: details=cursor.execute("SELECT Bisaya from Information where id = 7").fetchall()                
            if self.indexer==7: details=cursor.execute("SELECT Bisaya from Information where id = 8").fetchall() 
            if self.indexer==8: details=cursor.execute("SELECT Bisaya from Information where id = 9").fetchall()                
            if self.indexer==9: details=cursor.execute("SELECT Bisaya from Information where id = 10").fetchall() 
            
            for res in details:
                self.userInterface.labe_benefits.setText(str(res[0]))

        elif(self.transpoint==1):

            self.transpoint=0
            db =sqlite3.connect('herbal_database.db')  #OPEN DATABASE
            cursor=db.cursor()                         #MANIPULATE DATA FROM DATABASE
      
            if self.indexer==0: details=cursor.execute("SELECT English from Information where id = 1").fetchall()
            if self.indexer==1: details=cursor.execute("SELECT English from Information where id = 2").fetchall()
            if self.indexer==2: details=cursor.execute("SELECT English from Information where id = 3").fetchall() 
            if self.indexer==3: details=cursor.execute("SELECT English from Information where id = 4").fetchall() 
            if self.indexer==4: details=cursor.execute("SELECT English from Information where id = 5").fetchall() 
            if self.indexer==5: details=cursor.execute("SELECT English from Information where id = 6").fetchall() 
            if self.indexer==6: details=cursor.execute("SELECT English from Information where id = 7").fetchall()                
            if self.indexer==7: details=cursor.execute("SELECT English from Information where id = 8").fetchall() 
            if self.indexer==8: details=cursor.execute("SELECT English from Information where id = 9").fetchall()                
            if self.indexer==9: details=cursor.execute("SELECT English from Information where id = 10").fetchall() 
            
            for res in details:
                self.userInterface.labe_benefits.setText(str(res[0]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainForm()
    window.show()
    sys.exit(app.exec_())
