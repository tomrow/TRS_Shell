from machine import Pin
def keyScan():
    muxPins=[8,9,11]
    colPins=[13,15,3,4,5,6,7]
    currkey = 0
    keys=[]
    for i in range(8):
        for j in range(3):
            bit = 1 << j
            #print(j,bit)
            Pin(muxPins[j], Pin.OUT).value((bit & i) > 0)
        for k in range(7):
            if Pin(colPins[k], Pin.IN, Pin.PULL_UP).value() == False:
                #print(i,k, Pin(colPins[k], Pin.IN, Pin.PULL_UP).value())
                keys.append(i*7+k)
        #input()
    return keys
def keyScanToText(keys):
    output = ""
    try:
        ascii = "\0zcbm. \0sfhk;\nqetuo[\\13579-\x08\0\0xvn,/\0adgjl'\x09wryip]`24680="
        if 7 in keys:
            ascii = "\0ZCBM> \0SFHK:\nQETUO{|!#%&(_\x7f\0\0XVN<?\0ADGJL\"\x09WRYIP}~@$^*)+"
        #if 29 in keys:
        #    ascii = ascii[0:21]+"£"+ascii[23:50]+"€"+ ascii[52:55]
        #    ascii = ascii[0:14]+"é"+ascii[16]+"úó" + ascii[19:35] + "á" + ascii[37:45] + "í" + ascii[47:55]
        #    if 7 in keys:
        #        ascii = ascii[0:14]+"É"+ascii[16]+"ÚÓ" + ascii[19:35] + "Á" + ascii[37:45] + "Í" + ascii[47:55]
            
            #ascii = ascii[0:22] + "£" + ascii[24:50] + "€" + ascii[52:55]
        if (0 in keys) or (28 in keys) or (35 in keys):
            output = ""
        for i in keys:
            if (i!=0) and (i!=7) and (i!=28) and (i!=29) and (i!=35):
                output = ascii[i]
                break
        if 35 in keys:
            output = ansiCodes(keys)
    except IndexError:
        output = ""
    return output
def ansiCodes(keys):
    if 49 in keys:
        return "\x1b" #esc
    if 33 in keys:
        return "\x1b[D" #left
    if 34 in keys:
        return "\x1b[C" #right
    if 5 in keys:
        return "\x1b[B" #down
    if 12 in keys:
        return "\x1b[A" #up
    if 27 in keys:
        return "\x7f" #del
    return ""
    
