from RPLCD.i2c import CharLCD

LCD_ADDRESS = 0x27
LCD_PORT    = 1
LCD_COLS    = 16
LCD_ROWS    = 2

def init_lcd():
    lcd = CharLCD(
        i2c_expander='PCF8574',
        address=LCD_ADDRESS,
        port=LCD_PORT,
        cols=LCD_COLS,
        rows=LCD_ROWS,
        dotsize=8
    )
    lcd.clear()
    return lcd

def lcd_ok(lcd, contador):
    lcd.clear()
    lcd.write_string("Acceso OK")
    lcd.cursor_pos = (1, 0)
    lcd.write_string(f"Total: {contador}")

def lcd_alerta(lcd, falta_casco, falta_chaleco):
    lcd.clear()
    if falta_casco and falta_chaleco:
        lcd.write_string("Falta casco")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("y chaleco")
    elif falta_casco:
        lcd.write_string("Falta:")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("CASCO")
    else:
        lcd.write_string("Falta:")
        lcd.cursor_pos = (1, 0)
        lcd.write_string("CHALECO")

def lcd_apagar(lcd):
    lcd.clear()
    lcd.backlight_enabled = False
