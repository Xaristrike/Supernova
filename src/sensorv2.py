import machine
from machine import Pin

import utime

def check(arr1,arr2):
    equals=True
    for i in range(0,len(arr1)):
        if arr1[i]!=arr2[i]:
          equals=False
    return equals

def left_motor():
    p1 ="GP11"
    p2 ="GP10"
    mt = machine.Pin(p1,machine.Pin.OUT)
    mtg = machine.Pin(p2,machine.Pin.OUT)
    mt.on()
    mtg.off()
def right_motor():
    p1 ="GP8"
    p2 ="GP9"
    mt = machine.Pin(p1,machine.Pin.OUT)
    mtg = machine.Pin(p2,machine.Pin.OUT)
    mt.on()
    mtg.off()

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


sens_pins=["GP2","GP3","GP4"]




sens =[]

time=0


for s in sens_pins:
      sens.append(machine.Pin(s,machine.Pin.IN))  
#s1 = machine.Pin("GP2",machine.Pin.IN)

   
    
    
    
while True:
    c_state=[]
    stop_left_motor()
    stop_right_motor()
    print(f"time : {time}")
    for s in sens:
        c_state.append(s.value())
    print(c_state)
    
    if(check([1, 1 ,1],c_state)):
        print("stop")
    elif (check([1,0,1],c_state)):
        print("forw")
    elif (check([0,0,1],c_state)):
        print("right")
    elif (check([0,1,1],c_state)):
        print("right")
    elif (check([1,1,0],c_state)):
        print("left")
    elif (check([1,0,0],c_state)):
        print("left")
    else:
        print("stop")
    
    utime.sleep(0.1)
    time+=0.1
