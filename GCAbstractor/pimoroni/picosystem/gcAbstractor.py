#gamecontrol Abstractor 1
import machine

def keyU():
    return btnDown(23)
def keyD():
    return btnDown(20)
def keyL():
    return btnDown(22)
def keyR():
    return btnDown(21)
def keyA():
    return btnDown(18)
def keyB():
    return btnDown(19)
def keyX():
    return btnDown(17)
def keyY():
    return btnDown(16)

def btnDown(pinID):
    return machine.Pin(pinID).value() == 0
def __init__():
    tomrow = 1
    global pressedCheck
    pressedCheck = []
def drawCharacter(x,y,character,colorWord,fontHandle):
    pen(colorWord)
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
                pixel(x+j,y+i)
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
    flip()

def monoFill(color):
    pen(0,0,0)
    if color>0:
        pen(15,15,15)
    clear()
def monoRectF(x,y,w,h,color):
    pen(0,0,0)
    if color>0:
        pen(15,15,15)
    frect(x,y,w,h)
    
def monoColor(color):
    if color>0:
        return rgb(15,15,15)
    return rgb(0,0,0)
def ScreenWidth():
    return 120
def ScreenHeight():
    return 120
def FixedWidthFontSize():
    return (8, 8)
def originalText(string,x,y,colorWord):
    display.drawText(string, x, y, colorWord)
class AbstractAudio:
    def __init__(self, psv):
        self.psv = psv
        print("sound abstractor setting up")
    def play(self, beepfreq, beepdur, beepvol):
        self.psv.envelope(0,0,100,0)
        #this sets up adsr envelope, each value in the order of the acronym.
        #0ms atk,0ms dcy,100% stn, 0ms rel
        self.psv.bend(0,0)
        #this sets up pitch bend.
        #0hz amount, 0 milliseconds duration.
        self.psv.effects(0,0,0)
        #sets up fx. 
        #0 ms reverb, 0 ms noise, 0% distort
        
        self.psv.play(beepfreq, beepdur, beepvol)