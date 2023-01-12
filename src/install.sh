# Needed for selenium tests
pip install selenium

# Needed for runing on raspberry pi (headless)
sudo apt-get install xvfb xserver-xephyr tigervnc-standalone-server x11-utils gnumeric
sudo apt-get install chromium-browser

python3 -m pip install selenium pyvirtualdisplay pillow EasyProcess

# Permissions
# Add execute permissions for run file. This is needed for scheduling.
chmod +x src/runbot.sh
chmod +x src/main.py