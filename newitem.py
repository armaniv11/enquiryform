

import sys
import platform
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
import sqlite3
from PyQt5.QtGui import QIcon, QPixmap
from datetime import datetime
import time, threading
from PyQt5.QtCore import *
import xlwt
from xlsxwriter.workbook import Workbook

import pyexcel
import os



## ==> SPLASH SCREEN
from newitemui import Ui_NewItem
from itemdetailsui import Ui_ItemDetails

## ==> MAIN WINDOW
# from ui_main import Ui_MainWindow

## ==> GLOBALS
class IconDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(IconDelegate, self).initStyleOption(option, index)
        if option.features & QtWidgets.QStyleOptionViewItem.HasDecoration:
            s = option.decorationSize
            s.setWidth(option.rect.width())
            option.decorationSize = s

# YOUR APPLICATION
class NewItem(QDialog,Ui_NewItem):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_NewItem()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(self.closeclicked)
        self.show()
        self.tabWidget.setCurrentIndex(0)
        self.comboBox_2.setEditable(True)
        self.comboBox_4.setEditable(True)
        self.onlyInt = QtGui.QIntValidator()
        self.onlyfloat = QtGui.QDoubleValidator()
        self.lineEdit_2.setValidator(self.onlyfloat)
        self.lineEdit.setValidator(self.onlyfloat)
        self.lineEdit_15.setValidator(self.onlyfloat)
        self.lineEdit_16.setValidator(self.onlyfloat)
        self.lineEdit_19.setValidator(self.onlyfloat)
        self.lineEdit_21.setValidator(self.onlyfloat)
        self.lineEdit_13.setValidator(self.onlyfloat)
        self.pushButton.clicked.connect(self.saveitem)
        self.lineEdit_2.textEdited.connect(self.calc)
        self.lineEdit.textEdited.connect(self.calc)
        self.pushButton_2.clicked.connect(self.saveservice)
        self.databasename = ''
        self.autoload()
        self.oldPos = self.pos()
        self.counter = 0
        self.lineEdit_4.textEdited.connect(self.auto_capital1)
        # self.timer = QTimer()
        # self.timer.setInterval(2000)
        # self.timer.timeout.connect(self.recurring_timer)
        # self.timer.start()
        self.timer = threading.Timer(2, self.recurring_timer)
        self.timer.start()


    def recurring_timer(self):
        self.counter +=1
        print(self.counter)
        if self.counter==5:
            self.timer.cancel()

    def auto_capital1(self):
        ai = self.lineEdit_4.text().upper()
        self.lineEdit_4.setText(ai)


    def loadexcel(self):
        conn = sqlite3.connect(self.databasename)
        added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        for row in pyexcel.get_array(file_name="itemimport.xls", start_row=1,start_column=1,column_limit=11):
            try:
                openingqty = row[4]
            except Exception:
                openingqty = 0
            try:
                openingprice = row[5]
            except Exception:
                openingprice = 0

            if row[6]==0 or row[6]==3 or row[6]==5 or row[6]==12 or row[6]==18 or row[6]==28:
                tax = row[6]
            else:
                tax = 0
            if row[0]!='':
                conn.execute('INSERT into newitem(name,desc,sac_hsn,unit,quantity,opening_price,tax_rate,tax_name,cess_rate,pur_rate,sell_price,is_inclusive,added,opening_stock) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)',(row[0],row[1],row[2],row[3],openingqty,openingprice,tax,tax,row[7],row[8],row[9],row[10],added,openingprice*openingqty))
                conn.commit()
        QMessageBox.information(self,'Success','Import Successfull')


        


    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def closeclicked(self):
        self.close()

    def autoload(self):
        conn = sqlite3.connect("universal.db")
        c = conn.cursor()
        c.execute("SELECT shopid||session from current")
        result = c.fetchall()
        try:
            self.databasename = str(result[0][0])+'.db'
        except Exception:
            self.databasename = 'no.db'
        print(self.databasename)
        conn = sqlite3.connect(self.databasename)
        self.comboBox_2.clear()
        self.comboBox_4.clear()
        c = conn.cursor()
        c.execute("SELECT distinct unit FROM newitem")
        pmList = c.fetchall()
        pmn = [i[0] for i in pmList]
        self.comboBox_4.addItems(pmn)
        self.comboBox_2.addItems(pmn)
        c.execute('SELECT gst_type from selfparty')
        companyresult = c.fetchall()
        try:
            compgst = str(companyresult[0][0])
        except Exception:
            compgst = 'UNREGISTERED'
        if compgst=='COMPOSITION SCHEME':
            self.checkBox_2.hide()
            self.checkBox.hide()
        conn.close()
        # self.loadexcel()

    def comboload(self):
        conn = sqlite3.connect(self.databasename)
        self.comboBox_2.clear()
        self.comboBox_4.clear()
        c = conn.cursor()
        c.execute("SELECT distinct name FROM newunit")
        pmList = c.fetchall()
        pmn = [i[0] for i in pmList]
        self.comboBox_4.addItems(pmn)
        self.comboBox_2.addItems(pmn)

        conn.close()
        
    def calc(self):
        try:
            qty = float(self.lineEdit.text())
        except Exception:
            qty = 1
        try:
            unit =float(self.lineEdit_2.text())
        except Exception:
            unit = 0
        val = round(qty * unit,2)
        self.lineEdit_17.setText(str(val))

    def saveitem(self):
        # os.system('start "excel.exe" "GSTR3B.xlsm"')
        # try:
        #     self.t.cancel()
        # except Exception:
        #     pass
        name = self.lineEdit_4.text()
        sac_hsn = self.lineEdit_3.text()
        unit = self.comboBox_2.currentText()
        quantity = self.lineEdit.text()
        opening_price = self.lineEdit_2.text()
        opening_stock = self.lineEdit_17.text()
        tax_name = self.comboBox_11.currentText() 
        tax_rate = 0
        if len(tax_name) <3:
            tax_rate = tax_name
        # expiry =self.dateEdit.date().toString('dd-MM-yyyy')
        desc = self.lineEdit_12.text()
        pur_price = self.lineEdit_15.text()
        sell_price = self.lineEdit_16.text()
        cess_rate = self.lineEdit_13.text()
        if self.checkBox.isChecked():
            is_inclusive = "True"
        else:
            is_inclusive = 'False'
        if pur_price=='':
            pur_price = 0
        if sell_price == '':
            sell_price = 0
        conn = sqlite3.connect(self.databasename)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM newitem")
        pmList = cursor.fetchall()
        pmn = [i[0] for i in pmList]
        
        added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if name=='':
            QMessageBox.warning(self,"Alert","Please Provide Item Name")
        elif tax_name=='':
            QMessageBox.warning(self,"Alert","Please Select Tax Rate")
        elif name in pmn:
            QMessageBox.warning(self,"Alert","Item with same name already exists")
        else:
            cursor.execute('select distinct name from newunit')
            result = cursor.fetchall()
            pmn = [i[0] for i in result]
            if unit in pmn:
                pass
            else:
                conn.execute('INSERT into newunit(name) values (?)',(unit,))
                conn.commit()


            conn.execute("insert into newitem(name,sac_hsn,unit,quantity,opening_price,opening_stock,tax_name,tax_rate,desc,pur_rate,sell_price,cess_rate,is_inclusive,added) values (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(name,sac_hsn,unit,quantity,opening_price,opening_stock,tax_name,tax_rate,desc,pur_price,sell_price,cess_rate,is_inclusive,added))

            conn.commit()
            print("success")
            conn.close()
            QMessageBox.about(self,"SUCCESS","Item Added Successfully")
            buttonReply = QMessageBox.question(self,'Confirm Action!','Do you want to add another item?',QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if buttonReply ==QMessageBox.Yes:
                self.lineEdit.clear()
                self.lineEdit_2.clear()
                self.lineEdit_3.clear()
                self.lineEdit_4.clear()
                self.lineEdit_17.clear()
                self.lineEdit_12.clear()
                self.lineEdit_13.clear()
                self.lineEdit_15.clear()
                self.lineEdit_16.clear()
                self.autoload()
            else:
                # from dashboard import Dashboard
                # self.main = Dashboard()
                # self.main.autoload()
                self.close()
    def saveservice(self):
        name = self.lineEdit_6.text()
        sac_hsn = self.lineEdit_8.text()
        unit = self.comboBox_4.currentText()
        tax_rate = self.lineEdit_7.text()
        desc = self.lineEdit_9.text()
        pur_price = self.lineEdit_19.text()
        cess_rate = self.lineEdit_21.text()
        if self.checkBox_2.isChecked():
            is_inclusive = "True"
        else:
            is_inclusive = 'False'
        if pur_price=='':
            pur_price = 0
        type_product = 'S'
        added = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if name=='':
            QMessageBox.warning(self,"Alert","Please Provide Item Name")
        elif tax_rate=='':
            QMessageBox.warning(self,"Alert","Please Provide Tax Rate")
        
        else:
            conn = sqlite3.connect(self.databasename)
            # conn = sqlite3.connect(self.databasename)
            cursor = conn.cursor()
            cursor.execute('select distinct name from newunit')
            result = cursor.fetchall()
            pmn = [i[0] for i in result]
            if unit in pmn:
                pass
            else:
                conn.execute('INSERT into newunit(name) values (?)',(unit,))
                conn.commit()
            conn.execute("insert into newitem(name,sac_hsn,unit,tax_rate,desc,pur_rate,sell_price,cess_rate,is_inclusive,type_product,added) values (?,?,?,?,?,?,?,?,?,?,?)",(name,sac_hsn,unit,tax_rate,desc,0,pur_price,cess_rate,is_inclusive,type_product,added))

            conn.commit()
            print("success")
            conn.close()
            QMessageBox.about(self,"SUCCESS","Service Added Successfully")
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
            self.lineEdit_8.clear()
            self.lineEdit_9.clear()
            self.lineEdit_19.clear()
            self.lineEdit_21.clear()
            self.autoload()

class ItemDetails(QDialog,Ui_ItemDetails):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_ItemDetails()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(self.closeclicked)
        self.show()
        self.tableWidget.cellClicked.connect(self.cellclick)
        self.lineEdit_4.textEdited.connect(self.search)
        self.pushButton_2.clicked.connect(self.addItem)
        self.databasename = ''
        self.pushButton_3.clicked.connect(self.exportdata)
        self.autoload()

        self.oldPos = self.pos()

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()


    def closeclicked(self):
        self.close()

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

    def autoload(self):
        conn = sqlite3.connect("universal.db")
        c = conn.cursor()
        c.execute("SELECT shopid||session from current")
        result = c.fetchall()
        try:
            self.databasename = str(result[0][0])+'.db'
        except Exception:
            self.databasename = 'no.db'
        print(self.databasename)
        self.itemshow()

    def addItem(self):
        self.close()
        self.main = NewItem()
        self.main.show()

    def itemshow(self):
        conn = sqlite3.connect(self.databasename)
        c = conn.cursor()
        c.execute("SELECT itemid,name,desc,sac_hsn,type_product,unit,pur_rate,sell_price,'',deactivate from newitem where deactivate='False'")
        result = c.fetchall()
        self.tableWidget.setRowCount(0)
        delegate = IconDelegate(self.tableWidget) 
        self.tableWidget.setItemDelegate(delegate)
        for row_number, row_data in enumerate (result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number==8:
                    bank_item = QtWidgets.QTableWidgetItem()
                    bank_icon = QtGui.QIcon()
                    bank_icon.addPixmap(QtGui.QPixmap('edit.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    bank_item.setIcon(bank_icon)
                    self.tableWidget.setItem(row_number,column_number , bank_item)
                elif column_number==9:
                    # print(data)
                    if data=='False':
                        bank_item = QtWidgets.QTableWidgetItem()
                        bank_icon = QtGui.QIcon()
                        bank_icon.addPixmap(QtGui.QPixmap('multiply.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        bank_item.setIcon(bank_icon)
                        self.tableWidget.setItem(row_number,column_number , bank_item)

                    else:
                        bank_item = QtWidgets.QTableWidgetItem()
                        bank_icon = QtGui.QIcon()
                        bank_icon.addPixmap(QtGui.QPixmap('check.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        bank_item.setIcon(bank_icon)
                        self.tableWidget.setItem(row_number,column_number , bank_item)
                elif column_number==3 and data=='P':
                    
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem('Product'))
                elif column_number==3 and data=='S':
                        self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem('Service'))
                else:
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def cellclick(self, row,column):

        
        # print("Row %d and Column %d was clicked" % (row, column))
        if column==9:
            ite = self.tableWidget.item(row,0).text()
            print(ite)
            conn = sqlite3.connect(self.databasename)
            c = conn.cursor()
            c.execute("SELECT deactivate from newitem where itemid=(?)",(ite))
            result = c.fetchall()
            print(result)
            try:
                result = result[0][0]
            except Exception:
                result = False
            print(result)
            buttonReply = QMessageBox.question(self, 'CONFIRM ACTION', 'Are you sure you want to Delete the Item?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if buttonReply == QMessageBox.Yes:
                conn = sqlite3.connect(self.databasename)
                conn.execute("update newitem set deactivate=(?) where itemid=(?)",('True',ite))
                conn.commit()
                conn.close()
                self.itemshow()
        elif column==8:
            ite = self.tableWidget.item(row,0).text()
            typepro = self.tableWidget.item(row,3).text()
            if typepro =='Product':
                typepro='P'
            else:
                typepro='S'
            print(ite)
            conn = sqlite3.connect(self.databasename)
            conn.execute("delete from itemedit")

            
            conn.execute("insert into itemedit(itemid,type) values (?,?)",(ite,typepro))
            conn.commit()
            conn.close()
            # self.window = QtWidgets.QDialog()
            self.main = UpdateItem()
            self.main.show()
            self.close()

            # self.window.show()

        
    def search(self):
        search  = self.lineEdit_4.text()
        conn = sqlite3.connect(self.databasename)
        c = conn.cursor()
        c.execute("SELECT itemid,name,desc,sac_hsn,type_product,unit,pur_rate,sell_price,'',deactivate from newitem where deactivate='False' and (name like(?) or type_product like(?)) ",(search+'%',search+'%'))
        result = c.fetchall()
        self.tableWidget.setRowCount(0)
        delegate = IconDelegate(self.tableWidget) 
        self.tableWidget.setItemDelegate(delegate)
        for row_number, row_data in enumerate (result):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                if column_number==8:
                    bank_item = QtWidgets.QTableWidgetItem()
                    bank_icon = QtGui.QIcon()
                    bank_icon.addPixmap(QtGui.QPixmap('edit.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    bank_item.setIcon(bank_icon)
                    self.tableWidget.setItem(row_number,column_number , bank_item)
                elif column_number==9:
                    # print(data)
                    if data=='False':
                        bank_item = QtWidgets.QTableWidgetItem()
                        bank_icon = QtGui.QIcon()
                        bank_icon.addPixmap(QtGui.QPixmap('multiply.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        bank_item.setIcon(bank_icon)
                        self.tableWidget.setItem(row_number,column_number , bank_item)

                    else:
                        bank_item = QtWidgets.QTableWidgetItem()
                        bank_icon = QtGui.QIcon()
                        bank_icon.addPixmap(QtGui.QPixmap('check.png'), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                        bank_item.setIcon(bank_icon)
                        self.tableWidget.setItem(row_number,column_number , bank_item)
                elif column_number==3 and data=='P':
                    
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem('Product'))
                elif column_number==3 and data=='S':
                        self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem('Service'))
                else:
                    self.tableWidget.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

class UpdateItem(QDialog,Ui_NewItem):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_NewItem()
        self.setupUi(self)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.pushButton_4.clicked.connect(self.closeclicked)
        self.show()
        self.tabWidget.setCurrentIndex(0)
        self.comboBox_2.setEditable(True)
        self.comboBox_4.setEditable(True)
        self.onlyInt = QtGui.QIntValidator()
        self.onlyfloat = QtGui.QDoubleValidator()
        self.lineEdit_2.textEdited.connect(self.calc)
        self.lineEdit.textEdited.connect(self.calc)
        self.pushButton.clicked.connect(self.updateitem)
        self.pushButton_2.clicked.connect(self.updateservice)

        self.label_4.setText('UPDATE')
        self.databasename = ''
        self.autoload()
        self.oldPos = self.pos()




    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint (event.globalPos() - self.oldPos)
        #print(delta)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

    def closeclicked(self):
        self.close()

    def autoload(self):
        conn = sqlite3.connect("universal.db")
        c = conn.cursor()
        c.execute("SELECT shopid||session from current")
        result = c.fetchall()
        try:
            self.databasename = str(result[0][0])+'.db'
        except Exception:
            self.databasename = 'no.db'
        print(self.databasename)
        conn = sqlite3.connect(self.databasename)
        self.comboBox_2.clear()
        self.comboBox_4.clear()
        c = conn.cursor()
        c.execute("SELECT distinct name FROM newunit")
        pmList = c.fetchall()
        pmn = [i[0] for i in pmList]
        self.comboBox_4.addItems(pmn)
        self.comboBox_2.addItems(pmn)

        c.execute('select itemid,type from itemedit')
        resul = c.fetchall()
        try:
            resu = str(resul[0][0])
            self.itemno = resu
        except Exception:
            resu = ''
            self.itemno = resu
        print('itemno is ',self.itemno)
        try:
            protype = str(resul[0][1])
        except Exception:
            protype = ''
        print(resul)
        if protype =='P':
            cursor = conn.cursor()
            cursor.execute("select name,sac_hsn,unit,quantity,opening_price,opening_stock,tax_name,desc,pur_rate,sell_price,cess_rate,is_inclusive from newitem where itemid=(?)",(resu,))
            result = cursor.fetchall()
            try:
                name = str(result[0][0])
            except Exception:
                name = ""
            self.lineEdit_4.setText(name)
            try:
                hsn = str(result[0][1])
            except Exception:
                hsn = ""
            self.lineEdit_3.setText(hsn)
            try:
                unit = str(result[0][2])
            except Exception:
                unit = ""
            # print(result)
            index = self.comboBox_2.findText(unit)
            self.comboBox_2.setCurrentIndex(index)
            try:
                qty = str(result[0][3])
            except Exception:
                qty = ""
            # print(result)
            self.lineEdit.setText(qty)
            try:
                openingprice = str(result[0][4])
            except Exception:
                openingprice = ""
            # print(result)
            self.lineEdit_2.setText(openingprice)
            try:
                openingstock = str(result[0][5])
            except Exception:
                openingstock = ""
            self.lineEdit_17.setText(openingstock)
            
            try:
                taxname = str(result[0][6])
            except Exception:
                taxname = ""
            index = self.comboBox_11.findText(taxname)
            self.comboBox_11.setCurrentIndex(index)
            try:
                desc = str(result[0][7])
            except Exception:
                desc = ""
            self.lineEdit_12.setText(desc)
            try:
                purrate = str(result[0][8])
            except Exception:
                purrate = ""
            self.lineEdit_15.setText(purrate)
            try:
                sellrate = str(result[0][9])
            except Exception:
                sellrate = ""
            self.lineEdit_16.setText(sellrate)
            try:
                cess = str(result[0][10])
            except Exception:
                cess = ""
            self.lineEdit_13.setText(cess)
            try:
                inclusive = str(result[0][11])
            except Exception:
                inclusive = ""
            if inclusive=='True':
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
        elif protype=='S':
            self.tabWidget.setCurrentIndex(1)

            cursor = conn.cursor()
            cursor.execute("select name,sac_hsn,unit,tax_rate,desc,sell_price,cess_rate,is_inclusive from newitem where itemid=(?)",(resu,))
            result = cursor.fetchall()
            try:
                name = str(result[0][0])
            except Exception:
                name = ""
            self.lineEdit_6.setText(name)
            try:
                hsn = str(result[0][1])
            except Exception:
                hsn = ""
            self.lineEdit_8.setText(hsn)
            try:
                unit = str(result[0][2])
            except Exception:
                unit = ""
            index = self.comboBox_4.findText(unit)
            self.comboBox_4.setCurrentIndex(index)
            try:
                tax = str(result[0][3])
            except Exception:
                tax = ""
            # print(result)
            index = self.comboBox_12.findText(tax)
            self.comboBox_12.setCurrentIndex(index)
            try:
                desc = str(result[0][4])
            except Exception:
                desc = ""
            # print(result)
            self.lineEdit_9.setText(desc)
            try:
                value = str(result[0][5])
            except Exception:
                value = ""
            self.lineEdit_19.setText(value)
            try:
                cess = str(result[0][6])
            except Exception:
                cess = ""
            # print(result)
            self.lineEdit_21.setText(cess)
            try:
                inclusive = str(result[0][7])
            except Exception:
                inclusive = ""
            if inclusive=='True':
                self.checkBox_2.setChecked(True)
            else:
                self.checkBox_2.setChecked(False)

    def calc(self):
        try:
            qty = float(self.lineEdit.text())
        except Exception:
            qty = 1
        try:
            unit =float(self.lineEdit_2.text())
        except Exception:
            unit = 0
        val = round(qty * unit,2)
        self.lineEdit_17.setText(str(val))

    def updateitem(self):
        name = self.lineEdit_4.text()
        sac_hsn = self.lineEdit_3.text()
        unit = self.comboBox_2.currentText()
        quantity = self.lineEdit.text()
        opening_price = self.lineEdit_2.text()
        opening_stock = self.lineEdit_17.text()
        tax_name = self.comboBox_11.currentText() 
        tax_rate = 0
        if len(tax_name) <3:
            tax_rate = tax_name
        desc = self.lineEdit_12.text()
        pur_price = self.lineEdit_15.text()
        sell_price = self.lineEdit_16.text()
        cess_rate = self.lineEdit_13.text()
        if self.checkBox.isChecked():
            is_inclusive = "True"
        else:
            is_inclusive = 'False'
        if name=='':
            QMessageBox.warning(self,'Note','Name cannot be empty')
        elif pur_price=='' or sell_price=='':
            QMessageBox.warning(self,'Note','Please Provide Price Info')
        else:
            edited = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            conn = sqlite3.connect(self.databasename)
            conn.execute("update newitem set name=(?),sac_hsn=(?),unit=(?),quantity=(?),opening_price=(?),opening_stock=(?),tax_name=(?),tax_rate=(?),desc=(?),pur_rate=(?),sell_price=(?),cess_rate=(?),is_inclusive=(?),edited=(?) where itemid=(?)",(name,sac_hsn,unit,quantity,opening_price,opening_stock,tax_name,tax_rate,desc,pur_price,sell_price,cess_rate,is_inclusive,edited,self.itemno))
            conn.commit()
            print("success")
            conn.close()
            QMessageBox.about(self,"SUCCESS","Item Updated Successfully")
            self.close()
            self.main = ItemDetails()
            self.main.show()

    def updateservice(self):
        name = self.lineEdit_6.text()
        sac_hsn = self.lineEdit_8.text()
        unit = self.comboBox_4.currentText()
        tax_rate = self.lineEdit_7.text()
        desc = self.lineEdit_9.text()
        pur_price = self.lineEdit_19.text()
        cess_rate = self.lineEdit_21.text()
        if self.checkBox_2.isChecked():
            is_inclusive = "True"
        else:
            is_inclusive = 'False'
        edited = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        if name=='':
            QMessageBox.warning(self,'Note','Name cannot be empty')
        elif pur_price=='':
            QMessageBox.warning(self,'Note','Please Provide Amount')
        else:
            conn = sqlite3.connect(self.databasename)
            conn.execute("update newitem set name=(?),sac_hsn=(?),unit=(?),tax_rate=(?),desc=(?),pur_rate=(?),cess_rate=(?),is_inclusive=(?),edited=(?) where itemid=(?)",(name,sac_hsn,unit,tax_rate,desc,pur_price,cess_rate,is_inclusive,edited,self.itemno))
            conn.commit()
            print("success")
            conn.close()
            QMessageBox.about(self,"SUCCESS","Service Details Has Been Updated Successfully")
            self.close()
            self.main = ItemDetails()
            self.main.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = NewItem()
    sys.exit(app.exec_())
