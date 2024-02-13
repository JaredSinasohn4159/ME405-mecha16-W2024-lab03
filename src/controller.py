import micropython
import pyb
import utime
import encoder_reader.py
import motor_driver.py
class CLControl:
    """! 
    This class implements a closed loop controller based on an input sensor.  This class uses previously created . 
    """

    def __init__ (self, motor, sensor, kp, ki, kd, reference):
        """! 
        Creates a motor driver by initializing GPIO
        pins and turning off the motor for safety. 
        @param sensor - the sensor the controller will be using and reading to calculate error
        @param kp - proportional controller constant
        @param ki - integral controller constant
        @param kd - derivative controller constant
        @param reference - the target postition for the controller to aim for
        """
        self.sensor = sensor
        self.kp = kp
        self.ki = kip
        self.kd = kp
        self.ref = reference
        # the effort the controller will send to the motor in percentage
        self.eff = 0
        # current value is the current reading of the sensor
        self.curr = self.sensor.read()
        # error is how far current value is from sensor
        self.err = self.ref - self.curr
        print (f"Creating controller with kp = {kp}, ki = {ki}, and kd = {kd}")

    def run(self):
        """!
        This method sets the duty cycle to be sent
        to the motor based on the saturated effort calculated in this function.
        """
        self.curr = 

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
