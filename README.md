# Install
* [MS C++ Build Tools](https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=14)

# Crontab
```sudo crontab -e -u root``` Because Pi scripts need to be run as root
0 18 * * * /usr/bin/python3 /home/pi/scripts/christmasRelayServer.py