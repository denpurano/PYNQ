"""Test module for led8.py"""


__author__      = "Giuseppe Natale, Yun Rock Qu"
__copyright__   = "Copyright 2015, Xilinx"
__maintainer__  = "Giuseppe Natale"
__email__       = "giuseppe.natale@xilinx.com"


import pytest
import sys, select, termios
from time import sleep
from pyxi.pmods._iop import _flush_iops
from pyxi.pmods.led8 import LED8
from pyxi.test.util import user_answer_yes

flag = user_answer_yes("\nLED8 attached to the board?")
if flag:
    global led_id
    led_id = int(input("Type in the PMOD ID of the LED8 (1 ~ 4): "))

@pytest.mark.run(order=17)  
@pytest.mark.skipif(not flag, reason="need LED8 attached in order to run") 
def test_led0():
    """TestCase for the PMOD LED class.
    Instantiates a LED object on index 0 and performs some actions 
    on it, requesting user confirmation.""" 
    led = LED8(led_id,0)    
    led.on()
    assert led.read() is 1 
    assert user_answer_yes("\nPMOD LED 0 on?")
    led.off()
    assert led.read() is 0 
    assert user_answer_yes("PMOD LED 0 off?")
    led.toggle()
    assert led.read() is 1 
    assert user_answer_yes("PMOD LED 0 on again?")
    led.write(0)
    assert led.read() is 0 
    assert user_answer_yes("PMOD LED 0 off again?")
    led.write(1)
    assert led.read() is 1 
    led.off()

@pytest.mark.run(order=18) 
@pytest.mark.skipif(not flag, reason="need LED8 attached in order to run") 
def test_shift_leds():
    """Instantiates 8 LED objects and shifts from right to left.""" 
    DelaySec1 = 0.1
    leds = [LED8(led_id,index) for index in range(0, 8)] 
        
    for led in leds:
        led.off()
    
    print("\nShifting PMOD LEDs. Press enter to stop shifting...", end="")
    while True:
        for led in leds:
            led.on()
            sleep(DelaySec1)
        for led in leds:
            led.off()
            sleep(DelaySec1)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            break

    assert user_answer_yes("PMOD LEDs were shifting from LD0 to LD7?")

@pytest.mark.run(order=19) 
@pytest.mark.skipif(not flag, reason="need LED8 attached in order to run")  
def test_toggle_leds():
    """Instantiates 8 LED objects and toggles them.""" 
    DelaySec2 = 0.2
    leds = [LED8(led_id,index) for index in range(0, 8)] 
        
    for led in leds:
        led.off()
    leds[0].on()
    leds[2].on()
    leds[4].on()
    leds[6].on()
    
    print("\nToggling PMOD LEDs. Press enter to stop toggling...", end="")
    while True:
        for led in leds:
            led.toggle()
        sleep(DelaySec2)
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            termios.tcflush(sys.stdin, termios.TCIOFLUSH)
            break
            
    for led in leds:
        led.off()
    assert user_answer_yes("PMOD LEDs were toggling?")
    _flush_iops()