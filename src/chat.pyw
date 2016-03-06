__author__ = 'Chelsea'


from chatapp import *
import sys
import os
import aiml
import random
import time
import socket
from thread import *


class ChatApplication(QtGui.QMainWindow):

    # setup window
    def __init__(self, parent=None):
        # setup the gui
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # load kernel
        self.kernel = aiml.Kernel()
        self.kernel.setBotPredicate('name', 'Chelsea')

        # connect the buttons to the methods
        QtCore.QObject.connect(self.ui.sendMessage_Button, QtCore.SIGNAL('clicked()'), self.send_message)
        QtCore.QObject.connect(self.ui.clearLogs_Button, QtCore.SIGNAL('clicked()'), self.clear_logs)
        QtCore.QObject.connect(self.ui.connect_Button, QtCore.SIGNAL('clicked()'), self.connect)

        # self.actionExit.triggered.connect(quit())

        self.user_list = []
        self.previous_message = ""

    def load_brain(self):

        # change this to wherever your directory is

        os.chdir('C:\Users\user\Desktop\ChatApp')

        # if brain file is in directory, load it else load aiml files and create brain file.
        if os.path.isfile('brain.brn'):
            self.kernel.bootstrap(brainFile='brain.brn')
        else:
            self.kernel.bootstrap(learnFiles='startup.xml', commands='load aiml b')
            self.kernel.saveBrain('brain.brn')

    def send_message(self):

        message = str(self.ui.lineEdit_2.text())
        current_message = message.lower()

        if current_message == self.previous_message:
            self.ui.listWidget.addItem(self.user_list[0] + ": " + message)
            call_out = ["Please don't repeat yourself", "You are repeating yourself", "Theres no need for repetition", "Stop it", "Well thats annoying"]
            self.ui.listWidget.addItem(self.user_list[1] + ": " + random.choice(call_out))
            print (message,current_message, self.previous_message)
        if current_message == "":
            pass
            # add pop up window telling user to type text, null values is not allowed.

        if current_message != self.previous_message:

            self.ui.listWidget.addItem(self.user_list[0] + ": " + message)
            self.previous_message = current_message
            self.ui.lineEdit_2.clear()
            self.respond(message)

    def respond(self, message):
        response = (self.kernel.respond(message))
        self.ui.listWidget.addItem(self.user_list[1] + ": " + response)

    def reload_brain(self):

        self.kernel.bootstrap(learnFiles='startup.xml', commands='load aiml b')
        self.kernel.saveBrain('brain.brn')

    def clear_logs(self):
        self.ui.listWidget.clear()

    def connect(self):

        try:
            if self.ui.lineEdit.text() == "":
                print "Need to enter name to chat"
            else:

                answer = "Connecting to user..."
                self.ui.listWidget.addItem(answer)

                ai_system = "Chelsea"
                answer = "Connection Established"
                self.ui.listWidget.addItem(answer)

                del answer

                if str(self.ui.lineEdit.text()) in self.user_list:

                    # change to pop up window telling user name already exists.
                    print "name already exists please choose another"

                else:
                    self.user_list.append(str(self.ui.lineEdit.text()))
                    self.user_list.append(ai_system)

                    self.ui.lineEdit.clear()

                    for name in self.user_list:

                        self.ui.listWidget_2.addItem(name)
                    else:
                        pass

        except:

            pass


# Execute application
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = ChatApplication()
    myapp.load_brain()
    myapp.show()
    sys.exit(app.exec_())