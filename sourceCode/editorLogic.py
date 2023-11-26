import os
import shutil
import ctypes
from PyQt5.QtWidgets import QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageFilter, ImageEnhance

def add_image(setImage):
    file_path, _ = QFileDialog.getOpenFileName(None, "Select Image", "./Pictures", "Image Files (*.png *.jpg *.bmp *.gif)")
    shutil.copyfile(file_path, './.cache/temporary.jpg')
    
    if not file_path:
        return

    setImage(file_path)
    return file_path

def apply_filters(stockImage, setImage, brightness, black_and_white, blur, contrast, sharpen, smooth):
    stock = Image.open(stockImage)

    directory = './.cache/temporary.jpg'

    if black_and_white:
        stock = ImageEnhance.Color(stock).enhance(1 - (black_and_white / 100.0))
    
    if sharpen:
        stock = ImageEnhance.Sharpness(stock).enhance(sharpen)

    if contrast:
        stock = ImageEnhance.Contrast(stock).enhance(contrast / 100.0)

    if brightness!=100:
        stock = ImageEnhance.Brightness(stock).enhance(brightness/100)

    if blur:
        stock = stock.filter(ImageFilter.BLUR)

    if smooth:
        stock = stock.filter(ImageFilter.SMOOTH)

    stock.save(directory)
    setImage(directory)

    print(f"""
        stockImage={stockImage},
        black_and_white={black_and_white},
        contrast={contrast}, 
        sharpen={sharpen}, 
        smooth={smooth}
    """)

# file_path, _ = QFileDialog.getSaveFileName('./.cache/temporary.jpg', "Save Image", "./Pictures", "Image Files (*.png *.jpg *.bmp *.gif)")

def save_file():
    dialog = QFileDialog(None, "Save Image", "image", "Image Files (*.png *.jpg *.jpeg)")
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setAcceptMode(QFileDialog.AcceptSave)

    if dialog.exec_():
        path = dialog.selectedFiles()[0]

        name = os.path.basename(path)

        shutil.copyfile("./.cache/temporary.jpg", path)

        os.rename(path, os.path.join(os.path.dirname(path), name))
        ctypes.windll.user32.MessageBoxW(0, f"Saved in {path}", "Success", 0)
