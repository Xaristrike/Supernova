import machine
from machine import Pin
import math
import utime
import _thread


#initialization
Handle_sensors_thread_inter=False
sens =[]
DELAY=0.0001
#DELAY=1
STOP_MIN_DELAY=0.05
time=0
time_from_last_command=0
time_from_for=0
sin_rate=800
machine.Pin("GP27", machine.Pin.OUT).on()

sens_pins=["GP16","GP2","GP3","GP4","GP5"]
start_button = machine.Pin("GP20", machine.Pin.IN, machine.Pin.PULL_DOWN)
start_led_pin = machine.Pin("GP0", machine.Pin.OUT)

for s in sens_pins:
      sens.append(machine.Pin(s,machine.Pin.IN))  
STOP=True 
c_state=[1,1,1]     
#  buzzer pin
buzzer_pin = machine.Pin(22)
# Initialize PWM 
buzzer_pwm = machine.PWM(buzzer_pin)

#buzzer func
def play_tone(frequency):
    buzzer_pwm.freq(frequency)
    buzzer_pwm.duty_u16(int(abs(32768/2)))  
    
    
def stop_tone() :   
    buzzer_pwm.duty_u16(0)

# Sensors thread
def Handle_sensors_thread():
    import utime
    global c_state
    print("Handle sens Started")
    while not Handle_sensors_thread_inter:
        l_c_state=[]
        for i in range(1,4,1):
            l_c_state.append(sens[i].value())
        c_state=l_c_state
        if(c_state[0]==0 and c_state[1]==0 and c_state[2]==0):
            play_tone(250) 
        elif(c_state[1]==0):
            play_tone(150)    
        else:
            stop_tone()
        #print("l c s: ",l_c_state)
        #utime.sleep(0.5)
    print("Handle sens interrupt")


#eval of sensor state
def check(arr1,arr2):
    equals=True
    for i in range(0,len(arr1)):
        if arr1[i]!=arr2[i]:
          equals=False
    return equals

#left motor movement  -100<speed<100
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

#right motor movement -100<speed<100
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


    
#main loop    
while True:    
    while not STOP:
        stop_tone()
        print(f"time : {time} command_time : {time_from_last_command} frw time : {time_from_for} ")
        
            
        print("c_state",c_state)
        
        
        #movement des
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
        
        #timers and shit 
        utime.sleep(DELAY)
        time+=DELAY
        time_from_last_command+=DELAY
        if(time_from_for<0.5):
            time_from_for+=DELAY
    
    #Stop and interrupt handle
    STOP= start_button.value()
    if STOP:
        Handle_sensors_thread_inter=True
        start_led_pin.off()
        play_tone(671)
    else:
        Handle_sensors_thread_inter=False
        _thread.start_new_thread(Handle_sensors_thread, ())
        start_led_pin.on()
        utime.sleep(3)
    
    utime.sleep(1)


