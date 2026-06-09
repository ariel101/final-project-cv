import sys
import time
import cv2
from picamera2 import Picamera2
from ultralytics import YOLO

sys.path.insert(0, '/home/raspberrypiiii/ppe_control')
import config
from hardware.lcd  import init_lcd, lcd_ok, lcd_alerta, lcd_apagar
from hardware.gpio import init_gpio, led_verde, led_rojo, led_apagado, \
                         buzzer_on, buzzer_off, barrera_abrir, barrera_cerrar, cleanup

# ── Inicializar hardware ────────────────────────────────────────
print("Iniciando sistema EPP...")
lcd = init_lcd()
init_gpio()

led_verde()
barrera_abrir()
lcd_ok(lcd, 0)
print("Hardware listo")

# ── Cargar modelo ───────────────────────────────────────────────
print("Cargando modelo YOLO...")
model = YOLO(config.MODELO_DIR, task="detect")
print("Modelo listo")

# ── Inicializar cámara ──────────────────────────────────────────
picam2 = Picamera2()
cam_config = picam2.create_preview_configuration(
    main={"size": (config.CAM_ANCHO, config.CAM_ALTO)}
)
picam2.configure(cam_config)
picam2.start()
print("Camara lista\n")
print("Sistema activo - ESC para salir")
print("-" * 40)

# ── Variables de estado ─────────────────────────────────────────
estado_actual    = "OK"
frames_sin_epp   = 0
frames_con_epp   = 0
contador_accesos = 0
buzzer_timer     = 0.0

def activar_alerta(falta_casco, falta_chaleco):
    led_rojo()
    buzzer_on()
    barrera_cerrar()
    lcd_alerta(lcd, falta_casco, falta_chaleco)

def desactivar_alerta():
    global contador_accesos
    contador_accesos += 1
    led_verde()
    buzzer_off()
    barrera_abrir()
    lcd_ok(lcd, contador_accesos)

# ── Bucle principal ─────────────────────────────────────────────
try:
    while True:
        frame = picam2.capture_array()
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        results = model(frame, imgsz=config.IMGSZ, conf=config.CONFIANZA)

        casco_detectado   = False
        chaleco_detectado = False

        for box in results[0].boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf  = float(box.conf[0])
            cls   = int(box.cls[0])
            nombre = model.names[cls].lower()

            if nombre in config.CLASES_CASCO:
                label = "casco"
                casco_detectado = True
            elif nombre in config.CLASES_CHALECO:
                label = "chaleco"
                chaleco_detectado = True
            else:
                label = nombre

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
            cv2.putText(frame, f"{label} {conf:.2f}",
                        (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 255), 2)

        epp_completo = casco_detectado and chaleco_detectado

        # ── Confirmación por frames ─────────────────────────────
        if epp_completo:
            frames_sin_epp = 0
            frames_con_epp = min(frames_con_epp + 1, config.FRAMES_CONFIRMACION)
        else:
            frames_con_epp = 0
            frames_sin_epp = min(frames_sin_epp + 1, config.FRAMES_CONFIRMACION)

        # ── Cambio de estado ────────────────────────────────────
        if frames_sin_epp >= config.FRAMES_CONFIRMACION and estado_actual == "OK":
            estado_actual = "ALERTA"
            activar_alerta(not casco_detectado, not chaleco_detectado)
            buzzer_timer = time.time()
            print(f"[ALERTA] Casco={casco_detectado} Chaleco={chaleco_detectado}")

        elif frames_con_epp >= config.FRAMES_CONFIRMACION and estado_actual == "ALERTA":
            estado_actual = "OK"
            desactivar_alerta()
            print(f"[OK] Acceso autorizado - Total: {contador_accesos}")

        # ── Actualizar LCD en tiempo real durante ALERTA ────────
        elif estado_actual == "ALERTA":
            lcd_alerta(lcd, not casco_detectado, not chaleco_detectado)

        # ── Apagar buzzer tras DURACION_BUZZER segundos ─────────
        if estado_actual == "ALERTA":
            if time.time() - buzzer_timer > config.DURACION_BUZZER:
                buzzer_off()

        # ── Overlay en pantalla ─────────────────────────────────
        color  = (0, 255, 0) if estado_actual == "OK" else (0, 0, 255)
        texto  = "ACCESO OK" if estado_actual == "OK" else "ACCESO DENEGADO"
        cv2.putText(frame, texto,
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        cv2.putText(frame, f"Accesos: {contador_accesos}",
                    (10, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

        if not casco_detectado:
            cv2.putText(frame, "NO CASCO",
                        (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
        if not chaleco_detectado:
            cv2.putText(frame, "NO CHALECO",
                        (10, 115), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

        cv2.imshow("Control de acceso - EPP", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

except KeyboardInterrupt:
    pass

finally:
    print("\nApagando sistema...")
    buzzer_off()
    led_apagado()
    barrera_cerrar()
    lcd_apagar(lcd)
    cleanup()
    cv2.destroyAllWindows()
    picam2.stop()
    print("Sistema apagado correctamente")
