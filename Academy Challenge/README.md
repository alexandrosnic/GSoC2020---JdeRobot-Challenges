# README

**MyAlgorithm.py** contains the python code for the **Follow Line** challenge of the Jderobot Academy that can be found [here](https://jderobot.github.io/RoboticsAcademy/exercises/AutonomousCars/follow_line/).
The complete directory of the Jderobot Academy, consisting of Robot exercises, implementing ROS and Gazebo integration solutions, can be found [here](https://github.com/JdeRobot/RoboticsAcademy).

In my solution for the **Follow line** problem I used a PID controller.

In order to choose the gains Kp, Ki, and Kd, I followed the trian and error method. Thus, I first set Ki and Kd values to zero and increased proportional term (Kp) until system reaches to oscillating behavior. 
Once it is oscillating, I adjusted Ki (Integral term) so that oscillations stops and finally I adjusted D to get fast response.
Another way would be using the Zeigler Nichols method.

The video demonstration of my solution can be found here:

[![](http://img.youtube.com/vi/XrxZNXNOdAs/0.jpg)](http://www.youtube.com/watch?v=XrxZNXNOdAs "Video Demonstration")

