from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from dashboardui import Ui_Dashboard
from newenquiry import NewEnquiry
from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
import sys
class Dashboard(QDialog,Ui_Dashboard):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui=Ui_Dashboard()
        self.setupUi(self)
        #self.label_2.setText('ashu')
        self.pushButton_6.clicked.connect(self.add_new_student)
        self.show()

    def add_new_student(self):
        self.main = NewEnquiry()
        self.main.show()
        self.close()
        #self.pushButton_2.clicked.connect(self.InsertStudentDetail)

    def CallNextTab(self):

        self.tabWidget.setCurrentIndex(1)
    def InsertStudentDetail(self):
        name=self.lineEdit.text()
        class_det=self.comboBox.currentText()
        dob=self.dateEdit.date().toString("yyyy-MM-dd")
        school=self.lineEdit_2.text()
        addre=self.plainTextEdit.toPlainText()

        con=sqlite3.connect("FollowUp.db")
        con.execute("insert into Student (StudentName,class,dob,schoolname,address) values (?,?,?,?,?) ",(name,class_det,dob,school,addre))
        con.commit()
        con.close()
        QMessageBox.about(self,'Message','insert successfull')

if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle('Fusion')
    window=Dashboard()
    sys.exit(app.exec_())
