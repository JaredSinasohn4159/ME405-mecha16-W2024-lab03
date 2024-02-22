# ME405-mecha16-W2024-lab03
  Our closed loop motor controller inputs values of Kp, set_point, and measured_position. The measured position is read from our encoder_read.py. Kp is the proportional gain constant. The signal sent to the motor is then the difference between set_point and measured position multiplied by the Kp. Tuning of the Kp value is essential for proper motor funciton. If Kp is set too high the motor will overshoot. Additionally, the maximum effort is saturated, so increasing Kp too much has dimininshing terms. If Kp is too low it will undershoot. The lower the value, the more steady state error.
  
  For step-response test, we prompted the motor to do 360 degree turn (which is inputted by the setpoint). In the GUI, we created a get text prompt in order to enter in Kp values. main.py was then written to collect the time and position until the controller would prompt the motor to stop. Additionally, we connected our motor to a large aluminum flywheel as to add some inertia to our system so that our results were more substantial between Kp values. 
  
  We tested the Kp around our nominally appropriate value from testing which was  .This value was found by continually running our step response until we got the fastest response time with very slight overshoot. The other two values were  and   . These were chosen as +- away from the optimal Kp we found.
The results of our test are shown in the plot below, with all three values of Kp overlapped on the same graph.
  
