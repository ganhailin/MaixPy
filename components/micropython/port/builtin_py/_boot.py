import os, sys, time

sys.path.append('')
sys.path.append('.')

# chdir to "/sd" or "/flash"
devices = os.listdir("/")
if "sd" in devices:
    os.chdir("/sd")
    sys.path.append('/sd')
else:
    os.chdir("/flash")
sys.path.append('/flash')

print("[MaixPy] init end") # for IDE
for i in range(200):
    time.sleep_ms(1) # wait for key interrupt(for maixpy ide)
del i

# check IDE mode
ide_mode_conf = "/flash/ide_mode.conf"
ide = True
try:
    f = open(ide_mode_conf)
    f.close()
except Exception:
    ide = False

if ide:
    os.remove(ide_mode_conf)
    from machine import UART
    import lcd
    lcd.init(color=lcd.PINK)
    repl = UART.repl_uart()
    repl.init(1500000, 8, None, 1, read_buf_len=2048, ide=True, from_ide=False)
    sys.exit()    

import gc
import machine
from board import board_info
from fpioa_manager import fm
from pye_mp import pye
from Maix import FPIOA, GPIO


# detect boot.py
main_py = '''
from fpioa_manager import *
import os, Maix, lcd, image
from Maix import FPIOA, GPIO

test_pin=16
fm.fpioa.set_function(test_pin,FPIOA.GPIO7)
test_gpio=GPIO(GPIO.GPIO7,GPIO.PULL_UP)
lcd.init(color=(255,0,0))
lcd.draw_string(lcd.width()//2-68,lcd.height()//2-24, "Welcome to MaixPy", lcd.WHITE, lcd.RED)
v = sys.implementation.version
lcd.draw_string(lcd.width()//2-70,lcd.height()//2+12, 'V{}.{}.{} : maixpy.io'.format(v[0],v[1],v[2]), lcd.WHITE, lcd.RED)
del v
if test_gpio.value() == 0:
    print('PIN 16 pulled down, enter test mode')
    lcd.clear(lcd.PINK)
    lcd.draw_string(lcd.width()//2-68,lcd.height()//2-4, "Test Mode, wait ...", lcd.WHITE, lcd.PINK)
    import sensor
    import image
    sensor.reset()
    sensor.set_pixformat(sensor.RGB565)
    sensor.set_framesize(sensor.QVGA)
    sensor.run(1)
    lcd.freq(16000000)
    while True:
        img=sensor.snapshot()
        lcd.display(img)
'''

flash_ls = os.listdir()
if not "main.py" in flash_ls:
    f = open("main.py", "wb")
    f.write(main_py)
    f.close()
del main_py

flash_ls = os.listdir("/flash")
try:
    sd_ls = os.listdir("/sd")
except Exception:
    sd_ls = []
if "cover.boot.py" in sd_ls:
    code0 = ""
    if "boot.py" in flash_ls:
        with open("/flash/boot.py") as f:
            code0 = f.read()
    with open("/sd/cover.boot.py") as f:
        code=f.read()
    if code0 != code:
        with open("/flash/boot.py", "w") as f:
            f.write(code)
        import machine
        machine.reset()

if "cover.main.py" in sd_ls:
    code0 = ""
    if "main.py" in flash_ls:
        with open("/flash/main.py") as f:
            code0 = f.read()
    with open("/sd/cover.main.py") as f:
        code = f.read()
    if code0 != code:
        with open("/flash/main.py", "w") as f:
            f.write(code)
        import machine
        machine.reset()

try:
    del flash_ls
    del sd_ls
    del code0
    del code
except Exception:
    pass

banner = '''
 __  __              _____  __   __  _____   __     __
|  \/  |     /\     |_   _| \ \ / / |  __ \  \ \   / /
| \  / |    /  \      | |    \ V /  | |__) |  \ \_/ /
| |\/| |   / /\ \     | |     > <   |  ___/    \   /
| |  | |  / ____ \   _| |_   / . \  | |         | |
|_|  |_| /_/    \_\ |_____| /_/ \_\ |_|         |_|

Official Site : https://www.sipeed.com
Wiki          : https://maixpy.sipeed.com
'''
print(banner)
del banner

