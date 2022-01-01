import Printer
from PIL import Image, ImageGrab, ImageFilter
import pytesseract, cv2, win32gui, re
import numpy as np
from nltk.corpus import words
import time

XM = 1.25
YM = 1.25
AX_START, AY_START = 146, 90

XM = 1.25
YM = 1.25
LETTER_CROP = 0, 750, 400, 800
PY = 67
PX1, PX2, PX3, PX4, PX5, PX6 = 119, 129, 139.5, 150.5, 161.5, 172
ENTER_X, ENTER_Y = 145, 98

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

printer = Printer.Printer("COM3")

#enumerate through windows and find screen recorder
toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)
ap = [(hwnd, title) for hwnd, title in winlist if 'Apowersoft' in title]
ap = ap[0]
hwnd = ap[0]
win32gui.SetForegroundWindow(hwnd)

x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
bbox = max(0, round(x1*1.25)), max(0, round(y1*YM)), round(x2*XM), round(y2*YM)
img = ImageGrab.grab(bbox)
img = img.resize(tuple(2*x for x in img.size))
img = img.convert('L')

s = pytesseract.image_to_string(img)

#screenshot screen window
x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
bbox = max(0, round(x1*1.25)), max(0, round(y1*YM)), round(x2*XM), round(y2*YM)
img = ImageGrab.grab(bbox)

#crop and filter image
img = img.crop(LETTER_CROP)
img = img.resize(tuple(2*x for x in img.size))
img = img.convert('L')
(thresh, BWimg) = cv2.threshold(np.array(img), 60, 255, cv2.THRESH_BINARY )
img = Image.fromarray(BWimg)

#image to string
s = pytesseract.image_to_string(img)
print(s)
letters = []
for char in s:
    if len(letters) >= 6:
        break
    if char.isalpha() and char.isupper() and letters.count(char) < 2:
        letters.append(char.lower())
    elif char == '1' or char == '|':
        letters.append("i")
    elif char == '§':
        letters.append("s")
print(letters)