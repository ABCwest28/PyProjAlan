import sys
import sqlite3
import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *


class SigninPage(QDialog):
    def __init__(self):
        super(SigninPage, self).__init__()
        self.signin_user_label = QLabel('E-mail:')
        self.signin_pwd_label = QLabel('Password:')
        self.signin_pwd2_label = QLabel('Password:')
        self.signin_user_line = QLineEdit()
        self.signin_pwd_line = QLineEdit()
        self.signin_pwd2_line = QLineEdit()
        self.signin_button = QPushButton('Sign in')

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    def layout_init(self):
        self.user_h_layout.addWidget(self.signin_user_label)
        self.user_h_layout.addWidget(self.signin_user_line)
        self.pwd_h_layout.addWidget(self.signin_pwd_label)
        self.pwd_h_layout.addWidget(self.signin_pwd_line)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_label)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addWidget(self.signin_button)

        self.setLayout(self.all_v_layout)

    def lineedit_init(self):
        self.signin_pwd_line.setEchoMode(QLineEdit.Password)
        self.signin_pwd2_line.setEchoMode(QLineEdit.Password)

        self.signin_user_line.textChanged.connect(self.check_input_func)
        self.signin_pwd_line.textChanged.connect(self.check_input_func)
        self.signin_pwd2_line.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.check_signin_func)

    def check_input_func(self):
        if self.signin_user_line.text() and \
                self.signin_pwd_line.text() and \
                self.signin_pwd2_line.text():
            self.signin_button.setEnabled(True)
        else:
            self.signin_button.setEnabled(False)

    def check_signin_func(self):
        if self.signin_pwd_line.text() != self.signin_pwd2_line.text():
            QMessageBox.critical(self, 'Wrong', 'Two Passwords Typed Are Not Same!')
        #elif self.signin_user_line.text() not in USER_PWD:
        else:
            self.myfunc_signin_user_checklogin(str(self.signin_user_line.text()))
        self.signin_user_line.clear()
        self.signin_pwd_line.clear()
        self.signin_pwd2_line.clear()

    def myfunc_signin_user_checklogin(self, login):
        try:
            sqlite_connection = sqlite3.connect('logins.db')
            cursor = sqlite_connection.cursor()
            print("myfunc_signin_user_checklogin---->Подключен к SQLite")
            print("myfunc_signin_user_checklogin---->login:", login, sep="")

            sqlite_select_query = """SELECT login FROM users WHERE login = ?"""
            cursor.execute(sqlite_select_query, (login,))
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                print("myfunc_signin_user_checklogin---->not such user in DB")
                sqlite_connection.close()
                self.myfunc_signin_add()
                QMessageBox.information(self, 'Information', 'Register Successfully')
                self.close()
            else:
                print("myfunc_signin_user_checklogin---->user in DB already")
                print("myfunc_signin_user_checklogin---->DB:", result[0], sep="")
                QMessageBox.critical(self, 'Wrong', 'This Username Has Been Registered!')

        except sqlite3.Error as error:
            print("myfunc_signin_user_checklogin---->Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("myfunc_signin_user_checklogin---->Соединение с SQLite закрыто")

    def myfunc_signin_add(self):
        try:
            sqlite_connection = sqlite3.connect('logins.db')
            cursor = sqlite_connection.cursor()
            print("myfunc_signin_add---->Подключен к SQLite")

            login = str(self.signin_user_line.text())
            password = str(self.signin_pwd_line.text())

            sqlite_insert_with_param = """INSERT INTO users (login, password) VALUES (?, ?);"""
            data = (login, password)
            cursor.execute(sqlite_insert_with_param, data)
            sqlite_connection.commit()
            cursor.close()
            print("myfunc_signin_add---->Добавлен пользователь:", data)
        except sqlite3.Error as error:
            print("myfunc_signin_add---->Ошибка при работе с SQLite", error)
            return False
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("myfunc_signin_add---->Соединение с SQLite закрыто")


class WindowUser(QtWidgets.QMainWindow):
    def __init__(self, name):
        super().__init__()
        self.resize(640, 480)
        self.centralwidget = QtWidgets.QWidget()
        self.setCentralWidget(self.centralwidget)

        data_male = self.myfunc_getdata("male")
        data_female = self.myfunc_getdata("female")

        data_male_age1 = 0
        data_male_age2 = 0
        data_male_age3 = 0
        data_male_age4 = 0
        data_female_age1 = 0
        data_female_age2 = 0
        data_female_age3 = 0
        data_female_age4 = 0

        for i in range(len(data_male)):
            print(data_male[i][0])
            if data_male[i][0] in range(0, 19):
                data_male_age1 += 1
            elif data_male[i][0] in range(19, 30):
                data_male_age2 += 1
            elif data_male[i][0] in range(30, 45):
                data_male_age3 += 1
            elif data_male[i][0] >= 45:
                data_male_age4 += 1

        for i in range(len(data_female)):
            if data_female[i][0] in range(0, 19):
                data_female_age1 += 1
            elif data_female[i][0] in range(19, 30):
                data_female_age2 += 1
            elif data_female[i][0] in range(30, 45):
                data_female_age3 += 1
            elif data_female[i][0] >= 45:
                data_female_age4 += 1

        #x1 = np.arange(1, 5) - 0.2
        #x2 = np.arange(1, 5) + 0.2
        #y1 = [data_male[0:len(data_male)][0]]
        #y2 = data_female[0:len(data_male)][0]

        fig, ax = plt.subplots()

        ax.bar([0.8, 1.8, 2.8, 3.8], [data_male_age1, data_male_age2, data_male_age3, data_male_age4], width=0.4)
        ax.bar([1.2, 2.2, 3.2, 4.2], [data_female_age1, data_female_age2, data_female_age3, data_female_age4], width=0.4)

        ax.set_facecolor('seashell')
        fig.set_figwidth(12)
        fig.set_figheight(6)
        fig.set_facecolor('floralwhite')

        plt.show()
        self.showMinimized()

    def myfunc_getdata(self, arg):
        try:
            sqlite_connection = sqlite3.connect('logins.db')
            cursor = sqlite_connection.cursor()
            print("myfunc_getdata---->Подключен к SQLite")
            if arg == "male":
                sqlite_select_query0 = """SELECT age FROM data WHERE sex = 0"""
                cursor.execute(sqlite_select_query0)
                result = cursor.fetchall()
            else:
                sqlite_select_query1 = """SELECT age FROM data WHERE sex = 1"""
                cursor.execute(sqlite_select_query1)
                result = cursor.fetchall()
            cursor.close()
            print("myfunc_getdata---->", len(result))
            return result

        except sqlite3.Error as error:
            print("myfunc_getdata---->Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("myfunc_getdata---->Соединение с SQLite закрыто")


class Login(QWidget):
    def __init__(self):
        super(Login, self).__init__()
        self.resize(300, 100)

        self.user_label = QLabel('E-mail address:', self)
        self.pwd_label = QLabel('Password:', self)
        self.user_line = QLineEdit(self)
        self.user_line.setClearButtonEnabled(True)
        self.pwd_line = QLineEdit(self)
        self.pwd_line.setClearButtonEnabled(True)
        self.login_button = QPushButton('Войти', self)
        self.signin_button = QPushButton('Зарегистрироватся', self)

        self.grid_layout = QGridLayout()
        self.h_layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()
        self.signin_page = SigninPage()

    def layout_init(self):
        self.grid_layout.addWidget(self.user_label, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.user_line, 0, 1, 1, 1)
        self.grid_layout.addWidget(self.pwd_label, 1, 0, 1, 1)
        self.grid_layout.addWidget(self.pwd_line, 1, 1, 1, 1)
        self.h_layout.addWidget(self.login_button)
        self.h_layout.addWidget(self.signin_button)
        self.v_layout.addLayout(self.grid_layout)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)

    def lineedit_init(self):
        self.user_line.setPlaceholderText('Please enter your email')
        self.pwd_line.setPlaceholderText('Please enter your password')
        self.pwd_line.setEchoMode(QLineEdit.Password)

        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.login_button.setEnabled(False)
        #self.login_button.clicked.connect(self.check_login_func)
        self.login_button.clicked.connect(self.myfunc_login)
        self.signin_button.clicked.connect(self.show_signin_page_func)

    def myfunc_login(self):
        try:
            cur_login = self.user_line.text()
            cur_password = self.pwd_line.text()
            sqlite_connection = sqlite3.connect('logins.db')
            cursor = sqlite_connection.cursor()
            print("myfunc_login---->Подключен к SQLite")
            print("myfunc_login---->login:", cur_login, sep="")
            print("myfunc_login---->password:", cur_password, sep="")

            sqlite_select_query = """SELECT login, password FROM users WHERE login = ? AND password = ?"""
            cursor.execute(sqlite_select_query, (cur_login, cur_password))
            result = cursor.fetchone()
            cursor.close()
            if result is None:
                print("myfunc_login---->not such user in DB")
                QMessageBox.critical(self, 'Wrong', 'Wrong Username or Password!')
                return
            else:
                print("myfunc_login---->user in DB")
                print("myfunc_login---->DB:login:", result[0], sep="")
                print("myfunc_login---->DB:password:", result[1], sep="")
                self.windowUser = WindowUser(cur_login)
                self.windowUser.show()
                self.close()

        except sqlite3.Error as error:
            print("myfunc_login---->Ошибка при работе с SQLite", error)
        finally:
            if sqlite_connection:
                sqlite_connection.close()
                print("myfunc_login---->Соединение с SQLite закрыто")


    def show_signin_page_func(self):
        self.signin_page.exec_()

    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text():
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Login()
    w.show()
    sys.exit(app.exec_())

