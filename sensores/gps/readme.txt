1º create virtualenv:
$python3 -m venv venv

2º activate and install requirements:
$source venv/bin/activate
$ pip3 install -r requirements.txt

3º connect sensor to raspberry
VCC - 5V, RX - GPIO14, TX - GPIO15 and GND - GROUND

4º run 
$python3 main.py
