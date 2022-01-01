import Printer
from PIL import Image, ImageGrab, ImageFilter
import win32gui, pytesseract, time
from anagrams import anagrams

XM = 1.25
YM = 1.25
AX_START, AY_START = 146, 90

printer = Printer.Printer("COM7")

#enumerate through windows and find screen recorder
toplist, winlist = [], []
def enum_cb(hwnd, results):
    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))
win32gui.EnumWindows(enum_cb, toplist)
ap = [(hwnd, title) for hwnd, title in winlist if 'Apowersoft' in title]
ap = ap[0]
hwnd = ap[0]
win32gui.SetForegroundWindow(hwnd)

def main():
    while True:
        i = input("INPUT:")
        if i == "start":
            x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
            bbox = max(0, round(x1*1.25)), max(0, round(y1*YM)), round(x2*XM), round(y2*YM)
            img = ImageGrab.grab(bbox)
            img = img.resize(tuple(2*x for x in img.size))
            img = img.convert('L')

            s = pytesseract.image_to_string(img)

            if "Combine letters to make words" in s:
                printer.move(AX_START, AY_START)
                time.sleep(1)
                printer.tap()
                time.sleep(1.5)
                anagrams(printer, hwnd)

main()