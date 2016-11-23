
Code to fetch METAR data and display on an LCD (SunFounder LCD1602), connected to a raspberry pi.
[sunfounder reference](https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-30-i2c-lcd1602-sensor-kit-v2-0-for-b-plus.html)

This LCD uses the I2C bus, which requires configuration:

`sudo apt-get install -y python-smbus i2c-tools`

`sudo raspi-config`  menu -> (Advanced -> A7 I2C) then select "enable kernel module" then reboot.

Video:
 * [Single-line scrolling](https://www.youtube.com/watch?v=gfDjs_ALQ_U)
 * [Both lines scrolling](https://www.youtube.com/watch?v=372PiuKn2_s)
