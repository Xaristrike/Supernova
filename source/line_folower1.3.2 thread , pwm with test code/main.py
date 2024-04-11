import machine
from machine import Pin
import utime


test_move_button = machine.Pin("GP21", machine.Pin.IN, machine.Pin.PULL_DOWN)
test_led = machine.Pin("GP28", machine.Pin.OUT)
machine.Pin("GP27", machine.Pin.OUT).off()

utime.sleep(3)

if(test_move_button.value()!=1):
    test_led.on()
    import movement_test
else:
    import line_follow