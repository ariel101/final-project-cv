import sys
import time
sys.path.insert(0, '/home/raspberrypiiii/ppe_control')

from hardware.gpio import init_gpio, buzzer_on, buzzer_off, cleanup

print("Iniciando buzzer...")
init_gpio()
print("OK - Buzzer inicializado")

print("Prueba 1: Sonido continuo 2 segundos")
buzzer_on()
time.sleep(2)
buzzer_off()
time.sleep(1)

print("Prueba 2: 3 pitidos cortos (patron de alerta)")
for i in range(3):
    buzzer_on()
    time.sleep(0.3)
    buzzer_off()
    time.sleep(0.3)
time.sleep(1)

print("Prueba 3: 1 pitido largo")
buzzer_on()
time.sleep(1)
buzzer_off()

cleanup()
print("Listo - todas las pruebas completadas")
