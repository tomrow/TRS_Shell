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



def getLineInput(start):
    u = 0
    d = 1
    l = 2
    r = 3
    a = 4
    b = 5
    global inputSpace
    global textAreaWindowBottom
    global beepfreq
    global beepdur
    global beepvol
    global pressedCheck
    global rows
    global ScreenWidth
    prevInputSpace = inputSpace
    inputSpace = True
    textAreaWindowBottom = len(textArea)-1
    drawConsoleToScreen(textAreaWindowBottom)
    editing = True
    viewWidth = 11
    viewPos = 0
    newCharacter = 33
    inputString = start
    counter = 0
    justPressed = []
    while editing:
        justPressed = gcAbstractor.justPressedList()
        #print("editing tick")
        if True in justPressed:
            v.play(beepfreq, beepdur, beepvol)
        if gcAbstractor.keyY():
            inputString = Quickies(inputString)
        if gcAbstractor.keyX():
            editing = False 
        if gcAbstractor.keyB():
            #print("b pushed")
            if gcAbstractor.keyA():
                if justPressed[u]:
                    textAreaWindowBottom -= 1
                    if textAreaWindowBottom < 3:
                        textAreaWindowBottom = 3
                    drawConsoleToScreen(textAreaWindowBottom)
                    counter = 0
                if justPressed[d]:
                    textAreaWindowBottom += 1
                    if textAreaWindowBottom > len(textArea)-1:
                        textAreaWindowBottom = len(textArea)-1
                    drawConsoleToScreen(textAreaWindowBottom)
                    counter = 0
                if justPressed[l]:
                    inputString = Quickies(inputString)
            else:    
                if justPressed[r]:
                    editing = False                                        #Confirm
                if justPressed[l]:
                    if ConfirmChoice("Erase input?"):
                        viewWidth = 12                                         #DelAll
                        viewPos = 0
                        inputString = ""
                if justPressed[u]:
                    newCharacter += 32
                    counter = 0
                if justPressed[d]:
                    newCharacter -= 32
                    counter = 0
        elif gcAbstractor.keyA():
            if justPressed[r]:
                newCharacter = ord("(")
            if justPressed[u]:
                newCharacter += 10
                counter = 0
            if justPressed[d]:
                newCharacter -= 10
                counter = 0
            if justPressed[l]:
                newCharacter = 33
                counter = 0
        else:
            if justPressed[r]:
                if newCharacter<32:
                    newCharacter = 32
                if newCharacter>126:
                    newCharacter = 126
                inputString = inputString + chr(newCharacter)          #NextChar
            if justPressed[l]:
                inputString = inputString[:-1]
            if justPressed[u]:
                newCharacter += 1
                counter = 0
            if justPressed[d]:
                newCharacter -= 1
                counter = 0
        if newCharacter<32:
            newCharacter = 32
        if newCharacter>126:
            newCharacter = 126
        viewPos = len(inputString) - (columns-1) if len(inputString) > (columns-1) else 0
        gcAbstractor.monoRectF(0, rows*fh, gcAbstractor.ScreenWidth(), fh, 1)
        drawText(inputString[viewPos:],0,rows*fh,0,False)
        gcAbstractor.monoRectF(gcAbstractor.ScreenWidth()-fw, rows*fh, fw, fh, 0)
        counter = (counter + 1) % 15
        if viewPos>0:
            gcAbstractor.monoRectF(0, rows*fh, fw, fh, 1)
            drawText("<",0,rows*fh,0,False)
        if counter<7:
            drawText(chr(newCharacter),gcAbstractor.ScreenWidth()-fw, rows*fh,1,False)
        gcAbstractor.updDisplay()
    return inputString
