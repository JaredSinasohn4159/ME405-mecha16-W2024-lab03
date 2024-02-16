"""!
@file main.py
This file produces a step response on the nucleo micro processor through the pin C0
and collects data from the pin B0 about the voltage of an RC circuit.  That data is
then printed in the console.
"""

import micropython
import pyb
import utime
import Serial
from Lab3.encoder_reader import Encoder
from Lab3.motor_driver import MotorDriver
from Lab3.controller import CLController

def motor_setup():
    # create pin to power motor
    en_pin =  pyb.Pin(pyb.Pin.board.PA10, mode = pyb.Pin.OPEN_DRAIN, pull = pyb.Pin.PULL_UP, value=1)
    
    # create first pwm pin
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    
    # create first pwm pin
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    
    # create timer for pwm
    timer = pyb.Timer(3, freq=25000) #setting frequency for motor
    
    # create and return motor object
    return MotorDriver(en_pin,in1pin,in2pin,timer) #call to the motor class you just made!
        
def encoder_setup():
    # create the pin object to read encoder channel A
    pin1 = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    
    # create the pin object to read encoder channel B
    pin2 = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    
    # create the timer object.  For C6 and C7 use timer 8,
    # set the prescaler to zero and the period to the max 16bit number
    timer = pyb.Timer(8, prescaler = 0, period = 65535)
    
    # create the encoder object
    encoder = Encoder(pin1, pin2, timer)
    encoder.zero()
    return encoder


# interupt callback fucntion    

def step_response (controller, motor, encoder, frequency, collection_time):
    """!
    This function initiates a step output voltage in pin C0 and enables timer
    interrupts to allow for the accurate collection of RC voltage data through
    pin B0.  The function then generates a queue of time data based on the times
    the voltage data was collected and prints the time and voltage data to the
    console.
    @param   t_channel The timer channel to use for interrupts
    @param   frequency How often the program should collect data in Hz
    @param   collection_time How long the program should collect data for
    """
    
    
    # We want to run this program until the keyboard interrupts the program so
    # that we can stop the program if necessary
    try:
        while controller.get_curr_time() < (collection_time*1000):
            encoder_reading = encoder.read()
            encoder_angle = encoder_reading/16/256/4*360
            eff = con.run(encoder_angle)
            motor.set_duty_cycle(eff)
            utime.sleep_ms(int(1/frequency*1000))
        times = controller.get_t_list()
        positions = controller.get_pos_list()
        for i in range(len(times)):
            print(f"{times[i]},{positions[i]}")
            
    except KeyboardInterrupt:  # keyboard interrupt to exit program (ctrl+c)
            motor.set_duty_cycle(0)
            print("program ended")
            pass

if __name__ == "__main__":
    kp = input("Enter a Kp value: ")
    while True:
        try:
            kp = float(kp)
            break
        except:
            kp = input("Enter a Kp value: ")
    motor = motor_setup()
    motor.set_duty_cycle(0)
    encoder = encoder_setup()
    
    # create controller object
    con = CLController(kp, 0, 0, 180)
    step_response(con, motor, encoder, 100, 1.5)


