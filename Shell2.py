#TRS_Shell 2
import os
import time
import gc
import gcAbstractor
from math import ceil
from math import floor
import machine
import sys
import hashlib
from binascii import crc32
def doesExist(path):
    try:
        os.stat(path)
        return True
    except:
        return False
mColor = gcAbstractor.monoColor
beepfreq = 4040
beepdur = 40
beepvol = 100
trs_shell_ver = 05
rows = floor(gcAbstractor.ScreenHeight()/gcAbstractor.FixedWidthFontSize()[1])-1
print(rows)
columns = floor(gcAbstractor.ScreenWidth()/gcAbstractor.FixedWidthFontSize()[0])
fw=gcAbstractor.FixedWidthFontSize()[0]
fh=gcAbstractor.FixedWidthFontSize()[1]
#thumby.display.setFPS(60)
#wd = "/"
textArea = []
for i in range(rows):
    textArea.append("")
textAreaWindowBottom = len(textArea)-1
global inputSpace
inputSpace = True
fontOverRide = False
if doesExist("/lib/thumby.py"):
    fontOverRide = True
else:
    font = open('/font.bin', 'rb')
pressedCheck = []
psv = None
try:
    psv=Voice()
    psv.envelope(0,0,100,0)
    #this sets up adsr envelope, each value in the order of the acronym.
    #0ms atk,0ms dcy,100% stn, 0ms rel
    psv.bend(0,0)
    #this sets up pitch bend.
    #0hz amount, 0 milliseconds duration.
    psv.effects(0,0,0)
    #sets up fx. 
    #0 ms reverb, 0 ms noise, 0% distort
    v=gcAbstractor.AbstractAudio(psv)
except Exception as errorInfo:
    print("sound module is not picosystem")
    v=gcAbstractor.AbstractAudio(None)

def drawText(string,x,y,colorWord,proportional):
    global font
    global fontOverRide
    colorWord = gcAbstractor.monoColor(colorWord)
    if proportional or fontOverRide:
        gcAbstractor.originalText(string,x,y,colorWord)
    else:
        gcAbstractor.drawMonoSpaceText(string,x,y,colorWord,font,gcAbstractor.FixedWidthFontSize()[0])

def ConsoleSplitter(pendingOut):
    #12 characters per line for 5x7 font
    toAppend = []
    charDump = ''
    for i in range(len(pendingOut)):
        charDump = charDump + pendingOut[i]
        if charDump[-1] == "\n":
            toAppend.append(charDump[:-1])
            charDump = ""
        if len(charDump)==columns:
            toAppend.append(charDump)
            charDump = ""
    if len(charDump)>0:
        toAppend.append(charDump)
        charDump = ""
    return(toAppend)

def ConsoleWriteLine(stringIn):
    print(stringIn)
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
    gcAbstractor.monoFill(0)
    screenLines = rows
    #if inputSpace:
    #    #//draw text Box
    #    screenLines = rows - 1
    for line in range(screenLines):
        pos = rows - screenLines
        #drawText(textArea[winBottom-line],0,(screenLines-line-pos)*gcAbstractor.FixedWidthFontSize()[1],mColor(1),False)
        drawText(textArea[winBottom-line], 0, fh*(screenLines-(1+line)), mColor(1),False)
    gcAbstractor.updDisplay()
    
    
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

def prompt(inPrompt):
    ConsoleWriteLine(">"+inPrompt)
    try:
        exec(inPrompt+"\n")
    except Exception as errorInfo:
        try:
            if inPrompt in os.listdir():
                handle = open(inPrompt,"r")
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
    #print('\n'.join(os.listdir()))
    ConsoleWriteLine('\n'.join(os.listdir()))



def cd(path):
    os.chdir(path)
    pwd()
def pwd():
    ConsoleWriteLine(os.getcwd())

def ConfirmChoice(caption):
    gcAbstractor.monoFill(1)
    drawText(caption,0,0,0,False)
    drawText(" A:Yes B:No",0,rows*fh,0,False)
    while gcAbstractor.keyA() or gcAbstractor.keyB():
        time.sleep(0.3)
    while True:                 #confirm replace
        gcAbstractor.updDisplay()
        if gcAbstractor.keyA():   
            drawConsoleToScreen(textAreaWindowBottom)
            return True
        if gcAbstractor.keyB():
            drawConsoleToScreen(textAreaWindowBottom)
            return False
    drawConsoleToScreen(textAreaWindowBottom)
    




def isFolder(path):
    if doesExist(path):
        return os.stat(path)[0] == 16384
    else:
        return False
        

def getFreeSpaceBlocks():
    return os.statvfs("")[4]
def getTotalSpaceBlocks():
    return os.statvfs("")[2]
def getUsedSpaceBlocks():
    return os.statvfs("")[2] - os.statvfs("")[4]
def Blocks2Bytes(blocks):
    return os.statvfs("")[1] * blocks
def getBlockSize():
    return os.statvfs("")[0]


    
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
    destHandle = open(destination, "wb")
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
    copyAbsolute(source,dest,False)
    
def move(source,dest):
    copyAbsolute(source,dest,True)
    
def r(path): ##relative path to absolute converter
    if path[0] != "/":
        path = os.getcwd() + path
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
    
def echo(stringin):
    ConsoleWriteLine(stringin)
    print(stringin)
def sh_help():
    echo("""HELP
    (Variables)
    wd: working
    directory
    
    more to come later
    """)
def usbin():
    while True:
        prompt(input())

def TextMenu(editline, quickiesList, menuTitle):
    print(editline)
    global inputSpace
    global beepfreq
    global beepdur
    global beepvol
    global pressedCheck
    u = 0
    d = 1
    l = 2
    r = 3
    a = 4
    b = 5
    global textAreaWindowBottom
    quickiesIndex = 0
    gcAbstractor.monoFill(1)
    drawText(menuTitle,0,0,0,False)
    while gcAbstractor.keyA() or gcAbstractor.keyB():
        print("waiting")
        time.sleep(0.3)
    drawText("A:OK B:Cancel",0,rows*fh,0,False)
    selecting = True
    output = editline
    justPressed = []
    while selecting:
        justPressed = gcAbstractor.justPressedList()
        #while gcAbstractor.keyB():
        #    print("waiting")
        #    time.sleep(0.3)
        #print("select start")
        if True in justPressed:
            v.play(beepfreq, beepdur, beepvol)
        drawText("A:OK B:Cancel",0,rows*fh,0,False)
        drawText(menuTitle,0,0,0,False)
        drawText(str(quickiesIndex),gcAbstractor.ScreenWidth()-(fw*2),0,0,False)
        drawText(quickiesList[quickiesIndex],0,fw*2,0,False)
        time.sleep(0.02)
        gcAbstractor.updDisplay()
        if justPressed[u]:
            print("up")
            quickiesIndex -=1
            gcAbstractor.monoFill(1)
            if quickiesIndex<0:               #scroll up
                quickiesIndex = 0
        
        if justPressed[d]:
            print("down")
            quickiesIndex +=1                 #scroll down
            gcAbstractor.monoFill(1)
            if quickiesIndex>len(quickiesList)-1:
                quickiesIndex = len(quickiesList)-1
        
        if gcAbstractor.keyB():
            print("b")
            drawConsoleToScreen(textAreaWindowBottom)
            return editline                   #cancel

        if gcAbstractor.keyA():
            print("a")
            if ConfirmChoice("Confirm?"):
                drawConsoleToScreen(textAreaWindowBottom)
                return quickiesList[quickiesIndex]
            while gcAbstractor.keyA() or gcAbstractor.keyB():
                time.sleep(0.3)

def Quickies(editline):
    menus = { "!Quickies" :["cd(\"",
                           "pwd()",
                           "sh_help()",
                           "ls()",
                           "echo(\"",
                           "ipt(\"",
                           "type(\"",
                           "f=open(\"",
                           "f.write(\"",
                           "g=f.read()",
                           "f.close()",
                           "os.remove(\"",
                           "os.rename(\"",
                           "os.rmdir(\"",
                           "os.mkdir(\"",
                           "gc.collect()",
                           "CullConsoleHistory(rows)",
                           "beepfreq=",
                           "beepdur=",
                           "fontOverRide=" ],
              "os, etc.": ["un=os.uname()",
                           "ur=os.urandom(",
                           "wd=os.getcwd()",
                           "ild=os.ilistdir()",
                           "dir=os.listdir()",
                           "st=os.stat()",
                           "sv=os.statvfs(\""]
              }
    picked = TextMenu("quit", list(menus.keys()), "Category")
    if picked=="quit":
        return editline
    pickedSub = TextMenu("quit", menus[picked], picked)
    if pickedSub=="quit":
        return editline
    return pickedSub

def picoMgr():
    print("UUUUUTRS_Shell")
    ConsoleWriteLine("PC\nConnected")
    

def crcHexStr(dataIn):
    return hex(crc32(dataIn))[2:]
    
def crcHexFile(path):
    handle = open(path,"rb")
    handle.seek(0,2)
    size = handle.tell()-1
    handle.seek(0,0)
    crc = crc32(handle.read(1))
    while handle.tell() <= size:
        crc = crc32(handle.read(1), crc)
    handle.close()
    return hex(crc)[2:]
    
    
def loopWriteSer(handle): #file needs to be open()ed before this is called
    try:
        while True:
            decimal = int(input())
            if not decimal in range(0,255):
                raise ValueError()
            if getFreeSpaceBlocks() < 3:
                raise OSError(28)
            handle.write(decimal.to_bytes(1,"little")) #screw endianness, I'm using single bytes
            #I think I can just leave the subroutine like this, we'll see if anything goes wrong
    except Exception as e:
        print(repr(e))
        print("ERR")
        
def copyAbsoluteOverwrite(source,destination,delSource):
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
    #if doesExist(destination):
    #    if ConfirmChoice("Overwrite?") == False:
    #        raise Exception("\nDestination\nalready\nexists")
    destHandle = open(destination, "wb")
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

if doesExist("/trsauto.py"):
    prompt("/trsauto.py")

while True:
    prompt(getLineInput(""))
time.sleep(5)

