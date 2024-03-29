# Description
Python program that sends G-code instructions to a 3D printer to play Anagrams, a mobile game where players must use a set of six letters to form as many words as possible.
# How It Works
For the actual "robot", the extruder on a 3D printer was replaced with a stylus. To caputre the phone's screen, the Apowersoft iPhone recorded application was used, which opens a window that iPhone's could share screen to. Then, the `win32gui` library is used to take a photo of this window, thereby getting an image of the phone screen. Next, text on the phone screen is read using the optical character recognition (OCR) tool Python-tesseract to get the six letters. The program then iterates through a list of every English word and adds any words that can be formed from the six input letters into the output list. Finally, a function sends G-code instructions to the 3D printer via `pyserial` based on the output words and the position of each letter that forms each word until the time limit runs out. 
# Demo
https://github.com/abeinn/gamebot/assets/63220193/5ff2b265-27dd-46dc-8aa6-dd14bf4dde06

