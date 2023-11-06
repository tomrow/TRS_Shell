import os
import thumby
import time
import gc
from math import ceil
import machine
import sys
beepfreq = 8000
beepdur = 40
trs_shell_ver = 05
thumby.display.setFPS(60)
wd = "/"
textArea = ["","","",""]
textAreaWindowBottom = len(textArea)-1
global inputSpace
inputSpace = True
def ConsoleSplitter(pendingOut):
    #12 characters per line for 5x7 font
    toAppend = []
    charDump = ""
    for i in range(len(pendingOut)):
        charDump = charDump + pendingOut[i]
        if charDump[-1] == "\n":
            toAppend.append(charDump[:-1])
            charDump = ""
        if len(charDump)==12:
            toAppend.append(charDump)
            charDump = ""
    if len(charDump)>0:
        toAppend.append(charDump)
        charDump = ""
    return(toAppend)

def ConsoleWriteLine(stringIn):
    toWrite = ConsoleSplitter(stringIn)
    for item in toWrite:
        textArea.append(item)
        textAreaWindowBottom = len(textArea)-1
        drawConsoleToScreen(textAreaWindowBottom)

def CullConsoleHistory(maxLines):
    global textArea
    while len(textArea) > maxLines:
        textArea.pop(0)
    return 0
        
def drawConsoleToScreen(winBottom):
    thumby.display.fill(0)
    screenLines = 5
    if inputSpace:
        #//draw Text Box
        screenLines = 4
    for line in range(screenLines):
        pos = 5 - screenLines
        thumby.display.drawText(textArea[winBottom-line],0,(screenLines-line-pos)*8,1)
    thumby.display.update()
    
    
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
        justPressed = []
        justPressed.append(thumby.buttonU.justPressed())
        justPressed.append(thumby.buttonD.justPressed())
        justPressed.append(thumby.buttonL.justPressed())
        justPressed.append(thumby.buttonR.justPressed())
        justPressed.append(thumby.buttonA.justPressed())
        justPressed.append(thumby.buttonB.justPressed())
        #print("editing tick")
        if True in justPressed:
            thumby.audio.play(beepfreq, beepdur)
        if thumby.buttonB.pressed():
            #print("b pushed")
            if thumby.buttonA.pressed():
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
        elif thumby.buttonA.pressed():
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
        viewPos = len(inputString) - 11 if len(inputString) > 11 else 0
        thumby.display.drawFilledRectangle(0, 4*8, 72, 8, 1)
        thumby.display.drawText(inputString[viewPos:],0,4*8,0)
        thumby.display.drawFilledRectangle(11*6, 4*8, 6, 8, 0)
        counter = (counter + 1) % 15
        if viewPos>0:
            thumby.display.drawFilledRectangle(0, 4*8, 6, 8, 1)
            thumby.display.drawText("<",0,4*8,0)
        if counter<7:
            thumby.display.drawText(chr(newCharacter),11*6, 4*8,1)
        thumby.display.update()
    return inputString

def prompt(inPrompt):
    ConsoleWriteLine(">"+inPrompt)
    try:
        exec(inPrompt+"\n")
    except Exception as errorInfo:
        try:
            if inPrompt in os.listdir(wd):
                handle = open(wd+"/"+inPrompt,"r")
                program = handle.read()
                handle.close()
                exec(program)
            elif inPrompt in os.listdir("/"):
                handle = open(inPrompt,"r")
                program = handle.read()
                handle.close()
                exec(program)
            else:
                ConsoleWriteLine(repr(errorInfo))
                print(errorInfo)
                print(sys.print_exception(errorInfo))
        except Exception as errorInfo2:
            ConsoleWriteLine(repr(errorInfo2))
            print(sys.print_exception(errorInfo2))
def ls():
    print('\n'.join(os.listdir(wd)))
    ConsoleWriteLine('\n'.join(os.listdir(wd)))


def cd(path):
    global wd
    if str(type(path)) == "<class 'str'>" and len(path)>0:
        if path[0]!="/":
            if os.stat(wd+"/"+path)[0] == 16384:
                wd = wd+"/"+path
            else:
                raise Exception("\nThis is not a directory")
        else:
            if os.stat(path)[0] == 16384:
                wd=path
            else:
                raise Exception("\nThis is not a directory")
    
        if wd[0]=="/" and wd[1]=="/":
            wd=wd[1:]
        pathList = wd.split("/")
        for i in range(len(pathList)):
            if pathList[i] == "..":
                pathList.pop(i-1)
                pathList.pop(i-1)
                wd = "/".join(pathList)
    pwd()
            
def pwd():
    ConsoleWriteLine(wd)

def ConfirmChoice(caption):
    thumby.display.fill(1)
    thumby.display.drawText(caption,0,0,0)
    thumby.display.drawText(" A:Yes B:No",0,4*8,0)
    while thumby.buttonA.pressed() or thumby.buttonB.pressed():
        time.sleep(0.3)
    while True:                 #confirm replace
        thumby.display.update()
        if thumby.buttonA.pressed():   
            drawConsoleToScreen(textAreaWindowBottom)
            return True
        if thumby.buttonB.pressed():
            drawConsoleToScreen(textAreaWindowBottom)
            return False
    #thumby.display.fill(1)
    #thumby.display.drawText("A:OK B:Cancl",0,4*8,0)
    #thumby.display.drawText("Shortcuts-",0,0,0)
    drawConsoleToScreen(textAreaWindowBottom)
    
def Quickies(editline):
    global inputSpace
    global beepfreq
    global beepdur
    u = 0
    d = 1
    l = 2
    r = 3
    a = 4
    b = 5
    global textAreaWindowBottom
    quickiesList = ["cd(\"", "pwd()", "ls()", "ipt(\"", "f=open(\"", "f.write(\"", "g=f.read()", "f.close()", "os.remove(\"","os.rmdir(\"","os.mkdir(\"", "gc.collect()", "CullConsoleHistory(4)", "beepfreq=", "beepdur=" ]
    quickiesIndex = 0
    thumby.display.fill(1)
    thumby.display.drawText("Shortcuts-",0,0,0)
    while thumby.buttonA.pressed() or thumby.buttonB.pressed():
        print("waiting")
        time.sleep(0.3)
    thumby.display.drawText("A:OK B:Cancl",0,4*8,0)
    selecting = True
    output = editline
    justPressed = []
    while selecting:
        justPressed = []
        justPressed.append(thumby.buttonU.justPressed())
        justPressed.append(thumby.buttonD.justPressed())
        justPressed.append(thumby.buttonL.justPressed())
        justPressed.append(thumby.buttonR.justPressed())
        justPressed.append(thumby.buttonA.justPressed())
        justPressed.append(thumby.buttonB.justPressed())
        #while thumby.buttonB.pressed():
        #    print("waiting")
        #    time.sleep(0.3)
        #print("select start")
        if True in justPressed:
            thumby.audio.play(beepfreq, beepdur)
        thumby.display.fill(1)
        thumby.display.drawText("A:OK B:Cancl",0,4*8,0)
        thumby.display.drawText("Shortcuts-",0,0,0)
        thumby.display.drawText(str(quickiesIndex),10*6,0,0)
        thumby.display.drawText(quickiesList[quickiesIndex],0,16,0)
        thumby.display.update()
        if justPressed[u]:
            print("up")
            quickiesIndex -=1
            if quickiesIndex<0:               #scroll up
                quickiesIndex = 0
        
        if justPressed[d]:
            print("down")
            quickiesIndex +=1                 #scroll down
            if quickiesIndex>len(quickiesList)-1:
                quickiesIndex = len(quickiesList)-1
        
        if thumby.buttonB.pressed():
            print("b")
            drawConsoleToScreen(textAreaWindowBottom)
            return editline                   #cancel

        if thumby.buttonA.pressed():
            print("a")
            if ConfirmChoice("Confirm?"):
                drawConsoleToScreen(textAreaWindowBottom)
                return quickiesList[quickiesIndex]
            while thumby.buttonA.pressed() or thumby.buttonB.pressed():
                time.sleep(0.3)

def doesExist(path):
    try:
        os.stat(path)
        return True
    except:
        return False

def isFolder(path):
    if doesExist(path):
        return os.stat(path)[0] == 16384
def getFreeSpaceBlocks():
    return os.statvfs("")[4]
def getTotalSpaceBlocks():
    return os.statvfs("")[2]
def getUsedSpaceBlocks():
    return os.statvfs("")[2] - os.statvfs("")[4]
def Blocks2Bytes(blocks):
    return os.statvfs("")[1] * blocks



    
def copyAbsolute(source,destination,delSource):
    if isFolder(source):
        raise Exception("\nSource is \na directory")
    if isFolder(destination):
        raise Exception("\nDestination\nis \na directory")
    fsinfo = os.stat(source) #generate enoent exception if source doesnt exist
    fsinfo = os.statvfs("")  #get block size
    copyChunkSize = fsinfo[0]
    sourceHandle = open(source,"rb")
    sourceHandle.read()#advance seek to the end of the file to find how big it is
    sourceFileSize = sourceHandle.tell()
    sourceHandle.seek(0) #seek back to start to begin copying
    sourceSizeBlocks = ceil(sourceFileSize / copyChunkSize)
    if doesExist(destination):
        if ConfirmChoice("Overwrite?") == False:
            raise Exception("\nDestination\nalready\nexists")
    destHandle = open(destination, "w")
    for i in range(sourceSizeBlocks):
        destHandle.write(sourceHandle.read(copyChunkSize))
        ConsoleWriteLine("Copying\n"+ str(i)+ " of "+ str(sourceSizeBlocks))
        if getFreeSpaceBlocks()<2:
            destHandle.close()
            os.remove(destination)
            raise Exception("\nMemory full")
    ConsoleWriteLine("Done copying")
    if delSource:
        os.remove(source)
        ConsoleWriteLine("Source file removed")
        
def copy(source,dest):
    if source[0] != "/":
        source = wd + "/" + source
    if dest[0] != "/":
        dest = wd + "/" + dest
    copyAbsolute(source,dest,False)
    
def move(source,dest):
    if source[0] != "/":
        source = wd + "/" + source
    if dest[0] != "/":
        dest = wd + "/" + dest
    copyAbsolute(source,dest,True)        
def r(path): ##relative path to absolute convert34
    if path[0] != "/":
        path = wd + "/" + path
    return path
def ipt(path):
    __import__(r(path))
    #saveConfigSetting("lastgame", r(path))
    #machine.mem32[0x4005800C]=1 # WDT scratch register '0'
    #machine.soft_reset()
    
def saveConfigSetting(key, setting):
    cfgfile = open("thumby.cfg", "r")
    cfg = cfgfile.read().split(',')
    cfgfile.close()
    for k in range(len(cfg)):
        if(cfg[k] == key):
            cfg[k+1] = setting
    cfgfile = open("thumby.cfg", "w")
    cfgfile.write(','.join(cfg))
    cfgfile.close()

def typeFile(path):
    _f = open(r(path))
    print(_f.read())
    _f.seek(0)
    ConsoleWriteLine(_f.read())
    _f.close()
    





#print("start")
#ConsoleWriteLine("1\n2\n3\n4\n5")
#ConsoleWriteLine("1234567\n test")
#exec("ConsoleWriteLine(\"exec()\\n test\")")
while True:
    prompt(getLineInput(""))
time.sleep(5)
