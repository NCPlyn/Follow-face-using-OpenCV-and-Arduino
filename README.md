# Follow face using OpenCV, Arduino and Webcam
Python script (and Arduino sketch) to follow face using OpenCV Haar Cascades, 28BYJ-48 stepper & servo and Webcam.

This script + arduino with stepper motor as yaw rotation and servo motor as pitch for the webcam, will basically follow any visible face.
Now it's using Haar Cascades, I also plan to commit version using Caffe deep learning model in future.

## Prerequirements

You need to install these to run the Haar script:

```bash
python3
pip3

opencv-python
pyserial
```

If you are going to use it on Linux/Ubuntu, add this: `QT_X11_NO_MITSHM=1` at the end of this file: `/etc/environment`

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

Open the 'facehaar' folder in command prompt or terminal.

Now you can start the python script using `followface.py` on Windows or `python3 ./followface.py` on Linux and enter the values as the serial port of the Arduino, webcam number and if you want to see detected faces etc.

**OR**

You can enter config file after it and skip all of that like this: `followface.py example.txt` or `python3 ./followface.py example.txt` on linux.

To exit, just press 'q'.

### BotControl.exe

This app works only on Windows and you need to have .NET framework installed (https://dotnet.microsoft.com/download/dotnet-framework) (it can also work on linux using Wine, idunno)

Start the app, select port, click connect and now you can control the Arduino using your arrows.

## Pictures/Videos
*tobedone*
