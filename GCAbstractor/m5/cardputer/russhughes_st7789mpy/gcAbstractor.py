#gamecontrol Abstractor 1
from machine import Pin, SPI
import keylib
import st7789
import font437
haveKeyLib = False
try:
    import keylib
except ImportError:
    haveKeyLib = False
else:
    haveKeyLib = True

screen = st7789.ST7789(
    SPI(2, baudrate=40000000, sck=Pin(36), mosi=Pin(35), miso=None),
    135,
    240,
    reset=Pin(33, Pin.OUT),
    cs=Pin(37, Pin.OUT),
    dc=Pin(34, Pin.OUT),
    backlight=Pin(38, Pin.OUT),
    rotation=1,
    color_order=st7789.RGB
    )
screen.init()
screen.on()
screen.fill(st7789.BLACK)
def keyU():
    scan = keylib.keyScan()
    return 12 in scan
def keyD():
    scan = keylib.keyScan()
    return 5 in scan
def keyL():
    scan = keylib.keyScan()
    return 33 in scan
def keyR():
    scan = keylib.keyScan()
    return 34 in scan 
def keyA():
    scan = keylib.keyScan()
    return 13 in scan
def keyB():
    scan = keylib.keyScan()
    return 49 in scan
def keyX():
    scan = keylib.keyScan()
    return 42 in scan
def keyY():
    return btnDown(0)

def btnDown(pinID):
    return Pin(pinID).value() == 0
def __init__():
    tomrow = 1
    global pressedCheck
    pressedCheck = []
def drawCharacter(x,y,character,colorWord,fontHandle):
    if (character<1 or character>254 or character==32):
        return
    fontHandle.seek(character * 8, 0)
    byteindex=0
    characterbits = fontHandle.read(8)
    for i in range(8):
        bit=128
        charRow = characterbits[i]
        for j in range(8):
            if charRow & bit > 0:
                screen.pixel(x+j,y+i, colorWord)
            bit=bit >> 1
def drawMonoSpaceText(textData, x, y, colorWord, fontHandle, fontWidth): #if you want unicode you'll have to do it yourself
    if type(textData) == type(""):
        textData = textData.encode('cp437')
    elif type(textData) != type(b""):
        textData = repr(textData).encode('cp437')
    if type(textData) != type(b""): #how is it not string still? i give up
        raise Exception("textData argument could not be converted to bytes")
    offset = 0
    for i in range(len(textData)):
        chara= int(textData[i])
        drawCharacter(x+offset,y, chara, colorWord, fontHandle)
        offset+=fontWidth
def buttonDownList():
    global pressedCheck
    pressedCheck = [keyU(),keyD(),keyL(),keyR(),keyA(),keyB(),keyX(),keyY()]
    return [keyU(),keyD(),keyL(),keyR(),keyA(),keyB(),keyX(),keyY()]
def justPressedList():
    global pressedCheck
    now = [keyU(),keyD(),keyL(),keyR(),keyA(),keyB(),keyX(),keyY()]
    jp = []
    for i in range(8):
        jp.append(now[i] and (not pressedCheck[i]))
    pressedCheck = [keyU(),keyD(),keyL(),keyR(),keyA(),keyB(),keyX(),keyY()]
    return jp
def updDisplay():
    print("flip dummy")

def monoFill(color):
    if color>0:
        screen.fill(65535)
    else:
        screen.fill(0)
def monoRectF(x,y,w,h,color):
    if color>0:
        screen.fill_rect(x, y, w, h, 65535)
    else:
        screen.fill_rect(x, y, w, h, 65535)
    
    
def monoColor(color):
    if color>0:
        return 65535
    return 0
def ScreenWidth():
    return 240
def ScreenHeight():
    return 135
def FixedWidthFontSize():
    return (8, 8)
def originalText(string,x,y,colorWord):
    screen.text(font437, string, x,y,colorWord, colorWord ^ 65535)
class AbstractAudio: ##TODO: i2s Audio driver
    def __init__(self, psv):
        self.psv = psv
        print("sound abstractor setting up")
    def play(self, beepfreq, beepdur, beepvol):
        #self.psv.envelope(0,0,100,0)
        #this sets up adsr envelope, each value in the order of the acronym.
        #0ms atk,0ms dcy,100% stn, 0ms rel
        #self.psv.bend(0,0)
        #this sets up pitch bend.
        #0hz amount, 0 milliseconds duration.
        #self.psv.effects(0,0,0)
        #sets up fx. 
        #0 ms reverb, 0 ms noise, 0% distort
        print("beep")
        #self.psv.play(beepfreq, beepdur, beepvol)

