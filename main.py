from PyQt5 import QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication,QMainWindow
import sys
from PyQt5.QtCore import Qt, QSize
import requests

class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow,self).__init__()
        self.setGeometry(100,100,600,400)
        self.setUpGui()
    def setUpGui(self):
        
        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setText("Package Name:")
        self.lbl.move(50,20)

        
        self.SearchButton = QtWidgets.QPushButton(self)
        self.SearchButton.move(260,15)
        self.SearchButton.resize(130,40)
        self.SearchButton.setText("Search Package")
        self.SearchButton.clicked.connect(self.click)
        
        self.demandedText = QtWidgets.QLineEdit(self)
        self.demandedText.move(150,20)
        
        self.scroll = QtWidgets.QScrollArea(self)             
        self.widget = QtWidgets.QWidget()                 
        self.vbox = QtWidgets.QVBoxLayout() 
                     
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed) #sizePolicy fixed parameter limits the content as its size 
        
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setLayout(self.vbox)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.lbl = QtWidgets.QLabel(self)
        self.lbl.setText("Package:")
        self.lbl.move(10,100)

        self.scroll.move(80,100)
        self.scroll.resize(500,200)

    def click(self):
        demand =self.demandedText.text()
        mes= self.getPackage(demand)
        self.setDemandedPackage(mes)
    
    def getPackage(self,demand):
        url="https://pypi.org/pypi/{}/json".format(demand)
        req = requests.get(url,timeout=5)
        mes=""
        try:
            myDict = req.json()
            mes=myDict['info']
        except:
            mes={'name':False}
        return mes

    def refresh(self):
        d = self.widget.children()
        e = reversed(d)
        for g in e:
            if type(g)!=type(self.vbox):
                g.deleteLater()


    def setDemandedPackage(self,content):
        if not content['name']:
            self.refresh()
            objectt = QtWidgets.QLabel("Package is not found")
            self.vbox.addWidget(objectt)
            self.widget.update()
        else:
            self.refresh()
            objectt = QtWidgets.QLabel(content['name'])
            font = QtGui.QFont()
            font.setBold(True)
            font.setWeight(75)
            objectt.setFont(font)


            self.vbox.addWidget(objectt)

            objectt1 = QtWidgets.QLabel(content['description'])
            self.vbox.addWidget(objectt1)
            objectt1.setMaximumWidth(470)
            objectt1.setWordWrap(True)    

            self.widget.update()


def App():
    app = QApplication(sys.argv)
    win = mainWindow()

    win.show()
    sys.exit(app.exec_())

App()