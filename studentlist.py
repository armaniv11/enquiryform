from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox

from studentlistui import Ui_StudentList
from newenquiry import EditEnquiry
from PyQt5 import QtCore, QtGui, QtWidgets
import xlwt
from xlsxwriter.workbook import Workbook
import sqlite3
import sys

class IconDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(IconDelegate, self).initStyleOption(option, index)
        if option.features & QtWidgets.QStyleOptionViewItem.HasDecoration:
            s = option.decorationSize
            s.setWidth(option.rect.width())
            option.decorationSize = s

class StudentList(QDialog,Ui_StudentList):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.ui=Ui_StudentList()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(lambda:self.close())
        self.tableWidget.cellClicked.connect(self.cellclick)
        self.lineEdit.textEdited.connect(self.search)
        self.pushButton.clicked.connect(self.exportdata)


        self.show()
        self.autoload()

    def autoload(self):
        conn = sqlite3.connect('FollowUp.db')
        cursor = conn.cursor()
        cursor.execute("SELECT enquiryid,StudentName,fname,dob,email,mob1,remark,reminder from Student")
        result = cursor.fetchall()
        for row_number, row_data in enumerate(result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        delegate = IconDelegate(self.tableWidget) 

        self.tableWidget.setItemDelegate(delegate)

        for x in range(len(result)):
            bank_item = QtWidgets.QTableWidgetItem()
            bank_icon = QtGui.QIcon()
            bank_icon.addPixmap(QtGui.QPixmap('edit.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            bank_item.setIcon(bank_icon)
            self.tableWidget.setItem(x,8, bank_item)
            bank_item = QtWidgets.QTableWidgetItem()
            bank_icon = QtGui.QIcon()
            bank_icon.addPixmap(QtGui.QPixmap('msg.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            bank_item.setIcon(bank_icon)
            self.tableWidget.setItem(x,9, bank_item)

    def cellclick(self, row,column):
        ite = self.tableWidget.item(row,0).text()
        if column==self.tableWidget.columnCount()-2:
            self.main = EditEnquiry()
            self.main.label.setText("Edit Enquiry")
            self.main.autoload(ite)
            self.main.show()

    def exportdata(self):
        filename,_ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("sheet", cell_overwrite_ok=True)
        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.bold = True
        style.font = font
        model = self.tableWidget.model()
        for c in range(model.columnCount()):
            text = model.headerData(c, QtCore.Qt.Horizontal)
            sheet.write(0, c+1, text, style=style)

        for r in range(model.rowCount()):
            text = model.headerData(r, QtCore.Qt.Vertical)
            sheet.write(r+1, 0, text, style=style)

        for c in range(model.columnCount()):
            for r in range(model.rowCount()):
                text = model.data(model.index(r, c))
                sheet.write(r+1, c+1, text)
        try:
            wbk.save(filename)
        except FileNotFoundError:
            pass
        


    def search(self,value):
        if value=='':
            self.tableWidget.setRowCount(0)
            self.autoload()
        else:
            conn = sqlite3.connect('FollowUp.db')
            cursor = conn.cursor()
            cursor.execute("SELECT enquiryid,StudentName,fname,dob,email,mob1,remark,reminder from Student where StudentName like ?",(value+'%',))
            result = cursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(result):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
            delegate = IconDelegate(self.tableWidget) 

            self.tableWidget.setItemDelegate(delegate)

            for x in range(len(result)):
                bank_item = QtWidgets.QTableWidgetItem()
                bank_icon = QtGui.QIcon()
                bank_icon.addPixmap(QtGui.QPixmap('edit.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                bank_item.setIcon(bank_icon)
                self.tableWidget.setItem(x,8, bank_item)
                bank_item = QtWidgets.QTableWidgetItem()
                bank_icon = QtGui.QIcon()
                bank_icon.addPixmap(QtGui.QPixmap('msg.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                bank_item.setIcon(bank_icon)
                self.tableWidget.setItem(x,9, bank_item)

            
            





if __name__ == "__main__":
    app=QApplication(sys.argv)
    app.setStyle('Fusion')
    window=StudentList()
    sys.exit(app.exec_())
