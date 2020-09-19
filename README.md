# Follow face using OpenCV, Arduino and Webcam
Python script (and Arduino sketch) to follow face using OpenCV Haar Cascades, 28BYJ-48 stepper & servo and Webcam.

This script + arduino with stepper motor as yaw rotation and servo motor as pitch for the webcam, will basically follow any visible face.
There are two versions, one using haar cascades (slow & not that good) and other one using Deep Neural Network & SSD (faster & more precise).

## Prerequirements

## Windows
For windows install Python 3 and add it to your PATH. Next install pip3 and opencv-python, pyserial and imutils.

## Ubuntu
Run these commands to install dependencies

```bash
apt install python3 python3-pip

pip3 install opencv-python pyserial imutils
```

For Arduino IDE, all libraires used are already in IDE. (Servo.h & Stepper.h)

## Usage

### Arduino & motors

Firstly connect your ULN2003 driver board to power and these pins on the Arduino:

```bash
IN1 ->> D8
IN2 ->> D9
IN3 ->> D10
IN4 ->> D11
```
And also connect your servo motor to power and its signal cable to pin 6 on the Arduino.

Ensure that if you move the servo to 0°, the webcam is looking few degrees down and not hiting anything.

Now you can upload the code in 'ardcode' folder to your Arduino.

### Python script

Open the one of the folders in command prompt or terminal.

Now you can start the python script using `followface.py` on Windows or `python3 followface.py` on Linux and enter the values of the serial port of the Arduino, webcam number and if you want to see detected faces etc.

**OR**

You can enter config file after it and skip all of that like this: `followface.py example.txt` or `python3 followface.py example.txt` on linux.

To exit, just press 'q'.

### BotControl.exe

This app works only on Windows and you need to have .NET framework installed (https://dotnet.microsoft.com/download/dotnet-framework) (it can also work on linux using Wine, idunno)

Start the app, select port, click connect and now you can control the Arduino using your arrows.

## Pictures/Videos
*tobedone*
