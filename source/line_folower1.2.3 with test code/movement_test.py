import machine
from machine import Pin

import utime


def left_motor(rev=False):
    p1 ="GP11"
    p2 ="GP10"
    mt=[]
    if not rev:
        mt.append(machine.Pin(p1,machine.Pin.OUT))
        mt.append(machine.Pin(p2,machine.Pin.OUT))
    else:
        mt.append(machine.Pin(p2,machine.Pin.OUT))
        mt.append(machine.Pin(p1,machine.Pin.OUT))
    mt[0].on()
    mt[1].off()
def right_motor(rev=False):
    p1 ="GP8"
    p2 ="GP9"
    mt=[]
    if not rev:
        mt.append(machine.Pin(p1,machine.Pin.OUT))
        mt.append(machine.Pin(p2,machine.Pin.OUT))
    else:
        mt.append(machine.Pin(p2,machine.Pin.OUT))
        mt.append(machine.Pin(p1,machine.Pin.OUT))
    mt[0].on()
    mt[1].off()

def stop_left_motor():
    p1 ="GP11"
    p2 ="GP10"
    mt = machine.Pin(p1,machine.Pin.OUT)
    mtg = machine.Pin(p2,machine.Pin.OUT)
    mt.off()
    mtg.off()
def stop_right_motor():
    p1 ="GP9"
    p2 ="GP8"
    mt = machine.Pin(p1,machine.Pin.OUT)
    mtg = machine.Pin(p2,machine.Pin.OUT)
    mt.off()
    mtg.off()

stop_left_motor()
stop_right_motor()
left_motor()
right_motor()
print("f f")

utime.sleep(1)
stop_left_motor()
stop_right_motor()
print("s s")

utime.sleep(1)
left_motor(True)
right_motor(True)
print("b b")

utime.sleep(1)
stop_left_motor()
stop_right_motor()

utime.sleep(1)
left_motor()
right_motor(True)
print("f b")


utime.sleep(1)
stop_left_motor()
stop_right_motor()

utime.sleep(1)
left_motor(True)
right_motor()
print("b f")


utime.sleep(1)
stop_left_motor()
stop_right_motor()

utime.sleep(1)
right_motor()
print("s f")


utime.sleep(1)
stop_left_motor()
stop_right_motor()

utime.sleep(1)
left_motor()
print("f s")

utime.sleep(1)
stop_left_motor()
stop_right_motor()
print("end")

machine.Pin("GP28", machine.Pin.OUT).off()
test_move_button = machine.Pin("GP21", machine.Pin.IN, machine.Pin.PULL_DOWN)

while(test_move_button.value()==1):
    utime.sleep(0.5)
import line_follow


