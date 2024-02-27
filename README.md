<<<<<<< HEAD
# Generating Music with GANs 

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

## Prerequisites
What things you need to install the software and how to install them:

Python (3.x recommended)
pip (Python package installer)
virtualenv (optional, but recommended for creating isolated Python environments)
CUDA Toolkit 12.3 Update 2 (to be able to run pytorch locally on NVIDIA)

## Installation
A step-by-step series of examples that tell you how to get a development environment running.

### Step 1: Install virtualenv
First, you need to install virtualenv if you haven't already. Open your command prompt or PowerShell and run:
pip install virtualenv

### Step 2: Create a Virtual Environment
Navigate to your project directory and create a virtual environment:
>>> cd /path/to/your/project
>>> virtualenv venv
This command creates a new directory named venv that contains the virtual environment.

### Step 3: Activate the Virtual Environment
Activate the virtual environment:

>>> .\venv\Scripts\activate
You should now see (venv) prefixed to your command line prompt, indicating that the virtual environment is active.

### Step 4: Install Required Packages
Install the required packages using pip:

>>> pip install matplotlib tqdm livelossplot gdown "pypianoroll>=1.0.2"

### Step 5: Verify Installation
To ensure all packages were installed correctly:

>>> pip list
This will list all the packages installed in the virtual environment along with their versions.

### Step 6: Deactivate the Virtual Environment
When you're finished, deactivate the virtual environment to return to your global environment:

>>> deactivate

## Installation Cuda
You could install cuda from https://developer.nvidia.com/cuda-downloads

After install ends open a new terminal and check your cuda version with:
>>> nvcc --version

Then go [here](https://pytorch.org/get-started/locally/) and select your os and preferred package manager(pip or anaconda), and the cuda version you installed, and copy the generated install command

Then open python console and check for cuda availability

>>> import torch
>>> torch.cuda.is_available()
=======
It will be an application that could generate lyrics and song melodies from trending songs but the voice will be client' own voice and they will try to perform them.
>>>>>>> 0c1a54077a688aa535ea498dbfbed3155554401b
