# visiontasker

Two-stage framework combining vision-based UI understanding and LLM task planning for mobile task automation in a step-by-step manner.
  1. Vision-Based UI Understanding
  2. Step-by-Step Task Planning based on user input

Pre-requisites : 

  1. Python & Android SDK platform tools (connect android device and run adb devices)
  2. setup ADB Keyboard (https://github.com/senzhk/ADBKeyBoard)

Setup Steps :

1. git clone https://github.com/AkimotoAyako/VisionTasker.git
2. conda create -n visiontasker python=3.8
3. pip install -r requirements.txt
4. Place pre-trained models (target detection model and CLIP) under pt_model/ (Google drive path will be shared separately)

Input Method
For text input on your phone, please refer to ADBKeyBoard and install the corresponding applications on both your phone and computer.
