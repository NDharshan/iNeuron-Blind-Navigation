# iNeuron-Blind-Navigation
This project attempts to create a system which would bring in added ease to the visually impaired, through our nagivation, obstacle-detection, obstacle distance identification and speech-driven system to seamlessly integrate applications like Ola, Uber, etc. This was built during the PW-Hacks Jan-2023.


# The problem this Application solves
* Visually impaired means that one can hardly fathom to cross the busy day-to-day life laden with obstacles, nay, even navigating through a micro-environment like home or work-place is a challenge.
* We attempt to solve this through a two way model. That is we work with both the individual and his/her guardian to create a safe navigating experience for the person.
* Hosting this application in any hand-held device like a mobile for ease of access


# Technology Stack
## Web Application
* Flask (Python)
* HTML
* CSS 
## Mobile Application 
* Kivy (Python)
* Android Studio


# Getting started
Install the pre-requisite modules namely Flask and Kivy and other modules as applicable
Running the Detection Code independently
## Obstacle detection
`python object classification/yolo_opencv.py`
## Obstacle-User distance detection
`python person distance/distance.py`
## Sound-driven instructions
`python speech recognition/speech.py`
## Flask application
`python main.py`
## Kivy application
`python kivy3.py`
* Requires KivyMD as well

# Working and Features
* The Web-application calls the voice-assisted system and is recieptive to user commands
* There is always an alert for obstacle and when the obstacle arrives beyond a certain safe distance from an individual a beep sound is raised
* The user can easily book an Ola by just an instructions


# Snapshots of the Working Web Application
![Screenshot (13)](https://user-images.githubusercontent.com/98468801/215315685-4312194b-00de-4a85-85b0-9b72e30e8a84.png)
![Screenshot (14)](https://user-images.githubusercontent.com/98468801/215315687-3a225ce8-76b0-4193-8f31-8ad836763a05.png)


# Snapshots of the Working Mobile Application

![mobile screens](https://user-images.githubusercontent.com/98468801/215316375-54f338a2-c00b-4a1d-aaf6-b7a756e54496.png)


# Challenges we ran into and Acknowledgements
* We faced issues in figuring out the weights in the model and in the design of the mobile application linked to the cloud, but were able to find that use of COCO dataset and Firebase which enabled seamless deployment


# Further Enhancements
*	Integrating Face Recognition
*	Including Map API for Navigation

# Video Demonstration
* https://www.loom.com/share/81663c4ab2684b14ac4adac4f243cd56
* https://www.loom.com/share/0705a9717f444843a6f9e510d2e1a250
* https://www.loom.com/share/aa7c4922a2644034938e23dc5b33d81a


# Team
### Sujan Reddy
https://github.com/sujan-reddy
### N.Dharshan
https://github.com/NDharshan
