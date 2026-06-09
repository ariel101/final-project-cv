import RPi.GPIO as GPIO
import time

# ── Pines ──────────────────────────────────────────────────────
PIN_LED_R  = 17
PIN_LED_G  = 27
PIN_LED_B  = 22
PIN_BUZZER = 18
PIN_SERVO  = 12

# ── Ángulos de la barrera ───────────────────────────────────────
SERVO_ABIERTO = 90
SERVO_CERRADO = 0

servo_pwm = None

def init_gpio():
    global servo_pwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN_LED_R,  GPIO.OUT)
    GPIO.setup(PIN_LED_G,  GPIO.OUT)
    GPIO.setup(PIN_LED_B,  GPIO.OUT)
    GPIO.setup(PIN_BUZZER, GPIO.OUT)
    GPIO.setup(PIN_SERVO,  GPIO.OUT)

    servo_pwm = GPIO.PWM(PIN_SERVO, 50)
    servo_pwm.start(0)

    led_apagado()
    buzzer_off()

# ── LED RGB ─────────────────────────────────────────────────────
def led_verde():
    GPIO.output(PIN_LED_R, GPIO.LOW)
    GPIO.output(PIN_LED_G, GPIO.HIGH)
    GPIO.output(PIN_LED_B, GPIO.LOW)

def led_rojo():
    GPIO.output(PIN_LED_R, GPIO.HIGH)
    GPIO.output(PIN_LED_G, GPIO.LOW)
    GPIO.output(PIN_LED_B, GPIO.LOW)

def led_apagado():
    GPIO.output(PIN_LED_R, GPIO.LOW)
    GPIO.output(PIN_LED_G, GPIO.LOW)
    GPIO.output(PIN_LED_B, GPIO.LOW)

# ── Buzzer ──────────────────────────────────────────────────────
def buzzer_on():
    GPIO.output(PIN_BUZZER, GPIO.HIGH)

def buzzer_off():
    GPIO.output(PIN_BUZZER, GPIO.LOW)

# ── Servo ───────────────────────────────────────────────────────
def _angulo_a_ciclo(angulo):
    return 2.5 + (angulo / 180.0) * 10.0

def mover_servo(angulo):
    servo_pwm.ChangeDutyCycle(_angulo_a_ciclo(angulo))
    time.sleep(0.5)
    servo_pwm.ChangeDutyCycle(0)  # evita vibración

def barrera_abrir():
    mover_servo(SERVO_ABIERTO)

def barrera_cerrar():
    mover_servo(SERVO_CERRADO)

# ── Limpieza ────────────────────────────────────────────────────
def cleanup():
    led_apagado()
    buzzer_off()
    try:
        if servo_pwm is not None:
            servo_pwm.stop()
    except Exception:
        pass
    GPIO.cleanup()
