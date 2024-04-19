import machine
from machine import Pin

import utime


def left_motor(speed):
    p1 =11
    p2 =10
    mt=[]
    mt.append(machine.PWM(machine.Pin(p1)))
    mt.append(machine.PWM(machine.Pin(p2)))
    mt[0].freq(1000)
    mt[1].freq(1000)
    if speed>0: 
        mt[0].duty_u16(int(abs(speed) * 65535 / 100))
        mt[1].duty_u16(0)
    elif speed<0:
        mt[1].duty_u16(int(abs(speed) * 65535 / 100))
        mt[0].duty_u16(0)
    else:
        mt[0].duty_u16(0)
        mt[1].duty_u16(0)
        
def right_motor(speed):
    p1 =8
    p2 =9
    mt=[]
    mt.append(machine.PWM(machine.Pin(p1)))
    mt.append(machine.PWM(machine.Pin(p2)))
    mt[0].freq(1000)
    mt[1].freq(1000)
    if speed>0: 
        mt[0].duty_u16(int(abs(speed) * 65535 / 100))
        mt[1].duty_u16(0)
    elif speed<0:
        mt[1].duty_u16(int(abs(speed) * 65535 / 100))
        mt[0].duty_u16(0)
    else:
        mt[0].duty_u16(0)
        mt[1].duty_u16(0)


left_motor(100)
right_motor(100)
utime.sleep(10)



for i in range(30,100):
    print(f"f f speed {i}")
    left_motor(i)
    right_motor(i)
    utime.sleep(0.2)


for i in range(30,100):
    print(f"f bspeed {i}")
    left_motor(i)
    right_motor(-i)
    utime.sleep(0.2)

for i in range(30,100):
    print(f"b fspeed {i}")
    left_motor(-i)
    right_motor(i)
    utime.sleep(0.2)

left_motor(0)
right_motor(0)
print("stop")

machine.Pin("GP28", machine.Pin.OUT).off()
test_move_button = machine.Pin("GP21", machine.Pin.IN, machine.Pin.PULL_DOWN)

while(test_move_button.value()==1):
    utime.sleep(0.5)
import line_follow


