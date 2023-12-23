import RPi.GPIO as GPIO
import time
import Adafruit_DHT

# sensor pin and DHT object
sensor = Adafruit_DHT.DHT11
pin = 2
Adafruit_DHT.AM2302

# motor pins and configuration
AIN1 = 13
AIN2 = 15

# LED pin
led_pin = 21

# Initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(led_pin, GPIO.OUT)

# function for motor control
def step_motor(direction):
    GPIO.output(AIN1, direction)
    for pw in range(0, 101, 10):
        # GPIO.output(PWMA, GPIO.HIGH)  # Comment or remove this line
        time.sleep(0.05)
    for pw in range(100, -1, -10):
        # GPIO.output(PWMA, GPIO.LOW)  # Comment or remove this line
        time.sleep(0.05)

def reset_motor():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.LOW)

# function for DHT11 sensor
def get_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print(f"온도: {temperature:.1f}°C, 습도: {humidity:.1f}%")
    else:
        print("센서 데이터 읽기 실패. 다시 시도하세요!")

# run the program
try:
    # control motor
    for i in range(2):
        step_motor(GPIO.HIGH)
        time.sleep(2)
        reset_motor()
        time.sleep(2)

    # read sensor data
    get_sensor_data()

    # control LED
    for i in range(3):
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(1)

except KeyboardInterrupt:
    print("프로그램 중지")
    GPIO.cleanup()
