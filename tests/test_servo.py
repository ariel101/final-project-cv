import sys
import time
sys.path.insert(0, '/home/raspberrypiiii/ppe_control')

from hardware.gpio import init_gpio, barrera_abrir, barrera_cerrar, cleanup

print("Iniciando servo...")
init_gpio()
print("OK - GPIO inicializado")

print("Prueba 1: Barrera abierta (90 grados)")
barrera_abrir()
time.sleep(2)

print("Prueba 2: Barrera cerrada (0 grados)")
barrera_cerrar()
time.sleep(2)

print("Prueba 3: Abrir y cerrar 2 veces")
for i in range(2):
    print(f"  Ciclo {i+1}")
    barrera_abrir()
    time.sleep(1.5)
    barrera_cerrar()
    time.sleep(1.5)

cleanup()
print("Listo - todas las pruebas completadas")
