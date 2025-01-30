class StringHandler:
    def getString(self):
        self.text = input()

    def printString(self):
        print(self.text.upper())

handler = StringHandler()
handler.getString()
handler.printString()