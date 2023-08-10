from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QMenuBar, QFileDialog, QMessageBox

import sys

class Window(QMainWindow):
    def __init__(self, app):
        super(Window, self).__init__()
        self.fname = ""
        self.app = app
        self.setWindowTitle("Text editor")
        self.setGeometry(200, 200, 600, 600)
        
        self.text_input = QtWidgets.QPlainTextEdit()
        self.setCentralWidget(self.text_input)
        
        self.createMenuBar()
        
    def createMenuBar(self):
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)
        self.fmenu = QMenu("File", self) 
        self.menu_bar.addMenu(self.fmenu)
        
        self.openf = self.fmenu.addAction("Open", self.fmenu_actions)
        self.savef = self.fmenu.addAction("Save", self.fmenu_actions)
        self.saveasf = self.fmenu.addAction("Save as", self.fmenu_actions)
        self.close = self.fmenu.addAction("Close", self.fmenu_actions)
    
    @QtCore.pyqtSlot()
    def fmenu_actions(self):
        action = self.sender().text()
        if action == 'Open':
            self.fopen_handle()
        elif action == 'Save':
            self.fsave_handle()
        elif action == 'Save as':
            self.fsaveas_handle()
        elif action == 'Close':
            self.fclose_handle()
    
    def fopen_handle(self):
        self.fname = QFileDialog.getOpenFileName(self)[0]
        try:
            with open(self.fname, 'r') as f:
                data = f.read()
            self.text_input.setPlainText(data)
        except FileNotFoundError or FileExistsError:
            print("Failed to open file")
    
    def fsave_handle(self):
        if self.fname == '':
            self.fname = QFileDialog.getSaveFileName(self)[0]
        try:
            data = self.text_input.toPlainText()
            with open(self.fname, 'w') as f:
                f.write(data)
        except FileNotFoundError or FileExistsError:
            print("Failed to save")
    
    def fsaveas_handle(self):
        self.fname = QFileDialog.getSaveFileName(self)[0]
        try:
            data = self.text_input.toPlainText()
            with open(self.fname, 'w') as f:
                f.write(data)
        except FileNotFoundError or FileExistsError:
            print("Failed to save")
    
    def fclose_handle(self):
        self.message = QMessageBox()
        self.message.setWindowTitle("Warning")
        self.message.setIcon(QMessageBox.Warning)
        if self.fname == '':
            if len(self.text_input.toPlainText()) != 0:
                self.message.setText("You have unsaved changes. Do you want to save them?")
                self.message.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
                self.message.adjustSize()
                self.message.exec_()
                self.message.buttonClicked.connect(self.popup_action)
            else:
                self.close()
                sys.exit(self.app.quit())
        else:
            self.message.setText("You might have unsaved changes. Do you want to save them?")
            self.message.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
            self.message.adjustSize()
            self.message.exec_()
            self.message.buttonClicked.connect(self.popup_action_2)
            
    
    def popup_action(self, btn):
        if btn.text() == 'Yes':
            self.fsaveas_handle()
        else:
            sys.exit(self.app.quit())
    
    def popup_action_2(self, btn):
        if btn.text() == 'Yes':
            self.fsave_handle()
        else:
            sys.exit(self.app.quit())

def start_app():
    app = QApplication(sys.argv)
    win = Window(app)
    
    win.show()
    sys.exit(app.exec_())

if __name__=='__main__':
    start_app()
