import RPi.GPIO as GPIO
import time

# functia de initializare a servo-urilor
def init_servos():
    # pinii si frecventa pentru servo-uri
    servo_pin1 = 18
    servo_pin2 = 12
    frequency = 50

    # setup-ul prinilor de GPIO out
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servo_pin1, GPIO.OUT)
    GPIO.setup(servo_pin2, GPIO.OUT)

    # crearea pinilor de pwm din pinii de GPIO si frecventa
    pwm1 = GPIO.PWM(servo_pin1, frequency)
    pwm2 = GPIO.PWM(servo_pin2, frequency)

    return pwm1, pwm2


# functia de mapare a unghiurior la duty_cycle (timpul in care semnalul este activ)
def map_angle_to_duty_cycle(angle):
    min_duty = 5
    max_duty = 10
    return ((angle / 180.0) * (max_duty - min_duty)) + min_duty


# functia de deschidere a capacului
def servos_open_lid(pwm1, pwm2, base_position1=110, base_position2=0):
    duty_cycle1 = map_angle_to_duty_cycle(base_position1)
    duty_cycle2 = map_angle_to_duty_cycle(base_position2)
    pwm1.ChangeDutyCycle(duty_cycle1)
    pwm2.ChangeDutyCycle(duty_cycle2)
    time.sleep(0.5)


# functia de inchidere a capacului
def servos_close_lid(pwm1, pwm2, position1=20, position2=130):
    duty_cycle1 = map_angle_to_duty_cycle(position1)
    duty_cycle2 = map_angle_to_duty_cycle(position2)
    pwm1.ChangeDutyCycle(duty_cycle1)
    pwm2.ChangeDutyCycle(duty_cycle2)
    time.sleep(0.5)


# functia de oprire a servo-urilor
def gpio_cleanup(pwm1, pwm2):
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
