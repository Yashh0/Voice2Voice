#!/bin/bash

# Update package list
apt-get update

# Install system dependencies
apt-get install -y portaudio19-dev python3-pyaudio libportaudio2 libasound-dev libsndfile1 ffmpeg build-essential python3-dev

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Verify installations
python3 -c "import sounddevice; print('sounddevice installed successfully')"
python3 -c "import pyaudio; print('pyaudio installed successfully')"
