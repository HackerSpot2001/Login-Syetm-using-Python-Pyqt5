#!/usr/bin/python3
from PyQt5.QtWidgets import QLineEdit, QMainWindow,QApplication, QMessageBox, QPushButton, QTabWidget
from PyQt5.uic import loadUi
import sys
import sqlite3




class UIWindow(QMainWindow):
    def __init__(self):
        super(UIWindow,self).__init__()
        loadUi("UIFILE.ui",self)
        self.tabs = self.findChild(QTabWidget,"tabWidget")
        self.tabs.setCurrentIndex(0)
        self.tabs.tabBar().setVisible(False)

        self.loginInput = self.findChild(QLineEdit,"lineEdit")
        self.loginPassword = self.findChild(QLineEdit,"lineEdit_2")

        self.signupInput = self.findChild(QLineEdit,"lineEdit_3")
        self.signupPhone = self.findChild(QLineEdit,"lineEdit_4")
        self.signupConfirmPassword = self.findChild(QLineEdit,"lineEdit_5")
        self.signupPassword = self.findChild(QLineEdit,"lineEdit_6")
        self.loginBtn = self.findChild(QPushButton,"pushButton")
        self.signUpBtn = self.findChild(QPushButton,"pushButton_2")
        self.notMember = self.findChild(QPushButton,"pushButton_3")
        self.alreadyMember = self.findChild(QPushButton,"pushButton_4")
        self.loginBtn.clicked.connect(self.onLogin)
        self.alreadyMember.clicked.connect(self.getloginTab)

        self.notMember.clicked.connect(self.getSignUpTab)
        self.signUpBtn.clicked.connect(self.onSignUp)
        self.conn = sqlite3.connect("users.db")
        self.cursr = self.conn.cursor()
        self.sqlQuery = ""

    def setBlank(self):
        self.signupInput.setText("")
        self.signupPassword.setText("")
        self.signupPhone.setText("")
        self.signupConfirmPassword.setText("")
        self.loginInput.setText("")
        self.loginPassword.setText("")

    def getSignUpTab(self):
        self.tabs.setCurrentIndex(1)
    
    def getloginTab(self):
        self.tabs.setCurrentIndex(0)
    
    def onLogin(self):
        if (str(self.loginInput.text()) != "") and( str(self.loginPassword.text()) != ""):
            try:
                self.sqlQuery = f"SELECT * FROM users WHERE email='{str(self.loginInput.text())}' OR phone='{str(self.loginInput.text())}'"       
                self.cursr.execute(self.sqlQuery)
                data = self.cursr.fetchall()
                if len(data) == 0:
                    QMessageBox.warning(self,"Warning","Your are not a Member, Please Sign-Up")
                    self.setBlank()
                    self.getSignUpTab()

                else:
                    if str(data[0][2]) != str(self.loginPassword.text()):
                        QMessageBox.warning(self,"Warning","Your Credentials are Wrong!")
                    
                    else:
                        QMessageBox.about(self,"Warning","Welcome {}".format(str(self.loginInput.text())))

            
            except Exception as e:
                QMessageBox.warning(self,"Error",str(e))
                
        else:
            QMessageBox.warning(self,"Warning","Please Fill All Fields!")


    def onSignUp(self):
        if (str(self.signupInput.text()) != "") and (str(self.signupPhone.text()) != "") and (str(self.signupPassword.text()) != "") and (str(self.signupConfirmPassword.text()) != ""):
            if (str(self.signupPassword.text()) == str(self.signupConfirmPassword.text())):
                try:
                    self.sqlQuery = f"SELECT * FROM users WHERE email='{self.signupInput.text()}' OR phone='{self.signupPhone.text()}'"
                    self.cursr.execute(self.sqlQuery)
                    data = self.cursr.fetchall()
                    if len(data) != 0:
                        QMessageBox.about(self,"Warning","You are Already a Member.")
                        self.getloginTab()
                    
                    else:
                        self.sqlQuery = f"INSERT INTO users (email,phone,password) VALUES ('{str(self.signupInput.text().lower())}','{str(self.signupPhone.text().lower())}','{str(self.signupPassword.text().lower())}')"
                        self.cursr.execute(self.sqlQuery)
                        self.conn.commit()
                        QMessageBox.about(self,"Warning","Your Account Was Created Successfully.")
                    
                    self.setBlank()

                except Exception as e:
                    QMessageBox.warning(self,"Warning",str(e))

            else:
                QMessageBox.warning(self,"Warning","Make Sure Password and Confirm Password are Same!")

        else:
            QMessageBox.warning(self,"Warning","Please Fill All Fields!")



    
    def initializeDB(self):
        self.sqlQuery = """CREATE TABLE users(
            email VARCHAR(255) NOT NULL,
            phone CHAR(255) NOT NULL,
            password CHAR(255) NOT NULL
        );"""
        self.cursr.execute(self.sqlQuery)
        self.conn.commit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UIWindow() 
    window.show()
    sys.exit(app.exec())