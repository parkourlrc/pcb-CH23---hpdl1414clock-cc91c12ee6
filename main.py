from machine import Pin
import network
import time
import requests
import re
import os

A0 = Pin(7, Pin.OUT)
A1 = Pin(8, Pin.OUT)
WR0 = Pin(9, Pin.OUT)
WR1 = Pin(10, Pin.OUT)
WR2 = Pin(11, Pin.OUT)
WR3 = Pin(12, Pin.OUT)
WR4 = Pin(13, Pin.OUT)
WR5 = Pin(14, Pin.OUT)
WR6 = Pin(15, Pin.OUT)
WR7 = Pin(16, Pin.OUT)
WR0.value(1)
WR1.value(1)
WR2.value(1)
WR3.value(1)
WR4.value(1)
WR5.value(1)
WR6.value(1)
WR7.value(1)

network.country('NL')

chartable = {
    " ":0b0100000,
    "!":0b0100001,
    '"':0b0100010,
    "#":0b0100011,
    "$":0b0100100,
    "%":0b0100101,
    "&":0b0100110,
    "'":0b0100111,
    "<":0b0101000,
    ">":0b0101001,
    "(":0b0101000,
    ")":0b0101001,
    "*":0b0101010,
    "+":0b0101011,
    ",":0b0101100,
    "-":0b0101101,
    ".":0b0101110,
    "/":0b0101111,
    "0":0b0110000,
    "1":0b0110001,
    "2":0b0110010,
    "3":0b0110011,
    "4":0b0110100,
    "5":0b0110101,
    "6":0b0110110,
    "7":0b0110111,
    "8":0b0111000,
    "9":0b0111001,
    ":":0b0111010,
    ";":0b0111011,
    "{":0b0111100,
    "=":0b0111101,
    "}":0b0111110,
    "?":0b0111111,
    "@":0b1000000,
    "a":0b1000001,
    "b":0b1000010,
    "c":0b1000011,
    "d":0b1000100,
    "e":0b1000101,
    "&euml;":0b1000101,
    "f":0b1000110,
    "g":0b1000111,
    "h":0b1001000,
    "i":0b1001001,
    "j":0b1001010,
    "k":0b1001011,
    "l":0b1001100,
    "m":0b1001101,
    "n":0b1001110,
    "o":0b1001111,
    "p":0b1010000,
    "q":0b1010001,
    "r":0b1010010,
    "s":0b1010011,
    "t":0b1010100,
    "u":0b1010101,
    "v":0b1010110,
    "w":0b1010111,
    "x":0b1011000,
    "y":0b1011001,
    "z":0b1011010,
    "A":0b1000001,
    "B":0b1000010,
    "C":0b1000011,
    "D":0b1000100,
    "E":0b1000101,
    "&EUML;":0b1000101,
    "F":0b1000110,
    "G":0b1000111,
    "H":0b1001000,
    "I":0b1001001,
    "J":0b1001010,
    "K":0b1001011,
    "L":0b1001100,
    "M":0b1001101,
    "N":0b1001110,
    "O":0b1001111,
    "P":0b1010000,
    "Q":0b1010001,
    "R":0b1010010,
    "S":0b1010011,
    "T":0b1010100,
    "U":0b1010101,
    "V":0b1010110,
    "W":0b1010111,
    "X":0b1011000,
    "Y":0b1011001,
    "Z":0b1011010,
    "[":0b1011011,
    "\\":0b1011100,
    "]":0b1011101,
    "^":0b1011110,
    "_":0b1011111,
    }

def letter(inputchar,position):
    lettercode=chartable[inputchar.lower()]
    display = position // 4
    position = position % 4
    position = 3 - position
    for i in range(0,7):
        value=(lettercode>>i)&1
        D=Pin(i, Pin.OUT)
        D.value(value)
    A0.value(position & 1)
    A1.value((position >> 1) & 1)
    screen=Pin((display + 9), Pin.OUT)
    screen.value(0)
    time.sleep_us(1)
    screen.value(1)
    time.sleep_us(1)

def printstring(text,startingposition):
    for i, char in enumerate(text):
        currentposition = startingposition+i
        if currentposition > 31:
            return
        letter(char, currentposition)

class TextScroller:
    def __init__(self, delay):
        self.delay = delay
        self.characters = ""
        self.max_position = 31

    def scroll_text(self,text):
        fill_ratio = len(self.characters) + 1
        scroll_position = (self.max_position - len(self.characters))
        lower_window = 0
        new_text = self.characters + text

        for i in range(0, len(text)):
            temp_text = new_text[lower_window:fill_ratio]
            printstring(temp_text, scroll_position)
            fill_ratio += 1
            if scroll_position == 0:
                lower_window += 1
            else:
                scroll_position -= 1
            time.sleep_us(self.delay)
        self.characters = text[-self.max_position:]

def clearscreen():
    printstring("                                ",0)
#    printstring(" *** NOS TELETEKST PAGINA 101:  ",0)

# 2: 'Link NoIP',
# 1: 'Link Join',
# 0: 'Link Down',
# -1: 'Link Fail',
# -2: 'NoNet',
# -3: 'BadAuth'

def readWebsiteData():
    response = requests.get(url='https://teletekst-data.nos.nl/json/101/')
    matches = []
    regex = r'<span class=\\"cyan \\">\ ([^<]+?)<'
    match = re.search(regex, response.content)
    max_news = 18
    if match is None:
        response.close()
        return "       something is wrong       "
    text = match.groups()[0]
    matches.append(text)
    while max_news > 0:
        next_pos = response.content.find(text)
        match = re.search(regex, response.content[next_pos+len(text):])
        if match:
            text = match.groups()[0]
# replace characters here, probably?
            print("match", text)
            for x in range(len(text)):
                try:
                    if chartable[chr(text[x])] > 0:
                        pass
                except:
                    print(f"Unsupported char found {chr(text[x])}")
                    z = chr(text[x]).encode('ascii')
                    text = text.replace(z,b' ')

            matches.append(text)
        else:
            break
        max_news -= 1
    response.close()
    return b' *** '.join(matches).decode() + 32 * ' '

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    wlan.active(True)
    if not wlan.isconnected():
        clearscreen()
        print('connecting to network...')
        printstring("      connecting to wifi...     ",0)
        wlan.connect('SSID', 'Password')
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ifconfig())

do_connect()
time.sleep(0.5)
time.sleep(1)
clearscreen()

while 1:

    teletekst = TextScroller(70000)
    teletekst.scroll_text(readWebsiteData())
    clearscreen()
