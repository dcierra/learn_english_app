import sys
from PyQt5 import QtWidgets
import random
import translators
from thread_methods import *
from auth import *
from english_app_ui import *
import pyttsx3


class GUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Иницилизация голоса
        self.engine = pyttsx3.init()

        # Убираем рамки
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.user_can_drag_window()

        # Обработчики кнопок
        self.ui.tBtn_minimaze.clicked.connect(self.minimize_window)
        self.ui.tBtn_closeWindow.clicked.connect(self.close_window)
        self.ui.tBtn_first_word.clicked.connect(self.check_first_btn)
        self.ui.tBtn_second_word.clicked.connect(self.check_second_btn)
        self.ui.tBtn_third_word.clicked.connect(self.check_third_btn)
        self.ui.tBtn_fourth_word.clicked.connect(self.check_fourth_btn)
        self.ui.tBtn_load_file.clicked.connect(self.choose_path_load_file)
        self.ui.tBtn_voice.clicked.connect(self.voice_word)

        # Создание потока
        self.thread_progress_bar = MyThreadProgressBar()
        self.thread_progress_bar.mysignal.connect(self.signal_thread_progress_bar)

        self.arr_russian_words = self.russian_words()
        self.arr_english_words = self.english_words()

        # Начальное заполнение
        self.filling()

    # Выбор пути до файла со словами
    def choose_path_load_file(self):
        self.path = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.arr_english_words = self.english_words(self.path)
        self.filling()

    def signal_thread_progress_bar(self, value):
        if value:
            value_progress_bar = self.ui.progressBar.value()
            if value_progress_bar == 9:
                self.msg_win()
            else:
                self.ui.progressBar.setValue(value_progress_bar + 1)
            count_word = self.ui.label_count_word.text()
            self.ui.label_count_word.setText(f'{str(int(count_word) + 1)}')
        else:
            self.msg_miss()
            self.ui.progressBar.setValue(0)

    # Озвучка слова
    def voice_word(self):
        self.engine.say(self.ui.label_word.text())
        self.engine.runAndWait()

    # Функции, выводящие сообщения
    def msg_win(self):
        QtWidgets.QMessageBox.warning(self, 'Победа', 'Поздравляю, вы смогли отгадать 10 слов подряд.')
        self.ui.progressBar.setValue(0)

    def msg_miss(self):
        QtWidgets.QMessageBox.warning(self, 'Мимо', 'Не правильно, ваш прогресс сбрасывается.')
        self.ui.progressBar.setValue(0)

    # Заполнение
    def filling(self):
        self.ui.label_word.setText(random.choice(self.arr_english_words))
        self.ui.tBtn_first_word.setText(random.choice(self.arr_russian_words))
        self.ui.tBtn_second_word.setText(random.choice(self.arr_russian_words))
        self.ui.tBtn_third_word.setText(random.choice(self.arr_russian_words))
        self.ui.tBtn_fourth_word.setText(random.choice(self.arr_russian_words))
        random.choice([self.ui.tBtn_first_word, self.ui.tBtn_second_word, self.ui.tBtn_third_word, self.ui.tBtn_fourth_word]).setText(translators.google(self.ui.label_word.text(), from_language='en', to_language='ru').lower())

    # Проверка, что нажата правильная кнопка
    def check_first_btn(self):
        if self.ui.tBtn_first_word.text().lower() == translators.google(self.ui.label_word.text(), from_language='en', to_language='ru').lower():
            self.update()
        else:
            self.incorrect_answer()

    def check_second_btn(self):
        if self.ui.tBtn_second_word.text().lower() == translators.google(self.ui.label_word.text(), from_language='en', to_language='ru').lower():
            self.update()
        else:
            self.incorrect_answer()

    def check_third_btn(self):
        if self.ui.tBtn_third_word.text().lower() == translators.google(self.ui.label_word.text(), from_language='en', to_language='ru').lower():
            self.update()
        else:
            self.incorrect_answer()

    def check_fourth_btn(self):
        if self.ui.tBtn_fourth_word.text().lower() == translators.google(self.ui.label_word.text(), from_language='en', to_language='ru').lower():
            self.update()
        else:
            self.incorrect_answer()

    def update(self):
        self.thread_progress_bar.start()
        self.filling()

    def incorrect_answer(self):
        self.signal_thread_progress_bar(False)
        self.filling()

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

    # Методы создания массивов со словами
    def english_words(self, path='english.txt'):
        with open(path) as english_file:
            valid_words = list(set(english_file.read().split()))
        return valid_words

    def russian_words(self):
        with open('russian.txt') as russian_file:
            valid_words = list(set(russian_file.read().split()))
        return valid_words


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    english_app = GUI()
    english_app.show()
    auth = Auth()
    auth.show()
    sys.exit(app.exec_())