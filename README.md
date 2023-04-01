# Underwater challenge solution

</br>

</div>

<h1 align="center">

![The challenge](/picutures/rexrov.gif)

</h1>

</br>

## The Challenge

<div style="text-align: justify">

The challenge is to make the RexROV, a Remotely Operated Vehicle, be able to autonomously approach a sunken vessel, take a picture, and return to the world's point of origin. For more information click [here](https://github.com/Brazilian-Institute-of-Robotics/bir-underwater-challenge).

</div>

<h1 align="center">

![The challenge](/picutures/rexrov2.gif)

</h1>

</br>

## First steps

<div style="text-align: justify">

First a package was created in the workspace called findsunkenvessel. There is a python file there called go2goal.py. This file consists, basically, in publishing in the cmd_pose topic the pre-determined coordinates that the user wants the RexROV to follow, all the position control and orientation part is done by a ready-made controller that is in the Plankton package. Finally, when arriving at the desired point, a Python Cv2 library was used to take a picture of the vessel, along with a Cvbridge package that converts images between ROS and Opencv. After that a new coordinate is published for the ROV to return to the origin of the world.

</div>

## Next steps

Create a workspace in your machine.

```
$ mkdir -p ~/<your_workspace_name>/src

```
```
$ cd ~/<your_workspace_name>/src

```

Clone the following repository.

```
$ git clone git@github.com:Alexandreaags/bir-underwater-challenge-solution.git

```

 Install the dependencies

```
$ cd ~/<your_workspace_name>

```
```

$ rosdep install -i --from-path src --rosdistro foxy -y

```
To launch the environment in the gazebo.

```
$ source /usr/share/gazebo/setup.sh

```
```

$ . install/setup.bash

```
```

$ ros2 launch uuv_gazebo_worlds underwater_challenge.launch

```

To spawn the work vehicle, in a second terminal.

```
$ ros2 launch uuv_descriptions upload_rexrov.launch mode:=default x:=0 y:=0 z:=-1 namespace:=rexrov

```
 In a third terminal, to activate the cmd_pose topic.

```
$ ros2 launch uuv_control_cascaded_pid position_hold.launch uuv_name:=rexrov model_name:=rexrov

```
In a fourth terminal, to see the RexROV achieving the mission.

```
$ ros2 run findsunkenvessel go2goal

```

 With these steps, you'll can see the challenge solution in your machine. 
 
 Good lucky!

## References
**1.** https://github.com/Liquid-ai/Plankton  

**2.** https://uuvsimulator.github.io/

**3.** https://github.com/Brazilian-Institute-of-Robotics/bir-underwater-challenge

## Any Questions?

[Alexandre Adonai](https://github.com/Alexandreaags) : alexandre.adonai2002@hotmail.com

[Marco Reis](https://github.com/mhar-vell) : _marcoreis@fieb.org.br_

<hr>

_For more codes visit_ [BIR - BrazilianInstituteofRobotics](https://github.com/Brazilian-Institute-of-Robotics)
_For more informations visit_ [RASC](https://www.braziliansinrobotics.com/)
