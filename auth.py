from auth_ui import *


class Auth(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowModality(2)

        # Убираем рамки
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.user_can_drag_window()

        # Обработчики кнопок
        self.ui.tBtn_minimaze.clicked.connect(self.minimize_window)
        self.ui.tBtn_closeWindow.clicked.connect(self.close_window)
        self.ui.btn_enter.clicked.connect(self.auth)

    # Авторизация пользователя
    def auth(self):
        # Получаем список всех пользователей
        with open('users.txt') as file:
            users = [i.strip().split(', ') for i in file.readlines()]

        username = self.ui.lE_enter_username.text()
        flag = True
        if len(username) > 0:
            for user in users:
                if username == user[0]:
                    QtWidgets.QMessageBox.information(self, 'Приветствие', f'С возвращением, {username}!')
                    flag = False
                    self.close()
            if flag:
                with open('users.txt', 'a') as file:
                    file.write('\n' + username)
                QtWidgets.QMessageBox.information(self, 'Приветствие', f'Добро пожаловать, {username}!')
                self.close()
        else:
            QtWidgets.QMessageBox.information(self, 'Ошибка', 'Вы не ввели имя')


    # Методы позволяющие пользователю двигать окно
    def user_can_drag_window(self):
        fg = self.frameGeometry()
        cp = QtWidgets.QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QtCore.QPoint(event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except AttributeError:
            pass

    # Методы кнопок
    def close_window(self):
        if QtWidgets.QMessageBox.warning(self, 'Выход', 'Вы действительно хотите выйти?',
                                         QtWidgets.QMessageBox.Yes,
                                         QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            raise SystemExit
        else:
            return

    def minimize_window(self):
        self.showNormal()
        self.showMinimized()