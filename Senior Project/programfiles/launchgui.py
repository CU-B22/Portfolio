from ast import Return
from matplotlib import pyplot as plt
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt
from PyQt6 import uic
from numpy import isin
import pandas as pd
import csv
import sys



class UI(QMainWindow):
    def  __init__(self):
        super(UI, self).__init__()
        
        # load ui file
        uic.loadUi('MainGUI.ui', self) # change string in ' ' to the .ui file name in order to launch desired GUI file
        
        # # define our widgets
        self.table = self.findChild(QTableWidget, "tableWidget")
        
        
        # show apps
        self.show()
    
        
    
    def loadcsvData(self, filename):
        df = pd.read_csv(filename, skip_blank_lines = True)
        if df.size == 0:
            return

        df.drop(df.columns.difference(["Process Name","Device ID","Build Mode","Align MA0", "Align MA1", "Align MA2", "Align MA3", "Align MA4", "Align VX", "Align VY", "Result"]), axis = 1, inplace = True)
        df['Result'] = df['Result'].replace(to_replace=['FAIL', 'PASS'], value = [0, 1]) # changes 'PASS' values to 1 and 'FAIL' values to 0 
        
        df = df[df["Build Mode"].str.contains('AAA')==False] # removes rows under Build Mode based on AAA values if needed
        df = df[df["Build Mode"].str.contains('BBB')==False] # removes rows under Build Mode based on BBB values if needed
        df = df[df["Build Mode"].str.contains('CCC')==False] # removes rows under Build Mode based on CCC values if needed
        
        df = df[df["Process Name"].str.contains('YYY')==True] # only keeps cells that match 'Process Name' entered
        df = df[df["Device ID"].str.contains('XXX')==True] # only keeps cells that match 'Device ID' entered
        df = df.dropna() # drops null values
        df = df.drop_duplicates(subset = ['Process Name', 'Device ID', 'Build Mode', 'Result'], keep = 'last') # drops duplicates w/n these columns

        print(df.iloc[0:50]) # should actually save this using df = df.iloc[0:50] which would limit it to 50 rows
        # print(df) # prints what the datafile would look like
        
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLables(df.columns)
        


    
# intiliaze the app
if __name__ == '__main__':
    
    filename = 'MasterProcessLog.csv'
    
    app = QApplication(sys.argv)
    UIWindow = UI()
    app.exec()
