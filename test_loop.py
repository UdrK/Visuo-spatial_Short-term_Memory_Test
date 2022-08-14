import sys
import winsound
import threading
import random
import time
from datetime import datetime
import csv

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QObject, QRunnable, QThreadPool, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QMainWindow, QSizePolicy, QStackedWidget, QPushButton
from PyQt5.QtGui import QPalette, QColor, QFont

def async_win_notification():
    x = threading.Thread(target=win_notification)
    x.start()

def async_loss_notification():
    x = threading.Thread(target=loss_notification)
    x.start()

def win_notification():
    winsound.Beep(440, 150)  # frequency, duration
    winsound.Beep(660, 150)  # frequency, duration
    winsound.Beep(880, 150)  # frequency, duration

def loss_notification():
    winsound.Beep(300, 200)  # frequency, duration
    winsound.Beep(250, 400)  # frequency, duration

## TEST ----------------------------------------------------------------------------------------------------------------
class AisTest(QWidget):

    finished_test = pyqtSignal(int)
    first_click_sig = pyqtSignal()
    def __init__(self):
        super(AisTest, self).__init__()
        self.first_click = True
        self.button_list = []
        self.counter = 0
        self.test_setup()

    def test_setup(self):
        self.layout = QGridLayout()
        button_index = 0
        random.shuffle(NUMBER_POOL)
        for i in range(BUTTON_COLUMN_HEIGHT):
            for j in range(BUTTON_ROW_LENGTH):
                # keep a reference to the buttons
                button = HiderButton(button_index, NUMBER_POOL[button_index])
                button.mouse_press_signal.connect(self.button_clicked)
                self.button_list.append(button)
                # add to the layout
                self.layout.addWidget(button, i, j)
                button_index += 1
        self.setLayout(self.layout)

    def button_clicked(self, index):
        if self.first_click:
            self.first_click_sig.emit()

        if self.button_list[index].get_number() == self.counter + 1:
            self.button_list[index].set_background_color('black')
            self.button_list[index].set_label('')
            if self.first_click:
                self.first_click = False
                for button in self.button_list:
                    if button.get_number() != -1 and button.get_number() > self.counter + 1:
                        button.set_background_color('white')
            if self.counter + 1 == NUMBER:
                async_win_notification()
                self.finished_test.emit(self.counter + 1)
            self.counter += 1
        else:
            async_loss_notification()
            self.finished_test.emit(self.counter)

    def hide_all(self):
        for button in self.button_list:
            button.set_background_color('white')

class HiderButton(QWidget):
    mouse_press_signal = pyqtSignal(int)
    def __init__(self, index, number):
        self.label = ""
        self.index = index
        self.number = number
        super(HiderButton, self).__init__()
        self.setAutoFillBackground(True)
        self.setGeometry(0, 0, BUTTON_SIZE, BUTTON_SIZE)

        if self.number != -1:
            color = 'black'
            self.label = str(self.number)
        else:
            color = 'white'

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        self.label = QLabel(self.label)
        self.label.setStyleSheet("color : white;")
        self.label.setFont(QFont('Arial', int(BUTTON_SIZE/2)))
        self.label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

    def set_label(self, label):
        self.layout.itemAt(0).widget().setText(label)

    def set_background_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

    def get_number(self):
        return self.number

    def mousePressEvent(self, event):
        self.mouse_press_signal.emit(self.index)

# ----------------------------------------------------------------------------------------------------------------------
## MAIN GUI ------------------------------------------------------------------------------------------------------------

def get_test(type):
    if type == 'ai_1':
        return AisTest()
    if type == 'ayumu':
        return None


class StartButton(QPushButton):
    def __init__(self):
        super(StartButton, self).__init__()
        self.setSizePolicy(QSizePolicy().Fixed, QSizePolicy().Fixed)
        self.setFixedSize(100, 100)
        self.setStyleSheet("border: 3px solid white; border-radius: 50px;")


class ClockSignal(QObject):
    sig = pyqtSignal()


class Clock(QRunnable):
    def __init__(self):
        super(Clock, self).__init__()
        self.past_time = ClockSignal()

    def run(self):
        time.sleep(CLOCK_TIME)
        self.past_time.sig.emit()


class MainWindow(QMainWindow):
    def __init__(self, type, timed):
        self.timed = timed
        self.index = 1
        self.type = type
        super(MainWindow, self).__init__()
        self.widget_stack = QStackedWidget()
        self.button = StartButton()
        self.button.clicked.connect(lambda: self.circular_button())
        self.test = get_test(type)
        self.test.finished_test.connect(self.end_test)
        self.test.first_click_sig.connect(lambda : self.set_test_first_click_time())
        self.widget_stack.addWidget(self.button)
        self.widget_stack.addWidget(self.test)
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Visuo-Spatial Short-Term Memory Test")
        self.setGeometry(MAIN_WINDOW_X_POSITION, MAIN_WINDOW_Y_POSITION, MAIN_WINDOW_WIDTH, MAIN_WINDOW_HEIGHT)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor('black'))
        self.setPalette(palette)
        self.setCentralWidget(self.widget_stack)

    def circular_button(self):
        self.test_start_time = datetime.now()
        self.widget_stack.removeWidget(self.test)
        self.test = get_test(self.type)
        self.test.finished_test.connect(self.end_test)
        self.test.first_click_sig.connect(lambda: self.set_test_first_click_time())
        self.widget_stack.addWidget(self.test)
        self.widget_stack.setCurrentIndex(1)

        if self.timed:
            self.clock = Clock()
            self.clock.past_time.sig.connect(lambda: self.test.hide_all())
            self.pool = QThreadPool.globalInstance()
            self.pool.setMaxThreadCount(1)
            self.pool.start(self.clock)

    def end_test(self, number_reached):
        self.widget_stack.setCurrentIndex(0)
        with open('test_data.csv', 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Test_Type', 'Start_Time', 'First_Click', 'Number_Reached', 'Out_Of'])
            dict_to_write = {
                'Test_Type': TEST_TYPE,
                'Start_Time': self.test_start_time,
                'First_Click': CLOCK_TIME if TIMED else (self.test_fist_click_time - self.test_start_time).total_seconds(),
                'Number_Reached': number_reached,
                'Out_Of': NUMBER
            }
            writer.writerow(dict_to_write)

    def set_test_first_click_time(self):
        self.test_fist_click_time = datetime.now()


# ----------------------------------------------------------------------------------------------------------------------
## SCRIPT --------------------------------------------------------------------------------------------------------------

BUTTON_SIZE = 100
BUTTON_COLUMN_HEIGHT = 5
BUTTON_ROW_LENGTH = 8
MAIN_WINDOW_HEIGHT = BUTTON_COLUMN_HEIGHT * BUTTON_SIZE
MAIN_WINDOW_WIDTH = BUTTON_ROW_LENGTH * BUTTON_SIZE
MAIN_WINDOW_X_POSITION = int((1920 / 2) - (MAIN_WINDOW_WIDTH / 2))
MAIN_WINDOW_Y_POSITION = int((1080 / 2) - (MAIN_WINDOW_HEIGHT / 2))
NUMBER_POOL = [1,2,3,4,5,6,7,8,9]
NUMBER_POOL += [-1]*((BUTTON_COLUMN_HEIGHT*BUTTON_ROW_LENGTH)-len(NUMBER_POOL))
TIMED = False
TEST_TYPE = 'ai_1'
CLOCK_TIME = 3.5
NUMBER = 9

HELP_STRING = '-ti: TIMED flag: when using this flag, a set time period elapses before numerals are hidden\n' \
              "-ct='float_number' specify how many seconds you want to elapse before hiding the numerals, only applies if -ti is used\n" \
              "-n=number in [1-9] specify how many numerals to display on screen\n" \
              '-ty=opt allows for test type selection:\n\n' \
              '     -ty=ai_1    runs a test in which the grid is covered in white squares from the beginning\n' \
              'TODO:-ty=ai_2    runs a test in which the grid is covered in white squares once the test starts\n' \
              'TODO:-ty=ayumu   runs a test in which only squares corresponding to the numerals are shown\n'

print('Called script with arguments: {}'.format(sys.argv[1:]))
if sys.argv[1] == '-h':
    print(HELP_STRING)
else:
    for argument in sys.argv[1:]:
        if argument == '-ti':
            TIMED = True
        if '-ty' in argument:
            TEST_TYPE = str(argument[4:])
        if '-ct' in argument:
            CLOCK_TIME = float(argument[4:])
        if '-n' in argument:
            NUMBER = int(argument[3:])
            NUMBER_POOL = []
            for i in range(1,NUMBER+1):
                NUMBER_POOL.append(i)
            NUMBER_POOL += [-1] * ((BUTTON_COLUMN_HEIGHT * BUTTON_ROW_LENGTH) - len(NUMBER_POOL))

    app = QApplication(sys.argv)

    window = MainWindow(TEST_TYPE, TIMED)
    window.show()

    app.exec_()
