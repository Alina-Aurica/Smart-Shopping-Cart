import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711

# crearea unei instante de senzor de greutate conectat la pinii 5 si 6
# setarea valorii de referinta
# realizarea functiei tare - initializare senzor
hx = HX711(5, 6)
hx.set_reading_format("MSB", "MSB")
referenceUnit = -515.22
hx.set_reference_unit(referenceUnit)
hx.reset()
hx.tare()

print("Tare done! Add weight now...")

# se citesc 15 valori intr-o bucla - pentru stabilizare
# se ia ultima valoare (care e media a 5 valori - pentru eliminarea zgomotului)
def weight_logic():
    i = 0
    weight = 0
    while i < 15:
        weight = hx.get_weight(5)
        i = i + 1
        hx.power_down()
        hx.power_up()
        time.sleep(0.1)
    return (-2)*weight

