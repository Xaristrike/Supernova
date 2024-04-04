import machine
from machine import Pin

import utime

def check(arr1,arr2):
    equals=True
    for i in range(0,len(arr1)):
        if arr1[i]!=arr2[i]:
          equals=False
    return equals

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

machine.Pin("GP27", machine.Pin.OUT).on()

sens_pins=["GP1","GP2","GP3","GP4","GP5"]
reverce_button = machine.Pin("GP20", machine.Pin.IN, machine.Pin.PULL_DOWN)
reverce_led_pin = machine.Pin("GP0", machine.Pin.OUT)


sens =[]
REVERSE = False
DELAY=0.001
STOP_MIN_DELAY=0.3
time=0
time_from_last_command=0

for s in sens_pins:
      sens.append(machine.Pin(s,machine.Pin.IN))  
#s1 = machine.Pin("GP2",machine.Pin.IN)


   
    
    
    
while True:
    
    print(f"REVERSE : {REVERSE}")
    if(reverce_button.value()!=1) and (time_from_last_command>0.1):
        REVERSE=not REVERSE
        time_from_last_command=0
    if REVERSE:
        reverce_led_pin.on()
    else:
        reverce_led_pin.off()
    c_state=[]
    print(f"time : {time} command_time : {time_from_last_command}")
    
    
    for i in range(1,4,1):
        c_state.append(sens[i].value())
    print(c_state)
    
    #whene gp1 will work add it
    if(0 or sens[4].value()==0):
        stop_left_motor()
        stop_right_motor()
        print("Emer stop")
        time_from_last_command=0
    elif(check([1, 1 ,1],c_state) and (time_from_last_command>STOP_MIN_DELAY)):
        stop_left_motor()
        stop_right_motor()
        time_from_last_command=0
        print("stop")
    elif (check([1,0,1],c_state)and (time_from_last_command>0)):
        right_motor(REVERSE)
        left_motor(REVERSE)
        time_from_last_command=0
        print("forw")
    elif (check([0,0,1],c_state)and (time_from_last_command>0)):
        print("right")
        left_motor(REVERSE)
        stop_right_motor()
        time_from_last_command=0
    elif (check([0,1,1],c_state)and (time_from_last_command>0)):
        print("right")
        left_motor(REVERSE)
        stop_right_motor()
        time_from_last_command=0
    elif (check([1,1,0],c_state)and (time_from_last_command>0)):
        right_motor(REVERSE)
        stop_left_motor()
        print("left")
        time_from_last_command=0
    elif (check([1,0,0],c_state)and (time_from_last_command>0)):
        right_motor(REVERSE)
        stop_left_motor()
        time_from_last_command=0
        print("left")
    elif (time_from_last_command >STOP_MIN_DELAY):
        stop_left_motor()
        stop_right_motor()
        time_from_last_command=0
        print("stop")
    
    utime.sleep(DELAY)
    time+=DELAY
    time_from_last_command+=DELAY




