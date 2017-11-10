# -*- coding:utf-8 -*-

from os import path
import jieba
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FontCN_NLPtools():
    def __init__(self, stopwordsPath):
        self.__TextPath = " "
        self.d = path.dirname(__file__)
        self.__stopwordsPath = stopwordsPath
        self.__userWords = []
        self.__text = ""

    def jiebaCutText(self, isAddWord=False):

        for i in self.__userWords:
            jieba.add_word(i)

        seg_list = list(jieba.cut(self.__text, cut_all=False))

        self.__seg_list = []
        for i in seg_list:
            if i.isspace() == False:
                self.__seg_list.append(i)

        return ' '.join(self.__seg_list)

    def clearText(self, NewStopWordsPath='no'):

        if NewStopWordsPath != 'no':
            self.__stopwordsPath = NewStopWordsPath

        mywordlist = []
        f_stop = open(self.__stopwordsPath)

        try:
            f_stop_text = f_stop.read()
            f_stop_text = unicode(f_stop_text, 'utf-8')
        finally:
            f_stop.close()
        f_stop_seg_list = f_stop_text.split('\n')

        for myword in self.__seg_list:
            if not (myword.strip() in f_stop_seg_list) and len(myword.strip()) > 1:
                mywordlist.append(myword)

        return ' '.join(mywordlist)

    def getText(self, textData, isJieba=True):

        self.__text = textData

        if isJieba == True:
            self.jiebaCutText()

        clearText = self.clearText()
        return clearText

