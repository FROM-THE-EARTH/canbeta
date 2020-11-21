pipenv shell
chmod 777 /dev/serial0
chmod 777 /dev/ttyUSB0
stty -F /dev/serial0 -echo
pigpiod -s 1
