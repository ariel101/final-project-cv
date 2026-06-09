import sys
import time
sys.path.insert(0, '/home/raspberrypiiii/ppe_control')

from hardware.gpio import init_led, led_verde, led_rojo, led_apagado, cleanup

print("Iniciando LED RGB...")
init_led()
print("OK - GPIO inicializado")

print("Prueba 1: Verde (acceso OK)")
led_verde()
time.sleep(3)

print("Prueba 2: Rojo (alerta)")
led_rojo()
time.sleep(3)

print("Prueba 3: Apagado")
led_apagado()
time.sleep(1)

print("Prueba 4: Parpadeo rojo x3 (simulando alarma)")
for i in range(3):
    led_rojo()
    time.sleep(0.5)
    led_apagado()
    time.sleep(0.5)

cleanup()
print("Listo - todas las pruebas completadas")
