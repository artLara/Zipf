from Zipf_ui import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from scipy.optimize import curve_fit
import numpy as np
import keyword
# import random

# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as Navi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

# import math
# import os

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.pushButtonBrowse.clicked.connect(self.browse)
        self.pushButtonHist.clicked.connect(self.generarGrafico)
        self.keywords_c = ['auto',	'break', 'case',	'char',	'const', 'continue',	'default',
              'do', 'double',	'else',	'enum',	'extern',	'float',	'for',
              'goto',	'if', 'int',	'long',	'register',	'return',	'short',
              'signed',	'sizeof',	'static', 'struct',	'switch',	'typedef',
              'union',	'unsigned',	'void',	'volatile',	'while']

        self.keywords_java = ['abstract','boolean', 'break','byte','case','catch','char',
              'class', 'continue',	'default',	'do',	'double',	'else',	'extends',
              'final',	'finally', 'float',	'for',	'if',	'implements',	'import',
              'instanceof',	'int',	'interface', 'long',	'native',	'new',
              'package',	'private',	'protected',	'public',	'return',
              'short', 'static', 'super',	'switch',	'synchronized',	'this',	'throw',
              'throws', 'transient', 'try',	'void',	'volatile',	'while']

        self.keywords_python = keyword.kwlist

        self.keywords_c_dict = {}
        self.keywords_java_dict = {}
        self.keywords_python_dict = {}


        self.file_name = 'c.txt'

    def foo_c(self, x):
        return self.keywords_c_dict[x]

    def foo_java(self, x):
        return self.keywords_java_dict[x]

    def foo_python(self, x):
        return self.keywords_python_dict[x]

    def countKeyWords(self, dict, list_words):
        file1 = open(self.file_name, 'r')
        lines = file1.readlines()
        count = 0
        # Strips the newline character
        for line in lines:
            words = line.strip().split(' ')
            for word in words:
                #print("{}".format(word))
                if word in list_words:
                    dict[word] += 1

    def power_law(self, x, a, b):
        return a*np.power(x, b)

    def generarGrafico(self):
        dict_tmp = {}
        keywords_tmp = []
        if self.radioButtonC.isChecked():
            for c in self.keywords_c:
                self.keywords_c_dict[c] = 0
            self.countKeyWords(self.keywords_c_dict, self.keywords_c)
            self.keywords_c.sort(key=self.foo_c, reverse=False)
            dict_tmp = self.keywords_c_dict
            keywords_tmp = self.keywords_c

        elif self.radioButtonJava.isChecked():
            for c in self.keywords_java:
                self.keywords_java_dict[c] = 0
            self.countKeyWords(self.keywords_java_dict, self.keywords_java)
            self.keywords_java.sort(key=self.foo_java, reverse=False)
            dict_tmp = self.keywords_java_dict
            keywords_tmp = self.keywords_java

        elif self.radioButtonPython.isChecked():
            for c in self.keywords_python:
                self.keywords_python_dict[c] = 0
            self.countKeyWords(self.keywords_python_dict, self.keywords_python)
            self.keywords_python.sort(key=self.foo_python, reverse=False)
            dict_tmp = self.keywords_python_dict
            keywords_tmp = self.keywords_python


        values = list(dict_tmp.values())
        values.sort(reverse=False)
        pars, cov = curve_fit(f=self.power_law, xdata=range(len(values)+1, 1, -1), ydata=values)
        a = pars[0]
        b = pars[1]

        power_law_values = []
        for i in range(len(values)+1, 1, -1):
            power_law_values.append(self.power_law(i, a, b))
        power_law_values = np.array(power_law_values) * 1
        fig = plt.figure(figsize = (13, 7))
        plt.rcParams.update({'font.size': 8})
        plt.bar(keywords_tmp, values, color ='maroon',width = 0.4)
        plt.plot(keywords_tmp, power_law_values,'b-', lw=1, alpha=0.7, label='powerlaw pdf')

        # plt.legend(loc="lower right")
        # plt.grid(linestyle='--')
        # plt.savefig('tmp.png', dpi=75)


        # adding image to label
        # self.hist.setPixmap(self.pixmap)
        plt.savefig('tmp.png', dpi=90)
        self.pixmap = QPixmap('tmp.png')

        self.hist_2.setPixmap(self.pixmap)
        plt.cla()
        plt.clf()


    def browse(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home/lara/Desktop/Proba/Zipf')[0]
        self.plainTextEditPrevio.setPlainText(self.file_name)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
