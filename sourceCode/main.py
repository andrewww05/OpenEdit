import sys
import shutil
import os
import io
import ctypes
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QVBoxLayout, QPushButton, QLabel, QSizePolicy, QSlider, QGroupBox, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image
from view import styles

import editorLogic as script

_cacheDir = "./.cache"

def binary_file_to_image(binary_file_path, save_path):
    with open(binary_file_path, 'rb') as file:
        binary_data = file.read()

    image_stream = io.BytesIO(binary_data)
    image = Image.open(image_stream)
    
    image.save(save_path)

def init_check():
    if not os.path.exists(_cacheDir):
        os.makedirs(_cacheDir)
        FILE_ATTRIBUTE_HIDDEN = 0x02
        ret = ctypes.windll.kernel32.SetFileAttributesW(_cacheDir, FILE_ATTRIBUTE_HIDDEN)
    if not os.path.exists("./Pictures"):
        os.mkdir("./Pictures")
    if not os.path.exists("./Pictures/doge.jpg"):
        binary_file_to_image('./assets/doge.bin', './Pictures/doge.jpg')
        

init_check()

class OpenEdit(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('OpenEdit')
        self.setWindowIcon(QIcon('./assets/icon.png'))

        # Створення grid layout для головного вікна
        layout = QGridLayout()
        layout.setSpacing(20)
        self.setStyleSheet(styles.window_style)
        self.setLayout(layout)

        # Лівий блок (з grid layout для кнопок)
        left_block = QWidget()
        left_block.setStyleSheet(styles.actions_menu_style)
        left_block.setFixedWidth(200)
        left_block.setFixedHeight(850)
        left_layout = QGridLayout()
        left_layout.setSpacing(20)
        left_block.setLayout(left_layout)


        class Button:
            def __init__(self, char: str, func: callable, btnStyle: bool) -> None:
                self.char = char
                self.func = func
                self.btnStyle = btnStyle # 0 = grey, 1 = blue
            
            def draw(self, Y):
                button = QPushButton(self.char, left_block)
                button.clicked.connect(self.func)
                button.setStyleSheet(styles.button_style if self.btnStyle == 0 else styles.button_style_secondary)
                button.setCursor(Qt.PointingHandCursor)
                left_layout.addWidget(button, Y, 0)

        class Slider:
            def __init__(self, name: str, func: callable, defaultState: int = 0, minValue: int = 0, maxValue: int = 100):
                self.name = name
                self.func = func
                self.defaultState = defaultState
                self.minValue = minValue
                self.maxValue = maxValue

            def draw(self, Y):
                group_box = QGroupBox("", parent=left_block)
                group_box.setStyleSheet(styles.slider_groupbox)
                vbox_layout = QVBoxLayout(group_box)

                slider = QSlider(Qt.Horizontal)
                slider.setMinimum(self.minValue)
                slider.setMaximum(self.maxValue)
                slider.setValue(self.defaultState)
                slider.setStyleSheet(styles.slider_style)
                slider.valueChanged.connect(self.func)

                label = QLabel(self.name)
                label.setStyleSheet(styles.slider_label)
                label.setAlignment(Qt.AlignCenter)

                vbox_layout.addWidget(label)
                vbox_layout.addWidget(slider)

                left_layout.addWidget(group_box, Y, 0)

        class CheckBox:
            def __init__(self, name: str, func: callable):
                self.name = name
                self.func = func

            def draw(self, Y):
                group_box = QGroupBox("", parent=left_block)
                group_box.setStyleSheet(styles.slider_groupbox)
                vbox_layout = QVBoxLayout(group_box)
                checkBox = QCheckBox()
                checkBox.setStyleSheet(styles.checkbox_style)
                checkBox.stateChanged.connect(self.func)
                checkBox.setCursor(Qt.PointingHandCursor)
                checkBox.setTristate(False)

                label = QLabel(self.name)
                label.setStyleSheet(styles.checkbox_label)
                
                label.setAlignment(Qt.AlignCenter)
                

                vbox_layout.addWidget(label)
                vbox_layout.addWidget(checkBox)

                left_layout.addWidget(group_box, Y, 0)

        class FiltersBufferClass:
            def __init__(self, bNw: int, blur: int, contrast: int, shrp: int, smth: int) -> None:
                self._brightness = 100
                self._bNw = bNw
                self._contrast = contrast
                self._blur = blur
                self._shrp = shrp
                self._smth = smth
                self._imgPath = ''

            def _processImage(self) -> None:
                script.apply_filters(
                    stockImage=self._imgPath,
                    setImage=setImage,
                    brightness=self._brightness,
                    black_and_white=self._bNw, 
                    blur=self._blur, 
                    contrast=self._contrast,
                    sharpen=self._shrp,
                    smooth=self._smth
                )
            
            def setBrightness(self, v) -> None:
                self._brightness=v
                self._processImage()

            def setBnw(self, v) -> None:
                self._bNw=v
                self._processImage()

            def setBlur(self, v) -> None:
                self._blur=v
                self._processImage()

            def setContrast(self, v) -> None:
                self._contrast=v
                self._processImage()
            
            def setShrp(self, v) -> None:
                self._shrp=v
                self._processImage()

            def setSmth(self, v) -> None:
                self._smth=v
                self._processImage()

            def setImg(self, v) -> None:
                self._imgPath=v

            def resetFilters(self) -> None:
                self._bNw = 0
                self._contrast = 100
                self._blur = 0
                self._shrp = 0
                self._smth = 0
        
        # Ініціалізаційний блок
        filtersBuffer = FiltersBufferClass(0,0,0,0,0)
        def selectFileHandler():
            drawToolbar()
            filtersBuffer.resetFilters()
            filtersBuffer.setImg(script.add_image(setImage))

        def resetHandler():
            filtersBuffer.resetFilters()
            setImage(filtersBuffer._imgPath)
            drawToolbar()

        buttons = [
            Button(
                char='Select image',
                func=selectFileHandler,
                btnStyle=0
            ),
            Button(
                char='Save image',
                func=script.save_file,
                btnStyle=1
            ),
            Slider(
                name='Brightness',
                func=lambda e: filtersBuffer.setBrightness(e),
                defaultState=100,
                maxValue=200
            ),
            Slider(
                name='Contrast',
                func=lambda e: filtersBuffer.setContrast(e),
                defaultState=100,
                maxValue=200,
                minValue=1
            ),
            Slider(
                name='Black and white',
                func=lambda e: filtersBuffer.setBnw(e),
            ),
            Slider(
                name='Sharpen',
                func=lambda e: filtersBuffer.setShrp(e),
                minValue=0,
                maxValue=10
            ),
            CheckBox(
                name='Smooth',
                func=lambda e: filtersBuffer.setSmth(bool(e)),
            ),
            CheckBox(
                name='Blur',
                func=lambda e: filtersBuffer.setBlur(bool(e)),
            ),
            Button(
                char='Reset',
                func=resetHandler,
                btnStyle=0
            )
        ]

        def drawToolbar():
            i = 0
            for btn in buttons:
                btn.draw(i)
                i+=1

        drawToolbar()

        # Додаємо лівий блок у grid layout головного вікна
        layout.addWidget(left_block, 0, 0)

        # Правий блок
        right_block = QWidget()
        right_layout = QGridLayout()
        right_block.setLayout(right_layout)

        image_label = QLabel()
        
        def setImage(imgPath):
            # Завантаження зображення
            pixmap = QPixmap(imgPath)
            
            # Встановлення політики розміщення для QLabel
            image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            image_label.setAlignment(Qt.AlignCenter)

            # Отримання розмірів QLabel
            label_size = image_label.size()

            # Масштабування зображення до розмірів QLabel зі збереженням пропорцій
            scaled_pixmap = pixmap.scaled(label_size*1, Qt.KeepAspectRatio)

            # Встановлення масштабованого зображення у QLabel
            image_label.setPixmap(scaled_pixmap)

            # Додаємо QLabel зображення в правий блок
            right_layout.addWidget(image_label)

        # Ініціалізація
        setImage('./Pictures/doge.jpg')
        shutil.copyfile('./Pictures/doge.jpg', './.cache/temporary.jpg')

        layout.addWidget(right_block, 0, 1)

        # Налаштування вікна
        self.setGeometry(0, 0, 1600, 900)
        self.setWindowTitle('OpenEdit')
        self.show()
        filtersBuffer.setImg(os.path.abspath('./Pictures/doge.jpg'))
        setImage('./Pictures/doge.jpg')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = OpenEdit()
    ex.showMaximized()
    sys.exit(app.exec_())
