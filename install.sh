#!/bin/bash

# Initialize the virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

# Add application to run at startup by running start.sh
chmod u+x start.sh

sudo echo "[Desktop Entry]" >> /etc/xdg/autostart/display.desktop
sudo echo "Name=Stop The Bleed" >> /etc/xdg/autostart/display.desktop
sudo echo "Exec=/$(pwd)/start.sh" >> /etc/xdg/autostart/display.desktop

echo "Installation complete. Please restart the device to run the application."

