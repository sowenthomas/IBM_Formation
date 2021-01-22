import sys
import re
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication,QWidget,QLineEdit,QCompleter, QMessageBox
from PyQt5.QtCore import QDate, Qt                  #Importe la date
from PyQt5.QtCore import QTime, Qt                  #Importer le temps (heure,min,sec )


class Livraison(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()
        uic.loadUi("Index.ui",self)  
        
        self.viticulteur.activated[str].connect(self.UpdateParcelle)     
        self.parcelle.activated[str].connect(self.UpdateCepage)   
        self.cepage.activated[str].connect(self.UpdatePoids)  
        self.pushButton.clicked.connect(self.RegisterOrder)
        self.resultats.clicked.connect(self.final)

        self.DataCollection()
        self.viticulteur.addItems(sorted(set(x[0] for x in self.data))) 
        self.InitializeComboBoxes()

    ligne =""
    dict_Cepage = {"1":"Pinot Noir", "2": "Merlot", "3":"Malbec", "4":"Trousseau", "5":"Gamay","6":"Chardonnay",
    "7":"Sauvignon", "8":"Grenache","9":"Savagnin","10":"Chenin"}
    data=[] 
    Vue = None     

    #Permet de definir les combobox (et leurs valeurs)
    def InitializeComboBoxes(self):                     
        self.viticulteur.setCurrentIndex(0)
        self.viticulteur.setDisabled(False)
        self.parcelle.clear()
        self.cepage.clear() 
        self.poidsRaisin.clear() 
        self.cepage.setDisabled(True)
        self.parcelle.setDisabled(True)
        self.poidsRaisin.setDisabled(True)

   
    def UpdateParcelle(self):
        self.parcelle.clear()
        self.cepage.clear() 
        self.poidsRaisin.clear() 
        self.parcelle.setDisabled(True)   
        self.poidsRaisin.setDisabled(True) 
        lu = sorted(set(x[1] for x in self.data if x[0]==self.viticulteur.currentText()))
        if len(lu)==1 : 
            self.parcelle.addItems(lu)
            self.parcelle.setCurrentText(lu[0])
            self.parcelle.setDisabled(True)
            self.UpdateCepage()
        else : 
            self.parcelle.addItems(lu)
            self.parcelle.setDisabled(False)

    def UpdateCepage(self):
        self.cepage.clear() 
        for i in range ( 0, len(self.data)) : 
            if (self.data[i][1]==self.parcelle.currentText()):
                print(self.data[i][2])
                cepage_list = sorted(self.data[i][2])

        print(cepage_list)
        if len(cepage_list)==1 :             
            self.cepage.addItem(self.dict_Cepage[cepage_list[0]])
            self.cepage.setCurrentText(cepage_list[0])
            self.cepage.setDisabled(True)
            self.poidsRaisin.setDisabled(False)
        else : 
            for n in cepage_list : 
                self.cepage.addItem(self.dict_Cepage[n])
            self.cepage.setDisabled(False)
    
        
    def UpdatePoids(self) : 
        self.poidsRaisin.setDisabled(False)
           




    def DataCollection (self): 
        chemin = "producteurs.txt"
        with open(chemin,"r") as fichier:
            next(fichier)
            for line in fichier : 
                self.data.append(line)
        for i in range (0,len(self.data)):
            newline = self.data[i].replace(" ","")[:-1].split(";")
            self.data[i] = [newline[0],newline[1],newline[2].split(",")]
             
               
    def RegisterOrder (self):   
        if re.match(r'^[0-9]*$',str(self.poidsRaisin.toPlainText())):  
            self.ligne = f"{str(self.viticulteur.currentText())};{str(self.parcelle.currentText())};{str(self.cepage.currentText())};{str(self.poidsRaisin.toPlainText())};{QDate.currentDate().toString('d.M.yy')};{QTime.currentTime().toString('h.m.s')}\n"
            self.CommitToTextFile()
        else : 
            self.show_popup("Mauvaise saisie")

    
    def CommitToTextFile (self):
        with open('historique.txt','a') as fichier:
            fichier.write(self.ligne)
        self.show_popup("Entrée enregistré avec succès")
        self.InitializeComboBoxes()

    
    def show_popup(self,texte):
        msg = QMessageBox()
        msg.setWindowTitle("OK")
        msg.setText(texte)
        x = msg.exec_()
    
    def final(self):
        
        self.hide()
        Vue= Recapitulatif(self)
        Vue.show()


class Recapitulatif(QtWidgets.QMainWindow):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("Index2.ui",self)  
        self.pushButton.clicked.connect(self.UpdateTable)
        self.livraison.clicked.connect(self.retour)
        self.viticulteur.activated[str].connect(self.Update)     
        self.cepage.setDisabled(True)
        self.DataCollection()
        self.viticulteur.addItems(sorted(set(x[0] for x in self.data)))
    data =[]
    arrayToDisplay = []
    Vue = None


    def DataCollection (self): 
        chemin = "historique.txt"
        with open(chemin,"r") as fichier:
            next(fichier)
            for line in fichier : 
                self.data.append(line)
            for i in range (0,len(self.data)):
                newline = self.data[i][:-1].split(";")
                self.data[i] = [newline[0],newline[1],newline[2],newline[3],newline[4],newline[5]]


        


    def Update(self):
        self.cepage.clear() 
        liste_cepage = []
        for i in range ( 0, len(self.data)) : 
            if (self.data[i][0]==self.viticulteur.currentText()):
                if (self.data[i][2] not in liste_cepage):
                    liste_cepage.append(self.data[i][2])
        if len(liste_cepage)==1 : 
            self.cepage.addItems(liste_cepage)
            self.cepage.setDisabled(True)
            self.cepage.setCurrentText(liste_cepage[0])
            
        else: 
            self.cepage.addItems(liste_cepage)
            self.cepage.setDisabled(False)



    def UpdateTable(self): 
        self.arrayToDisplay =[]  
        Total = 0      
        for i in range ( 0, len(self.data)) : 
            if (self.data[i][0]==self.viticulteur.currentText() and self.data[i][2]==self.cepage.currentText()):
                self.arrayToDisplay.append([self.data[i][4],self.data[i][5],self.data[i][1],self.data[i][3]])
                Total += int(self.data[i][3])
        self.total.setText(str(Total))
        self.qtableFromArray(self.arrayToDisplay, self.mytable)

    
  
    def qtableFromArray(self, array, qtable):
        nbRow = len(array)
        nbCol = len(array[0])
        qtable.setRowCount(nbRow)
        qtable.setColumnCount(nbCol)
        qtable.setHorizontalHeaderLabels(['Date','Heure','Parcelle','Quantité','Cépage']) 
        for i in range(nbRow):
            for j in range(nbCol):
                qtable.setItem(i,j,QtWidgets.QTableWidgetItem(str(array[i][j])))


    def retour(self):
        self.parent().show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Livraison()
    window.show()
    sys.exit(app.exec_())