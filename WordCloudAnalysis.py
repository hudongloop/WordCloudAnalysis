# -*- coding:utf-8 -*-

import sys
from PyQt4 import QtCore, QtGui, uic
import chardet # check character type

import FontCN_NLPtools as fts
import nltk
import jieba.posseg as pseg
from wordcloud import WordCloud
import matplotlib.pyplot as plt

reload(sys)
sys.setdefaultencoding('utf-8')
nltk.data.path.append('./nltk_data')

qtCreatorFile = "WordAnalysis.ui" # Enter file here.
stopWordsFile = 'CNENstopwords.txt' # stop word list

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class UI_Window(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, stopwordsPath):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())

        # define variable
        self.__data = "" # original data
        self.__resultFDOrigin = nltk.FreqDist() # origin result data of freq dist
        self.__resultFDCurrent = nltk.FreqDist() # current select result data of freq dist
        self.__poSpeech = self.SpeechOption() # part of speech
        self.__maxFreq = 0 # max freq dist
        self.fontsTools = fts.FontCN_NLPtools(stopwordsPath)

        # add event
        self.openData.clicked.connect(self.OpenData)
        self.saveResult.clicked.connect(self.SaveResult)
        self.cloudResult.clicked.connect(self.CloudResult)
        self.analysisWord.clicked.connect(self.AnalysisWord)
        self.confirmOption.clicked.connect(self.ConfirmOption)
        self.inverseSelection.clicked.connect(self.InverseSelection)



    # define event
    def OpenData(self):
        fname = QtGui.QFileDialog.getOpenFileName(self)

        with open(fname, 'r') as f:
            self.__data = f.read().replace('\n','').replace(' ','')

        # show data in window
        if self.__data != "":
            sample_str = self.__data[:10] if len(self.__data) > 10 else self.__data
            type = chardet.detect(sample_str)
            try:
                self.inputData.setText(self.__data.decode(type["encoding"]))
            finally:
                self.inputData.setText(self.__data.decode('gb18030'))

    def SaveResult(self):
        fname = QtGui.QFileDialog.getSaveFileName(self, filter="Text Files (*.txt);;All Files (*)")
        with open(fname, 'w') as f:
            f.write(self.outputResult.toPlainText())

    def AnalysisWord(self):

        # analysis text data
        lztext = self.fontsTools.getText(self.__data)
        tokenstr = nltk.word_tokenize(lztext)
        self.__resultFDOrigin = nltk.FreqDist(tokenstr)

        self.outputResult.setText(self.DealResult())

    def ConfirmOption(self):
        # setting part of speech
        self.__poSpeech = self.SpeechOption()
        # setting max freq dist
        self.__maxFreq = self.spinFrequence.value()
        # show
        self.outputResult.setText(self.DealResult())

    def CloudResult(self):
        self.CalculationCloud()

    def InverseSelection(self):
        self.wordN.setChecked(not self.wordN.isChecked())
        self.wordV.setChecked(not self.wordV.isChecked())
        self.wordA.setChecked(not self.wordA.isChecked())
        self.wordR.setChecked(not self.wordR.isChecked())
        self.wordD.setChecked(not self.wordD.isChecked())
        self.wordMQ.setChecked(not self.wordMQ.isChecked())
        self.wordT.setChecked(not self.wordT.isChecked())
        self.wordP.setChecked(not self.wordP.isChecked())
        self.wordC.setChecked(not self.wordC.isChecked())
        self.wordU.setChecked(not self.wordU.isChecked())
        self.wordW.setChecked(not self.wordW.isChecked())
        self.wordEY.setChecked(not self.wordEY.isChecked())
        self.wordO.setChecked(not self.wordO.isChecked())
        self.wordX.setChecked(not self.wordX.isChecked())
        self.wordOther.setChecked(not self.wordOther.isChecked())

    # deal with result
    def DealResult(self):
        # deal with result
        listKVL = [] #save key val flag
        resultFDDelete = nltk.FreqDist()  # delete result data of freq dist
        orderFdist = enumerate(sorted(self.__resultFDOrigin.iteritems(), key=lambda x: (x[1], x[0]), reverse=True))
        for index, (key, val) in orderFdist:
            words = pseg.cut(key)
            for w in words:
                if (w.flag in self.__poSpeech) and (val > self.__maxFreq):
                    listKVL.append(key)
                    listKVL.append(str(val))
                    listKVL.append(w.flag)
                    listKVL.append('\n')
                else:
                    resultFDDelete.setdefault(key, val)
                break # forced end

            # show progress
            self.ShowProgress((index+1)/len(self.__resultFDOrigin)*100)
        self.__resultFDCurrent = self.__resultFDOrigin - resultFDDelete
        return '\t\t'.join(listKVL).replace('\t\t\n\t\t','\n')

    # show progress
    def ShowProgress(self, value):
        self.progressAnalysis.setValue(value)

    # Choosing part of speech
    def SpeechOption(self):
        poSpeech = [] #save part of speech

        # noun
        if self.wordN.isChecked():
            poSpeech += ['n', 'nr', 'nr1', 'nr2', 'nrj', 'nrf', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng']
        # verb
        if self.wordV.isChecked():
            poSpeech += ['v', 'vd', 'vn', 'vshi', 'vyou', 'vg', 'vx', 'vi', 'vl', 'vg']
        # adjective
        if self.wordA.isChecked():
            poSpeech += ['a', 'ad', 'an', 'ag', 'al']
        # pronoun
        if self.wordR.isChecked():
            poSpeech += ['r', 'rr', 'rz', 'rzt', 'rzs', 'rzv', 'ry', 'ryt', 'rys', 'ryv', 'rg']
        # adverb
        if self.wordD.isChecked():
            poSpeech += ['d']
        # numeral and classifier
        if self.wordMQ.isChecked():
            poSpeech += ['m', 'mq', 'q', 'qv', 'qt']
        # time
        if self.wordT.isChecked():
            poSpeech += ['t', 'tg']
        # preposition
        if self.wordP.isChecked():
            poSpeech += ['p', 'pba', 'pbei']
        # conjunction
        if self.wordC.isChecked():
            poSpeech += ['c', 'cc']
        # auxiliary word
        if self.wordU.isChecked():
            poSpeech += ['u', 'uzhe', 'ule', 'uguo', 'ude1', 'ude2', 'ude3', 'usuo', 'sdeng', 'uyy', 'udh', 'uls', 'uzhi', 'ulian']
        # punctuation
        if self.wordW.isChecked():
            poSpeech += ['w', 'wkz', 'wky', 'wyz', 'wyy', 'wj', 'ww', 'wt', 'wd', 'wf', 'wn', 'wm', 'ws', 'wp', 'wb', 'wh']
        # Interjection and modal
        if self.wordEY.isChecked():
            poSpeech += ['e', 'y']
        # onomatopoeia
        if self.wordO.isChecked():
            poSpeech += ['o']
        # string
        if self.wordX.isChecked():
            poSpeech += ['x', 'xx', 'xu']
        # other
        if self.wordOther.isChecked():
            poSpeech += ['s', 'f', 'b', 'bl', 'z', 'h', 'k']

        return poSpeech

    def CalculationCloud(self):

        font = r'simfang.ttf'
        my_wordcloud = WordCloud(collocations=False, font_path=font, width=1400, height=1400,
                                 margin=2).generate_from_frequencies(self.__resultFDCurrent)
        plt.imshow(my_wordcloud)
        plt.axis("off")
        plt.show()



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = UI_Window(stopWordsFile)
    window.show()
    sys.exit(app.exec_())