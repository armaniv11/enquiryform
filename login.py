from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from loginui import Ui_Login
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import sys
# from newenquiry import NewEnquiry
from dashboard import Dashboard

class Login(QDialog,Ui_Login):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui=Ui_Login()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.show()
        self.pushButton.clicked.connect(self.checkcredentials)
    def checkcredentials(self):
        username=self.lineEdit.text()
        password=self.lineEdit_2.text()


        con=sqlite3.connect("FollowUp.db")
        cur=con.cursor()
        cur.execute("select * from login where username=? and password=?",(username,password))
        if len(cur.fetchall()) >0:
            self.main=Dashboard()
            self.main.label_2.setText(username)
            self.main.show()
            self.close()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid Credentials')


        con.close()


if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle('Fusion')
    window=Login()
    sys.exit(app.exec_())
