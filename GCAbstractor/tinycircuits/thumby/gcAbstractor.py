#gamecontrol Abstractor 2, for TinyCircuits Thumby
import machine
from thumbyGraphics import display
from thumbyAudio import audio
display.setFont("/lib/font5x7.bin", 5, 7, 1)
originalText = display.drawText
def keyU():
    return btnDown(4)
def keyD():
    return btnDown(6)
def keyL():
    return btnDown(3)
def keyR():
    return btnDown(5)
def keyA():
    return btnDown(27)
def keyB():
    return btnDown(24)
def keyX():
    return False
def keyY():
    return False

def btnDown(pinID):
    return machine.Pin(pinID).value() == 0
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
                display.setPixel(x+j,y+i, colorWord)
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
    display.update()
    display.setFPS(30)

def monoFill(color):
    display.fill(color)
def monoRectF(x,y,w,h,color):
    display.drawFilledRectangle(x, y, w, h, color)
    
def monoColor(color):
    if color>0:
        return 1
    return 0
def ScreenWidth():
    return display.width
def ScreenHeight():
    return display.height
def FixedWidthFontSize():
    return (6, 8)
def originalText(string,x,y,colorWord):
    display.drawText(string, x, y, colorWord)
class AbstractAudio:
    def __init__(self, psv):
        self.psv = psv
        print("sound abstractor setting up")
    def play(self, beepfreq, beepdur, beepvol):
        #psv.envelope(0,0,100,0)
        #this sets up adsr envelope, each value in the order of the acronym.
        #0ms atk,0ms dcy,100% stn, 0ms rel
        #psv.bend(0,0)
        #this sets up pitch bend.
        #0hz amount, 0 milliseconds duration.
        #psv.effects(0,0,0)
        #sets up fx. 
        #0 ms reverb, 0 ms noise, 0% distort
        audio.setEnabled(beepvol)
        audio.play(beepfreq, beepdur)
        
