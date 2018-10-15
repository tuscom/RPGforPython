"""
機能
・関数一覧表を作成する。

"""

import os

class SourceHelper:
    def __init__(self):
        self.OneSetText = """
        {classNameText:=^60}
        ・{funcNameText: ^30} : {numberText}
        """
        self.fileName = "SourceHelper.txt"

        self.FileNameList = []

        self.dataDic = {} #className+funcName+argumentList : versionText

        self.KeySentenceList = None
        self.classNameList = None
        self.funcNameList = None
        self.argumentList = None
        self.versionText = None

    def Main(self):
        self.GetFileNameListInThisFolder()

        for fileName in self.FileNameList:
            self.OneFileFunctions(fileName)

        self.AdjustData()
        self.CheckData()
        self.WriteInFile()

    #全体
    def GetFileNameListInThisFolder(self):
        self.FileNameList = os.listdir("./")
        self.FileNameList = list(filter(lambda fileName : ".py" in fileName, self.FileNameList))
        #print(self.FileNameList)

    def CheckData(self):
        keys = [*self.dataDic]
        keys.sort()
        for key in keys:
            print(key + " : " + self.dataDic[key])

    def AdjustData(self):
        values = [*self.dataDic.values()]
        for key in self.dataDic:
            value = self.dataDic[key]
            valueList = value.split(", ")
            valueList.sort()
            self.dataDic[key] = ", ".join(valueList)

    def WriteInFile(self):
        text = ""
        keys = [*self.dataDic]
        keys.sort()

        for key in keys:
            text += key + " : " + self.dataDic[key] + "\n"
        
        file = open(self.fileName, "w")
        file.write(text)
        file.close()

    #各ファイル毎
    def OneFileFunctions(self, fileName):
        self.ReadFile(fileName)
        self.GetClassName(fileName)
        self.GetFuncNameList()
        self.GetArgumentNameList()
        self.GetVersion(fileName)
        self.SetDataDic()

    def ReadFile(self, fileName):
        self.file = open(fileName, "r", encoding="utf-8")
        SentenceList = self.file.readlines()
        self.KeySentenceList = list(filter(lambda sentence : "class " in sentence, SentenceList)) + list(filter(lambda sentence : "def " in sentence, SentenceList))
        self.file.close()

    def GetClassName(self, fileName):
        stopCutLetterList = ["(", ":"]
        classList = list(filter(lambda sentence : "class " in sentence[0:7], self.KeySentenceList))
        classList = list(map(lambda sentence : sentence[6:], classList))
        classList = list(map(lambda classText:SourceHelper.StopCutTextWithList(classText, stopCutLetterList), classList))
        self.classNameList = classList
        #print(classList)

    def GetFuncNameList(self):
        stopCutLetterList = ["("]
        classList = list(filter(lambda sentence : "def " in sentence[0:8], self.KeySentenceList))
        classList = list(map(lambda sentence : sentence[8:], classList))
        classList = list(map(lambda classText:SourceHelper.StopCutTextWithList(classText, stopCutLetterList), classList))
        self.funcNameList = classList
        #print(classList)

    def GetArgumentNameList(self):
        startCutLetterList = ["("]
        stopCutLetterList = [")"]
        classList = list(filter(lambda sentence : "def " in sentence[0:8], self.KeySentenceList))
        classList = list(map(lambda sentence : sentence[8:], classList))
        classList = list(map(lambda sentence : SourceHelper.CutTextWithList(sentence, startCutLetterList, stopCutLetterList), classList))
        self.argumentList = classList
        #print(classList)

    def GetVersion(self, fileName):
        index = -4
        result = ""
        while True:
            if fileName[index].isdigit():
                result = fileName[index] + result
                index -= 1
            else:
                break

        self.versionText = result
        #print(self.versionText)

    def SetDataDic(self):
        index = 0
        for funcName in self.funcNameList:
            key = "{className} > {funcName}({argumentName})".format(
                className = self.classNameList,
                funcName = funcName,
                argumentName = self.argumentList[index]
                )
            try:
                self.dataDic[key] += ", " + self.versionText
            except KeyError:
                self.dataDic[key] = self.versionText

            index += 1
        #print(self.dataDic)

    #↓静的空間
    def StopCutTextWithList(text, letterList):
        for letter in letterList:
            text = SourceHelper.StopCutTextWithLetter(text, letter)

        return text

    def CutTextWithList(text, startLetterList, stopLetterList):
        for letter in startLetterList:
            text = SourceHelper.StartCutTextWithLetter(text, letter)
        for letter in stopLetterList:
            text = SourceHelper.StopCutTextWithLetter(text, letter)

        return text

    def StopCutTextWithLetter(text, letter):
        result = None
        try:
            index = text.index(letter)
            result = text[:index]
        except ValueError:
            result = text
        return result

    def StartCutTextWithLetter(text, letter):
        result = None
        try:
            index = text.index(letter)
            result = text[index+1:]
        except ValueError:
            result = text
        return result


    #def CutTextWithLetter(text, startLetter, stopLetter):
    #    result = None
    #    try:
    #        startIndex = text.index(startIndex)
    #        stopIndex = text.index(stopLetter)
    #        result = text[startIndex+1:stopIndex]
    #    except ValueError:
    #        result = text

    #    return result

if __name__ == "__main__":
    SourceHelper().Main()
