import sys
import time
sys.path.insert(0, '/home/raspberrypiiii/ppe_control')

from hardware.lcd import init_lcd, lcd_ok, lcd_alerta, lcd_apagar

print("Iniciando LCD...")
lcd = init_lcd()
print("OK - LCD inicializada")

print("Prueba 1: Acceso OK con contador")
lcd_ok(lcd, 5)
time.sleep(3)

print("Prueba 2: Falta casco")
lcd_alerta(lcd, falta_casco=True, falta_chaleco=False)
time.sleep(3)

print("Prueba 3: Falta chaleco")
lcd_alerta(lcd, falta_casco=False, falta_chaleco=True)
time.sleep(3)

print("Prueba 4: Falta todo")
lcd_alerta(lcd, falta_casco=True, falta_chaleco=True)
time.sleep(3)

print("Prueba 5: Apagar pantalla")
lcd_apagar(lcd)
print("Listo - todas las pruebas completadas")
