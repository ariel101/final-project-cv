import sys
import time
sys.path.insert(0, '/home/raspberrypiiii/ppe_control')

from hardware.lcd import init_lcd, lcd_ok, lcd_alerta, lcd_apagar
from hardware.gpio import init_gpio, led_verde, led_rojo, led_apagado, buzzer_on, buzzer_off, barrera_abrir, barrera_cerrar, cleanup

print("="*40)
print("TEST DE INTEGRACION - Sistema EPP")
print("="*40)

# Inicializar
print("\nInicializando componentes...")
lcd = init_lcd()
init_gpio()
print("OK - Todo inicializado")

# ── Estado inicial: todo OK ─────────────────
print("\n[1] Estado inicial - Acceso OK")
led_verde()
barrera_abrir()
lcd_ok(lcd, 0)
time.sleep(4)

# ── Simulacion: falta casco ─────────────────
print("\n[2] Alerta - Falta casco")
led_rojo()
barrera_cerrar()
buzzer_on()
lcd_alerta(lcd, falta_casco=True, falta_chaleco=False)
time.sleep(2)
buzzer_off()
time.sleep(2)

# ── Vuelve a OK ─────────────────────────────
print("\n[3] Persona se pone el casco - Vuelve a OK")
led_verde()
barrera_abrir()
lcd_ok(lcd, 1)
time.sleep(4)

# ── Simulacion: falta chaleco ───────────────
print("\n[4] Alerta - Falta chaleco")
led_rojo()
barrera_cerrar()
buzzer_on()
lcd_alerta(lcd, falta_casco=False, falta_chaleco=True)
time.sleep(2)
buzzer_off()
time.sleep(2)

# ── Vuelve a OK ─────────────────────────────
print("\n[5] Persona se pone el chaleco - Vuelve a OK")
led_verde()
barrera_abrir()
lcd_ok(lcd, 2)
time.sleep(4)

# ── Simulacion: falta todo ──────────────────
print("\n[6] Alerta - Falta casco y chaleco")
led_rojo()
barrera_cerrar()
buzzer_on()
lcd_alerta(lcd, falta_casco=True, falta_chaleco=True)
time.sleep(2)
buzzer_off()
time.sleep(2)

# ── Estado final ────────────────────────────
print("\n[7] Fin del test - Apagando sistema")
led_apagado()
barrera_cerrar()
lcd_apagar(lcd)
time.sleep(1)
cleanup()
print("\nTest de integracion completado")
