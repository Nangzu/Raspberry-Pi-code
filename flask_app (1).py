# flask_app.py
from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

AIN1 = 13
PWMA = 12
c_step = 1
target_speed = 50  # 원하는 속도 (0~100)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(AIN1, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(PWMA, GPIO.OUT, initial=GPIO.LOW)
p = GPIO.PWM(PWMA, 100)
p.start(0)

# 현재 동작을 저장할 변수
current_action = None

# 기본 페이지
@app.route('/')
def index():
    return render_template('index.html')

# "/control_motor" 엔드포인트에 대한 핸들러
@app.route('/control_motor', methods=['POST'])
def control_motor():
    global current_action

    # POST 요청에서 데이터 추출
    motor_action = request.form.get('motor_action')

    # 현재 동작 중인 경우 중지
    if current_action:
        stop_motor()

    # 여기에서 모터 제어 동작을 수행
    if motor_action == 'start':
        # 모터 시작 코드
        start_motor()
        current_action = 'start'
    elif motor_action == 'stop':
        # 모터 정지 코드
        current_action = None  # 모터 정지 요청을 받으면 current_action을 초기화
        stop_motor()

    return "Motor Control Received and Processed!"

def start_motor():
    GPIO.output(AIN1, GPIO.HIGH)
    for pw in range(0, target_speed + 1, c_step):
        p.ChangeDutyCycle(pw)
        time.sleep(0.5)
    p.ChangeDutyCycle(target_speed)

def stop_motor():
    GPIO.output(AIN1, GPIO.LOW)
    for pw in range(100, -1, c_step*-1):
        p.ChangeDutyCycle(pw)
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        pass
    finally:
        p.stop()
        GPIO.cleanup()
