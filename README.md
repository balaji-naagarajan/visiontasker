# visiontasker

Two-stage framework combining vision-based UI understanding and LLM task planning for mobile task automation in a step-by-step manner.
  1. Vision-Based UI Understanding
  2. Step-by-Step Task Planning based on user input

Pre-requisites : 

  1. Python & Android SDK platform tools (connect android device and run adb devices)
  2. setup ADB Keyboard (https://github.com/senzhk/ADBKeyBoard)

Setup Steps :

1. git clone https://github.com/AkimotoAyako/VisionTasker.git
2. Python 3.9 is required. [Please jump to Installation Instructions](#installation-instructions)

   Note: Official Project docuemnt recommends using Python3.8. However, there are issues in setting up the python 3.8 in Macbook. PyMUPDF package dist is  not stable. So, we have updated to Python3.9 and updated the dependency versions in the setup and it is verified and tested in Macbook.

4. Download the pre-trained models (target detection model and CLIP) from the Google Drive(which will be shared separately) and Place them under pt_model/ 

```
pt_model/
├── clip_labels/
├── clip_mdl.pth
├── yolo_mdl.pt
└── yolo_vins_14_mdl.pt
```

5. Clip : https://github.com/openai/CLIP.git

Additional Steps :

1. update values in core\Config.py for DeviceName and Keyboard
2. Update path to font in PIL/ImageFont.py (in case of any errors)

Input Method
For text input on your phone, please refer to ADBKeyBoard and install the corresponding applications on both your phone and computer.
Python Environment Setup:

This document provides instructions for setting up the project environment. You can choose between setting up the environment using `pip` with a manually installed Python 3.9, or using `conda` with the provided `environment.yml` file.


#       
<h2 id="installation-instructions">Python Environment Setup Installation</h2>

## Method 1: Using Pip and a Manually Installed Python 3.9

1.  **Install Python 3.9:**
    -   Download and install Python 3.9 from the official Python website (python.org). Ensure that you add Python 3.9 to your system's PATH during installation.
    -   Verify the installation by opening your terminal or command prompt and running:
        ```bash
        python3.9 --version
        ```
        or
        ```bash
        python --version
        ```
        (If python3.9 is the default python version on your system.)
    -   If the output shows Python 3.9.x, the installation was successful.

2.  **Create a Virtual Environment (Recommended):**
    -   Navigate to the project directory in your terminal.
    -   Create a virtual environment:
        ```bash
        python3.9 -m venv venv
        ```
    -   Activate the virtual environment:
        -   On macOS and Linux:
            ```bash
            source venv/bin/activate
            ```
        -   On Windows:
            ```bash
            venv\Scripts\activate
            ```

3.  **Install Dependencies using `requirements.txt`:**
    -   Ensure you are in the project directory with the virtual environment activated.
    -   Install the required Python packages:
        ```bash
        pip install -r requirements.txt
        ```

4.  **Verify Installation:**
    -   You can verify the installed packages by running:
        ```bash
        pip list
        ```

## Method 2: Using Conda and `environment.yml`

1.  **Install Conda (if not already installed):**
    -   Download and install Miniconda or Anaconda from the official Anaconda website (anaconda.com).
    -   Follow the installation instructions for your operating system.

2.  **Create the Conda Environment:**
    -   Navigate to the project directory in your terminal.
    -   Create the Conda environment from the `environment.yml` file:
        ```bash
        conda env create -f environment.yml
        ```

3.  **Activate the Conda Environment:**
    -   Activate the newly created environment:
        ```bash
        conda activate visiontasker-env
        ```

4.  **Verify Installation:**
    -   Verify the installed packages:
        ```bash
        conda list
        ```

## Running the Script


