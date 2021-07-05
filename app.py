import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtkeybind import keybinder
import pyautogui
from tensor2tensor import models
from user_problems import *
from translate import Translator
from configs import *


class WinEventFilter(QtCore.QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class Ui_MainWindow(object):
    def __init__(self):

        self.translate_direction = 0  # 0: En -> Vi; 1: Vi -> En
        self.envi_translator = Translator(UniEnViConfig)
        self.vien_translator = Translator(UniViEnConfig)

        self.app = QtWidgets.QApplication(sys.argv)
        self.main_window = QtWidgets.QMainWindow()
        self.stylesheet = """
        QPushButton#switch_button{
            background-color: rgba(255, 255, 255, 0);
            border-color: #0b5ed7;
            border-style: solid;
            border-width: 2px;
            border-radius: 7px;
        }
        QPushButton#switch_button:hover{
            background-color: #0b5ed7
        }
        
        QPushButton#clear_button{
            color:#ffffff;
            background-color:#0d6efd;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
        }
        QPushButton#clear_button:hover{
            background-color: #0b5ed7
        }
        
        QPushButton#translate_button{
            color:#ffffff;
            background-color:#0d6efd;
            border-style: outset;
            border-width: 2px;
            border-radius: 10px;
        }
        QPushButton#translate_button:hover{
            background-color: #0b5ed7
        }
        
        """
        self.setupUi(self.main_window)
        self.setup_shortcuts()
        self.main_window.show()
        self.app.setStyleSheet(self.stylesheet)
        sys.exit(self.app.exec_())

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(781, 591)
        MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.input_box = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.input_box.setGeometry(QtCore.QRect(30, 170, 341, 231))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.input_box.setFont(font)
        self.input_box.setObjectName("input_box")
        self.output_box = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.output_box.setReadOnly(True)
        self.output_box.setGeometry(QtCore.QRect(410, 170, 341, 231))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.output_box.setFont(font)
        self.output_box.setObjectName("output_box")
        self.input_lang_label = QtWidgets.QLabel(self.centralwidget)
        self.input_lang_label.setGeometry(QtCore.QRect(30, 110, 241, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.input_lang_label.setFont(font)
        self.input_lang_label.setStyleSheet("color: #1967d2")
        self.input_lang_label.setObjectName("input_lang_label")
        self.output_lang_lablel = QtWidgets.QLabel(self.centralwidget)
        self.output_lang_lablel.setGeometry(QtCore.QRect(510, 110, 241, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.output_lang_lablel.setFont(font)
        self.output_lang_lablel.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.output_lang_lablel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.output_lang_lablel.setStyleSheet("color: #1967d2")
        self.output_lang_lablel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.output_lang_lablel.setObjectName("output_lang_lablel")
        self.switch_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.click_switch())
        self.switch_button.setGeometry(QtCore.QRect(355, 120, 71, 31))
        self.switch_button.setAutoFillBackground(False)
        self.switch_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("gui/images/two-way-arrow-2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.switch_button.setIcon(icon)
        self.switch_button.setIconSize(QtCore.QSize(20, 20))
        self.switch_button.setObjectName("switch_button")
        self.clear_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.click_clear())
        self.clear_button.setGeometry(QtCore.QRect(30, 420, 81, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.clear_button.setFont(font)
        self.clear_button.setObjectName("clear_button")
        self.translate_button = QtWidgets.QPushButton(self.centralwidget, clicked=lambda: self.click_translate())
        self.translate_button.setGeometry(QtCore.QRect(325, 460, 131, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.translate_button.setFont(font)
        self.translate_button.setObjectName("translate_button")
        self.app_name_label = QtWidgets.QLabel(self.centralwidget)
        self.app_name_label.setGeometry(QtCore.QRect(170, 20, 441, 51))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.app_name_label.setFont(font)
        self.app_name_label.setStyleSheet("color: #1967d2")
        self.app_name_label.setAlignment(QtCore.Qt.AlignCenter)
        self.app_name_label.setObjectName("app_name_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 781, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_shortcuts(self):
        # self.translate_shortcut = QtWidgets.QShortcut(
        #     QtGui.QKeySequence('Ctrl+D'),
        #     self.main_window
        # )
        # self.translate_shortcut.activated.connect(lambda: self.click_translate())

        # shortcut when not focus
        keybinder.init()
        keybinder.register_hotkey(self.main_window.winId(), 'Ctrl+D', self.translate_selected_text)
        self.win_event_filter = WinEventFilter(keybinder)
        self.event_dispatcher = QtCore.QAbstractEventDispatcher.instance()
        self.event_dispatcher.installNativeEventFilter(self.win_event_filter)


    def click_clear(self):
        self.input_box.setPlainText('')

    def click_translate(self):
        print('Clicked Translate Button')
        self.translate_button.setEnabled(False)
        # self.output_box.setPlainText('Translating.....')
        input_text = self.input_box.toPlainText().strip()
        print('input: ', input_text)
        if self.translate_direction == 0:
            output_text = self.envi_translator.translate_docs(input_text)
        else:
            output_text = self.vien_translator.translate_docs(input_text)
        self.output_box.setPlainText(output_text)
        print('output: ', output_text)
        self.translate_button.setEnabled(True)

    def click_switch(self):
        if self.translate_direction == 0:
            self.translate_direction = 1
            self.input_lang_label.setText('Vietnamese')
            self.output_lang_lablel.setText('English')
        else:
            self.translate_direction = 0
            self.input_lang_label.setText('English')
            self.output_lang_lablel.setText('Vietnamese')

    def translate_selected_text(self):
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.03)
        text = QtWidgets.QApplication.clipboard().text()
        print(text)
        self.centralwidget.activateWindow()
        self.input_box.setPlainText(text)
        self.click_translate()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Translator"))
        self.input_box.setPlaceholderText(_translate("MainWindow", "Input"))
        self.output_box.setPlaceholderText(_translate("MainWindow", "Translation"))
        self.input_lang_label.setText(_translate("MainWindow", "English" if self.translate_direction == 0 else "Vietnamese"))
        self.output_lang_lablel.setText(_translate("MainWindow", "Vietnamese" if self.translate_direction == 0 else "English"))
        self.clear_button.setText(_translate("MainWindow", "Clear"))
        self.translate_button.setText(_translate("MainWindow", "Translate"))
        self.app_name_label.setText(_translate("MainWindow", "ABC TRANSLATOR"))


if __name__ == '__main__':
    Ui_MainWindow()