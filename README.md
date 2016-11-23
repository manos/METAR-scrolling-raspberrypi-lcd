Status: writing it currently

Code to fetch METAR data and display on an LCD (SunFounder LCD1602), connected to a raspberry pi.
Reference: https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-30-i2c-lcd1602-sensor-kit-v2-0-for-b-plus.html

This LCD uses the I2C bus, which requires configuration:

sudo apt-get install -y python-smbus i2c-tools

sudo raspi-config # menu -> (Advanced -> A7 I2C) then select "enable kernel module" then reboot.


