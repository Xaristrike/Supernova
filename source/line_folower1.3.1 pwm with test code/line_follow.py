import machine
from machine import Pin
import math
import utime



sens =[]
REVERSE = False
DELAY=0.0001
STOP_MIN_DELAY=0.05
time=0
time_from_last_command=0
time_from_for=0
sin_rate=500


# Define the buzzer pin
buzzer_pin = machine.Pin(22)

# Initialize PWM on the buzzer pin
buzzer_pwm = machine.PWM(buzzer_pin)

def play_tone(frequency):
    buzzer_pwm.freq(frequency)
    buzzer_pwm.duty_u16(int(abs(32768/2)))  
    
    
def stop_tone() :   
    buzzer_pwm.duty_u16(0)




def check(arr1,arr2):
    equals=True
    for i in range(0,len(arr1)):
        if arr1[i]!=arr2[i]:
          equals=False
    return equals

def left_motor(speed):
    speed = max(min(speed, 100), -100)
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
    speed = max(min(speed, 100), -100)
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

machine.Pin("GP27", machine.Pin.OUT).on()

sens_pins=["GP1","GP2","GP3","GP4","GP5"]
start_button = machine.Pin("GP20", machine.Pin.IN, machine.Pin.PULL_DOWN)
start_led_pin = machine.Pin("GP0", machine.Pin.OUT)



for s in sens_pins:
      sens.append(machine.Pin(s,machine.Pin.IN))  
#s1 = machine.Pin("GP2",machine.Pin.IN)


STOP=True 
    
    
while True:    
    while not STOP:
        stop_tone()
        c_state=[]
        print(f"time : {time} command_time : {time_from_last_command} frw time : {time_from_for} ")
        
            
        
        for i in range(1,4,1):
            c_state.append(sens[i].value())
        print(c_state)
        
        #whene gp1 will work add it sens[0].value()==0)
        if(sens[0].value()==0) and (sens[4].value()==0) and check([0,0,0],c_state):
            left_motor(0)
            right_motor(0)
            STOP=True
            print("Emer stop")
            time_from_last_command=0
        elif(check([1, 1 ,1],c_state) and (time_from_last_command>STOP_MIN_DELAY)):
            left_motor(0)
            right_motor(0)
            time_from_last_command=0
            print("stop")
        elif (check([1,0,1],c_state)and (time_from_last_command>0)):
            right_motor(100)
            left_motor(100)
            time_from_for=0;
            time_from_last_command=0
            print("forw")
        elif (check([0,0,1],c_state)and (time_from_last_command>0)):
            print("right")
            left_motor(100)
            #insta
            #-abs(math.sin(3*time_from_for))*sin_rate
            #smooth
            #-math.sin(6*time_from_for-7.854)*12000-11900
            right_motor(-abs(math.sin(3*time_from_for))*sin_rate)
            
            time_from_last_command=0
        elif (check([0,1,1],c_state)and (time_from_last_command>0)):
            print("right")
            left_motor(100)
            right_motor(-abs(math.sin(3*time_from_for))*sin_rate)
            time_from_last_command=0
            
        elif (check([1,1,0],c_state)and (time_from_last_command>0)):
            right_motor(100)
            left_motor(-abs(math.sin(3*time_from_for))*sin_rate)
            print("left")
            time_from_last_command=0
            
        elif (check([1,0,0],c_state)and (time_from_last_command>0)):
            right_motor(100)
            left_motor(-abs(math.sin(3*time_from_for))*sin_rate)
            time_from_last_command=0
            print("left")
        elif(sens[0].value()==0) and (time_from_last_command>0) :
            left_motor(100)
            right_motor(-100)
        elif(sens[4].value()==0) and (time_from_last_command>0) :
            left_motor(-100)
            right_motor(100)
            
        elif (sens[0].value()==1) and (sens[4].value()==1) and (time_from_last_command >STOP_MIN_DELAY):
            left_motor(0)
            right_motor(0)
            time_from_last_command=0
            print("stop")
        
        utime.sleep(DELAY)
        time+=DELAY
        time_from_last_command+=DELAY
        if(time_from_for<0.5):
            time_from_for+=DELAY
    
    
    STOP= start_button.value()
    if STOP:
        start_led_pin.off()
        play_tone(671)
    else:
        start_led_pin.on()
        play_tone(150)
        utime.sleep(3)
    
    utime.sleep(1)


