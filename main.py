import random
import time
import requests


class Dictionnair:
    def __init__(self):
        self.larousaddr = "https://www.larousse.fr/dictionnaires/francais/"
        self.exeTime = 0
        self.Historique = []

    def getExeTime(self):
        return self.exeTime

    def getHist(self):
        return self.Historique

    def askInt(self, string="entrez un int", stringError="erreur valeur"):
        userchoice = str(input(string))
        while not userchoice.isdigit():
            userchoice = str(input(stringError + "\n" + string))
        userchoice = int(userchoice)
        return userchoice

    def getdef(self, word):

        self.exeTime = time.time()
        sourceCode = requests.get(self.larousaddr + str(word)).content
        defi = sourceCode.split(b'<li class="DivisionDefinition">')[1].replace(b"&", b"|")
        defi = defi.replace(b"</li>", b"|")
        defi = defi.replace(b".", b" ", 1)
        if defi.find(b'<span class="numDef">') > 0:
            defi = defi.split(b"1.")[1].split(b"|")[0].decode("utf-8")
        else:
            defi = defi.split(b"|")[0].decode("utf-8")
        while defi.find("<") != -1 or defi.find(">") != -1:
            defi = defi.replace(defi[defi.find("<"):defi.find(">") + 1], "")
        self.exeTime = time.time() - self.exeTime
        return defi

    def randWord(self, nb=1):
        mots = []
        i = 0
        self.exeTime = time.time()
        while i < nb:
            rd = random.randint(0, 63500)
            sourceCode = requests.get(self.larousaddr + "coucou/" + str(rd)).content
            mot = sourceCode.split(b"<title>")[1].split(b"</title>")[0].decode("utf-8").replace(" ", "")
            if (mot.split(":")[0] != '\r\n\r\n'):
                i += 1
                mot = mot.split(":")[1].split("-")[0]
                if mot.find(",") != -1:
                    mot = mot.split(",")[0]
                mots.append(mot)
                self.Historique.append(mot)
        self.exeTime = time.time() - self.exeTime
        return mots[0]

class pendu:

    def __init__(self):
        self.dictionnair = Dictionnair()
        self.playerWord = ""
        self.wrongLetters = []
        self.searchedWord = ""
        self.maxTry = 15
        self.trys = 0
        self.definition = ""
    def askLetter(self):
        return input("nouvelle lettre")

    def affichage(self):
        print("-------pendu-------")
        print("definition : "+self.definition)
        print("Votre mot : "+self.playerWord)
        print("essaies :" + str(self.trys) + " / " + str(self.maxTry) )
        print("lettres déja dites :" + str(self.wrongLetters))
        print("------------------------------")

    def newWord(self):
        self.searchedWord = self.dictionnair.randWord()
        self.playerWord = "_" * (len(self.searchedWord))

    def addLetter(self, letter):
        i = 0
        tab = []
        for l in self.playerWord:
            tab.append(l)

        for l in self.searchedWord:
            if l == letter:
                tab[i] = letter
            i += 1
        self.playerWord = ""
        for l in tab:
            self.playerWord += l

    def stockWrong(self, letter):
        self.wrongLetters.append(letter)

    def run(self):
        self.newWord()
        self.definition = self.dictionnair.getdef(self.searchedWord)
        while (self.trys <= self.maxTry):
            self.affichage()
            letter = self.askLetter()
            if len(letter) == 1 :
                if (letter in self.searchedWord):
                    self.addLetter(letter)
                else:
                    self.stockWrong(letter)
                    self.trys += 1
                    if (self.trys == self.maxTry):
                        print("partie perdue, le mot etait :" + self.searchedWord)
                        break

            if (letter == self.searchedWord or self.playerWord == self.searchedWord ):
                print("partie gagnée, le mot etait :" + self.searchedWord)
                break


if __name__ == "__main__":
    mon_pendu = pendu()
    mon_pendu.run()
    print("fin")