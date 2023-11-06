TRS_Shell

TRS_Shell is an interactive shell built for handheld devices running MicroPython. 
TRS-Shell requires at least 6 (or possibly 5) buttons and a bitmap display ( recommended minimum resolutiuon 72x40 ).
It was originally designed for use with the TinyCircuits Thumby keychain game handheld. You can run any Python command or script, with a few caveats:

print() and input() use the serial port instead of to the display. Use echo() and getLineInput() instead for display and buttons
No attempt is made to protect subroutines or functions, so if a script redefines one, the shell will break and require a reboot
TRS_Shell uses a not-insignificant amount of memory, so some larger scripts may not work.

To install, copy Shell2.py to your device with a file name and in a path your launch process expects to find. e.g. "/main.py" or "/Games/Shell2/Shell2.py"

Then, copy the GCAbstractor library that corresponds to your device to the root directory of your device. "/gcAbstractor.py"

Lastly, copy the font.bin file to the root directory. This cannot be done directly with a text editor like Thonny as it cannot open binary files. it is a 1bpp planar raw bitmap containing a code page 437 font in 8x8 pixel cells. 
You can copy the contents of font.asc as text to the Python serial shell to generate this file (make sure to use a low baud rate like 9600 to ensure you don't overload the device RAM and fail the transfer).

Planned features that may or may not happen:
Support for text-only LCDs
Cleanup of the getLineInput function
better method of redefining font size