from PIL import Image, ImageGrab, ImageFilter
import pytesseract, cv2, win32gui, re
import numpy as np
from nltk.corpus import words
import time

#Constants
XM = 1.25
YM = 1.25
LETTER_CROP = 0, 750, 408, 810
PY = 67
PX1, PX2, PX3, PX4, PX5, PX6 = 119, 129, 139.5, 150.5, 161.5, 172
ENTER_X, ENTER_Y = 145, 98

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#Create list of all words 3 letters or more
WORD_LIST = []
for word in words.words():
    if len(word) >= 3 and len(word) <= 6 and word.islower() and word not in WORD_LIST:
        WORD_LIST.append(word)

def anagrams(printer, hwnd):

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

    #get list of words    
    words = word_search(letters)
    words = sorted(words, key=len, reverse=True)
    print(words)

    execute(printer, words, letters)



#anagram solver
def word_search(letters):
    output = []
    for word in WORD_LIST:
        w = word
        c = 0
        for letter in letters:
            if letter in w:
                c += 1
                w = re.sub(letter, "", w, 1)
        if len(word) == c:
            output.append(word)

    return output

#move printer
def execute(printer, words, letters):
    l_test = []
    l = []
    for letter in letters:
        if letter in l_test:
            l.append(letter + str(l_test.count(letter)))
        else:
            l.append(letter + '0')
        l_test.append(letter)

    positions = {
        l[0]: PX1,
        l[1]: PX2, 
        l[2]: PX3,
        l[3]: PX4,
        l[4]: PX5,
        l[5]: PX6
    }

    printer.up()
    print(len(words))
    lc = 0
    for i in range(len(words)):
        word = words[i]
        l_test = []
        for letter in word:
            PX = 0
            if letter in l_test:
                PX = positions[letter + str(l_test.count(letter))]
            else:
                PX = positions[letter + '0']
            l_test.append(letter)
            printer.move(PX, PY)
            time.sleep(0.55)
            printer.tap()
            time.sleep(0.55)
            lc += 1
        printer.move(ENTER_X, ENTER_Y)
        time.sleep(0.6)
        printer.tap() 
        time.sleep(0.6)
        if lc >= 40:
            break