import machine
from machine import Pin
import math
import utime
import _thread


#initialization
Handle_sensors_thread_inter=False
lock = _thread.allocate_lock()
sens =[]
DELAY=0.0001
#DELAY=5
STOP_MIN_DELAY=0.05
time=0
time_from_last_command=0
time_from_for=0
sin_rate=3700 # 500 working
machine.Pin("GP27", machine.Pin.OUT).on()

sens_pins=["GP16","GP2","GP3","GP4","GP5"]
start_button = machine.Pin("GP20", machine.Pin.IN, machine.Pin.PULL_DOWN)
start_led_pin = machine.Pin("GP0", machine.Pin.OUT)

for s in sens_pins:
      sens.append(machine.Pin(s,machine.Pin.IN, machine.Pin.PULL_UP))  
STOP=True 
c_state=0b111111 
#  buzzer pin
buzzer_pin = machine.Pin(22)
# Initialize PWM 
buzzer_pwm = machine.PWM(buzzer_pin)

def get_interrupt():
    global Handle_sensors_thread_inter
    return Handle_sensors_thread_inter

#buzzer func
def play_tone(frequency):
    buzzer_pwm.freq(frequency)
    buzzer_pwm.duty_u16(int(abs(32768/2)))  
    
    
def stop_tone() :   
    buzzer_pwm.duty_u16(0)


# Sensors thread
def Handle_sensors_thread():
    global lock
    global c_state
    global Handle_sensors_thread_inter
    print("Handle sens Started ")
    while not Handle_sensors_thread_inter:
        lock.acquire()
        l_c_state=0b10
        
        for s in sens:
            s_val=s.value()
            l_c_state+=int(s_val)
            l_c_state=((l_c_state)<<1)
        l_c_state=((l_c_state)>>1) 
        c_state=(l_c_state)
        lock.release()
        #utime.sleep(0.0001)
        #print("c_state",bin(c_state))
        if(c_state==0b100000):
            play_tone(250) 
        elif(c_state==0b111011):
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

def f0(t):
    return -100
def f1(t):
    return -abs(math.sin(3*t))*sin_rate
def f2(t):
    return -math.sin(6*t-7.854)*12000-11980
def f3(t):
    return math.cos(7*t)*100-150
def f4(t):
    x=30*t-5
    return -(math.exp(x)/(1+math.exp(x)))*5000+80

L_motor_t=False;
R_motor_t=False;


while True:    
    while not STOP:
        
    
        #print("gp: ",machine.Pin("GP5",machine.Pin.IN).value())
        stop_tone()
        print(f"time : {time} command_time : {time_from_last_command} frw time : {time_from_for} ")
        
        center_sens=c_state|0b110001
        side_sens=c_state |0b101110
        
            
        print("c_state",bin(c_state))
        print("center_sens",bin(center_sens))
        print("side_sens",bin(side_sens))
        #movement des
        
            
            #movement des
        #if(sens[0].value()==0) and (sens[4].value()==0) and check([0,0,0],c_state):
        if(c_state==0b100000):
            left_motor(0)
            right_motor(0)
            STOP=True
            print("Emer stop")
            L_motor_t=False
            R_motor_t=False
            time_from_last_command=0
        #elif(check([1, 1 ,1],c_state) and (time_from_last_command>STOP_MIN_DELAY)):
        elif((center_sens==0b111111 and (time_from_last_command>STOP_MIN_DELAY)) ):
            left_motor(0)
            right_motor(0)
            time_from_last_command=0
            print("stop")
        #elif (check([1,0,1],c_state)and (time_from_last_command>0)):
        elif ( center_sens==0b111011 and (time_from_last_command>0)) :
            L_motor_t=False
            R_motor_t=False
            right_motor(100)
            left_motor(100)
            time_from_for=0;
            time_from_last_command=0
            print("forw")
        #elif(sens[0].value()==0) and (time_from_last_command>0) :
        elif(side_sens==0b101111) and (time_from_last_command>0) :
            left_motor(85)
            right_motor(-85)
        #elif(sens[4].value()==0) and (time_from_last_command>0) :
        elif(side_sens==0b111110) and (time_from_last_command>0) :
            left_motor(-85)
            right_motor(85)
        #elif (check([0,0,1],c_state)and (time_from_last_command>0)):
        elif (center_sens==0b110011 and (time_from_last_command>0)) or R_motor_t:
            R_motor_t=True
            print("right")
            left_motor(100+f4(time_from_for))

            right_motor(f4(time_from_for))
            
            time_from_last_command=0
        #elif (check([0,1,1],c_state)and (time_from_last_command>0)):
        elif (center_sens==0b110111 and (time_from_last_command>0)) or R_motor_t:
            R_motor_t=True
            print("right")
            left_motor(100+f4(time_from_for))
            right_motor(f4(time_from_for))
            time_from_last_command=0
            
        #elif (check([1,1,0],c_state)and (time_from_last_command>0)):
        elif (center_sens==0b111101 and (time_from_last_command>0)) or L_motor_t:
            L_motor_t=True
            right_motor(100+f4(time_from_for))
            left_motor(f4(time_from_for))
            print("left")
            time_from_last_command=0
            
        #elif (check([1,0,0],c_state)and (time_from_last_command>0)):
        elif (center_sens==0b111001 and (time_from_last_command>0)) or L_motor_t:
            L_motor_t=False
            right_motor(100+f4(time_from_for))
            left_motor(f4(time_from_for))
            time_from_last_command=0
            print("left")
            
        #elif (sens[0].value()==1) and (sens[4].value()==1) and (time_from_last_command >STOP_MIN_DELAY):
        elif (side_sens==0b111111) and (time_from_last_command >STOP_MIN_DELAY):
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
    lock.acquire()
    if STOP:
        
        Handle_sensors_thread_inter=True
        start_led_pin.off()
        play_tone(671)
    else:
        
        Handle_sensors_thread_inter=False
        _thread.start_new_thread(Handle_sensors_thread, ())
        start_led_pin.on()
        utime.sleep(3)
    lock.release()
    
    utime.sleep(1)



