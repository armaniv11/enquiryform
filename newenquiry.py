from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from newenquiryui import Ui_NewEnquiry
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QPoint,QDate,Qt
from PyQt5.QtGui import QIcon, QPixmap
from datetime import date,datetime

import resources
import sqlite3
import sys
class NewEnquiry(QDialog,Ui_NewEnquiry):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui=Ui_NewEnquiry()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.tabWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(lambda:self.frame_3.show())
        self.pushButton_2.clicked.connect(lambda:self.frame_3.hide())
        self.pushButton_6.clicked.connect(lambda:self.frame_3.hide())
        self.pushButton_4.clicked.connect(lambda:self.close())
        self.pushButton_3.clicked.connect(self.img)
        self.dateEdit.dateChanged.connect(self.onDateChanged)
        self.lineEdit_4.setDisabled(True)
        datereminder = QDate.currentDate().addDays(7)
        self.dateEdit_2.setDate(datereminder)
        print(datereminder)
        self.pushButton_5.clicked.connect(self.InsertStudentDetail)

        self.oldPos = self.pos()
        self.imgname = ''
        self.show()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def onDateChanged(self,newDate):
        age = newDate.toString()
        # print("The new date is "+newDate.toString())
        age = age[10:]
        age = int(age)
        # print(age)
        day = date.today()
        age = day.year-age
        # print(age)
        self.lineEdit_4.setText(str(age))
    def img(self):
        fname =  QtWidgets.QFileDialog.getOpenFileName(self, 'a file','*.jpg')
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        # print(self.imagePath)
        # smaller_pixmap = pixmap.scaled(270, 140, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.imgname = imagePath
        # print(self.logoname)
        self.label_13.setPixmap(QPixmap(pixmap))
        self.label_13.setScaledContents(True)

    def InsertStudentDetail(self):
        name=self.lineEdit_2.text()
        class_det=self.comboBox.currentText()
        dob=self.dateEdit.date().toString("yyyy-MM-dd")
        mob1 = self.lineEdit_8.text()
        email = self.lineEdit_9.text()
        schoolname=self.lineEdit_10.text()
        address=self.plainTextEdit_2.toPlainText()
        reminder=self.dateEdit_2.date().toString("yyyy-MM-dd")
        remark = self.plainTextEdit_3.toPlainText()
        fname = self.lineEdit.text()
        mob2 = self.lineEdit_5.text()
        foccupation = self.lineEdit_6.text()
        mname = self.lineEdit_3.text()
        mob3 = self.lineEdit_7.text()
        paddress = self.plainTextEdit.toPlainText()
        added = datetime.now().strftime("%y/%m/%d %H:%M:%S")

        con=sqlite3.connect("FollowUp.db")
        con.execute("insert into Student (StudentName,class,dob,mob1,email,schoolname,address,reminder,remark,imgname,fname,mob2,foccupation,mname,mob3,paddress,added) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ",(name,class_det,dob,mob1,email,schoolname,address,reminder,remark,self.imgname,fname,mob2,foccupation,mname,mob3,paddress,added))
        con.commit()
        con.close()
        QMessageBox.about(self,'Message','insert successfull')

class EditEnquiry(QDialog,Ui_NewEnquiry):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui=Ui_NewEnquiry()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.dateEdit.dateChanged.connect(self.onDateChanged)
        self.imgname = ''
        self.pushButton.clicked.connect(lambda:self.frame_3.show())
        self.pushButton_2.clicked.connect(lambda:self.frame_3.hide())
        self.pushButton_6.clicked.connect(lambda:self.frame_3.hide())
        self.pushButton_4.clicked.connect(lambda:self.close())
        self.pushButton_3.clicked.connect(self.img)
        self.pushButton_5.clicked.connect(self.UpdateStudentDetail)


        # self.show()
    def img(self):
        fname =  QtWidgets.QFileDialog.getOpenFileName(self, 'a file','*.jpg')
        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        # print(self.imagePath)
        # smaller_pixmap = pixmap.scaled(270, 140, Qt.KeepAspectRatio, Qt.FastTransformation)
        self.imgname = imagePath
        # print(self.logoname)
        self.label_13.setPixmap(QPixmap(pixmap))
        self.label_13.setScaledContents(True)

    def onDateChanged(self,newDate):
        age = newDate.toString()
        # print("The new date is "+newDate.toString())
        age = age[10:]
        age = int(age)
        # print(age)
        day = date.today()
        age = day.year-age
        # print(age)
        self.lineEdit_4.setText(str(age))

    def autoload(self,enquiryid):
        self.label_22.setText(str(enquiryid))
        conn = sqlite3.connect('FollowUp.db')
        cursor = conn.cursor()
        cursor.execute('SELECT StudentName,class,dob,mob1,email,schoolname,address,reminder,remark,imgname,fname,mob2,foccupation,mname,mob3,paddress from Student where enquiryid=?',(enquiryid,))
        result = cursor.fetchall()
        try:
            name = result[0][0]
        except Exception:
            name = 'Name Not Set'
        self.lineEdit_2.setText(name)
        try:
            class_det = result[0][1]
        except Exception:
            class_det = 'Class Not Set'
        self.comboBox.addItem(class_det)
        try:
            dob = result[0][2]
        except Exception:
            dob = ''
        d = QDate.fromString(dob, "dd-MM-yyyy")
        self.dateEdit.setDate(d)
        try:
            mob1 = str(result[0][3])
        except Exception:
            mob1 = ''
        self.lineEdit_8.setText(mob1)
        try:
            email = str(result[0][4])
        except Exception:
            email = ''
        self.lineEdit_9.setText(email)
        try:
            schoolname = str(result[0][5])
        except Exception:
            schoolname = ''
        self.lineEdit_10.setText(schoolname)
        try:
            address = str(result[0][6])
        except Exception:
            address = ''
        self.plainTextEdit_2.setPlainText(address)
        try:
            reminder = str(result[0][7])
        except Exception:
            reminder = ''
        d = QDate.fromString(reminder, "dd-MM-yyyy")
        self.dateEdit_2.setDate(d)
        try:
            remark = str(result[0][8])
        except Exception:
            remark = ''
        self.plainTextEdit_3.setPlainText(remark)
        try:
            self.imgname = str(result[0][9])
        except Exception:
            self.imgname = ''
        if self.imgname =='':
            self.label_13.setPixmap(QtGui.QPixmap(":/images/Icons/img_415067.png"))
        else:
            pixmap2 = QPixmap(self.imgname)
            self.label_13.setPixmap(QPixmap(pixmap2))
            self.label_13.setScaledContents(True)
        try:
            fname = str(result[0][10])
        except Exception:
            fname = ''
        self.lineEdit.setText(fname)
        try:
            mob2 = str(result[0][11])
        except Exception:
            mob2 = ''
        self.lineEdit_5.setText(mob2)
        try:
            foccupation = str(result[0][12])
        except Exception:
            foccupation = ''
        self.lineEdit_6.setText(foccupation)
        try:
            mname = str(result[0][13])
        except Exception:
            mname = ''
        self.lineEdit_3.setText(mname)
        try:
            mob3 = str(result[0][14])
        except Exception:
            mob3 = ''
        self.lineEdit_7.setText(mob3)
        try:
            paddress = str(result[0][15])
        except Exception:
            paddress = ''
        self.plainTextEdit.setPlainText(paddress)

    def UpdateStudentDetail(self):
        enquiryid = self.label_22.text()
        name=self.lineEdit_2.text()
        class_det=self.comboBox.currentText()
        dob=self.dateEdit.date().toString("yyyy-MM-dd")
        mob1 = self.lineEdit_8.text()
        email = self.lineEdit_9.text()
        schoolname=self.lineEdit_10.text()
        address=self.plainTextEdit_2.toPlainText()
        reminder=self.dateEdit_2.date().toString("yyyy-MM-dd")
        remark = self.plainTextEdit_3.toPlainText()
        fname = self.lineEdit.text()
        mob2 = self.lineEdit_5.text()
        foccupation = self.lineEdit_6.text()
        mname = self.lineEdit_3.text()
        mob3 = self.lineEdit_7.text()
        paddress = self.plainTextEdit.toPlainText()
        updated = datetime.now().strftime("%y/%m/%d %H:%M:%S")

        con=sqlite3.connect("FollowUp.db")
        con.execute("UPDATE Student set StudentName=?,class=?,dob=?,mob1=?,email=?,schoolname=?,address=?,reminder=?,remark=?,imgname=?,fname=?,mob2=?,foccupation=?,mname=?,mob3=?,paddress=?,updated=? where enquiryid=? ",(name,class_det,dob,mob1,email,schoolname,address,reminder,remark,self.imgname,fname,mob2,foccupation,mname,mob3,paddress,updated,enquiryid))
        con.commit()
        con.close()
        QMessageBox.about(self,'Message','Record Has Been successfully Updated')







if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle('Fusion')
    window=NewEnquiry()
    sys.exit(app.exec_())
