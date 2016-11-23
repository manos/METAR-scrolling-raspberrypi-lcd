
Code to fetch METAR weather data from NOAA and display it on an LCD (SunFounder LCD1602), connected to a raspberry pi (
[sunfounder reference](https://www.sunfounder.com/learn/sensor-kit-v2-0-for-raspberry-pi-b-plus/lesson-30-i2c-lcd1602-sensor-kit-v2-0-for-b-plus.html)).

This LCD uses the I2C bus, which requires configuration:

`sudo apt-get install -y python-smbus i2c-tools`

`sudo raspi-config` in the menu: (Advanced -> A7 I2C) then select "enable kernel module" then reboot.

Just run `./run-lcd.py` and it should work (and specify -s KSFO to get SFO data, for example).

Dual line mode (default) scrolls left, wrapping the bottom line up to the top.

Video:
 * [Single-line scrolling](https://www.youtube.com/watch?v=gfDjs_ALQ_U)
 * [Both lines scrolling](https://www.youtube.com/watch?v=372PiuKn2_s)
