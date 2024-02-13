"""!
@file motor_driver.py
This file contains the class implementation for powering the ametek pittman motors via the ME 405 microcontroller.
This file also contains testing code to test if motor can be spun, and we can set the duty cycle to various levels by stopping
and restarting the code.

@author Jared Sinasohn, Sydney Ulvick, Sean Nakashimo
@date 15-Feb-2024
"""
import micropython
import pyb
import utime
class MotorDriver:
    """! 
    This class implements a motor driver for an ME405 kit. This class can set
    the motor duty cycle from percentages from -100 to 100
    """

    def __init__ (self, en_pin, in1pin, in2pin, timer):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param en_pin (There will be several parameters)
        """
        self.en_pin = en_pin
        self.in1pin = in1pin
        self.in2pin = in2pin
        self.timer = timer
        self.en_pin.high()
        self.ch1 = self.timer.channel(1, pyb.Timer.PWM, pin=self.in1pin)
        self.ch2 = self.timer.channel(2, pyb.Timer.PWM, pin=self.in2pin)
        self.ch1.pulse_width_percent(0)
        self.ch2.pulse_width_percent(0)
        print ("Creating a motor driver")

    def set_duty_cycle (self, level):
        """!
        This method sets the duty cycle to be sent
        to the motor to the given level. Positive values
        cause torque in one direction, negative values
        in the opposite direction.
        @param level A signed integer holding the duty
               cycle of the voltage sent to the motor 
        """
        print (f"Setting duty cycle to {level}")
        if level < 0:
            self.en_pin.high()
            self.ch1.pulse_width_percent(0)
            if level >= -100:
                self.ch2.pulse_width_percent(abs(level))
            else:
                self.ch2.pulse_width_percent(100)
        elif level > 0:
            self.en_pin.high()
            self.ch2.pulse_width_percent(0)
            if level <= 100:
                self.ch1.pulse_width_percent(level)
            else:
                self.ch1.pulse_width_percent(100)                
        else:
            self.ch1.pulse_width_percent(0)
            self.ch2.pulse_width_percent(0)

if __name__ == "__main__":
    en =  pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_OD)
    in1 = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2 = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    tim3 = pyb.Timer(3, freq=20000)
    motor = MotorDriver(en,in1,in2,tim3)
    try:
        motor.set_duty_cycle(0)
    except:
        motor.set_duty_cycle(0)
