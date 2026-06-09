import os

# ── Rutas ───────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODELO_DIR = "/home/raspberrypiiii/best26_ariel_ncnn_model/"
LOGS_DIR   = os.path.join(BASE_DIR, "logs")

# ── Cámara ──────────────────────────────────────────────────────
CAM_ANCHO  = 416
CAM_ALTO   = 320

# ── Modelo ──────────────────────────────────────────────────────
CONFIANZA      = 0.4
IMGSZ          = 416
CLASES_CASCO   = ["hardhat", "helmet"]
CLASES_CHALECO = ["safety vest", "vest"]

# ── Lógica de estados ───────────────────────────────────────────
FRAMES_CONFIRMACION = 5    # frames consecutivos para cambiar estado
DURACION_BUZZER     = 3.0  # segundos que suena la alarma

# ── Pines GPIO ──────────────────────────────────────────────────
PIN_LED_R  = 17
PIN_LED_G  = 27
PIN_LED_B  = 22
PIN_BUZZER = 18
PIN_SERVO  = 12

# ── Servo ───────────────────────────────────────────────────────
SERVO_ABIERTO = 90
SERVO_CERRADO = 0
